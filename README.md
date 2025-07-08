# 🚀 Interactive Prompt Engineering Tool

A comprehensive Streamlit application for learning, experimenting, and mastering prompt engineering techniques with multiple AI models. Perfect for educators, researchers, content creators, and anyone looking to optimize their AI interactions.

## 🌟 Key Features

### 🤖 **Multi-Model Support**
- **OpenAI Models**: GPT-4o, GPT-4o mini, GPT-4 Turbo, GPT-4, GPT-3.5 Turbo
- **Advanced Models**: o1, o1-mini, o3-mini (with specialized parameter handling)
- **Intelligent Model Selection**: Automatic parameter optimization per model type

### 🧠 **Advanced Prompt Engineering Techniques**
- **Zero-Shot Prompting**: Direct prompting without examples
- **Few-Shot Prompting**: Learning from contextual examples
- **Chain-of-Thought**: Step-by-step reasoning processes
- **Meta-Prompting**: AI-generated prompt optimization
- **Self-Consistency**: Coherent and logical response validation
- **Tree-of-Thought**: Multi-path exploration for complex problems

### 🏢 **Department-Specific Contexts**
- Customer Services & Fulfillment
- Editorial/Publishing
- Marketing & Communications
- Operations & Production
- Branding & Design
- Corporate Communications

### 🎙️ **Audio Integration**
- Speech-to-text transcription using OpenAI Whisper
- Support for multiple audio formats (MP3, WAV, M4A)
- Secure audio processing with size limits

### 🔒 **Enterprise-Grade Security**
- Advanced prompt injection prevention
- Input sanitization and validation
- Rate limiting with intelligent backoff
- Secure API key management

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/prompt-engineering-tool.git
cd prompt-engineering-tool

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the application
streamlit run src/app.py
```

## 📦 Installation & Setup

### Prerequisites
- **Python 3.8+** (recommended for full compatibility)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/signup))
- **Git** for version control

### Detailed Installation

1. **Clone and Navigate**:
   ```bash
   git clone https://github.com/yourusername/prompt-engineering-tool.git
   cd prompt-engineering-tool
   ```

2. **Create Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   ```bash
   # Create a .env file or set environment variable
   echo "OPENAI_API_KEY=your-actual-api-key-here" > .env
   
   # Or export directly (Linux/macOS)
   export OPENAI_API_KEY="your-actual-api-key-here"
   
   # Or set permanently (Windows)
   setx OPENAI_API_KEY "your-actual-api-key-here"
   ```

5. **Launch the Application**:
   ```bash
   streamlit run src/app.py
   ```

6. **Open in Browser**:
   Navigate to `http://localhost:8501` to start experimenting!

## 💡 Usage Examples

### Example 1: Customer Service Response Optimization

```python
# Original prompt
"How do I return a damaged book?"

# Using Few-Shot Prompting
# The app automatically adds relevant examples:
"""
Example: How to handle a return request.
Response: Thank you for contacting us. I'll help you process your return...

How do I return a damaged book?
"""

# Result: More structured, professional customer service response
```

### Example 2: Academic Content Creation

```python
# Original prompt
"Explain quantum computing"

# Using Chain-of-Thought Prompting
# The app transforms it to:
"""
Let's think step-by-step.
Explain quantum computing
"""

# Result: Detailed, logical progression from basic concepts to advanced topics
```

### Example 3: Marketing Copy Generation

```python
# Original prompt
"Write a product description for our new textbook"

# Using Meta-Prompting
# The app transforms it to:
"""
Create a new prompt based on the task requirements: 
Write a product description for our new textbook
"""

# Result: AI generates an optimized prompt for better marketing copy
```

### Example 4: Audio Input Workflow

1. **Record or upload** an audio file containing your prompt
2. **Automatic transcription** using OpenAI Whisper
3. **Apply techniques** to the transcribed text
4. **Generate responses** with your selected model

## 🛠️ Available Prompt Engineering Techniques

