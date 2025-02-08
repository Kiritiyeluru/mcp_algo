"""
@ai_metadata
Generated: 2025-02-08
Feature: Performance Benchmarking
Component: Monitoring
Purpose: Measure and track system performance metrics
Author: Claude
Environment: dev
Risk: Low
Dependencies: Memory MCP, Metrics Collector
Related Files: 
    - monitoring/metrics_collector.py
    - monitoring/ml_predictor.py
File Location: /monitoring/performance_benchmark.py
"""

import time
import json
import psutil
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BenchmarkResult:
    """Benchmark result data structure."""
    component: str
    execution_time: float
    cpu_usage: List[float]
    memory_usage: List[float]
    io_operations: int
    timestamp: str

class PerformanceBenchmark:
    """System performance benchmarking."""
    
    def __init__(self, results_path: str = "metrics/benchmark_results.json"):
        self.results_path = results_path
        self.current_benchmark = None
        self.io_start_counters = None
        
    def start_benchmark(self, component: str) -> None:
        """Start benchmarking a component."""
        self.current_benchmark = {
            "component": component,
            "start_time": time.time(),
            "cpu_usage": [],
            "memory_usage": [],
            "start_io": psutil.disk_io_counters()
        }
        
    def collect_metrics(self) -> None:
        """Collect current performance metrics."""
        if not self.current_benchmark:
            return
            
        self.current_benchmark["cpu_usage"].append(psutil.cpu_percent())
        self.current_benchmark["memory_usage"].append(psutil.virtual_memory().percent)
        
    def end_benchmark(self) -> BenchmarkResult:
        """Complete benchmarking and save results."""
        if not self.current_benchmark:
            raise RuntimeError("No active benchmark")
            
        end_time = time.time()
        end_io = psutil.disk_io_counters()
        
        # Calculate I/O operations
        io_ops = (
            (end_io.read_count - self.current_benchmark["start_io"].read_count) +
            (end_io.write_count - self.current_benchmark["start_io"].write_count)
        )
        
        result = BenchmarkResult(
            component=self.current_benchmark["component"],
            execution_time=end_time - self.current_benchmark["start_time"],
            cpu_usage=self.current_benchmark["cpu_usage"],
            memory_usage=self.current_benchmark["memory_usage"],
            io_operations=io_ops,
            timestamp=datetime.now().isoformat()
        )
        
        self._save_result(result)
        self.current_benchmark = None
        return result
        
    def _save_result(self, result: BenchmarkResult) -> None:
        """Save benchmark results to storage."""
        try:
            with open(self.results_path, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                    
                if result.component not in data:
                    data[result.component] = []
                    
                data[result.component].append({
                    "timestamp": result.timestamp,
                    "execution_time": result.execution_time,
                    "cpu_usage": result.cpu_usage,
                    "memory_usage": result.memory_usage,
                    "io_operations": result.io_operations
                })
                
                f.seek(0)
                json.dump(data, f, indent=2)
        except FileNotFoundError:
            with open(self.results_path, 'w') as f:
                json.dump({
                    result.component: [{
                        "timestamp": result.timestamp,
                        "execution_time": result.execution_time,
                        "cpu_usage": result.cpu_usage,
                        "memory_usage": result.memory_usage,
                        "io_operations": result.io_operations
                    }]
                }, f, indent=2)
                
    def get_component_benchmarks(self, component: str) -> List[Dict]:
        """Retrieve benchmark history for a component."""
        try:
            with open(self.results_path, 'r') as f:
                data = json.load(f)
                return data.get(component, [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
    def analyze_performance(self, component: str) -> Dict:
        """Analyze performance metrics for a component."""
        benchmarks = self.get_component_benchmarks(component)
        
        if not benchmarks:
            return {}
            
        execution_times = [b["execution_time"] for b in benchmarks]
        cpu_usage = [np.mean(b["cpu_usage"]) for b in benchmarks]
        memory_usage = [np.mean(b["memory_usage"]) for b in benchmarks]
        io_operations = [b["io_operations"] for b in benchmarks]
        
        return {
            "execution_time": {
                "mean": np.mean(execution_times),
                "std": np.std(execution_times),
                "min": np.min(execution_times),
                "max": np.max(execution_times)
            },
            "cpu_usage": {
                "mean": np.mean(cpu_usage),
                "std": np.std(cpu_usage),
                "min": np.min(cpu_usage),
                "max": np.max(cpu_usage)
            },
            "memory_usage": {
                "mean": np.mean(memory_usage),
                "std": np.std(memory_usage),
                "min": np.min(memory_usage),
                "max": np.max(memory_usage)
            },
            "io_operations": {
                "mean": np.mean(io_operations),
                "std": np.std(io_operations),
                "min": np.min(io_operations),
                "max": np.max(io_operations)
            }
        }
        
    def compare_benchmarks(self, 
                          component: str, 
                          baseline_date: str, 
                          current_date: str) -> Dict:
        """Compare performance between two time periods."""
        benchmarks = self.get_component_benchmarks(component)
        
        if not benchmarks:
            return {}
            
        baseline = [b for b in benchmarks if b["timestamp"] <= baseline_date]
        current = [b for b in benchmarks if b["timestamp"] > baseline_date 
                  and b["timestamp"] <= current_date]
                  
        if not baseline or not current:
            return {}
            
        def calculate_metrics(data):
            return {
                "execution_time": np.mean([b["execution_time"] for b in data]),
                "cpu_usage": np.mean([np.mean(b["cpu_usage"]) for b in data]),
                "memory_usage": np.mean([np.mean(b["memory_usage"]) for b in data]),
                "io_operations": np.mean([b["io_operations"] for b in data])
            }
            
        baseline_metrics = calculate_metrics(baseline)
        current_metrics = calculate_metrics(current)
        
        return {
            "baseline": baseline_metrics,
            "current": current_metrics,
            "changes": {
                key: ((current_metrics[key] - baseline_metrics[key]) 
                      / baseline_metrics[key] * 100)
                for key in baseline_metrics
            }
        }