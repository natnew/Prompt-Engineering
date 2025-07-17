# 🔧 Replace Deprecated OpenAI API in machine_learning.py

## 🚨 Problem Statement
The `machine_learning.py` module uses the deprecated OpenAI `Completion.create()` API and legacy authentication methods. This creates a critical dependency on deprecated APIs that could break without warning when OpenAI discontinues legacy support.

**Current Issues:**
- Uses deprecated `openai.Completion.create()` instead of chat completions
- Uses legacy `openai.api_key` authentication pattern
- Incorrect model usage (`gpt-3.5-turbo` with Completion API)
- No error handling for API failures
- Will break when OpenAI removes legacy API support

## 🎯 Acceptance Criteria

### Core API Migration
- [ ] Replace all `openai.Completion.create()` calls with `client.chat.completions.create()`
- [ ] Update authentication to use the new OpenAI client pattern (`OpenAI(api_key=...)`)
- [ ] Convert completion format to chat completion format (messages array)
- [ ] Ensure all 6 functions return the same data structure (backward compatibility)

### Function Updates Required
- [ ] `apply_few_shot_prompting()` - Convert to chat format with system/user messages
- [ ] `apply_zero_shot_prompting()` - Update to chat completion
- [ ] `apply_chain_of_thought_prompting()` - Migrate API calls
- [ ] `apply_meta_prompting()` - Update to new API
- [ ] `apply_self_consistency_prompting()` - Migrate to chat format
- [ ] `apply_tree_of_thought_prompting()` - Update API usage

### Technical Requirements
- [ ] Add proper error handling for API failures and rate limits
- [ ] Implement exponential backoff retry mechanism
- [ ] Add input validation and sanitization
- [ ] Update prompt formatting to work with chat completion format
- [ ] Test all functions with the new API to ensure functionality

### Documentation & Testing
- [ ] Update function docstrings to reflect API changes
- [ ] Remove deprecation warning from API_DOCUMENTATION.md
- [ ] Add usage examples with new API format
- [ ] Create unit tests for all migrated functions
- [ ] Test with different OpenAI models to ensure compatibility

## 📁 Files to Update

### Primary Files
- **`src/machine_learning.py`** - Complete rewrite of API calls and authentication
- **`requirements.txt`** - Ensure correct OpenAI library version (>=1.3.0)
- **`API_DOCUMENTATION.md`** - Remove deprecation warning, update examples

### Testing Files (New)
- **`tests/unit/test_machine_learning.py`** - Unit tests for all functions
- **`tests/fixtures/mock_responses.py`** - Mock OpenAI API responses

## 🔧 Technical Implementation Notes

### API Pattern Change
```python
# OLD (Deprecated)
response = openai.Completion.create(
    model="gpt-3.5-turbo",
    prompt=full_prompt,
    max_tokens=100
)
result = response.choices[0].text.strip()

# NEW (Current)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": full_prompt}],
    max_tokens=100
)
result = response.choices[0].message.content.strip()
```

### Authentication Update
```python
# OLD
openai.api_key = st.secrets.get("OPENAI_API_KEY", None)

# NEW
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

## 📊 Priority: 🔥 CRITICAL
This issue blocks the application from working reliably and poses a significant risk of sudden failure.

## 🏷️ Labels
- `bug`
- `critical`
- `technical-debt`
- `api-migration`
- `breaking-change`

## 📋 Definition of Done
- [ ] All deprecated API calls replaced with current OpenAI client
- [ ] Backward compatibility maintained for function interfaces
- [ ] Unit tests passing for all 6 prompt engineering functions
- [ ] Documentation updated to reflect changes
- [ ] No deprecation warnings in codebase
- [ ] Error handling implemented for API failures
- [ ] Code review completed and approved
