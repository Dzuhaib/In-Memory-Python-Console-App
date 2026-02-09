#!/usr/bin/env python3
"""Entry point for the Todo Console App."""

import sys
from pathlib import Path

# Add parent directory to path so 'src' package can be found
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli.main import main

if __name__ == "__main__":
    main()
