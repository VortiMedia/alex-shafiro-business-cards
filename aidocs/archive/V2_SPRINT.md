Here’s a focused, do-first plan for Sprint 2 (Testing & Quality Assurance) tailored to this codebase and the v2.0 hybrid workflow you now have.

Sprint 2 goals (Weeks 3–4)
- Build a testable foundation for ModernHybridWorkflow (dual model)
- Add robust API mocking to avoid real costs during development
- Validate image outputs (dimensions, color mode, content checks)
- Add API health checks and error/fallback coverage
- Provide cost estimation accuracy checks and session tracking validation

Branch and safety workflow
- new sprint-2-testing-qa
- save
- After each story, run: check → done "sprint-2: <story>" → ship (staging only)
- Never commit secrets. Use .env only (OPENAI_API_KEY, GOOGLE_API_KEY). Don’t echo secrets to terminal.

Deliverables (by end of sprint)
- tests/ with unit + integration + validation tests
- src/validation/ with image quality checks
- src/monitoring/ with API status check helpers
- Mocks for OpenAI and Google GenAI responses (no real cost in CI/dev)
- CLI smoke tests for generate_business_cards_v2.py
- Docs: Brief “How to test locally” and CI notes added to aidocs

Story A: Test scaffolding and utilities
1) Add dev test dependencies (do this once)
- pytest, pytest-mock, pillow (already present), freezegun (for time-stable tests)
- If you want to pin: add a dev-requirements.txt and keep requirements.txt for runtime only

2) Test directory structure (create these files)
- tests/test_modern_workflow_unit.py
- tests/test_modern_workflow_integration.py
- tests/test_validation.py
- tests/fixtures/mock_openai.py
- tests/fixtures/mock_gemini.py

3) CLI smoke test
- tests/test_cli_smoke.py: verifies menu prints, API status path, and mock generation happy-path without making network calls

Example: unit test skeleton
```python
import os
import builtins
from src.hybrid.modern_workflow import ModernHybridWorkflow, ModelType

def test_model_selection_prefers_gpt_for_production(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("GOOGLE_API_KEY", "test")
    wf = ModernHybridWorkflow()
    chosen = wf._select_model(ModelType.AUTO, "production")
    assert chosen == ModelType.GPT_IMAGE_1
```
Story B: API mocking (no real costs in tests)
- Mock OpenAI client images.generate to return an object with data[0].b64_json that decodes to a minimal valid PNG
- Mock Gemini client models.generate_content to return candidates[0].content.parts with inline_data.data as raw PNG bytes
- Ensure both mocks can simulate:
  - success
  - rate-limit error
  - auth error
  - empty response (no parts)

Example: tiny PNG bytes helper
```python
import base64
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP4BwQACfsD/IbLr9YAAAAASUVORK5CYII="
)
```
Story C: Unit tests (ModernHybridWorkflow)
- _select_model(): all branches: requested model unavailable → AUTO fallback; production → GPT; draft/review → Gemini; fallback when one API missing
- _validate_image(): rejects too-small or invalid mode; accepts RGB/RGBA
- _build_universal_prompt(): includes brand, colors, constraints; front/back differences; concept mapping
- _save_image(): writes file with naming convention and non-zero size

Example: save_image test
```python
from pathlib import Path
from src.hybrid.modern_workflow import ModernHybridWorkflow

def test_save_image_writes_file(tmp_path):
    wf = ModernHybridWorkflow()
    wf.production_dir = tmp_path  # redirect
    path = wf._save_image(b"\x89PNG\r\n\x1a\n", "Clinical-Precision", "front", "gpt-image-1", tmp_path)
    assert Path(path).exists()
    assert Path(path).stat().st_size > 0
    assert "Clinical-Precision" in Path(path).name
```
Story D: Integration tests (mocked I/O only)
- generate_card() draft → must call mocked Gemini, save to output/drafts/, set cost_estimate=0.005
- generate_card() production → must call mocked OpenAI, save to output/production/, set cost_estimate=0.19 (or mapped values)
- generate_full_concept_set(): returns both front/back with correct model selection
- Error path: when primary model fails (e.g., OpenAI rate-limits), tests ensure graceful error info is returned (no crash)

