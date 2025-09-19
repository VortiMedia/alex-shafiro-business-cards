# CI/CD Notes - Business Card Generator v2.0

**Purpose**: Outline for automated testing and deployment pipeline  
**Status**: Sprint 2 (Testing Infrastructure) - Ready for CI Implementation  
**Next**: Sprint 3-4 (CI/CD Setup)  

---

## GitHub Actions Workflow

### **Test Automation** (`.github/workflows/test.yml`)

```yaml
name: Test Suite
on:
  push:
    branches: [ main, develop, sprint-* ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-mock freezegun pytest-cov
    
    - name: Run tests
      run: |
        export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
        pytest --cov=src --cov-report=xml --cov-fail-under=90
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### **Quality Gates** (`.github/workflows/quality.yml`)

```yaml
name: Code Quality
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install linting tools
      run: |
        pip install black flake8 mypy
    
    - name: Run Black (formatting)
      run: black --check src/ tests/
    
    - name: Run Flake8 (linting)
      run: flake8 src/ tests/ --max-line-length=100
    
    - name: Run MyPy (type checking)
      run: mypy src/ --ignore-missing-imports
```

---

## Testing Pipeline

### **Test Execution Order**
1. **Fast Tests First**: Unit tests (validation, API status)
2. **Integration Tests**: End-to-end workflow testing
3. **Smoke Tests**: CLI interface validation
4. **Coverage Analysis**: Ensure 90%+ coverage

### **Environment Matrix**
- **Python**: 3.10, 3.11, 3.12
- **OS**: Ubuntu (Linux) primary, optional Windows/macOS
- **Dependencies**: Latest versions from requirements.txt

### **Security Considerations**
```yaml
# Never expose real API keys in CI
env:
  OPENAI_API_KEY: "mock-key-for-testing"
  GOOGLE_API_KEY: "mock-key-for-testing"
  
# All tests use mocks - no real API calls
- name: Verify no real API calls
  run: |
    grep -r "sk-[a-zA-Z0-9]" tests/ && exit 1 || echo "✅ No real keys in tests"
