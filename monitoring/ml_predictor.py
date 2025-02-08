"""
@ai_metadata
Generated: 2025-02-08
Feature: ML-based Test Prediction
Component: Monitoring
Purpose: Predict test outcomes and resource usage
Author: Claude
Environment: dev
Risk: Medium
Dependencies: Memory MCP, Metrics Collector
Related Files: 
    - monitoring/metrics_collector.py
    - monitoring/test_orchestrator.py
File Location: /monitoring/ml_predictor.py
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

@dataclass
class PredictionResult:
    """Prediction result data structure."""
    test_id: str
    failure_probability: float
    estimated_duration: float
    estimated_cpu_usage: float
    estimated_memory_usage: float
    confidence_score: float

class MLPredictor:
    """ML-based test prediction system."""
    
    def __init__(self, metrics_path: str = "metrics/test_metrics.json"):
        self.metrics_path = metrics_path
        self.failure_model = RandomForestClassifier()
        self.resource_scaler = StandardScaler()
        self.duration_scaler = StandardScaler()
        self.trained = False
        
    def prepare_training_data(self, metrics: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare metrics data for training."""
        features = []
        labels = []
        
        for test_id, test_data in metrics.items():
            # Extract features
            cpu_mean = np.mean(test_data["cpu_usage"])
            cpu_std = np.std(test_data["cpu_usage"])
            mem_mean = np.mean(test_data["memory_usage"])
            mem_std = np.std(test_data["memory_usage"])
            duration = test_data["duration"]
            
            features.append([cpu_mean, cpu_std, mem_mean, mem_std, duration])
            labels.append(1 if test_data["status"] == "failed" else 0)
            
        return np.array(features), np.array(labels)
        
    def train_model(self, metrics: Dict) -> None:
        """Train prediction models using historical metrics."""
        features, labels = self.prepare_training_data(metrics)
        
        if len(features) < 10:
            raise ValueError("Insufficient training data (minimum 10 samples required)")
            
        # Scale features
        self.resource_scaler.fit(features[:, :4])
        self.duration_scaler.fit(features[:, 4:])
        
        scaled_features = np.hstack([
            self.resource_scaler.transform(features[:, :4]),
            self.duration_scaler.transform(features[:, 4:])
        ])
        
        # Train model
        self.failure_model.fit(scaled_features, labels)
        self.trained = True
        
    def predict_test_outcome(self, 
                           test_id: str, 
                           current_metrics: Dict) -> PredictionResult:
        """Predict test outcome and resource usage."""
        if not self.trained:
            raise RuntimeError("Model not trained")
            
        # Extract current features
        cpu_mean = np.mean(current_metrics["cpu_usage"])
        cpu_std = np.std(current_metrics["cpu_usage"])
        mem_mean = np.mean(current_metrics["memory_usage"])
        mem_std = np.std(current_metrics["memory_usage"])
        duration = current_metrics.get("duration", 0)
        
        features = np.array([[cpu_mean, cpu_std, mem_mean, mem_std, duration]])
        
        # Scale features
        scaled_features = np.hstack([
            self.resource_scaler.transform(features[:, :4]),
            self.duration_scaler.transform(features[:, 4:])
        ])
        
        # Make predictions
        failure_prob = self.failure_model.predict_proba(scaled_features)[0][1]
        confidence = np.max(self.failure_model.predict_proba(scaled_features)[0])
        
        return PredictionResult(
            test_id=test_id,
            failure_probability=failure_prob,
            estimated_duration=duration * 1.1,  # Add 10% buffer
            estimated_cpu_usage=cpu_mean,
            estimated_memory_usage=mem_mean,
            confidence_score=confidence
        )
        
    def evaluate_model(self, test_metrics: Dict) -> Dict:
        """Evaluate model performance."""
        if not self.trained:
            raise RuntimeError("Model not trained")
            
        features, true_labels = self.prepare_training_data(test_metrics)
        scaled_features = np.hstack([
            self.resource_scaler.transform(features[:, :4]),
            self.duration_scaler.transform(features[:, 4:])
        ])
        
        predictions = self.failure_model.predict(scaled_features)
        
        # Calculate metrics
        accuracy = np.mean(predictions == true_labels)
        false_positives = np.sum((predictions == 1) & (true_labels == 0))
        false_negatives = np.sum((predictions == 0) & (true_labels == 1))
        
        return {
            "accuracy": accuracy,
            "false_positive_rate": false_positives / len(true_labels),
            "false_negative_rate": false_negatives / len(true_labels)
        }