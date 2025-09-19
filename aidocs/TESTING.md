# Testing Guide - Business Card Generator v2.0

**Version**: Sprint 2 (Testing & Quality Assurance)  
**Date**: September 18, 2025  
**Coverage**: Unit, Integration, Validation, CLI, API Status  

---

## Quick Start

```bash
# Install test dependencies
pip install pytest pytest-mock freezegun

# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test categories
pytest tests/test_validation.py -v        # Image validation
pytest tests/test_modern_workflow_unit.py -v  # Unit tests
pytest tests/test_api_status.py -v        # API monitoring
```

---

## Test Structure

```
tests/
├── fixtures/
│   ├── mock_openai.py         # OpenAI API mocks
│   └── mock_gemini.py         # Gemini API mocks
├── test_validation.py         # Image validation rules
├── test_modern_workflow_unit.py      # Core workflow unit tests
├── test_modern_workflow_integration.py  # End-to-end integration
├── test_cli_smoke.py          # CLI interface tests
└── test_api_status.py         # API health monitoring
```

---

## Test Categories

### 🧪 **Unit Tests** (`test_modern_workflow_unit.py`)
- **Model Selection Logic**: AUTO vs explicit model requests
- **Image Validation**: PNG format, size, quality checks
- **Prompt Building**: Brand info, concept mapping, front/back differentiation
- **File Saving**: Naming conventions, directory handling
- **Cost Estimation**: Quality-to-cost mapping accuracy
- **Error Handling**: Missing APIs, invalid inputs

**Run**: `pytest tests/test_modern_workflow_unit.py -v`

### 🔗 **Integration Tests** (`test_modern_workflow_integration.py`)
- **End-to-End Generation**: Complete card creation workflow
- **API Error Recovery**: Auth errors, rate limits, empty responses
- **Model Fallbacks**: When preferred model fails
- **Cost Tracking**: Session cost accumulation
- **File Management**: Directory creation, naming, existence

**Run**: `pytest tests/test_modern_workflow_integration.py -v`

### 🖼️ **Image Validation** (`test_validation.py`)
- **Resolution Checks**: Minimum 512×512 pixels
- **Color Mode**: RGB/RGBA acceptance, grayscale rejection
- **Aspect Ratio**: Business card proportions (1.75:1 ±0.1)
- **File Size**: 1KB to 10MB limits
- **Print DPI**: Estimated quality for 3.5″×2.0″ cards
- **Comprehensive**: All-in-one validation suite

**Run**: `pytest tests/test_validation.py -v`

### 🖥️ **CLI Tests** (`test_cli_smoke.py`)
- **Menu Display**: Banner, options, cost information
- **Cost Estimation**: Draft/review/production pricing
- **Workflow Integration**: ModernHybridWorkflow initialization
- **Error Handling**: Missing APIs, invalid inputs
- **Results Display**: Success/failure formatting

**Run**: `pytest tests/test_cli_smoke.py -v`

### 📊 **API Status** (`test_api_status.py`)
- **Key Detection**: OpenAI/Gemini API key presence
- **Format Validation**: `sk-*` and `AIza*` pattern checking
- **Status Reporting**: Detailed and brief report formats
- **Workflow Recommendations**: Based on available APIs
- **Environment Validation**: Overall system readiness

**Run**: `pytest tests/test_api_status.py -v`

---

## Mock System

### **No Real API Calls**
All tests use mocks to avoid costs and network dependencies:

```python
# OpenAI Mock Example
from fixtures.mock_openai import create_mock_openai_success
mock_client = create_mock_openai_success()
# Returns valid PNG data without real API call
```

### **Available Mocks**
- ✅ **Success Responses**: Valid image data
- ❌ **Auth Errors**: Authentication failures  
- ⚡ **Rate Limits**: Quota exceeded scenarios
- 📭 **Empty Responses**: No data returned
- 🚫 **Invalid Data**: Malformed responses

### **Mock Features**
- **Consistent**: Same PNG data across tests
- **Fast**: No network latency
- **Reliable**: No API service dependencies
- **Cost-Free**: Zero API charges during development

---

## Running Tests Locally

### **Standard Test Run**
```bash
# Basic test execution
pytest

# Verbose output with test names
pytest -v

# Short traceback format
pytest --tb=short

# Stop on first failure
pytest -x
```

### **Specific Test Categories**
```bash
# Only image validation
pytest tests/test_validation.py

# Only integration tests  
pytest tests/test_modern_workflow_integration.py

# Multiple specific files
pytest tests/test_validation.py tests/test_api_status.py
```

### **Test Selection Patterns**
```bash
# Run tests matching pattern
pytest -k "test_validation"

# Run specific test class
pytest tests/test_validation.py::TestMinResolution

# Run specific test method
pytest tests/test_validation.py::TestMinResolution::test_valid_resolution_passes
```

### **Coverage Analysis**
```bash
# Install coverage
pip install pytest-cov

# Run with coverage report
pytest --cov=src --cov-report=html

# Coverage with missing lines
pytest --cov=src --cov-report=term-missing
```

