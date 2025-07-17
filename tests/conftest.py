import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response for testing."""
    return Mock(
        choices=[
            Mock(message=Mock(content="Test response from OpenAI"))
        ],
        usage=Mock(total_tokens=50)
    )

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    client = Mock()
    client.chat.completions.create.return_value = Mock(
        choices=[Mock(message=Mock(content="Mocked response"))]
    )
    return client

@pytest.fixture
def sample_user_prompt():
    """Sample user prompt for testing."""
    return "What is the capital of France?"

@pytest.fixture
def sample_techniques_config():
    """Sample techniques configuration for testing."""
    return {
        "Zero-Shot Prompting": {
            "description": "Direct prompting without examples",
            "process": ["Step 1: Direct query", "Step 2: Generate response"]
        },
        "Few-Shot Prompting": {
            "description": "Prompting with examples",
            "process": ["Step 1: Provide examples", "Step 2: Ask question"]
        }
    }

@pytest.fixture
def sample_departments_config():
    """Sample departments configuration for testing."""
    return {
        "Marketing": [
            "Write a product description for our new software",
            "Create a social media campaign for our launch"
        ],
        "Customer Support": [
            "Draft a response to a customer complaint",
            "Create a help article for common issues"
        ]
    }
