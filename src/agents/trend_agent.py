import os
from typing import Dict, Any, List
import asyncio
from .base_agent import BaseAgent
import logging
from datetime import datetime
from pytrends.request import TrendReq
import praw
from newsapi import NewsApiClient

logger = logging.getLogger(__name__)

class TrendAnalysisAgent(BaseAgent):
    def __init__(self, model):
        self.model = model
        self.pytrends = TrendReq(hl='en-US', tz=360)
        
        # Initialize Reddit client only if credentials exist
        reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        
        self.reddit = None
        if reddit_client_id and reddit_client_secret:
            self.reddit = praw.Reddit(
                client_id=reddit_client_id,
                client_secret=reddit_client_secret,
                user_agent="TrendAnalysisAgent/1.0"
            )
        
        self.news_api = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

    async def get_google_trends(self, keyword: str) -> List[Dict]:
        """Fetch trending topics from Google Trends"""
        try:
            self.pytrends.build_payload([keyword], timeframe='today 1-m')
            related_topics = self.pytrends.related_topics()
            return related_topics[keyword]['rising'].to_dict('records')
        except Exception as e:
            logger.error(f"Google Trends error: {str(e)}")
            return []

    async def get_reddit_trends(self, keyword: str) -> List[Dict]:
        """Fetch trending posts from Reddit"""
        if not self.reddit:
            logger.warning("Reddit client not initialized - skipping Reddit trends")
            return []
            
        try:
            subreddit = self.reddit.subreddit('all')
            posts = subreddit.search(keyword, limit=10, sort='hot')
            return [{
                'title': post.title,
                'score': post.score,
                'url': post.url
            } for post in posts]
        except Exception as e:
            logger.error(f"Reddit API error: {str(e)}")
            return []

    async def calculate_virality_score(self, topic_data: Dict) -> float:
        """Calculate virality score based on various metrics"""
        score = 0
        weights = {
            'trend_score': 0.5,
            'engagement_score': 0.5
        }
        
        # Trend score
        if topic_data.get('google_trends'):
            score += weights['trend_score'] * len(topic_data['google_trends'])
        
        # Engagement score
        reddit_posts = topic_data.get('reddit_trends', [])
        if reddit_posts:
            avg_score = sum(post['score'] for post in reddit_posts) / len(reddit_posts)
            score += weights['engagement_score'] * min(avg_score / 1000, 1)  # Cap at 1
        
        return round(score, 2)

    async def process_request(self, topic: str) -> Dict[str, Any]:
        try:
            # Gather data from multiple sources
            tasks = [
                self.get_google_trends(topic),
                self.get_reddit_trends(topic)
            ]
            
            google_trends, reddit_trends = await asyncio.gather(*tasks)
            
            # Compile trend data
            trend_data = {
                'google_trends': google_trends,
                'reddit_trends': reddit_trends
            }
            
            # Calculate virality score
            virality_score = await self.calculate_virality_score(trend_data)
            
            return {
                "type": "trend_analysis",
                "content": trend_data,
                "metadata": {
                    "topic": topic,
                    "virality_score": virality_score,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Trend analysis failed: {str(e)}")
            raise 