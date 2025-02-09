from typing import Dict, Any
import logging
from src.agents.article_agent import ArticleAgent
from src.agents.visual_agent import VisualGeneratorAgent
from src.agents.verification_agent import VerificationAgent
from src.agents.engaging_content_agent import EngagingContentAgent
from src.agents.trend_agent import TrendAnalysisAgent
from src.utils.fact_checker import FactChecker

class ContentEngine:
    """
    Core content generation engine that orchestrates all agents
    """
    
    def __init__(self, config: Any):
        self.config = config
        self.trend_agent = TrendAnalysisAgent(config)
        
        # Initialize components for ArticleAgent
        hf_model_name = "distilgpt2"  # Default model
        fact_checker = FactChecker()  # Initialize fact checker
        
        # Initialize agents with required parameters
        self.article_agent = ArticleAgent(
            gemini_model=config,  # Your model instance
            hf_model_name=hf_model_name,
            fact_checker=fact_checker
        )
        
        # Initialize VerificationAgent with config
        self.verification_agent = VerificationAgent(config)  # Pass config here
        
        # Initialize EngagingContentAgent with config
        self.engaging_agent = EngagingContentAgent(config)  # Pass config here
        
        self.visual_agent = VisualGeneratorAgent(config)

    async def generate_content(self, topic: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate the content creation process through all agents
        """
        # 1. Analyze trends and gather research
        trend_data = await self.trend_agent.analyze(topic)
        
        # 2. Generate initial content
        initial_content = await self.article_agent.generate(
            topic,
            trend_data,
            preferences
        )
        
        # 3. Verify facts and sources
        verified_content = await self.verification_agent.verify(
            initial_content,
            preferences['fact_check_level']
        )
        
        # 4. Enhance engagement
        engaging_content = await self.engaging_agent.enhance(
            verified_content,
            preferences['target_audience']
        )
        
        # 5. Generate visuals and interactive elements
        visuals = await self.visual_agent.generate(
            engaging_content,
            preferences['include_visuals']
        )
        
        # 6. Compile final content
        final_content = self._compile_final_content(
            engaging_content,
            visuals
        )
        
        # 7. Generate statistics and metadata
        stats = self._generate_stats(final_content)
        
        return {
            "title": final_content['title'],
            "content": final_content['body'],
            "visuals": final_content['visuals'],
            "interactive_elements": final_content['interactive'],
            "sources": final_content['sources'],
            "stats": stats,
            "metadata": {
                "topic": topic,
                "preferences": preferences,
                "trend_data": trend_data['summary'],
                "word_count": len(final_content['body'].split()),
                "generated_visuals": len(final_content['visuals'])
            }
        }

    def _compile_final_content(self, content: Dict, visuals: Dict) -> Dict:
        """Compile all content elements into final format"""
        return {
            "title": content['title'],
            "body": content['body'],
            "visuals": visuals['charts'] + visuals['diagrams'],
            "interactive": visuals['interactive'],
            "sources": content['sources']
        }

    def _generate_stats(self, content: Dict) -> Dict:
        """Generate content statistics"""
        return {
            "word_count": len(content['body'].split()),
            "reading_time": len(content['body'].split()) // 200,  # Avg reading speed
            "credibility_score": self._calculate_credibility(content),
            "engagement_score": self._calculate_engagement(content)
        }

    def _calculate_credibility(self, content: Dict) -> float:
        """Calculate content credibility score"""
        # Implementation of credibility scoring
        return 8.5  # Example score

    def _calculate_engagement(self, content: Dict) -> float:
        """Calculate content engagement score"""
        # Implementation of engagement scoring
        return 9.0  # Example score 