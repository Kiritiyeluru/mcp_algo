"""
Advanced Performance Benchmarking for MCP Documentation System
"""

import os
import sys
import timeit
import statistics
from memory_profiler import memory_usage

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from documentation.generators.advanced_parser import AdvancedDocumentationParser

def benchmark_advanced_parsing(base_directory):
    """
    Benchmark advanced parsing performance.
    
    Args:
        base_directory: Directory containing Python files
    
    Returns:
        Dictionary with parsing metrics
    """
    def parse_function():
        parser = AdvancedDocumentationParser(base_directory)
        parser.parallel_parse()
        parser.generate_dependency_graph()
    
    # Time performance
    times = timeit.repeat(parse_function, repeat=5, number=1)
    
    # Memory usage
    mem_usage = memory_usage(parse_function, max_iterations=1)
    
    return {
        'min_time': min(times),
        'max_time': max(times),
        'avg_time': statistics.mean(times),
        'std_dev_time': statistics.stdev(times) if len(times) > 1 else 0,
        'peak_memory': max(mem_usage)
    }

def compare_parsing_strategies(base_directory):
    """
    Compare different parsing strategies.
    
    Args:
        base_directory: Directory containing Python files
    """
    print("=== Advanced Parsing Performance Benchmarks ===")
    
    # Parallel Parsing Benchmark
    print("\n--- Parallel Parsing Performance ---")
    parallel_metrics = benchmark_advanced_parsing(base_directory)
    for metric, value in parallel_metrics.items():
        print(f"{metric}: {value}")
    
    # Create comparison scenarios
    scenarios = [
        ("Serial Parsing", 1),
        ("Low Concurrency", 2),
        ("Medium Concurrency", 4),
        ("High Concurrency", os.cpu_count() - 1)
    ]
    
    print("\n--- Concurrency Comparison ---")
    for scenario_name, workers in scenarios:
        parser = AdvancedDocumentationParser(base_directory)
        start_time = timeit.default_timer()
        results = parser.parallel_parse(max_workers=workers)
        end_time = timeit.default_timer()
        
        print(f"\n{scenario_name} (Workers: {workers})")
        print(f"Modules Parsed: {len(results)}")
        print(f"Total Time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    # Use the project's root directory for benchmarking
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    compare_parsing_strategies(project_root)
