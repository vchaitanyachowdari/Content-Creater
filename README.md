# ChiatuAI: Advanced Content Generation System 🚀

A sophisticated AI-powered content generation system leveraging Google's Gemini API for creating high-quality, optimized content with visual elements.

## 🌟 Features

### Content Generation
- **AI-Powered Writing**: Utilizes Google's Gemini for advanced text generation
- **SEO Optimization**: Built-in SEO enhancement
- **Visual Content**: Automatic generation of charts and diagrams
- **Blog Integration**: Direct publishing to blogging platforms

### Quality Assurance
- **Fact Checking**: Automated verification of content
- **Source Citation**: Proper attribution and referencing
- **Engagement Metrics**: Content quality scoring

### Visual Elements
- **Charts & Graphs**: Data visualization using Plotly
- **Diagrams**: Concept visualization with Matplotlib
- **Interactive Elements**: Dynamic content components

## 🛠️ Technical Architecture

### Core Components
```
Chaitanya Agent/
├── src/
│   ├── agents/
│   │   ├── content_engine.py     # Main orchestrator
│   │   ├── article_agent.py      # Content generation
│   │   ├── visual_agent.py       # Visual creation
│   │   └── seo_agent.py         # SEO optimization
│   ├── models/
│   │   └── ai_model.py          # Gemini integration
│   ├── services/
│   │   └── blogger_service.py    # Blog publishing
│   └── utils/
│       ├── config.py            # Configuration
│       └── logger.py            # Logging
├── config/
│   └── config.yaml              # Settings
└── main.py                      # Entry point
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google AI API key
- Blogger API credentials (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chiatai.git
cd chiatai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
   - Create `.env` file:
```env
GOOGLE_AI_KEY=your_gemini_api_key
BLOGGER_API_KEY=your_blogger_key
```

### Usage

1. Run the system:
```bash
python main.py
```

2. Enter your topic when prompted:
```
=== ChiatuAI Content Generator ===
Enter your topic: Your topic here
```

3. View generated content:
```
=== Generated Content ===
Title: [Generated Title]
Content Preview: [Content Preview]
Word Count: [Count]
Generated Visuals: [Number]
```

## 📊 Content Generation Flow

1. **Input Processing**
   - Topic analysis
   - Preference configuration

2. **Content Creation**
   - AI-powered writing
   - SEO optimization
   - Fact verification

3. **Visual Generation**
   - Chart creation
   - Diagram generation
   - Interactive elements

4. **Output Formatting**
   - Content assembly
   - Visual integration
   - Quality checks

## 🔧 Configuration

### config.yaml
```yaml
api_keys:
  google_ai: "your-key"
  blogger: "your-key"

preferences:
  style: "professional"
  target_audience: "general"
  include_visuals: true
```

## 📦 Dependencies

Key packages:
- `google-generativeai`: AI content generation
- `transformers`: Visual generation
- `plotly`: Interactive charts
- `matplotlib`: Static visualizations

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Author

- **V Chaitanya Chowdari**
  - GitHub: [@vchaitanyachowdari](https://github.com/vchaitanyachowdari)

## 🙏 Acknowledgments

- Google AI for Gemini API
- Open-source community
- Contributors and testers

## 📞 Support

For support:
1. Open an issue
2. Email: vchaitanyachowdari@gmail.com
3. Documentation: [Link](www.vchaitanyachowdari.wordpress.com)

## 🔄 Updates

Latest version: 1.0.0
- Initial release
- Core functionality
- Visual generation
- Blog integration

## 🔮 Future Plans

- Enhanced visual generation
- More integration options
- Advanced SEO features
- Real-time analytics
