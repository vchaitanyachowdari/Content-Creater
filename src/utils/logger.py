import logging
import sys

def setup_logger(name='ChiatuAI'):
    """Set up logging configuration"""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(name)

# Export both the setup function and logger instance
__all__ = ['setup_logger']