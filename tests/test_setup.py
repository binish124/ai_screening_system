import os
import pytest
from utils.logger import setup_logger

def test_project_structure_exists():
    """Verify all required modular directories exist."""
    required_dirs = [
        "data", "parsers", "ats_engine", 
        "screening_ai", "interview_ai", 
        "scoring", "utils", "tests"
    ]
    
    for directory in required_dirs:
        assert os.path.isdir(directory), f"Missing required directory: {directory}"

def test_logger_creation():
    """Verify that the logger initializes and creates the log file."""
    logger = setup_logger("test_logger")
    logger.info("Test log entry")
    
    # Check if the logs directory and file were created
    assert os.path.isdir("logs"), "Logs directory was not created"
    assert os.path.isfile("logs/ai_system.log"), "Log file was not created"