"""Error handling utilities and decorators for the Prompt Engineering Tool.

This module provides standardized error handling patterns, retry mechanisms,
and user-friendly error display functions.
"""

import time
import logging
import functools
from typing import Callable, Any, Optional, Dict, Union
import streamlit as st

from exceptions import (
    APIError,
    ValidationError,
    ConfigurationError,
    AudioProcessingError,
    ModelError,
    PromptInjectionError,
)
from logging_config import get_logger, log_function_call

logger = get_logger(__name__)

def handle_api_errors(
    retry_count: int = 3,
    backoff_factor: float = 2.0,
    max_wait_time: float = 60.0,
    api_name: str = "API"
):
    """Decorator for handling API errors with exponential backoff retry logic.
    
    Args:
        retry_count: Number of retry attempts
        backoff_factor: Exponential backoff multiplier
        max_wait_time: Maximum wait time between retries
        api_name: Name of the API for error reporting
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(retry_count):
                try:
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    
                    log_function_call(
                        func.__name__,
                        {'attempt': attempt + 1},
                        duration
                    )
                    
                    return result
                    
                except Exception as e:
                    last_exception = e
                    
                    if attempt == retry_count - 1:
                        # Last attempt failed
                        logger.error(
                            f"{api_name} call failed after {retry_count} attempts",
                            extra={
                                'function': func.__name__,
                                'error': str(e),
                                'attempts': retry_count
                            }
                        )
                        raise APIError(
                            f"Failed after {retry_count} attempts: {str(e)}",
                            api_name=api_name
                        ) from e
                    
                    # Calculate wait time with exponential backoff
                    wait_time = min(backoff_factor ** attempt, max_wait_time)
                    
                    logger.warning(
                        f"{api_name} call failed, retrying in {wait_time}s",
                        extra={
                            'function': func.__name__,
                            'attempt': attempt + 1,
                            'wait_time': wait_time,
                            'error': str(e)
                        }
                    )
                    
                    time.sleep(wait_time)
            
            # This should never be reached, but just in case
            raise last_exception
        
        return wrapper
    return decorator

def validate_input(
    validation_func: Callable[[Any], bool],
    error_message: str,
    field_name: Optional[str] = None
):
    """Decorator for input validation.
    
    Args:
        validation_func: Function that returns True if input is valid
        error_message: Error message to display if validation fails
        field_name: Name of the field being validated
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Apply validation to the first argument (assumed to be the input)
            if args and not validation_func(args[0]):
                logger.warning(
                    f"Input validation failed for {func.__name__}",
                    extra={
                        'field_name': field_name,
                        'error_message': error_message
                    }
                )
                raise ValidationError(error_message, field_name=field_name)
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

