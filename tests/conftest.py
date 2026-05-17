import importlib.util
import sys
import os
import copy
import pytest
from fastapi.testclient import TestClient

# Load src/app.py as a module
spec = importlib.util.spec_from_file_location(
    "app_module",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "app.py")),
)
app_module = importlib.util.module_from_spec(spec)
sys.modules["app_module"] = app_module
spec.loader.exec_module(app_module)

# Keep an initial deep copy of activities to restore between tests
_initial_activities = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    # Restore in-memory state before each test
    app_module.activities = copy.deepcopy(_initial_activities)
    yield
    app_module.activities = copy.deepcopy(_initial_activities)

@pytest.fixture
def client():
    return TestClient(app_module.app)
