from typing import Dict, Any
from src.agents.base_agent import BaseAgent
import logging
from src.models.gemini_model import GeminiModel
from src.models.huggingface_model import HuggingFaceModel
from src.utils.fact_checker import FactChecker
from src.agents.verification_agent import VerificationAgent
from src.agents.engaging_content_agent import EngagingContentAgent, ContentStyle
from src.agents.visual_generator_agent import VisualGeneratorAgent

# Create logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler if needed
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class ArticleAgent(BaseAgent):
    def __init__(self, gemini_model: GeminiModel, hf_model_name: str, fact_checker: FactChecker):
        self.gemini_model = gemini_model
        self.hf_model = HuggingFaceModel(hf_model_name)
        self.fact_checker = fact_checker
        self.verification_agent = VerificationAgent()
        self.engaging_content_agent = EngagingContentAgent()
        self.visual_generator = VisualGeneratorAgent()
    
    async def ensure_high_quality(self, content: str) -> bool:
        # Implement checks for quality metrics (e.g., readability, factual accuracy)
        return len(content) > 100  # Example check: content length must be greater than 100 characters

    async def validate_content(self, content: str) -> bool:
        # Check each statement in the content
        statements = content.split('. ')  # Simple split for example
        for statement in statements:
            if not self.fact_checker.check_fact(statement):
                return False
        return True

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            topic = request.get('content', '')
            research_data = request.get('research', {}).get('content', '')
            seo_data = request.get('seo_data', {}).get('content', '')

            # Create blog post prompt
            prompt = f"""
            Write a complete blog post about: {topic}
            
            Use this research data: {research_data}
            
            Follow these SEO guidelines: {seo_data}
            
            Format requirements:
            1. Use the SEO title
            2. Include meta description
            3. Follow the recommended heading structure
            4. Incorporate primary and secondary keywords naturally
            5. Write engaging paragraphs
            6. Include examples and evidence
            7. End with a strong conclusion
            
            Make it engaging, informative, and SEO-optimized.
            """

            # Generate and improve content
            content = await self.gemini_model.generate_content(prompt)
            if not content:
                raise ValueError("Failed to generate content")

            improved_content = await self.hf_model.improve_content(content)
            if not improved_content:
                raise ValueError("Failed to improve content")

            # Validate content
            if not await self.validate_content(improved_content):
                logger.warning("Content validation failed. Regenerating content...")
                return await self.process_request(request)

            # After generating the content, verify it
            verification_results = self.verification_agent.verify_article(improved_content)
            
            # Handle flagged claims and bias analysis
            flagged_claims = verification_results['fact_check_results']
            bias_analysis = verification_results['bias_analysis']
            
            # Send flagged sections for revision if necessary
            if flagged_claims:
                # Logic to send flagged claims to the Article Agent for revision
                pass

            # Define content style based on user preferences or context
            style = ContentStyle(
                tone="conversational",
                complexity="intermediate",
                target_audience="general",
                content_type="article"
            )
            
            # Enhance content engagement
            enhancement_results = await self.engaging_content_agent.enhance_content(
                improved_content,
                style
            )
            
            # Combine with SEO optimization
            final_content = await self._combine_seo_and_engagement(
                enhancement_results['enhanced_content']
            )

            # Generate visuals
            visuals = await self.visual_generator.generate_visuals({
                "text": final_content,
                "style": style
            })
            
            # Combine content with visuals
            final_content = self._combine_content_and_visuals(
                final_content,
                visuals
            )
            
            return {
                "type": "article",
                "content": final_content,
                "visuals": visuals,
                "interactive_elements": visuals['interactive_elements'],
                "analysis": enhancement_results['analysis'],
                "verification_results": verification_results,
                "metadata": {
                    **request.get('metadata', {}),
                    "article_type": "blog_post",
                    "seo_optimized": True
                }
            }

        except Exception as e:
            logger.error(f"ArticleAgent error: {str(e)}")
            raise

    async def _combine_seo_and_engagement(self, content: str) -> str:
        """Balance SEO optimization with readability"""
        # Implementation of SEO and engagement balance
        return content

    def _combine_content_and_visuals(self, content: str, visuals: Dict[str, Any]) -> str:
        """Combine text content with visual elements"""
        html_content = f"<article>\n{content}\n"
        
        # Add illustrations
        for illustration in visuals['illustrations']:
            html_content += f"""
            <figure>
                <img src="data:image/png;base64,{illustration['image']}" 
                     alt="{illustration['caption']}">
                <figcaption>{illustration['caption']}</figcaption>
            </figure>
            """
        
        # Add charts
        for chart in visuals['charts']:
            html_content += f"""
            <div class="chart-container">
                {chart['html']}
            </div>
            """
        
        # Add infographics
        for infographic in visuals['infographics']:
            html_content += f"""
            <figure class="infographic">
                <img src="data:image/png;base64,{infographic['image']}" 
                     alt="{infographic['title']}">
                <figcaption>{infographic['title']}</figcaption>
            </figure>
            """
        
        # Add interactive elements
        html_content += visuals['interactive_elements']['plotly_html']
        html_content += visuals['interactive_elements']['custom_js']
        
        html_content += "\n</article>"
        return html_content