def safe_execute(
    func: Callable,
    *args,
    default_return: Any = None,
    log_errors: bool = True,
    **kwargs
) -> Any:
    """Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        default_return: Value to return if function fails
        log_errors: Whether to log errors
        *args, **kwargs: Arguments to pass to the function
        
    Returns:
        Function result or default_return if function fails
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_errors:
            logger.error(
                f"Error executing {func.__name__}",
                extra={'error': str(e), 'args': str(args)[:200]}
            )
        return default_return

def display_error_to_user(
    error: Exception,
    context: str = "",
    show_details: bool = False
) -> None:
    """Display user-friendly error messages in Streamlit.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
        show_details: Whether to show technical details
    """
    if isinstance(error, ValidationError):
        st.warning(f"⚠️ Input Validation Error: {str(error)}")
        if error.field_name:
            st.info(f"💡 Please check the '{error.field_name}' field and try again.")
    
    elif isinstance(error, APIError):
        st.error(f"🔌 API Connection Issue: {str(error)}")
        if error.status_code == 429:
            st.info("💡 Rate limit exceeded. Please wait a moment and try again.")
        elif error.status_code == 401:
            st.info("💡 API key issue. Please check your OpenAI API key configuration.")
        else:
            st.info("💡 Please check your internet connection and try again.")
    
    elif isinstance(error, ConfigurationError):
        st.error(f"⚙️ Configuration Error: {str(error)}")
        st.info("💡 Please check the configuration file and ensure it's properly formatted.")
    
    elif isinstance(error, AudioProcessingError):
        st.error(f"🎵 Audio Processing Error: {str(error)}")
        st.info("💡 Please check your audio file format and size (max 25MB).")
    
    elif isinstance(error, ModelError):
        st.error(f"🤖 Model Error: {str(error)}")
        st.info("💡 Please try selecting a different model or check the parameters.")
    
    elif isinstance(error, PromptInjectionError):
        st.warning(f"🛡️ Security Warning: {str(error)}")
        st.info("💡 Please modify your input and avoid potentially harmful patterns.")
    
    else:
        st.error(f"❌ Unexpected Error: {str(error)}")
        st.info("🔧 Please try again or contact support if the issue persists.")
    
    if context:
        st.caption(f"Context: {context}")
    
    if show_details and hasattr(error, '__traceback__'):
        with st.expander("🔍 Technical Details"):
            st.code(str(error), language="text")

def create_error_response(
    error: Exception,
    success: bool = False,
    correlation_id: str = None
) -> Dict[str, Any]:
    """Create standardized error response dictionary.
    
    Args:
        error: The exception that occurred
        success: Whether the operation was successful
        correlation_id: Request correlation ID
        
    Returns:
        Standardized error response dictionary
    """
    error_type = type(error).__name__
    
    response = {
        "success": success,
        "error": {
            "type": error_type,
            "message": str(error),
            "correlation_id": correlation_id
        },
        "timestamp": time.time()
    }
    
    # Add specific error details based on error type
    if isinstance(error, ValidationError):
        response["error"]["field_name"] = error.field_name
        response["error"]["suggestion"] = "Please check your input and try again."
    
    elif isinstance(error, APIError):
        response["error"]["api_name"] = error.api_name
        response["error"]["status_code"] = error.status_code
        if error.status_code == 429:
            response["error"]["suggestion"] = "Rate limit exceeded. Please wait and retry."
        else:
            response["error"]["suggestion"] = "Please check your API configuration."
    
    elif isinstance(error, ConfigurationError):
        response["error"]["config_file"] = error.config_file
        response["error"]["suggestion"] = "Please check your configuration file."
    
    else:
        response["error"]["suggestion"] = "Please try again or contact support."
    
    return response

def log_error_metrics(error: Exception, module_name: str) -> None:
    """Log error metrics for monitoring and analysis.
    
    Args:
        error: The exception that occurred
        module_name: Name of the module where error occurred
    """
    error_type = type(error).__name__
    
    logger.error(
        "Error metric recorded",
        extra={
            'error_type': error_type,
            'module': module_name,
            'error_message': str(error)[:200],  # Truncate long messages
            'metric_type': 'error_count'
        }
    )

class ErrorHandler:
    """Context manager for standardized error handling."""
    
    def __init__(
        self,
        context: str = "",
        show_user_error: bool = True,
        return_on_error: Any = None
    ):
        self.context = context
        self.show_user_error = show_user_error
        self.return_on_error = return_on_error
        self.error = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.error = exc_value
            
            # Log the error
            logger.error(
                f"Error in {self.context}",
                extra={'error': str(exc_value)}
            )
            
            # Show user-friendly error if requested
            if self.show_user_error:
                display_error_to_user(exc_value, self.context)
            
            # Log error metrics
            log_error_metrics(exc_value, self.context)
            
            # Suppress the exception and return the default value
            return True
    
    def get_result(self, default_value: Any = None) -> Any:
        """Get the result or default value if an error occurred."""
        if self.error:
            return self.return_on_error if self.return_on_error is not None else default_value
        return None
