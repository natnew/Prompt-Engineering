"""
Unit tests for src/models.py

This module contains comprehensive tests for all core functions in the models module.
"""
import pytest
import unittest.mock as mock
import sys
import os

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import is_complete_sentence, ensure_complete_ending, get_model_response, MODELS


class TestIsCompleteSentence:
    """Test cases for the is_complete_sentence function."""
    
    def test_sentence_ending_with_period(self):
        """Test that sentences ending with period are recognized as complete."""
        assert is_complete_sentence("This is a complete sentence.")
        assert is_complete_sentence("Hello world.")
        assert is_complete_sentence("A single word.")
    
    def test_sentence_ending_with_exclamation(self):
        """Test that sentences ending with exclamation mark are recognized as complete."""
        assert is_complete_sentence("This is exciting!")
        assert is_complete_sentence("Hello!")
        assert is_complete_sentence("Wow!")
    
    def test_sentence_ending_with_question(self):
        """Test that sentences ending with question mark are recognized as complete."""
        assert is_complete_sentence("How are you?")
        assert is_complete_sentence("What time is it?")
        assert is_complete_sentence("Really?")
    
    def test_incomplete_sentences(self):
        """Test that incomplete sentences are not recognized as complete."""
        assert not is_complete_sentence("This is incomplete")
        assert not is_complete_sentence("Hello world")
        assert not is_complete_sentence("What about this one")
    
    def test_empty_strings(self):
        """Test that empty strings are not recognized as complete."""
        assert not is_complete_sentence("")
        assert not is_complete_sentence("   ")
        assert not is_complete_sentence("\t\n")
    
    def test_sentences_with_whitespace(self):
        """Test sentences with leading/trailing whitespace."""
        assert is_complete_sentence("   This has whitespace.   ")
        assert is_complete_sentence("\t\nThis has tabs and newlines!\n\t")
        assert not is_complete_sentence("   This has no ending   ")
    
    def test_multiple_punctuation(self):
        """Test sentences with multiple punctuation marks."""
        assert is_complete_sentence("Really?!")
        assert is_complete_sentence("This is amazing!!!")
        assert is_complete_sentence("What...?")


class TestEnsureCompleteEnding:
    """Test cases for the ensure_complete_ending function."""
    
    def test_already_complete_sentences(self):
        """Test that already complete sentences remain unchanged."""
        complete_sentence = "This is already complete."
        assert ensure_complete_ending(complete_sentence) == complete_sentence
        
        exclamation_sentence = "This is exciting!"
        assert ensure_complete_ending(exclamation_sentence) == exclamation_sentence
        
        question_sentence = "How are you?"
        assert ensure_complete_ending(question_sentence) == question_sentence
    
    def test_incomplete_sentences_get_completion(self):
        """Test that incomplete sentences get the standard completion appended."""
        incomplete = "This is incomplete"
        expected = "This is incomplete Thank you for your understanding and support. Sincerely, [Your Company Name] Customer Support Team."
        assert ensure_complete_ending(incomplete) == expected
        
        incomplete_with_space = "Another incomplete sentence "
        expected_with_space = "Another incomplete sentence Thank you for your understanding and support. Sincerely, [Your Company Name] Customer Support Team."
        assert ensure_complete_ending(incomplete_with_space) == expected_with_space
    
    def test_empty_string_handling(self):
        """Test that empty strings are returned unchanged."""
        assert ensure_complete_ending("") == ""
        assert ensure_complete_ending("   ") == "   "
        assert ensure_complete_ending("\t\n") == "\t\n"
    
    def test_whitespace_handling(self):
        """Test proper handling of whitespace in sentences."""
        sentence_with_whitespace = "   This is complete.   "
        assert ensure_complete_ending(sentence_with_whitespace) == sentence_with_whitespace
        
        incomplete_with_whitespace = "   This is incomplete   "
        expected = "This is incomplete Thank you for your understanding and support. Sincerely, [Your Company Name] Customer Support Team."
        assert ensure_complete_ending(incomplete_with_whitespace) == expected


