from setuptools import setup, find_packages
import os
from pathlib import Path

def setup_project():
    # Project root directory
    root = Path(__file__).parent
    
    # Create directory structure
    directories = [
        "src/agents",
        "src/models",
        "src/services",
        "src/utils",
        "config/credentials",
        "tests"
    ]
    
    for directory in directories:
        (root / directory).mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py files
    init_locations = [
        "src",
        "src/agents",
        "src/models",
        "src/services",
        "src/utils",
        "tests"
    ]
    
    for location in init_locations:
        init_file = root / location / "__init__.py"
        init_file.touch()
    
    # Create config.yaml
    config_content = """api_keys:
  anthropic: "your-key"
  blogger: "your-key"

preferences:
  default_style: "engaging"
  default_tone: "professional"
  default_audience: "general"
"""
    
    with open(root / "config" / "config.yaml", "w") as f:
        f.write(config_content)
    
    # Create requirements.txt
    requirements = """anthropic
python-dotenv
google-auth-oauthlib
google-api-python-client
markdown
pyyaml
transformers
torch
pillow
matplotlib
plotly
numpy
textblob
spacy
"""
    
    with open(root / "requirements.txt", "w") as f:
        f.write(requirements)
    
    # Create .env template
    env_content = """ANTHROPIC_API_KEY=your_api_key_here
BLOGGER_API_KEY=your_blogger_key_here
"""
    
    with open(root / ".env", "w") as f:
        f.write(env_content)
    
    print("Project structure created successfully!")

if __name__ == "__main__":
    setup_project()

setup(
    name="chaitanya-agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'google-generativeai',
        'python-dotenv',
        'setuptools',
    ],
) 