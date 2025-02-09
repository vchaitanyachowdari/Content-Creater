from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForCausalLM,
    VisionEncoderDecoderModel,
    ViTImageProcessor
)
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import base64
from PIL import Image
import io
import numpy as np
from typing import List, Dict, Any, Union
import logging
import json

class VisualGeneratorAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize image generation model
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.model = AutoModelForCausalLM.from_pretrained("gpt2")
        
        # Initialize image captioning model
        self.caption_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.caption_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.caption_tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

    async def generate_visuals(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to generate all visual content"""
        try:
            # Extract key points for visualization
            key_points = self._extract_visualization_points(content['text'])
            
            # Generate different types of visuals
            illustrations = await self._generate_illustrations(key_points['main_concepts'])
            charts = self._generate_charts(key_points['data_points'])
            infographics = self._create_infographics(key_points)
            
            return {
                "illustrations": illustrations,
                "charts": charts,
                "infographics": infographics,
                "interactive_elements": self._generate_interactive_elements(key_points)
            }
        except Exception as e:
            self.logger.error(f"Visual generation failed: {e}")
            raise

    def _extract_visualization_points(self, text: str) -> Dict[str, Any]:
        """Extract key points from text that need visualization"""
        # Extract numerical data for charts
        data_points = self._extract_data_points(text)
        
        # Extract main concepts for illustrations
        main_concepts = self._extract_main_concepts(text)
        
        return {
            "data_points": data_points,
            "main_concepts": main_concepts,
            "key_statistics": self._extract_statistics(text)
        }

    async def _generate_illustrations(self, concepts: List[str]) -> List[Dict[str, Any]]:
        """Generate illustrations using Stable Diffusion"""
        illustrations = []
        
        for concept in concepts:
            try:
                # Generate image
                inputs = self.image_processor(concept, return_tensors="pt")
                image = self.image_generator.generate(**inputs)
                
                # Convert to PIL Image
                image = Image.fromarray(image[0])
                
                # Generate caption
                caption = await self._generate_caption(image)
                
                # Convert to base64 for web display
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                illustrations.append({
                    "image": img_str,
                    "caption": caption,
                    "concept": concept
                })
            except Exception as e:
                self.logger.error(f"Illustration generation failed for concept {concept}: {e}")
                
        return illustrations

    def _generate_charts(self, data_points: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate charts using Plotly"""
        charts = []
        
        for chart_type, data in data_points.items():
            try:
                if chart_type == "line":
                    fig = px.line(data['values'], title=data['title'])
                elif chart_type == "bar":
                    fig = px.bar(data['values'], title=data['title'])
                elif chart_type == "pie":
                    fig = px.pie(data['values'], title=data['title'])
                
                # Convert to HTML
                chart_html = fig.to_html(include_plotlyjs=True, full_html=False)
                
                charts.append({
                    "type": chart_type,
                    "html": chart_html,
                    "title": data['title']
                })
            except Exception as e:
                self.logger.error(f"Chart generation failed for type {chart_type}: {e}")
                
        return charts

    def _create_infographics(self, key_points: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create infographics using matplotlib"""
        infographics = []
        
        try:
            # Create figure with subplots
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Add text elements
            for i, (key, value) in enumerate(key_points['key_statistics'].items()):
                ax.text(0.1, 0.9 - (i * 0.1), f"{key}: {value}", 
                       fontsize=12, transform=ax.transAxes)
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            
            # Convert to base64
            img_str = base64.b64encode(buf.getvalue()).decode()
            
            infographics.append({
                "image": img_str,
                "type": "statistics",
                "title": "Key Statistics"
            })
            
            plt.close()
            
        except Exception as e:
            self.logger.error(f"Infographic generation failed: {e}")
            
        return infographics

    def _generate_interactive_elements(self, key_points: Dict[str, Any]) -> Dict[str, str]:
        """Generate HTML/JavaScript code for interactive elements"""
        # Generate interactive visualization using Plotly
        fig = go.Figure()
        
        for point in key_points['data_points'].get('interactive', []):
            fig.add_trace(go.Scatter(
                x=point['x'],
                y=point['y'],
                mode='lines+markers',
                name=point['name']
            ))
        
        fig.update_layout(title="Interactive Data Visualization")
        
        return {
            "plotly_html": fig.to_html(include_plotlyjs=True, full_html=False),
            "custom_js": self._generate_custom_js(key_points)
        }

    def _generate_custom_js(self, key_points: Dict[str, Any]) -> str:
        """Generate custom JavaScript for interactive features"""
        return """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Add interactive functionality
                const elements = document.querySelectorAll('.interactive-element');
                elements.forEach(element => {
                    element.addEventListener('click', function() {
                        // Handle click events
                        console.log('Element clicked:', this.dataset.info);
                    });
                });
            });
        </script>
        """

    async def _generate_caption(self, image: Image) -> str:
        """Generate caption for an image using the caption model"""
        try:
            inputs = self.caption_processor(image, return_tensors="pt")
            output_ids = self.caption_model.generate(**inputs)
            caption = self.caption_tokenizer.decode(output_ids[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            self.logger.error(f"Caption generation failed: {e}")
            return "Image caption generation failed"

    def _extract_data_points(self, text: str) -> Dict[str, Any]:
        """Extract numerical data points from text"""
        # Implement your data extraction logic here
        # This is a placeholder implementation
        return {
            "line": {
                "values": {"x": [1, 2, 3], "y": [4, 5, 6]},
                "title": "Sample Line Chart"
            },
            "bar": {
                "values": {"x": ["A", "B", "C"], "y": [10, 20, 30]},
                "title": "Sample Bar Chart"
            }
        }

    def _extract_main_concepts(self, text: str) -> List[str]:
        """Extract main concepts for illustration"""
        # Implement your concept extraction logic here
        # This is a placeholder implementation
        return ["concept1", "concept2"]

    def _extract_statistics(self, text: str) -> Dict[str, Any]:
        """Extract key statistics from text"""
        # Implement your statistics extraction logic here
        # This is a placeholder implementation
        return {
            "stat1": "value1",
            "stat2": "value2"
        } 