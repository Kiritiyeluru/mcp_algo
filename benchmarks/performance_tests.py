"""
Performance Benchmarking for MCP Documentation System
"""

import timeit
import statistics
import os
import sys
from memory_profiler import memory_usage

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from documentation.generators.docstring_parser import DocStringParser
from documentation.generators.cross_reference_manager import CrossReferenceManager

def benchmark_docstring_parsing(file_path):
    """
    Benchmark docstring parsing performance.
    
    Args:
        file_path: Path to Python file for parsing
    
    Returns:
        Dictionary with parsing metrics
    """
    def parse_function():
        parser = DocStringParser(file_path)
        parser.parse_docstring(parser.module_ast)
    
    # Time performance
    times = timeit.repeat(parse_function, repeat=5, number=10)
    
    # Memory usage
    mem_usage = memory_usage(parse_function, max_iterations=1)
    
    return {
        'min_time': min(times) / 10,  # Average time per iteration
        'max_time': max(times) / 10,
        'avg_time': statistics.mean(times) / 10,
        'std_dev_time': statistics.stdev(times) / 10 if len(times) > 1 else 0,
        'peak_memory': max(mem_usage)
    }

def benchmark_cross_reference_generation(directory):
    """
    Benchmark cross-reference generation performance.
    
    Args:
        directory: Directory containing Python files
    
    Returns:
        Dictionary with cross-reference metrics
    """
    def generate_references():
        ref_manager = CrossReferenceManager(directory)
        ref_manager.analyze_dependencies()
        ref_manager.generate_reference_links()
    
    # Time performance
    times = timeit.repeat(generate_references, repeat=5, number=1)
    
    # Memory usage
    mem_usage = memory_usage(generate_references, max_iterations=1)
    
    return {
        'min_time': min(times),
        'max_time': max(times),
        'avg_time': statistics.mean(times),
        'std_dev_time': statistics.stdev(times) if len(times) > 1 else 0,
        'peak_memory': max(mem_usage)
    }

def run_benchmarks(test_directory):
    """
    Run comprehensive performance benchmarks.
    
    Args:
        test_directory: Directory for performance testing
    """
    print("=== Performance Benchmarks ===")
    
    # Find a sample Python file
    sample_file = None
    for root, _, files in os.walk(test_directory):
        for file in files:
            if file.endswith('.py'):
                sample_file = os.path.join(root, file)
                break
        if sample_file:
            break
    
    if not sample_file:
        print("No Python files found for benchmarking!")
        return
    
    # Docstring Parsing Benchmark
    print("\n--- Docstring Parsing Performance ---")
    parsing_metrics = benchmark_docstring_parsing(sample_file)
    for metric, value in parsing_metrics.items():
        print(f"{metric}: {value}")
    
    # Cross-Reference Generation Benchmark
    print("\n--- Cross-Reference Generation Performance ---")
    ref_metrics = benchmark_cross_reference_generation(test_directory)
    for metric, value in ref_metrics.items():
        print(f"{metric}: {value}")

if __name__ == "__main__":
    # Use the project's root directory for benchmarking
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    run_benchmarks(project_root)
