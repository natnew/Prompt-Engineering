import pytest
import sys
import os
from unittest.mock import patch, Mock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import machine_learning

class TestMachineLearningModule:
    """Test cases for the machine_learning module."""
    
    @patch('machine_learning.client')
    def test_apply_few_shot_prompting_success(self, mock_client):
        """Test apply_few_shot_prompting with successful API response."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="The capital of Italy is Rome."))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = machine_learning.apply_few_shot_prompting("What is the capital of Italy?")
        
        assert result == "The capital of Italy is Rome."
        mock_client.chat.completions.create.assert_called_once()
        
        # Verify the call includes examples and proper formatting
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args[1]['messages']
        assert len(messages) == 2  # system and user messages
        assert "Example" in messages[1]['content']
    
    @patch('machine_learning.client')
    def test_apply_zero_shot_prompting_success(self, mock_client):
        """Test apply_zero_shot_prompting with successful API response."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Zero-shot response"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = machine_learning.apply_zero_shot_prompting("Test question")
        
        assert result == "Zero-shot response"
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('machine_learning.client')
    def test_apply_chain_of_thought_prompting_success(self, mock_client):
        """Test apply_chain_of_thought_prompting with successful API response."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Step-by-step solution"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = machine_learning.apply_chain_of_thought_prompting("Solve 2+2*3")
        
        assert result == "Step-by-step solution"
        
        # Verify the prompt includes step-by-step instruction
        call_args = mock_client.chat.completions.create.call_args
        user_message = call_args[1]['messages'][1]['content']
        assert "step by step" in user_message.lower()
    
    @patch('machine_learning.client')
    def test_apply_meta_prompting_success(self, mock_client):
        """Test apply_meta_prompting with successful API response."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Improved prompt"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = machine_learning.apply_meta_prompting("Write an email")
        
        assert result == "Improved prompt"
        
        # Verify the prompt asks for a better prompt
        call_args = mock_client.chat.completions.create.call_args
        user_message = call_args[1]['messages'][1]['content']
        assert "better prompt" in user_message.lower()
    
    @patch('machine_learning.client')
    def test_apply_self_consistency_prompting_success(self, mock_client):
        """Test apply_self_consistency_prompting with successful API response."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Consistent response"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = machine_learning.apply_self_consistency_prompting("Explain gravity")
        
        assert result == "Consistent response"
        
        # Verify the prompt mentions consistency
        call_args = mock_client.chat.completions.create.call_args
        user_message = call_args[1]['messages'][1]['content']
        assert "consistent" in user_message.lower()
    
    @patch('machine_learning.client')
    def test_apply_tree_of_thought_prompting_success(self, mock_client):
        """Test apply_tree_of_thought_prompting with successful API response."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Multiple approaches response"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = machine_learning.apply_tree_of_thought_prompting("Plan a project")
        
        assert result == "Multiple approaches response"
        
        # Verify the prompt mentions multiple approaches
        call_args = mock_client.chat.completions.create.call_args
        user_message = call_args[1]['messages'][1]['content']
        assert "multiple approaches" in user_message.lower()
    
    @patch('machine_learning.client')
    def test_api_error_handling(self, mock_client):
        """Test error handling when API calls fail."""
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        result = machine_learning.apply_few_shot_prompting("Test question")
        
        assert "Error:" in result
        assert "API Error" in result
    
    @patch('machine_learning.client')
    def test_all_functions_use_chat_completions(self, mock_client):
        """Test that all functions use the chat completions API."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        functions = [
            machine_learning.apply_few_shot_prompting,
            machine_learning.apply_zero_shot_prompting,
            machine_learning.apply_chain_of_thought_prompting,
            machine_learning.apply_meta_prompting,
            machine_learning.apply_self_consistency_prompting,
            machine_learning.apply_tree_of_thought_prompting
        ]
        
        for func in functions:
            mock_client.reset_mock()
            result = func("Test prompt")
            
            # Verify each function calls the chat completions API
            mock_client.chat.completions.create.assert_called_once()
            assert result == "Test response"
    
    @patch('machine_learning.client')
    def test_proper_message_format(self, mock_client):
        """Test that all functions use proper message format."""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        machine_learning.apply_few_shot_prompting("Test prompt")
        
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args[1]['messages']
        
        # Verify proper message structure
        assert isinstance(messages, list)
        assert len(messages) >= 2
        assert messages[0]['role'] == 'system'
        assert messages[1]['role'] == 'user'
        assert 'content' in messages[0]
        assert 'content' in messages[1]
