import os
import sys

# Add project root directory to sys.path so imports work in Vercel serverless environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
