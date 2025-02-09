from typing import Dict, Any, List, Optional
from src.agents.base_agent import BaseAgent
import asyncio
from datetime import datetime
import json
from src.utils.logger import logger

class ContentOptimizer:
    """Advanced content optimization with Claude-like principles"""
    
    def __init__(self, model):
        self.model = model
        self.optimization_principles = {
            "constitutional": {
                "helpfulness": True,
                "honesty": True,
                "harmlessness": True,
                "bias_avoidance": True,
            },
            "quality_metrics": {
                "trustworthiness": True,
                "expertise": True,
                "authoritativeness": True,
                "experience": True
            }
        }
    
    async def optimize_content(self, content: str, intent: Dict[str, Any]) -> str:
        prompt = f"""
        Optimize this content following Claude-style principles:

        Content: {content}
        Intent: {intent}

        Apply these principles:
        1. Constitutional AI Guidelines:
           * Ensure helpfulness and accuracy
           * Maintain ethical standards
           * Avoid harmful content
           * Remove biases

        2. Quality Requirements:
           * Demonstrate expertise
           * Show authoritativeness
           * Include experience-based insights
           * Maintain trustworthiness

        3. Writing Standards:
           * Clear and engaging style
           * Proper citations
           * Logical structure
           * Natural keyword usage

        Return optimized content maintaining these standards.
        """
        try:
            response = await self.model.generate_content(prompt)
            return str(response).strip()
        except Exception as e:
            logger.warning(f"Content optimization failed: {e}")
            return content  # Return original content if optimization fails

class ContentStructurer:
    """Handles content structure and organization"""
    
    def __init__(self, model):
        self.model = model
    
    async def create_outline(self, topic: str, keywords: List[str]) -> Dict[str, Any]:
        # Default outline
        default_outline = {
            "title": topic,
            "sections": [
                {
                    "heading": "Introduction",
                    "subheadings": [],
                    "key_points": ["Overview", "Background"]
                },
                {
                    "heading": "Main Content",
                    "subheadings": ["Key Points", "Analysis"],
                    "key_points": []
                },
                {
                    "heading": "Conclusion",
                    "subheadings": [],
                    "key_points": ["Summary", "Recommendations"]
                }
            ]
        }

        prompt = f"""
        Generate a content outline for: {topic}
        Keywords: {', '.join(keywords) if keywords else 'None'}
        
        Respond with ONLY a JSON object in this exact format:
        {json.dumps(default_outline, indent=2)}
        """
        
        try:
            response = await self.model.generate_content(prompt)
            if not response:
                return default_outline
                
            # Clean and parse response
            response_text = str(response).strip()
            # Remove any markdown or code block markers
            response_text = response_text.replace('```json', '').replace('```', '')
            
            try:
                # Try to parse the entire response first
                return json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON if full parse fails
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = response_text[start:end]
                    return json.loads(json_str)
                
            return default_outline
            
        except Exception as e:
            logger.warning(f"Outline creation failed: {e}")
            return default_outline

class ClaudeStyleAgent(BaseAgent):
    """Content generation agent using Claude-style principles"""
    
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.optimizer = ContentOptimizer(model)
        self.structurer = ContentStructurer(model)
        
    def _clean_json_string(self, text: str) -> str:
        """Clean and prepare string for JSON parsing"""
        text = text.strip()
        # Remove markdown code blocks
        text = text.replace('```json', '').replace('```', '')
        # Remove newlines and extra spaces
        text = ' '.join(text.split())
        return text
        
    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract and parse JSON from text"""
        try:
            # Try direct JSON parsing first
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON if embedded in text
            try:
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = text[start:end]
                    return json.loads(json_str)
            except:
                return None
        return None

    async def analyze_requirements(self, request: str) -> Dict[str, Any]:
        default_response = {
            "target_audience": "general",
            "content_type": "article",
            "required_depth": "comprehensive",
            "style_preferences": "professional",
            "key_objectives": ["inform", "engage"],
            "quality_metrics": ["accuracy", "readability"]
        }

        prompt = f"""
        Analyze requirements for: {request}
        Return ONLY a JSON object exactly like this (with appropriate values):
        {json.dumps(default_response, indent=2)}
        Do not include any additional text or formatting.
        """
        
        try:
            response = await self.model.generate_content(prompt)
            if not response:
                return default_response
                
            cleaned_response = self._clean_json_string(response)
            parsed_json = self._extract_json(cleaned_response)
            
            if parsed_json:
                # Validate required fields
                for key in default_response.keys():
                    if key not in parsed_json:
                        parsed_json[key] = default_response[key]
                return parsed_json
                
            return default_response
            
        except Exception as e:
            logger.error(f"Requirements analysis failed: {str(e)}")
            return default_response
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validate input
            if not isinstance(request, dict):
                raise ValueError("Request must be a dictionary")
            if 'content' not in request or 'metadata' not in request:
                raise ValueError("Request must contain 'content' and 'metadata' keys")
                
            # Process request
            requirements = await self.analyze_requirements(request['content'])
            
            # Get keywords safely
            keywords = request['metadata'].get('keywords', [])
            topic = request['metadata'].get('topic', request['content'])
            
            # Create outline
            outline = await self.structurer.create_outline(topic, keywords)
            
            # Generate content
            content_prompt = f"""
            Generate content following this structure:
            {json.dumps(outline, indent=2)}

            Requirements:
            {json.dumps(requirements, indent=2)}

            Guidelines:
            1. Focus on quality and accuracy
            2. Include expert insights
            3. Maintain clear structure
            4. Use natural language
            5. Incorporate citations
            6. Ensure readability
            """
            
            initial_content = await self.model.generate_content(content_prompt)
            if not initial_content:
                raise ValueError("Failed to generate initial content")
                
            # Optimize content
            optimized_content = await self.optimizer.optimize_content(
                initial_content,
                requirements
            )
            
            return {
                "type": "claude_style_content",
                "content": optimized_content,
                "metadata": {
                    **request['metadata'],
                    "optimization": {
                        "constitutional_principles": self.optimizer.optimization_principles,
                        "quality_metrics": True,
                        "content_structure": outline,
                        "requirements": requirements
                    },
                    "generation_timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error in ClaudeStyleAgent: {str(e)}")
            raise 