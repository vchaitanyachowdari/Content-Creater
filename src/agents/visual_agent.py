from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    VisionEncoderDecoderModel,
    ViTImageProcessor
)
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import logging
from typing import Dict, Any, List
import io

class VisualGeneratorAgent:
    """Agent responsible for generating visuals and charts"""
    
    def __init__(self, config: Any):
        self.logger = logging.getLogger(__name__)
        
        try:
            # Initialize models
            self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
            self.model = AutoModelForCausalLM.from_pretrained("gpt2")
            self.image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            self.caption_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            self.logger.info("Visual generator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize visual generator: {e}")
            raise

    async def generate_visuals(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visuals for the content"""
        try:
            charts = self._create_charts(content.get('data', {}))
            diagrams = self._create_diagrams(content.get('concepts', []))
            
            return {
                "charts": charts,
                "diagrams": diagrams
            }
            
        except Exception as e:
            self.logger.error(f"Visual generation failed: {e}")
            return {"charts": [], "diagrams": []}

    def _create_charts(self, data: Dict) -> List[Dict[str, Any]]:
        """Create charts using plotly"""
        charts = []
        try:
            if data:
                # Create bar chart
                fig = px.bar(data)
                chart_html = fig.to_html(include_plotlyjs=True, full_html=False)
                charts.append({
                    "type": "bar",
                    "html": chart_html
                })
                
        except Exception as e:
            self.logger.error(f"Chart creation failed: {e}")
            
        return charts

    def _create_diagrams(self, concepts: List[str]) -> List[Dict[str, Any]]:
        """Create diagrams using matplotlib"""
        diagrams = []
        try:
            if concepts:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.text(0.5, 0.5, "\n".join(concepts), ha='center', va='center')
                
                # Save to buffer
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)
                img_str = base64.b64encode(buf.getvalue()).decode()
                
                diagrams.append({
                    "type": "concept_map",
                    "image": img_str
                })
                
                plt.close()
                
        except Exception as e:
            self.logger.error(f"Diagram creation failed: {e}")
            
        return diagrams 