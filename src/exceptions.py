"""Custom exceptions for the Prompt Engineering Tool.

This module defines domain-specific exceptions that provide better error handling
and debugging capabilities throughout the application.
"""

class PromptEngineeringError(Exception):
    """Base exception for prompt engineering operations."""
    pass

class APIError(PromptEngineeringError):
    """Exception for external API failures (OpenAI, Whisper, etc.)."""
    
    def __init__(self, message, status_code=None, retry_after=None, api_name=None):
        super().__init__(message)
        self.status_code = status_code
        self.retry_after = retry_after
        self.api_name = api_name or "Unknown API"
    
    def __str__(self):
        base_msg = super().__str__()
        if self.status_code:
            return f"{self.api_name} API Error (Status {self.status_code}): {base_msg}"
        return f"{self.api_name} API Error: {base_msg}"

class ValidationError(PromptEngineeringError):
    """Exception for input validation failures."""
    
    def __init__(self, message, field_name=None, invalid_value=None):
        super().__init__(message)
        self.field_name = field_name
        self.invalid_value = invalid_value
    
    def __str__(self):
        base_msg = super().__str__()
        if self.field_name:
            return f"Validation Error in '{self.field_name}': {base_msg}"
        return f"Validation Error: {base_msg}"

class ConfigurationError(PromptEngineeringError):
    """Exception for configuration loading and validation failures."""
    
    def __init__(self, message, config_file=None, config_key=None):
        super().__init__(message)
        self.config_file = config_file
        self.config_key = config_key
    
    def __str__(self):
        base_msg = super().__str__()
        if self.config_file:
            return f"Configuration Error in '{self.config_file}': {base_msg}"
        return f"Configuration Error: {base_msg}"

class AudioProcessingError(PromptEngineeringError):
    """Exception for audio processing and transcription failures."""
    
    def __init__(self, message, file_name=None, file_size=None):
        super().__init__(message)
        self.file_name = file_name
        self.file_size = file_size
    
    def __str__(self):
        base_msg = super().__str__()
        if self.file_name:
            return f"Audio Processing Error for '{self.file_name}': {base_msg}"
        return f"Audio Processing Error: {base_msg}"

class ModelError(PromptEngineeringError):
    """Exception for model-related errors (selection, parameters, etc.)."""
    
    def __init__(self, message, model_name=None, parameter_name=None):
        super().__init__(message)
        self.model_name = model_name
        self.parameter_name = parameter_name
    
    def __str__(self):
        base_msg = super().__str__()
        if self.model_name:
            return f"Model Error for '{self.model_name}': {base_msg}"
        return f"Model Error: {base_msg}"

class PromptInjectionError(PromptEngineeringError):
    """Exception for detected prompt injection attempts."""
    
    def __init__(self, message, detected_pattern=None, input_text=None):
        super().__init__(message)
        self.detected_pattern = detected_pattern
        self.input_text = input_text[:100] + "..." if input_text and len(input_text) > 100 else input_text
    
    def __str__(self):
        base_msg = super().__str__()
        if self.detected_pattern:
            return f"Prompt Injection Detected (Pattern: {self.detected_pattern}): {base_msg}"
        return f"Prompt Injection Detected: {base_msg}"