---

## Environment Setup

### **Dependencies**
```bash
# Core testing framework
pip install pytest>=8.0.0

# Mocking utilities
pip install pytest-mock>=3.15.0

# Time manipulation for reproducible tests
pip install freezegun>=1.5.0

# Image processing (already in requirements.txt)
pip install Pillow>=10.0.0
```

### **Environment Variables**
Tests automatically manage environment variables:

```python
# Tests set mock API keys
monkeypatch.setenv("OPENAI_API_KEY", "sk-test123456789012345678")
monkeypatch.setenv("GOOGLE_API_KEY", "AIza1234567890123456789")

# Tests clean up after themselves
# No real keys needed for testing
```

### **Directory Structure**
Tests create temporary directories automatically:

```python
def test_file_creation(tmp_path):
    # tmp_path is automatically provided and cleaned up
    output_dir = tmp_path / "test_output"
    # Use output_dir for test file operations
```

---

## Debugging Failed Tests

### **Common Issues**

#### **Import Errors**
```bash
# Fix: Ensure src/ is in Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"

# Or: Add to test file
sys.path.append(str(Path(__file__).parent.parent / "src"))
```

#### **Mock Issues**
```python
# Verify mock is being called
with patch('hybrid.modern_workflow.OpenAI') as mock_openai:
    mock_openai.return_value = create_mock_openai_success()
    # Test code here
    assert mock_openai.called
```

#### **Environment Variables**
```python
# Check env var state
def test_debug_env(monkeypatch):
    print(f"OpenAI Key: {os.getenv('OPENAI_API_KEY')}")
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    print(f"After set: {os.getenv('OPENAI_API_KEY')}")
```

### **Debugging Commands**
```bash
# Run single test with debugging
pytest tests/test_validation.py::TestMinResolution::test_valid_resolution_passes -v -s

# Print all output (including print statements)
pytest tests/test_validation.py -s

# Debug on failure
pytest --pdb tests/test_validation.py

# Capture stdout/stderr
pytest --capture=no tests/test_validation.py
```

---

## Performance Guidelines

### **Test Speed Targets**
- **Unit tests**: <0.1s each
- **Integration tests**: <1s each  
- **Full suite**: <30s total
- **Individual files**: <5s each

### **Speed Optimization**
```python
# ✅ Good: Use fixtures for shared setup
@pytest.fixture
def mock_workflow():
    return setup_mocked_workflow()

# ❌ Bad: Recreate mocks in each test
def test_something():
    mock = create_complex_mock()  # Repeated setup
```

### **Parallel Execution**
```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest -n auto  # Auto-detect CPU cores
pytest -n 4     # Use 4 processes
```

---

## Success Criteria

### **Sprint 2 Acceptance**
- ✅ **95%+ Unit Coverage**: Core workflow functions
- ✅ **Integration Tests**: Both API models with error scenarios  
- ✅ **Validation Suite**: All image quality checks
- ✅ **CLI Testing**: Menu system and user interactions
- ✅ **Zero API Costs**: All tests use mocks
- ✅ **Fast Execution**: Full suite under 30 seconds
- ✅ **Reliable**: No flaky tests, consistent results

### **Quality Gates**
```bash
# All tests must pass
pytest --tb=short

# No warnings in test output
pytest --disable-warnings

# Coverage threshold met
pytest --cov=src --cov-fail-under=90
```

---

## Next Steps (Sprint 3+)

### **Future Enhancements**
- **Performance Tests**: Generation speed benchmarks
- **Stress Tests**: High-volume generation scenarios
- **Visual Regression**: Image output comparison
- **End-to-End**: Real API integration tests (optional)
- **Load Tests**: Concurrent generation handling

### **CI/CD Integration**
See [`CI_NOTES.md`](CI_NOTES.md) for GitHub Actions setup.

---

## Troubleshooting

### **Common Test Failures**

#### **ModuleNotFoundError**
```bash
# Add src to Python path
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
# Or run from project root
cd /path/to/business-card-designer-2025
pytest
```

#### **Fixture Not Found**
```python
# Ensure fixture is in same file or conftest.py
# Check fixture scope (function, class, module, session)
@pytest.fixture(scope="function")
def my_fixture():
    return setup_data()
```

#### **Mock Not Working**
```python
# Verify patch target
# Use exact import path from the code being tested
with patch('hybrid.modern_workflow.OpenAI'):  # ✅ Correct
# Not: patch('openai.OpenAI')  # ❌ Wrong path
```

### **Getting Help**
1. **Check test output**: `pytest -v --tb=long`
2. **Review mock setup**: Ensure correct patch targets
3. **Verify fixtures**: Check fixture scopes and dependencies
4. **Environment**: Confirm Python path and dependencies
5. **Documentation**: Reference this guide and pytest docs

---

**Questions? Check the test files for examples or review [`aidocs/V2_SPRINT.md`](V2_SPRINT.md) for Sprint 2 context.**