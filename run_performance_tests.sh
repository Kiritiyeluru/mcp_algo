#!/bin/bash

# Ensure the script is executable
chmod +x run_performance_tests.sh

# Install dependencies
pip install -r requirements.txt

# Run performance tests
python3 run_benchmarks.py
