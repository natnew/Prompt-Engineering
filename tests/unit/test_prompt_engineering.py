import pytest
import sys
import os
from unittest.mock import patch, Mock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import prompt_engineering

class TestPromptEngineering:
    """Test cases for the prompt_engineering module."""
    
    def test_apply_technique_zero_shot(self):
        """Test apply_technique with Zero-Shot prompting."""
        original_prompt = "What is AI?"
        result_prompt, explanation = prompt_engineering.apply_technique(original_prompt, "Zero-Shot")
        
        assert result_prompt == original_prompt
        assert "Zero-Shot" in explanation
        assert "without examples" in explanation.lower()
    
    def test_apply_technique_few_shot(self):
        """Test apply_technique with Few-Shot prompting."""
        original_prompt = "What is machine learning?"
        result_prompt, explanation = prompt_engineering.apply_technique(original_prompt, "Few-Shot")
        
        assert "Example" in result_prompt
        assert original_prompt in result_prompt
        assert "Few-Shot" in explanation
    
    def test_apply_technique_chain_of_thought(self):
        """Test apply_technique with Chain-of-Thought prompting."""
        original_prompt = "Solve 2+2*3"
        result_prompt, explanation = prompt_engineering.apply_technique(original_prompt, "Chain-of-Thought")
        
        assert "step-by-step" in result_prompt.lower()
        assert original_prompt in result_prompt
        assert "Chain-of-Thought" in explanation
    
    def test_apply_technique_meta_prompting(self):
        """Test apply_technique with Meta-Prompting."""
        original_prompt = "Write an email"
        result_prompt, explanation = prompt_engineering.apply_technique(original_prompt, "Meta-Prompting")
        
        assert "better prompt" in result_prompt.lower() or "improved prompt" in result_prompt.lower()
        assert original_prompt in result_prompt
        assert "Meta-Prompting" in explanation
    
    def test_apply_technique_self_consistency(self):
        """Test apply_technique with Self-Consistency prompting."""
        original_prompt = "Explain gravity"
        result_prompt, explanation = prompt_engineering.apply_technique(original_prompt, "Self-Consistency")
        
        assert "consistent" in result_prompt.lower()
        assert original_prompt in result_prompt
        assert "Self-Consistency" in explanation
    
    def test_apply_technique_tree_of_thought(self):
        """Test apply_technique with Tree-of-Thought prompting."""
        original_prompt = "Plan a project"
        result_prompt, explanation = prompt_engineering.apply_technique(original_prompt, "Tree-of-Thought")
        
        assert "multiple" in result_prompt.lower() or "different" in result_prompt.lower()
        assert original_prompt in result_prompt
        assert "Tree-of-Thought" in explanation
    
    def test_apply_technique_invalid_technique(self):
        """Test apply_technique with invalid technique name."""
        original_prompt = "Test prompt"
        result_prompt, explanation = prompt_engineering.apply_technique(original_prompt, "Invalid-Technique")
        
        # Should return original prompt when technique is not recognized
        assert result_prompt == original_prompt
        assert "not recognized" in explanation.lower() or "unknown" in explanation.lower()
    
    def test_apply_technique_empty_prompt(self):
        """Test apply_technique with empty prompt."""
        original_prompt = ""
        result_prompt, explanation = prompt_engineering.apply_technique(original_prompt, "Zero-Shot")
        
        assert isinstance(result_prompt, str)
        assert isinstance(explanation, str)
    
    def test_apply_technique_returns_tuple(self):
        """Test that apply_technique always returns a tuple."""
        original_prompt = "Test prompt"
        result = prompt_engineering.apply_technique(original_prompt, "Zero-Shot")
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)  # transformed prompt
        assert isinstance(result[1], str)  # explanation