class TestGetModelResponse:
    """Test cases for the get_model_response function."""
    
    @mock.patch('models.openai.ChatCompletion.create')
    @mock.patch('models.st.warning')
    @mock.patch('models.st.error')
    def test_successful_response(self, mock_error, mock_warning, mock_openai):
        """Test successful API response."""
        # Mock successful OpenAI response
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': 'This is a test response.'
                    }
                }
            ]
        }
        mock_openai.return_value = mock_response
        
        result = get_model_response("gpt-4", "Test prompt")
        
        assert result == "This is a test response."
        mock_openai.assert_called_once()
        mock_error.assert_not_called()
        mock_warning.assert_not_called()
    
    @mock.patch('models.openai.ChatCompletion.create')
    @mock.patch('models.st.warning')
    @mock.patch('models.st.error')
    def test_incomplete_response_gets_completion(self, mock_error, mock_warning, mock_openai):
        """Test that incomplete responses get proper completion."""
        # Mock incomplete OpenAI response
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': 'This is incomplete'
                    }
                }
            ]
        }
        mock_openai.return_value = mock_response
        
        result = get_model_response("gpt-4", "Test prompt")
        
        expected = "This is incomplete Thank you for your understanding and support. Sincerely, [Your Company Name] Customer Support Team."
        assert result == expected
    
    @mock.patch('models.openai.ChatCompletion.create')
    @mock.patch('models.st.warning')
    @mock.patch('models.st.error')
    @mock.patch('models.time.sleep')
    def test_rate_limit_handling(self, mock_sleep, mock_error, mock_warning, mock_openai):
        """Test handling of rate limit errors with retry logic."""
        import openai
        
        # First call raises rate limit error, second succeeds
        rate_limit_error = openai.error.RateLimitError("Rate limit reached. Please try again in 60s.")
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': 'Success after retry.'
                    }
                }
            ]
        }
        mock_openai.side_effect = [rate_limit_error, mock_response]
        
        result = get_model_response("gpt-4", "Test prompt")
        
        assert result == "Success after retry."
        assert mock_openai.call_count == 2
        mock_warning.assert_called_once()
        mock_sleep.assert_called_once()
    
    @mock.patch('models.openai.ChatCompletion.create')
    @mock.patch('models.st.warning')
    @mock.patch('models.st.error')
    @mock.patch('models.time.sleep')
    def test_rate_limit_exhausted_retries(self, mock_sleep, mock_error, mock_warning, mock_openai):
        """Test behavior when rate limit retries are exhausted."""
        import openai
        
        # All retries fail with rate limit error
        rate_limit_error = openai.error.RateLimitError("Rate limit reached. Please try again in 60s.")
        mock_openai.side_effect = rate_limit_error
        
        result = get_model_response("gpt-4", "Test prompt")
        
        assert result is None
        assert mock_openai.call_count == 3  # Initial + 2 retries
        assert mock_warning.call_count == 3
        mock_error.assert_called_once()
    
    @mock.patch('models.openai.ChatCompletion.create')
    @mock.patch('models.st.error')
    def test_general_exception_handling(self, mock_error, mock_openai):
        """Test handling of general exceptions."""
        # Mock a general exception
        mock_openai.side_effect = Exception("General API error")
        
        result = get_model_response("gpt-4", "Test prompt")
        
        assert result is None
        mock_error.assert_called_once()
    
    @mock.patch('models.openai.ChatCompletion.create')
    def test_o1_model_parameters(self, mock_openai):
        """Test that o1 models use correct parameters."""
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': 'O1 model response.'
                    }
                }
            ]
        }
        mock_openai.return_value = mock_response
        
        get_model_response("o1-mini", "Test prompt", temperature=0.5, top_p=0.9, max_tokens=1000)
        
        # Verify the call was made with o1-specific parameters
        call_args = mock_openai.call_args[1]
        assert call_args['model'] == "o1-mini"
        assert call_args['max_completion_tokens'] == 10000  # o1 models use max_completion_tokens
        assert call_args['temperature'] == 1  # o1 models only support temperature=1
        assert call_args['top_p'] == 1  # o1 models only support top_p=1
        assert 'max_tokens' not in call_args  # Should not have max_tokens for o1 models
    
    @mock.patch('models.openai.ChatCompletion.create')
    def test_regular_model_parameters(self, mock_openai):
        """Test that regular models use correct parameters."""
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': 'Regular model response.'
                    }
                }
            ]
        }
        mock_openai.return_value = mock_response
        
        get_model_response("gpt-4", "Test prompt", temperature=0.8, top_p=0.9, max_tokens=1000)
        
        # Verify the call was made with regular model parameters
        call_args = mock_openai.call_args[1]
        assert call_args['model'] == "gpt-4"
        assert call_args['max_tokens'] == 1000
        assert call_args['temperature'] == 0.8
        assert call_args['top_p'] == 0.9
        assert 'max_completion_tokens' not in call_args
    
    @mock.patch('models.openai.ChatCompletion.create')
    def test_default_parameters(self, mock_openai):
        """Test that default parameters are used when none are provided."""
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': 'Default parameters response.'
                    }
                }
            ]
        }
        mock_openai.return_value = mock_response
        
        get_model_response("gpt-4", "Test prompt")
        
        # Verify the call was made with default parameters
        call_args = mock_openai.call_args[1]
        assert call_args['max_tokens'] == 500  # Default max_tokens
        assert call_args['temperature'] == 0.7  # Default temperature
        assert call_args['top_p'] == 1.0  # Default top_p


