import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_benchmark():
    """
    Run advanced performance benchmarks and capture results
    """
    project_root = os.path.abspath(os.path.dirname(__file__))
    benchmark_script = os.path.join(project_root, 'benchmarks', 'advanced_performance_tests.py')
    
    # Ensure the benchmarking dependencies are installed
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
    
    # Run the benchmark script
    result = subprocess.run(
        [sys.executable, benchmark_script], 
        capture_output=True, 
        text=True
    )
    
    # Create a benchmark results file
    results_dir = os.path.join(project_root, 'benchmark_results')
    os.makedirs(results_dir, exist_ok=True)
    
    with open(os.path.join(results_dir, 'performance_results.txt'), 'w') as f:
        f.write(result.stdout)
        f.write("\n\nSTDERR:\n")
        f.write(result.stderr)
    
    print("Benchmark results saved to benchmark_results/performance_results.txt")
    
    # Print results to console
    print("\n=== Benchmark Results ===")
    print(result.stdout)
    
    if result.stderr:
        print("\n=== Benchmark Errors ===")
        print(result.stderr)

if __name__ == '__main__':
    run_benchmark()
