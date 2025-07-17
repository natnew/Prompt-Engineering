# Copilot Instructions for Prompt Engineering Tool

This is a Python-based Streamlit application designed to help users learn, experiment, and master prompt engineering techniques across multiple AI models. The tool provides an interactive web interface for applying various prompting strategies, supporting multiple OpenAI models (GPT-4o, GPT-4, GPT-3.5, o1-series), and includes advanced features like audio-to-text transcription, department-specific prompts, and comprehensive security measures.

## Code Standards

### Python Code Style
- Follow PEP 8 conventions for Python code formatting
- Use meaningful variable and function names that clearly describe their purpose
- Include comprehensive docstrings for all functions and classes using Google-style docstrings
- Maintain consistent indentation (4 spaces) throughout the codebase
- Keep line length under 100 characters where practical
- Use type hints for function parameters and return values where applicable

### Documentation Standards
- All functions must include docstrings with Parameters, Returns, and Example sections
- Code comments should explain "why" not "what" - the code should be self-explanatory
- Maintain up-to-date README.md and API_DOCUMENTATION.md files
- Document any breaking changes or new features in commit messages

### Security Requirements
- Always sanitize user input using the `sanitize_user_input()` function before processing
- Validate all file uploads (audio files) for size limits and allowed MIME types
- Never expose API keys in code - use environment variables exclusively
- Implement proper error handling for all external API calls
- Use rate limiting and exponential backoff for API requests

### Required Before Each Commit

#### Code Quality Checks
1. **Run all existing tests** to ensure no regressions
2. **Validate code formatting** with appropriate Python linters
3. **Check for security vulnerabilities** in dependencies and user inputs
4. **Verify error handling** for edge cases and API failures
5. **Test with multiple models** to ensure compatibility across OpenAI model variants

#### Documentation Updates
1. **Update API_DOCUMENTATION.md** if any public functions are added or modified
2. **Add or update docstrings** for any new or changed functions
3. **Update README.md** if new features or setup requirements are introduced
4. **Include usage examples** for any new functionality

#### Security Validation
1. **Test input sanitization** with potentially malicious prompts
2. **Verify file upload security** for audio processing features
3. **Check API key handling** to ensure no exposure in logs or responses
4. **Validate model parameter ranges** to prevent abuse

### Development Flow

#### Feature Development Process
1. **Create feature branch** from main (if working in teams)
2. **Implement core functionality** following established patterns
3. **Add comprehensive tests** for new features
4. **Update documentation** including API docs and examples
5. **Test integration** with existing Streamlit interface
6. **Perform security review** of all user-facing inputs
7. **Submit pull request** with detailed description of changes

#### Testing Requirements
- Test all prompt engineering techniques with sample inputs
- Verify model responses are properly streamed and displayed
- Test audio upload and transcription functionality
- Validate parameter sliders and form inputs work correctly
- Ensure error messages are user-friendly and informative

#### Code Review Checklist
- Functions follow single responsibility principle
- Error handling covers all expected failure modes
- Security measures are properly implemented
- Documentation is complete and accurate
- Code follows established project patterns

## Repository Structure

```
├── src/                          # Core application modules
│   ├── app.py                   # Main Streamlit application entry point
│   ├── models.py                # OpenAI API interaction and model management
│   ├── prompt_engineering.py   # Prompt transformation techniques
│   ├── utils.py                 # Configuration loading utilities
│   └── machine_learning.py     # ML-specific prompt implementations
├── pages/                       # Streamlit multipage components
│   ├── Home.py                  # Application overview and instructions
│   └── About.py                 # Course information and objectives
├── data/                        # Configuration and example data
│   ├── techniques.json          # Prompt engineering technique definitions
│   ├── departments_prompts.json # Department-specific example prompts
│   └── ethical_guidelines.json  # AI usage ethics and best practices
├── audio/                       # Audio processing resources
├── assets/                      # Static resources and documentation
├── API_DOCUMENTATION.md         # Comprehensive API reference
├── SECURITY_IMPROVEMENTS.md     # Security implementation details
├── README.md                    # Project overview and setup instructions
├── requirements.txt             # Python dependencies
└── Workflow.md                  # Development process guidelines
```

### Key File Descriptions
- **src/app.py**: Main Streamlit interface with UI components, audio processing, and user interaction
- **src/models.py**: OpenAI API wrapper with model selection, response streaming, and security functions
- **src/prompt_engineering.py**: Core prompt transformation logic for all supported techniques
- **data/techniques.json**: Configuration defining available prompt engineering methods
- **data/departments_prompts.json**: Example prompts organized by business department

## Key Guidelines

### Streamlit Development Patterns
- Use session state for maintaining user preferences across interactions
- Implement proper error handling with user-friendly st.error() messages
- Utilize st.spinner() for long-running operations like API calls
- Stream responses using st.write_stream() for better user experience
- Organize UI components logically with st.sidebar, st.columns, and st.expander

### OpenAI API Integration
- Always check model availability before making API calls
- Implement exponential backoff for rate limit handling
- Use appropriate parameters for different model families (especially o1-series)
- Handle streaming responses properly for real-time user feedback
- Sanitize all prompts before sending to prevent injection attacks

### Prompt Engineering Implementation
- Each technique should have a clear transformation function in prompt_engineering.py
- Include detailed explanations for educational purposes
- Maintain consistency in prompt formatting across techniques
- Support both educational examples and practical use cases
- Validate technique selection before applying transformations

### Configuration Management
- Store all configurable data in JSON files under data/ directory
- Use utils.py functions for loading configuration consistently
- Validate configuration file structure on application startup
- Provide clear error messages for missing or malformed configuration files
- Support easy extension of techniques and department prompts

### Audio Processing Guidelines
- Validate audio file format and size before processing
- Use OpenAI Whisper API for transcription with proper error handling
- Support multiple audio formats (MP3, WAV, M4A)
- Implement chunking for large audio files to stay within API limits
- Provide clear feedback to users during audio processing

### Security Best Practices
- Never trust user input - always sanitize and validate
- Implement comprehensive prompt injection detection patterns
- Use environment variables for all sensitive configuration
- Log security events without exposing sensitive data
- Regularly update dependencies to address security vulnerabilities
- Implement rate limiting to prevent abuse

### Performance Optimization
- Cache configuration data loading using Streamlit's caching mechanisms
- Minimize API calls through intelligent user interaction design
- Use streaming responses to improve perceived performance
- Implement proper loading states and progress indicators
- Optimize file upload handling for audio processing features

### Error Handling Standards
- Provide specific, actionable error messages to users
- Log detailed error information for debugging purposes
- Implement graceful degradation when external services are unavailable
- Use try-catch blocks around all external API calls
- Validate all user inputs before processing

### Testing and Quality Assurance
- Test all prompt engineering techniques with various input types
- Verify cross-model compatibility for different OpenAI models
- Test audio upload and transcription with various file formats
- Validate security measures with potential attack vectors
- Ensure responsive design works across different screen sizes
