"""
@ai_metadata
Generated: 2025-02-08
Feature: Integration Testing
Component: Monitoring
Purpose: Test integration between monitoring components
Author: Claude
Environment: dev
Risk: Low
Dependencies: pytest, Memory MCP
Related Files: 
    - monitoring/metrics_collector.py
    - monitoring/ml_predictor.py
File Location: /monitoring/tests/test_integration.py
"""

import pytest
import time
import json
import os
from monitoring.metrics_collector import MetricsCollector
from monitoring.ml_predictor import MLPredictor
from monitoring.context_manager import ContextManager

@pytest.fixture
def setup_test_environment():
    """Set up test environment with required files."""
    metrics_path = "test_metrics.json"
    context_path = "test_context.json"
    
    yield metrics_path, context_path
    
    # Cleanup
    for path in [metrics_path, context_path]:
        if os.path.exists(path):
            os.remove(path)

def generate_test_metrics():
    """Generate sample test metrics."""
    return {
        "test1": {
            "timestamp": "2025-02-08T00:00:00",
            "duration": 1.5,
            "cpu_usage": [10, 20, 30],
            "memory_usage": [40, 50, 60],
            "status": "passed",
            "error": None
        },
        "test2": {
            "timestamp": "2025-02-08T00:01:00",
            "duration": 2.0,
            "cpu_usage": [15, 25, 35],
            "memory_usage": [45, 55, 65],
            "status": "failed",
            "error": "AssertionError"
        }
    }

class TestMonitoringIntegration:
    """Integration tests for monitoring system components."""
    
    def test_metrics_collection_and_prediction(self, setup_test_environment):
        """Test integration between metrics collection and ML prediction."""
        metrics_path, _ = setup_test_environment
        
        # Initialize components
        collector = MetricsCollector(storage_path=metrics_path)
        predictor = MLPredictor(metrics_path=metrics_path)
        
        # Start collecting metrics
        test_id = "integration_test_1"
        collector.start_test_metrics(test_id)
        
        # Simulate test execution
        for _ in range(3):
            collector.collect_current_metrics(test_id)
            time.sleep(0.1)
            
        # End metrics collection
        metrics = collector.end_test_metrics(test_id, "passed")
        
        # Train predictor with sample data
        sample_metrics = generate_test_metrics()
        predictor.train_model(sample_metrics)
        
        # Make prediction
        prediction = predictor.predict_test_outcome(test_id, {
            "cpu_usage": metrics.cpu_usage,
            "memory_usage": metrics.memory_usage,
            "duration": metrics.duration
        })
        
        assert prediction.test_id == test_id
        assert 0 <= prediction.failure_probability <= 1
        assert prediction.confidence_score > 0
        
    def test_context_preservation_with_metrics(self, setup_test_environment):
        """Test integration between context manager and metrics collection."""
        metrics_path, context_path = setup_test_environment
        
        # Initialize components
        collector = MetricsCollector(storage_path=metrics_path)
        context_manager = ContextManager()
        
        # Create test context
        context = context_manager.save_generation_context(
            component="test_component",
            prompt="test prompt",
            generated_code="print('test')",
            modifications=["initial"]
        )
        
        # Start metrics collection
        test_id = context["component"]
        collector.start_test_metrics(test_id)
        
        # Collect metrics
        for _ in range(3):
            collector.collect_current_metrics(test_id)
            time.sleep(0.1)
            
        # End metrics collection
        metrics = collector.end_test_metrics(test_id, "passed")
        
        # Verify context and metrics
        latest_context = context_manager.get_latest_context()
        test_metrics = collector.get_test_metrics(test_id)
        
        assert latest_context["component"] == test_id
        assert test_metrics is not None
        assert test_metrics["status"] == "passed"
        
    def test_full_monitoring_pipeline(self, setup_test_environment):
        """Test complete monitoring pipeline integration."""
        metrics_path, context_path = setup_test_environment
        
        # Initialize all components
        collector = MetricsCollector(storage_path=metrics_path)
        predictor = MLPredictor(metrics_path=metrics_path)
        context_manager = ContextManager()
        
        # Train predictor
        predictor.train_model(generate_test_metrics())
        
        # Create test context
        context = context_manager.save_generation_context(
            component="pipeline_test",
            prompt="test prompt",
            generated_code="print('test')",
            modifications=["initial"]
        )
        
        # Collect metrics
        test_id = context["component"]
        collector.start_test_metrics(test_id)
        
        for _ in range(3):
            collector.collect_current_metrics(test_id)
            time.sleep(0.1)
            
        metrics = collector.end_test_metrics(test_id, "passed")
        
        # Make prediction
        prediction = predictor.predict_test_outcome(test_id, {
            "cpu_usage": metrics.cpu_usage,
            "memory_usage": metrics.memory_usage,
            "duration": metrics.duration
        })
        
        # Verify entire pipeline
        assert context_manager.get_latest_context()["component"] == test_id
        assert collector.get_test_metrics(test_id) is not None
        assert prediction.test_id == test_id
        assert prediction.confidence_score > 0

if __name__ == "__main__":
    pytest.main(["-v", __file__])