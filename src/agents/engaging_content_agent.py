from textblob import TextBlob
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import numpy as np
from typing import List, Dict, Any
import logging
from dataclasses import dataclass
from src.agents.base_agent import BaseAgent
from datetime import datetime
import ssl
import requests

# Create an SSL context that doesn't verify certificates
ssl._create_default_https_context = ssl._create_unverified_context

@dataclass
class ContentStyle:
    tone: str  # formal, conversational, storytelling
    complexity: str  # basic, intermediate, advanced
    target_audience: str  # general, technical, expert
    content_type: str  # article, case_study, summary

class EngagingContentAgent(BaseAgent):
    def __init__(self, config: Any = None):
        self.config = config
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Initialize transformers with SSL verification disabled
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                "gpt2",
                trust_remote_code=True,
                use_auth_token=False
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                "gpt2",
                trust_remote_code=True,
                use_auth_token=False
            )
            
            # Initialize pipelines
            self.sentiment_analyzer = pipeline("sentiment-analysis")
            self.summarizer = pipeline("summarization")
            self.text_generator = pipeline("text-generation")
        except Exception as e:
            self.logger.error(f"Failed to initialize models: {str(e)}")
            raise

    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request to enhance content"""
        try:
            content = request.get('content', '')
            target_audience = request.get('target_audience', 'general')
            
            # Create content style based on request parameters
            style = ContentStyle(
                tone=request.get('tone', 'professional'),
                complexity=request.get('complexity', 'intermediate'),
                target_audience=target_audience,
                content_type=request.get('content_type', 'article')
            )
            
            # Enhance content
            enhanced = await self.enhance_content(content, style)
            
            return {
                "type": "enhanced_content",
                "content": enhanced["enhanced_content"],
                "interactive_elements": enhanced["interactive_elements"],
                "analysis": enhanced["analysis"],
                "metadata": {
                    "style": style.__dict__,
                    "enhancement_timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error processing enhancement request: {str(e)}")
            raise

    async def enhance_content(self, content: str, style: ContentStyle) -> Dict[str, Any]:
        """Main method to enhance content engagement"""
        try:
            # Analyze current content
            analysis = self._analyze_content(content)
            
            # Apply enhancements based on style
            enhanced_content = await self._apply_enhancements(content, style, analysis)
            
            # Generate interactive elements
            interactive_elements = self._generate_interactive_elements(enhanced_content)
            
            return {
                "enhanced_content": enhanced_content,
                "interactive_elements": interactive_elements,
                "analysis": analysis
            }
        except Exception as e:
            self.logger.error(f"Content enhancement failed: {str(e)}")
            raise

    async def _apply_enhancements(self, content: str, style: ContentStyle, analysis: Dict) -> str:
        """Apply various enhancements based on style and analysis"""
        try:
            enhanced_content = content
            
            # Adjust tone
            enhanced_content = await self._adjust_tone(enhanced_content, style.tone)
            
            # Add storytelling elements if appropriate
            if style.tone == "storytelling":
                enhanced_content = await self._add_storytelling_elements(enhanced_content)
            
            # Adjust complexity based on target audience
            enhanced_content = await self._adjust_complexity(
                enhanced_content, 
                style.complexity,
                style.target_audience
            )
            
            return enhanced_content
            
        except Exception as e:
            self.logger.error(f"Enhancement application failed: {str(e)}")
            return content

    async def _adjust_complexity(self, content: str, complexity: str, audience: str) -> str:
        """Adjust content complexity based on target audience"""
        prompt = f"""
        Adjust the following content for a {audience} audience at {complexity} complexity level:
        {content}
        """
        
        try:
            response = self.text_generator(
                prompt,
                max_length=len(content) * 2,
                num_return_sequences=1,
                temperature=0.7
            )
            return response[0]['generated_text']
        except Exception as e:
            self.logger.error(f"Complexity adjustment failed: {str(e)}")
            return content

    def _analyze_content(self, content: str) -> Dict[str, Any]:
        """Analyze content for readability and engagement metrics"""
        try:
            blob = TextBlob(content)
            
            return {
                "sentiment": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity,
                "readability_score": self._calculate_readability(content),
                "emotion_analysis": self._analyze_emotions(content),
                "word_count": len(blob.words),
                "sentence_count": len(blob.sentences)
            }
        except Exception as e:
            self.logger.error(f"Content analysis failed: {str(e)}")
            return {}

    def _generate_interactive_elements(self, content: str) -> Dict[str, Any]:
        """Generate interactive elements for enhanced engagement"""
        try:
            return {
                "quiz": self._generate_quiz_questions(content),
                "summary": self._generate_summary(content),
                "key_points": self._extract_key_points(content),
                "tldr": self._generate_tldr(content)
            }
        except Exception as e:
            self.logger.error(f"Interactive element generation failed: {str(e)}")
            return {}

    def _generate_summary(self, content: str) -> str:
        """Generate a concise summary of the content"""
        try:
            summary = self.summarizer(
                content,
                max_length=150,
                min_length=50,
                do_sample=False
            )[0]['summary_text']
            return summary
        except Exception as e:
            self.logger.error(f"Summary generation failed: {str(e)}")
            return ""

    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from the content"""
        try:
            blob = TextBlob(content)
            sentences = blob.sentences
            
            # Use sentiment and subjectivity to identify important sentences
            key_sentences = [
                str(sentence)
                for sentence in sentences
                if abs(sentence.sentiment.polarity) > 0.3
                or sentence.sentiment.subjectivity < 0.5
            ]
            
            return key_sentences[:5]  # Return top 5 key points
        except Exception as e:
            self.logger.error(f"Key point extraction failed: {str(e)}")
            return []

    async def enhance(self, content: Dict[str, Any], target_audience: str) -> Dict[str, Any]:
        """Enhance content for specific target audience"""
        try:
            style = ContentStyle(
                tone="professional",
                complexity="intermediate",
                target_audience=target_audience,
                content_type="article"
            )
            
            enhanced = await self.enhance_content(content['body'], style)
            
            return {
                "title": content['title'],
                "body": enhanced['enhanced_content'],
                "interactive": enhanced['interactive_elements'],
                "analysis": enhanced['analysis']
            }
        except Exception as e:
            self.logger.error(f"Content enhancement failed: {str(e)}")
            return content

    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score using TextBlob"""
        blob = TextBlob(text)
        words = len(blob.words)
        sentences = len(blob.sentences)
        syllables = sum(self._count_syllables(word) for word in blob.words)
        
        # Calculate Flesch Reading Ease score
        if sentences == 0:
            return 0
        return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

    def _count_syllables(self, word: str) -> int:
        """Helper method to count syllables in a word"""
        count = 0
        vowels = "aeiouy"
        word = word.lower()
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count

    async def _adjust_tone(self, content: str, tone: str) -> str:
        """Adjust content tone using transformer models"""
        prompt = f"Convert the following text to a {tone} tone:\n{content}"
        
        response = self.text_generator(
            prompt,
            max_length=len(content) + 100,
            num_return_sequences=1
        )
        
        return response[0]['generated_text']

    async def _add_storytelling_elements(self, content: str) -> str:
        """Add storytelling elements like analogies and case studies"""
        # Generate analogies
        analogy_prompt = f"Generate an analogy to explain:\n{content}"
        analogy = self.text_generator(analogy_prompt, max_length=200)[0]['generated_text']
        
        # Generate case study
        case_study_prompt = f"Convert this into a case study:\n{content}"
        case_study = self.text_generator(case_study_prompt, max_length=500)[0]['generated_text']
        
        return f"{content}\n\nAnalogy:\n{analogy}\n\nCase Study:\n{case_study}"

    def _generate_quiz_questions(self, content: str, num_questions: int = 3) -> List[Dict]:
        """Generate quiz questions from content"""
        prompt = f"Generate {num_questions} quiz questions about:\n{content}"
        
        questions = self.text_generator(
            prompt,
            max_length=500,
            num_return_sequences=num_questions
        )
        
        return [
            {
                "question": q['generated_text'],
                "options": self._generate_options(q['generated_text']),
                "correct_answer": 0  # Index of correct answer
            }
            for q in questions
        ]

    def _generate_options(self, question: str) -> List[str]:
        """Generate multiple choice options for a question"""
        prompt = f"Generate 4 options for the question:\n{question}"
        
        options = self.text_generator(
            prompt,
            max_length=200,
            num_return_sequences=4
        )
        
        return [opt['generated_text'] for opt in options]

    def _generate_tldr(self, content: str) -> str:
        """Generate TL;DR summary"""
        return self.summarizer(
            content,
            max_length=50,
            min_length=20,
            num_return_sequences=1
        )[0]['summary_text']

    def _analyze_emotions(self, content: str) -> Dict[str, float]:
        """Analyze emotional content of text"""
        emotions = self.sentiment_analyzer(content)
        return emotions[0] if emotions else {} 