import pytest
from src.demo_data import fresh_candidate,jobs
@pytest.fixture
def candidate():return fresh_candidate()
@pytest.fixture
def inventory():return jobs()