Example: integration success
```python
def test_generate_card_production_uses_gpt(monkeypatch, mock_openai_success, mock_gemini_success, tmp_path):
    # set env
    monkeypatch.setenv("OPENAI_API_KEY", "ok")
    monkeypatch.setenv("GOOGLE_API_KEY", "ok")
    from src.hybrid.modern_workflow import ModernHybridWorkflow
    wf = ModernHybridWorkflow()
    wf.production_dir = tmp_path
    result = wf.generate_card("Clinical-Precision", "front", model=ModelType.AUTO, quality="production")
    assert result.success
    assert result.model_used == "gpt-image-1"
    assert result.cost_estimate > 0
```
Story E: Image validation module
- src/validation/image_rules.py with reusable checks:
  - min resolution (>= 512×512)
  - color mode allowed (RGB/RGBA)
  - optional heuristic: “flat artboard” checks (no EXIF, no alpha over-threshold?), keep it minimal now
- tests/test_validation.py: unit tests for each rule

Example: image rule API
```python
from PIL import Image
import io

def validate_min_resolution(data: bytes, min_w=512, min_h=512) -> bool:
    img = Image.open(io.BytesIO(data))
    return img.width >= min_w and img.height >= min_h
```
Story F: API health & environment checks
- src/monitoring/api_status.py:
  - check env presence (OPENAI_API_KEY, GOOGLE_API_KEY)
  - optional lightweight “ping” that’s just a no-op (do not generate in tests)
- tests validate status output
- Hook this into CLI option 9 (already present) to format a green/red summary

Example: status util
```python
import os

def api_status():
    return {
        "OpenAI": bool(os.getenv("OPENAI_API_KEY")),
        "Google": bool(os.getenv("GOOGLE_API_KEY")),
    }
```
Story G: Cost estimation accuracy tests
- Verify cost maps per quality (draft/review/production)
- Ensure session tracking adds up across multi-concept runs
- Guardrails: if cost mapping changes, tests fail loudly

Example: cost map test
```python
from src.hybrid.modern_workflow import ModernHybridWorkflow

def test_cost_map_values():
    wf = ModernHybridWorkflow()
    assert wf.COSTS["gemini_flash"] == 0.005
    assert wf.COSTS["gpt_image_1_high"] == 0.19
```
Runbook (local)
- new sprint-2-testing-qa
- save
- pip install -U pytest pytest-mock freezegun
- pytest -q
- check
- done "sprint-2: scaffolding + unit tests + mocks"
- ship
- Iterate by story, keeping commits small per story

Acceptance criteria (Sprint 2)
- 95%+ unit coverage on src/hybrid/modern_workflow.py core branches:
  - Model selection
  - Image validation
  - Prompt build
  - Save routine
- Integration tests cover:
  - Draft (Gemini mocked) and Production (OpenAI mocked)
  - Error fallback paths (rate-limit, auth error, empty response)
- Validation module passes all tests; catches bad image data
- CLI smoke tests pass (no network needed)
- No real API calls in tests; all network is mocked
- Cost estimation verified within defined constants
- Docs added:
  - aidocs/TESTING.md: “how to run tests/mocks locally and in CI”
  - aidocs/CI_NOTES.md: outline for adding pytest to CI (if applicable)

Definition of done (repeat per story)
- Tests pass locally (pytest) with 0 flakiness
- No console.log/print spam in production code (keep logging minimal and controlled)
- Nothing leaks secrets; tests don’t rely on real API keys
- Mobile and accessibility reminders are not applicable to image pipeline, but ensure file outputs and naming are consistent for downstream workflows
- Commit using your message format: emoji + type(scope): message; keep < 50 chars

Suggested commit messages
- ✅ Add scaffolding: 🧪 test(workflow): unit scaffolding + mocks
- ✅ Unit coverage: 🧪 test(validation): add image rules + tests
- ✅ Integration: 🧪 test(cli): smoke test with mocks
- ✅ Docs: 📚 docs(testing): local + CI runbook

Optional stretch goals (if time allows)
- Add a record-replay layer for network fixtures (e.g., vcrpy) to capture one or two real runs then rely on cassettes
- Add basic histogram reporting for generation times in tests (sanity check)
- Add linting and formatting (ruff/black) in pre-commit for consistent quality

Want me to scaffold the tests and validation modules now, or keep it as a guide and you’ll run save first?