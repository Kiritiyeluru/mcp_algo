"""
@ai_metadata
Generated: 2025-02-08
Feature: Real-time Metrics Collection
Component: Monitoring
Purpose: Collect and store real-time metrics from test execution
Author: Claude
Environment: dev
Risk: Medium
Dependencies: Memory MCP, Context Manager
Related Files: 
    - monitoring/context_manager.py
    - monitoring/test_orchestrator.py
File Location: /monitoring/metrics_collector.py
"""

import time
import json
import psutil
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class TestMetrics:
    """Test execution metrics data structure."""
    test_id: str
    start_time: float
    duration: Optional[float] = None
    cpu_usage: List[float] = None
    memory_usage: List[float] = None
    status: str = "running"
    error: Optional[str] = None

class MetricsCollector:
    """Real-time metrics collection and storage system."""
    
    def __init__(self, storage_path: str = "metrics/test_metrics.json"):
        self.storage_path = storage_path
        self.current_metrics: Dict[str, TestMetrics] = {}
        self.sampling_interval = 1.0  # 1 second
        
    def start_test_metrics(self, test_id: str) -> None:
        """Start collecting metrics for a test."""
        self.current_metrics[test_id] = TestMetrics(
            test_id=test_id,
            start_time=time.time(),
            cpu_usage=[],
            memory_usage=[]
        )
        
    def collect_current_metrics(self, test_id: str) -> None:
        """Collect current system metrics."""
        if test_id not in self.current_metrics:
            return
            
        metrics = self.current_metrics[test_id]
        metrics.cpu_usage.append(psutil.cpu_percent())
        metrics.memory_usage.append(psutil.virtual_memory().percent)
        
    def end_test_metrics(self, test_id: str, status: str, error: Optional[str] = None) -> TestMetrics:
        """Complete metrics collection for a test."""
        if test_id not in self.current_metrics:
            raise KeyError(f"No metrics found for test {test_id}")
            
        metrics = self.current_metrics[test_id]
        metrics.duration = time.time() - metrics.start_time
        metrics.status = status
        metrics.error = error
        
        self._save_metrics(test_id, metrics)
        return metrics
        
    def _save_metrics(self, test_id: str, metrics: TestMetrics) -> None:
        """Save metrics to storage."""
        try:
            with open(self.storage_path, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                    
                data[test_id] = {
                    "timestamp": datetime.now().isoformat(),
                    "duration": metrics.duration,
                    "cpu_usage": metrics.cpu_usage,
                    "memory_usage": metrics.memory_usage,
                    "status": metrics.status,
                    "error": metrics.error
                }
                
                f.seek(0)
                json.dump(data, f, indent=2)
        except FileNotFoundError:
            with open(self.storage_path, 'w') as f:
                json.dump({test_id: {
                    "timestamp": datetime.now().isoformat(),
                    "duration": metrics.duration,
                    "cpu_usage": metrics.cpu_usage,
                    "memory_usage": metrics.memory_usage,
                    "status": metrics.status,
                    "error": metrics.error
                }}, f, indent=2)
                
    def get_test_metrics(self, test_id: str) -> Optional[Dict]:
        """Retrieve metrics for a specific test."""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return data.get(test_id)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
            
    def get_all_metrics(self) -> Dict:
        """Retrieve all stored metrics."""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}