```

---

## Quality Metrics

### **Coverage Requirements**
- **Minimum**: 90% overall coverage
- **Critical Files**: 95% coverage
  - `src/hybrid/modern_workflow.py`
  - `src/validation/image_rules.py`
  - `src/monitoring/api_status.py`

### **Performance Benchmarks**
- **Full test suite**: <2 minutes
- **Unit tests**: <30 seconds
- **Integration tests**: <1 minute
- **Individual test files**: <30 seconds each

### **Quality Gates**
```bash
# Must pass ALL criteria
pytest --cov=src --cov-fail-under=90  # Coverage
black --check src/ tests/              # Formatting
flake8 src/ tests/                     # Linting
mypy src/ --ignore-missing-imports     # Type hints
```

---

## Branch Strategy

### **Development Flow**
```
main (production)
├── develop (integration)
├── sprint-2-testing-qa (current)
├── sprint-3-optimization
└── feature/* (individual features)
```

### **CI Triggers**
- **All branches**: Run full test suite
- **Main branch**: Additional deployment checks
- **Pull requests**: Full quality gates + review required
- **Tags**: Trigger release pipeline (future)

### **Merge Requirements**
- ✅ All tests passing
- ✅ Coverage threshold met (90%)
- ✅ No linting errors
- ✅ At least 1 code review approval
- ✅ No merge conflicts

---

## Deployment Pipeline (Future)

### **Staging Environment**
```yaml
deploy-staging:
  needs: [test, quality]
  if: github.ref == 'refs/heads/develop'
  runs-on: ubuntu-latest
  steps:
  - name: Deploy to staging
    run: |
      # Package application
      # Deploy to staging server
      # Run smoke tests
```

### **Production Release**
```yaml
deploy-production:
  needs: [test, quality]
  if: startsWith(github.ref, 'refs/tags/v')
  runs-on: ubuntu-latest
  steps:
  - name: Create release
    uses: actions/create-release@v1
    with:
      tag_name: ${{ github.ref }}
      release_name: Business Card Generator ${{ github.ref }}
```

---

## Monitoring & Alerting

### **Test Results Dashboard**
- **GitHub Actions**: Built-in test result reporting
- **Codecov**: Coverage tracking and visualization  
- **Badges**: README.md status indicators

### **Notification Strategy**
- **Slack/Discord**: Test failures on main/develop branches
- **Email**: Critical failures or coverage drops
- **GitHub**: PR status checks and reviews

### **Metrics to Track**
- **Test Pass Rate**: Target 100% on main branch
- **Coverage Trend**: Maintain 90%+ over time
- **Build Time**: Track performance degradation
- **Flaky Tests**: Identify and fix unreliable tests

---

## Docker Configuration (Optional)

### **Test Container** (`Dockerfile.test`)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install pytest pytest-mock freezegun pytest-cov

COPY src/ src/
COPY tests/ tests/

ENV PYTHONPATH="/app/src:${PYTHONPATH}"
CMD ["pytest", "--cov=src", "--cov-fail-under=90"]
```

### **Docker Compose** (`docker-compose.test.yml`)
```yaml
version: '3.8'
services:
  test:
    build:
      context: .
      dockerfile: Dockerfile.test
    volumes:
      - .:/app
    environment:
      - OPENAI_API_KEY=mock-key
      - GOOGLE_API_KEY=mock-key
```

---

## Security Scanning

### **Dependencies**
```yaml
- name: Security audit
  run: |
    pip install safety
    safety check
    
- name: Dependency scanning
  uses: pypa/gh-action-pip-audit@v1.0.8
```

### **Secret Detection**
```yaml
- name: Scan for secrets
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: main
    head: HEAD
```

---

## Performance Testing (Future Sprint)

### **Load Testing**
```python
# tests/test_performance.py
import pytest
import time
from concurrent.futures import ThreadPoolExecutor

def test_concurrent_generation():
    """Test multiple simultaneous generations"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(generate_test_card) 
            for _ in range(10)
        ]
        results = [f.result() for f in futures]
    
    assert all(r.success for r in results)
```

### **Memory Profiling**
```yaml
- name: Memory usage test
  run: |
    pip install memory-profiler
    python -m memory_profiler tests/test_memory_usage.py
```

---

## Local CI Simulation

### **Pre-commit Hooks** (`.pre-commit-config.yaml`)
```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: python
        pass_filenames: false
        always_run: true
      
      - id: black
        name: black
        entry: black
        language: python
        args: [--check]
        files: \.(py)$
      
      - id: flake8
        name: flake8
        entry: flake8
        language: python
        files: \.(py)$
```

### **Local Test Script** (`scripts/test-ci.sh`)
```bash
#!/bin/bash
set -e

echo "🧪 Running CI simulation locally..."

# Setup
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"

# Quality checks
echo "📝 Code formatting..."
black --check src/ tests/ || (echo "❌ Formatting failed" && exit 1)

echo "🔍 Linting..."
flake8 src/ tests/ || (echo "❌ Linting failed" && exit 1)

# Tests
echo "🧪 Running test suite..."
pytest --cov=src --cov-fail-under=90 || (echo "❌ Tests failed" && exit 1)

echo "✅ All checks passed!"
```

---

## Future Enhancements

### **Sprint 3-4 Goals**
- [ ] Set up GitHub Actions workflows
- [ ] Configure Codecov integration  
- [ ] Add pre-commit hooks
- [ ] Create deployment pipeline
- [ ] Set up monitoring dashboard

### **Long-term Roadmap**
- [ ] Multi-environment deployment (staging/prod)
- [ ] Performance regression testing
- [ ] Automated security scanning
- [ ] Integration with external services
- [ ] Container-based deployments

---

## Getting Started

### **Immediate Next Steps**
1. **Create `.github/workflows/` directory**
2. **Add basic test workflow** (start with test.yml above)
3. **Configure branch protection rules** in GitHub
4. **Set up Codecov account** and integration
5. **Test workflow** with a small PR

### **Implementation Order**
1. **Phase 1**: Basic test automation (Sprint 3)
2. **Phase 2**: Quality gates and coverage (Sprint 3)  
3. **Phase 3**: Deployment pipeline (Sprint 4)
4. **Phase 4**: Monitoring and alerting (Sprint 4+)

---

**Ready for CI implementation once Sprint 2 testing infrastructure is complete! 🚀**