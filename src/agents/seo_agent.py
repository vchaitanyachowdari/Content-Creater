from typing import Dict, Any, List
from .base_agent import BaseAgent
import asyncio
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

class SEOAgent(BaseAgent):
    def __init__(self, model):
        self.model = model
        
        # Comprehensive SEO guidelines
        self.seo_strategy = {
            "keyword_research": """
            Keyword Strategy Requirements:
            * Primary Keywords: Main topic focus
            * Long-tail Keywords: Specific phrases
            * LSI Keywords: Related terms
            * Search Intent: Match user goals
            * Keyword Placement: Strategic integration
            """,
            
            "on_page": """
            On-Page Optimization:
            * Title Tag: Primary keyword, <60 chars
            * Meta Description: Compelling, <160 chars
            * URL Structure: Short, keyword-focused
            * Headers: H1-H6 hierarchy
            * Content Quality: Original, valuable
            * Internal Links: Relevant cross-references
            * External Links: Authoritative sources
            * Image Alt Text: Descriptive, keyword-rich
            """,
            
            "content_quality": """
            Content Requirements:
            * Minimum Length: 1500+ words
            * Readability: Clear, concise language
            * Structure: Logical organization
            * Value: Comprehensive information
            * Freshness: Updated content
            * Engagement: Interactive elements
            * Citations: Credible sources
            """,
            
            "technical_seo": """
            Technical Optimization:
            * Mobile Optimization: Responsive design
            * Page Speed: Fast loading times
            * Schema Markup: Structured data
            * HTTPS: Secure protocol
            * XML Sitemap: Search engine guidance
            * Canonical URLs: Duplicate handling
            """
        }
        
        # Technical specifications
        self.technical_specs = {
            "title_length": 60,
            "meta_desc_length": 160,
            "min_word_count": 1500,
            "optimal_keyword_density": 0.02,
            "max_heading_depth": 6,
            "readability_target": 60  # Flesch Reading Ease
        }

    async def optimize_content(self, topic: str, research_content: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze this topic and research data for SEO optimization:
        Topic: {topic}
        Research: {research_content}

        Provide:
        1. Primary keyword
        2. Secondary keywords (3-5)
        3. Meta description (150-160 characters)
        4. SEO title (50-60 characters)
        5. Recommended heading structure
        """
        
        seo_data = await self.model.generate_content(prompt)
        
        return {
            "type": "seo",
            "content": seo_data,
            "metadata": {
                "topic": topic
            }
        }

    async def extract_keywords(self, topic: str) -> Dict[str, List[str]]:
        prompt = f"""
        Analyze this topic and extract SEO keywords:
        Topic: {topic}
        
        Provide:
        1. Primary keyword (main focus)
        2. Secondary keywords (3-5 related terms)
        3. Long-tail keywords (2-3 specific phrases)
        
        Format as JSON with 'primary', 'secondary', and 'long_tail' lists.
        """
        
        response = await self.model.generate_content(prompt)
        # Parse JSON response
        return eval(response)

    async def analyze_seo_metrics(self, content: str, keywords: Dict[str, List[str]]) -> Dict[str, Any]:
        # Calculate basic SEO metrics
        word_count = len(content.split())
        keyword_density = self._calculate_keyword_density(content, keywords['primary'][0])
        readability_score = self._calculate_readability(content)
        
        return {
            "word_count": word_count,
            "keyword_density": keyword_density,
            "readability_score": readability_score,
            "has_meta_description": bool(re.search(r'meta description:', content.lower())),
            "has_title_tag": bool(re.search(r'title tag:', content.lower())),
            "header_count": len(re.findall(r'#{1,6}\s', content))
        }

    def _calculate_keyword_density(self, content: str, keyword: str) -> float:
        word_count = len(content.split())
        keyword_count = len(re.findall(rf'\b{keyword}\b', content.lower()))
        return keyword_count / word_count if word_count > 0 else 0

    def _calculate_readability(self, content: str) -> float:
        sentences = len(re.findall(r'[.!?]+', content))
        words = len(content.split())
        syllables = len(re.findall(r'[aeiou]+', content.lower()))
        
        if sentences == 0 or words == 0:
            return 0
        
        # Simplified Flesch Reading Ease score
        return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

    async def process_request(self, content: Dict[str, Any]) -> Dict[str, Any]:
        try:
            text = content.get('content', '')
            topic = content.get('metadata', {}).get('topic', '')

            optimized_content = await self.optimize_content(topic, text)
            return optimized_content

        except Exception as e:
            logger.error(f"SEO optimization failed: {str(e)}")
            return content  # Return original content on error