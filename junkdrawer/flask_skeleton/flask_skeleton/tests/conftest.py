import os
import pytest
import yaml

import flask_skeleton


@pytest.fixture(scope="module")
def tests_dir():
    """Test directory"""
    return os.path.join(flask_skeleton.__path__[0], "tests")

@pytest.fixture(scope="module")
def test_config(tests_dir):
    """Load test configuration."""
    fp = os.path.join(tests_dir, "test_config.yml")
    return yaml.safe_load(open(fp, 'r'))