class TestModelsConstants:
    """Test cases for constants and configurations in models.py."""
    
    def test_models_dictionary_exists(self):
        """Test that MODELS dictionary is properly defined."""
        assert isinstance(MODELS, dict)
        assert len(MODELS) > 0
    
    def test_models_dictionary_content(self):
        """Test that MODELS dictionary contains expected models."""
        expected_models = {
            "GPT-4o": "gpt-4o",
            "GPT-4o mini": "gpt-4o-mini",
            "GPT-4 Turbo": "gpt-4-turbo",
            "GPT-4": "gpt-4",
            "GPT-3.5": "gpt-3.5-turbo",
            "o1": "o1",
            "o1-mini": "o1-mini",
            "o3-mini": "o3-mini",
            "GPT-4.5-preview": "gpt-4.5-preview"
        }
        
        for display_name, model_id in expected_models.items():
            assert display_name in MODELS
            assert MODELS[display_name] == model_id


# Integration tests
class TestModelsIntegration:
    """Integration tests for models.py functions working together."""
    
    @mock.patch('models.openai.ChatCompletion.create')
    def test_end_to_end_complete_response(self, mock_openai):
        """Test end-to-end flow with complete response."""
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': 'This is a complete response.'
                    }
                }
            ]
        }
        mock_openai.return_value = mock_response
        
        result = get_model_response("gpt-4", "Generate a complete sentence")
        
        # Response should be complete as-is
        assert result == "This is a complete response."
        assert is_complete_sentence(result)
        assert ensure_complete_ending(result) == result
    
    @mock.patch('models.openai.ChatCompletion.create')
    def test_end_to_end_incomplete_response(self, mock_openai):
        """Test end-to-end flow with incomplete response."""
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': 'This is incomplete'
                    }
                }
            ]
        }
        mock_openai.return_value = mock_response
        
        result = get_model_response("gpt-4", "Generate text")
        
        # Response should be completed automatically
        expected = "This is incomplete Thank you for your understanding and support. Sincerely, [Your Company Name] Customer Support Team."
        assert result == expected
        assert is_complete_sentence(result)


if __name__ == "__main__":
    pytest.main([__file__])