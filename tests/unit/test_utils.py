import pytest
import sys
import os
import json
import tempfile
from unittest.mock import patch, mock_open

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import utils

class TestUtilsModule:
    """Test cases for the utils module."""
    
    def test_load_techniques_success(self, sample_techniques_config):
        """Test load_techniques with valid JSON file."""
        mock_data = json.dumps(sample_techniques_config)
        
        with patch('builtins.open', mock_open(read_data=mock_data)):
            with patch('os.path.exists', return_value=True):
                result = utils.load_techniques()
                
                assert isinstance(result, dict)
                assert "Zero-Shot Prompting" in result
                assert "Few-Shot Prompting" in result
    
    def test_load_techniques_file_not_found(self):
        """Test load_techniques when file doesn't exist."""
        with patch('os.path.exists', return_value=False):
            with pytest.raises(FileNotFoundError):
                utils.load_techniques()
    
    def test_load_techniques_invalid_json(self):
        """Test load_techniques with invalid JSON."""
        invalid_json = "{ invalid json }"
        
        with patch('builtins.open', mock_open(read_data=invalid_json)):
            with patch('os.path.exists', return_value=True):
                with pytest.raises(json.JSONDecodeError):
                    utils.load_techniques()
    
    def test_load_techniques_custom_filename(self, sample_techniques_config):
        """Test load_techniques with custom filename."""
        mock_data = json.dumps(sample_techniques_config)
        custom_filename = "custom_techniques.json"
        
        with patch('builtins.open', mock_open(read_data=mock_data)):
            with patch('os.path.exists', return_value=True):
                result = utils.load_techniques(custom_filename)
                
                assert isinstance(result, dict)
    
    def test_load_prompts_success(self, sample_departments_config):
        """Test load_prompts with valid JSON file."""
        mock_data = json.dumps(sample_departments_config)
        
        with patch('builtins.open', mock_open(read_data=mock_data)):
            with patch('os.path.exists', return_value=True):
                result = utils.load_prompts()
                
                assert isinstance(result, dict)
                assert "Marketing" in result
                assert "Customer Support" in result
                assert isinstance(result["Marketing"], list)
    
    def test_load_prompts_file_not_found(self):
        """Test load_prompts when file doesn't exist."""
        with patch('os.path.exists', return_value=False):
            with pytest.raises(FileNotFoundError):
                utils.load_prompts()
    
    def test_load_prompts_invalid_json(self):
        """Test load_prompts with invalid JSON."""
        invalid_json = "{ invalid json }"
        
        with patch('builtins.open', mock_open(read_data=invalid_json)):
            with patch('os.path.exists', return_value=True):
                with pytest.raises(json.JSONDecodeError):
                    utils.load_prompts()
    
    def test_load_prompts_custom_filename(self, sample_departments_config):
        """Test load_prompts with custom filename."""
        mock_data = json.dumps(sample_departments_config)
        custom_filename = "custom_prompts.json"
        
        with patch('builtins.open', mock_open(read_data=mock_data)):
            with patch('os.path.exists', return_value=True):
                result = utils.load_prompts(custom_filename)
                
                assert isinstance(result, dict)
    
    def test_file_path_resolution(self):
        """Test that file paths are resolved correctly."""
        # This test ensures the relative path logic works
        with patch('os.path.exists', return_value=False):
            try:
                utils.load_techniques()
            except FileNotFoundError as e:
                # The error message should contain the resolved path
                assert "techniques.json" in str(e)
    
    def test_load_functions_return_dict(self, sample_techniques_config, sample_departments_config):
        """Test that both load functions return dictionaries."""
        techniques_mock = json.dumps(sample_techniques_config)
        prompts_mock = json.dumps(sample_departments_config)
        
        with patch('builtins.open', mock_open(read_data=techniques_mock)):
            with patch('os.path.exists', return_value=True):
                techniques_result = utils.load_techniques()
                assert isinstance(techniques_result, dict)
        
        with patch('builtins.open', mock_open(read_data=prompts_mock)):
            with patch('os.path.exists', return_value=True):
                prompts_result = utils.load_prompts()
                assert isinstance(prompts_result, dict)
