"""Logging configuration for the Prompt Engineering Tool.

This module provides centralized logging setup with structured logging,
correlation IDs for request tracing, and appropriate log levels.
"""

import logging
import logging.config
import json
import uuid
import os
from datetime import datetime
from contextvars import ContextVar
from typing import Optional, Dict, Any

# Correlation ID for tracing requests
correlation_id: ContextVar[str] = ContextVar('correlation_id', default=None)

class CorrelationIdFilter(logging.Filter):
    """Add correlation ID to log records for request tracing."""
    
    def filter(self, record):
        record.correlation_id = correlation_id.get() or str(uuid.uuid4())[:8]
        return True

class JSONFormatter(logging.Formatter):
    """Format log records as JSON for structured logging."""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'correlation_id': getattr(record, 'correlation_id', 'unknown')
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                          'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                          'thread', 'threadName', 'processName', 'process', 'getMessage',
                          'correlation_id']:
                log_entry[key] = value
        
        return json.dumps(log_entry)

def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True,
    enable_json: bool = False
) -> None:
    """Configure logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        enable_console: Whether to log to console
        enable_json: Whether to use JSON formatting
    """
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    # Configure logging
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s (%(correlation_id)s): %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'json': {
                '()': JSONFormatter
            }
        },
        'filters': {
            'correlation_id': {
                '()': CorrelationIdFilter
            }
        },
        'handlers': {},
        'loggers': {
            '': {  # root logger
                'handlers': [],
                'level': level,
                'propagate': False
            }
        }
    }
    
    # Add console handler
    if enable_console:
        config['handlers']['console'] = {
            'class': 'logging.StreamHandler',
            'level': level,
            'formatter': 'json' if enable_json else 'standard',
            'filters': ['correlation_id'],
            'stream': 'ext://sys.stdout'
        }
        config['loggers']['']['handlers'].append('console')
    
    # Add file handler
    if log_file:
        config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': level,
            'formatter': 'json' if enable_json else 'standard',
            'filters': ['correlation_id'],
            'filename': log_file,
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
        config['loggers']['']['handlers'].append('file')
    
    logging.config.dictConfig(config)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

def set_correlation_id(cid: str) -> None:
    """Set correlation ID for the current context.
    
    Args:
        cid: Correlation ID string
    """
    correlation_id.set(cid)

def get_correlation_id() -> str:
    """Get current correlation ID.
    
    Returns:
        Current correlation ID or generates a new one
    """
    cid = correlation_id.get()
    if not cid:
        cid = str(uuid.uuid4())[:8]
        correlation_id.set(cid)
    return cid

def log_function_call(func_name: str, args: Dict[str, Any] = None, 
                     duration: float = None) -> None:
    """Log function call details.
    
    Args:
        func_name: Name of the function being called
        args: Function arguments (sanitized)
        duration: Execution duration in seconds
    """
    logger = get_logger('function_calls')
    
    log_data = {
        'function': func_name,
        'correlation_id': get_correlation_id()
    }
    
    if args:
        # Sanitize sensitive data
        sanitized_args = {}
        for key, value in args.items():
            if 'api_key' in key.lower() or 'password' in key.lower():
                sanitized_args[key] = '***REDACTED***'
            elif isinstance(value, str) and len(value) > 100:
                sanitized_args[key] = value[:100] + '...'
            else:
                sanitized_args[key] = value
        log_data['args'] = sanitized_args
    
    if duration is not None:
        log_data['duration_seconds'] = round(duration, 3)
    
    logger.info("Function call", extra=log_data)

# Initialize logging with default configuration
def init_default_logging():
    """Initialize logging with sensible defaults."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_file = os.getenv('LOG_FILE')
    enable_json = os.getenv('LOG_JSON', 'false').lower() == 'true'
    
    setup_logging(
        level=log_level,
        log_file=log_file,
        enable_json=enable_json
    )

# Auto-initialize logging when module is imported
if not logging.getLogger().handlers:
    init_default_logging()