| Technique | Best For | Example Use Case |
|-----------|----------|------------------|
| **Zero-Shot** | Quick, direct questions | "What is the capital of France?" |
| **Few-Shot** | Pattern recognition, formatting | Creating consistent email templates |
| **Chain-of-Thought** | Complex reasoning, math problems | Multi-step calculations or analysis |
| **Meta-Prompting** | Prompt optimization | Improving existing prompts |
| **Self-Consistency** | Reliable, stable outputs | Professional communications |
| **Tree-of-Thought** | Creative problem-solving | Brainstorming sessions |

## 🏢 Department-Specific Use Cases

### Customer Services & Fulfillment
- Draft professional customer inquiry responses
- Create subscription access guides
- Develop automated response systems

### Editorial/Publishing
- Academic manuscript editing
- Research paper summarization
- Content formatting automation

### Marketing
- Product descriptions and campaigns
- Social media content strategy
- Engagement prediction models

### Operations
- Workflow optimization
- Process documentation
- Production scheduling

## 🔧 API Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional - for future model integrations
ANTHROPIC_API_KEY=your-anthropic-key
COHERE_API_KEY=your-cohere-key
```

### Model Parameters
- **Temperature**: 0.0-2.0 (creativity vs consistency)
- **Top-p**: 0.0-1.0 (nucleus sampling)
- **Max Tokens**: 500-10000 (response length)
- **Specialized handling** for o1/o3 series models

## 📁 Project Structure

```
prompt-engineering-tool/
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── models.py              # Model interaction and API calls
│   ├── prompt_engineering.py  # Technique implementations
│   ├── utils.py               # Utility functions
│   └── machine_learning.py    # ML utilities
├── data/
│   ├── techniques.json        # Technique definitions
│   ├── departments_prompts.json # Example prompts by department
│   └── ethical_guidelines.json # AI ethics guidelines
├── pages/
│   ├── Home.py               # Main interface
│   └── About.py              # Documentation
├── audio/                    # Audio processing utilities
├── assets/                   # Static assets and styling
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Extension Ideas

### 🔮 **Near-term Enhancements**
1. **Multi-Model Comparison**
   - Side-by-side response comparison
   - Performance benchmarking
   - Cost analysis per model

2. **Advanced Analytics**
   - Response quality scoring
   - Technique effectiveness metrics
   - Usage pattern analysis

3. **Collaboration Features**
   - Shared prompt libraries
   - Team workspaces
   - Version control for prompts

### 🌟 **Advanced Features**
4. **Custom Technique Builder**
   - Visual prompt engineering workflow
   - Drag-and-drop technique composition
   - Community-shared techniques

5. **Industry-Specific Modules**
   - Legal document analysis
   - Medical terminology handling
   - Financial report generation

6. **AI-Powered Optimization**
   - Automatic technique selection
   - Prompt quality prediction
   - Real-time improvement suggestions

### 🔬 **Research & Development**
7. **Model Fine-tuning Interface**
   - Custom model training workflows
   - Dataset management
   - Performance evaluation tools

8. **Ethical AI Dashboard**
   - Bias detection and mitigation
   - Content safety monitoring
   - Compliance reporting

9. **Enterprise Integration**
   - API endpoints for automation
   - Database connectivity
   - Single sign-on (SSO) support

### 🌐 **Platform Extensions**
10. **Multi-language Support**
    - Internationalization (i18n)
    - Cross-language prompt techniques
    - Cultural context adaptation

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 src/
black src/
```

### Contribution Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Contact

- **Documentation**: Check the `/pages/About.py` section in the app
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join our GitHub Discussions for questions
- **Security**: Report security vulnerabilities to [security@yourorg.com]

## 🙏 Acknowledgments

- **OpenAI** for providing powerful language models and APIs
- **Streamlit** for the excellent web app framework
- **Contributors** who help improve this tool
- **Academic community** for prompt engineering research

---

**Ready to revolutionize your AI interactions? Start experimenting with prompt engineering today!** 🎯
