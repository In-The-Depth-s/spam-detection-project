# spam_detector_ai/auto_config.py
"""
Smart Auto-Configuration Module for Spam Detection
This module provides intelligent configuration that adapts to:
- Dataset characteristics (size, features)
- Available system resources (memory, CPU)
- Use case requirements (accuracy vs speed)
- User/developer preferences
"""

import logging
import os
import platform
import psutil
from enum import Enum
from typing import Dict, Any, Optional, List, Tuple


class ConfigProfile(Enum):
    """Configuration profiles for different use cases"""
    DEVELOPMENT = "development"  # Fast training, lower accuracy
    PRODUCTION = "production"    # Balanced performance and accuracy
    HIGH_ACCURACY = "high_accuracy"  # Maximum accuracy, slower
    FAST_INFERENCE = "fast_inference"  # Quick predictions, lower accuracy
    CUSTOM = "custom"  # User-defined configuration


class ResourceTier(Enum):
    """System resource availability tiers"""
    LOW = "low"      # < 4GB RAM, < 2 cores
    MEDIUM = "medium"  # 4-8GB RAM, 2-4 cores
    HIGH = "high"    # > 8GB RAM, > 4 cores


class AutoConfig:
    """
    Intelligent auto-configuration system for spam detection models.
    Provides one-to-one configuration for individual models and components.
    """
    
    def __init__(self, profile: ConfigProfile = ConfigProfile.PRODUCTION, 
                 logger: Optional[logging.Logger] = None):
        """
        Initialize AutoConfig with a specific profile.
        
        Args:
            profile: Configuration profile to use
            logger: Optional logger instance
        """
        self.profile = profile
        self.logger = logger or self._create_default_logger()
        self.system_info = self._detect_system_resources()
        self.config = self._generate_config()
        self.logger.info(f"AutoConfig initialized with profile: {profile.value}")
        
    def _create_default_logger(self) -> logging.Logger:
        """Create a default logger if none provided"""
        logger = logging.getLogger('AutoConfig')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def _detect_system_resources(self) -> Dict[str, Any]:
        """
        Detect available system resources for intelligent configuration.
        
        Returns:
            Dictionary with system information
        """
        try:
            memory_gb = psutil.virtual_memory().total / (1024 ** 3)
            cpu_count = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            
            # Determine resource tier
            if memory_gb < 4 or cpu_count < 2:
                tier = ResourceTier.LOW
            elif memory_gb < 8 or cpu_count < 4:
                tier = ResourceTier.MEDIUM
            else:
                tier = ResourceTier.HIGH
            
            system_info = {
                'memory_gb': round(memory_gb, 2),
                'cpu_count': cpu_count,
                'cpu_freq_mhz': round(cpu_freq.current, 2) if cpu_freq else None,
                'platform': platform.system(),
                'architecture': platform.machine(),
                'resource_tier': tier
            }
            
            self.logger.info(f"Detected system resources: {tier.value} tier")
            return system_info
            
        except Exception as e:
            self.logger.warning(f"Could not detect system resources: {e}")
            return {
                'memory_gb': 4,
                'cpu_count': 2,
                'resource_tier': ResourceTier.MEDIUM
            }
    
    def _generate_config(self) -> Dict[str, Any]:
        """
        Generate configuration based on profile and system resources.
        
        Returns:
            Configuration dictionary with optimized settings
        """
        resource_tier = self.system_info.get('resource_tier', ResourceTier.MEDIUM)
        
        # Base configuration templates
        configs = {
            ConfigProfile.DEVELOPMENT: {
                'vectorizer': {
                    'max_features': 1000,
                    'min_df': 5,
                    'max_df': 0.8
                },
                'training': {
                    'test_size': 0.3,
                    'random_state': 42,
                    'n_jobs': 1
                },
                'models': {
                    'random_forest': {'n_estimators': 50, 'max_depth': 10},
                    'svm': {'kernel': 'linear', 'C': 0.5},
                    'xgb': {'n_estimators': 50, 'max_depth': 3}
                }
            },
            ConfigProfile.PRODUCTION: {
                'vectorizer': {
                    'max_features': 1500,
                    'min_df': 5,
                    'max_df': 0.7
                },
                'training': {
                    'test_size': 0.2,
                    'random_state': 0,
                    'n_jobs': -1
                },
                'models': {
                    'random_forest': {'n_estimators': 100, 'max_depth': None},
                    'svm': {'kernel': 'rbf', 'C': 1.0},
                    'xgb': {'n_estimators': 100, 'max_depth': 6}
                }
            },
            ConfigProfile.HIGH_ACCURACY: {
                'vectorizer': {
                    'max_features': 2000,
                    'min_df': 3,
                    'max_df': 0.8
                },
                'training': {
                    'test_size': 0.15,
                    'random_state': 0,
                    'n_jobs': -1
                },
                'models': {
                    'random_forest': {'n_estimators': 200, 'max_depth': None},
                    'svm': {'kernel': 'rbf', 'C': 1.5},
                    'xgb': {'n_estimators': 200, 'max_depth': 8}
                }
            },
            ConfigProfile.FAST_INFERENCE: {
                'vectorizer': {
                    'max_features': 800,
                    'min_df': 10,
                    'max_df': 0.9
                },
                'training': {
                    'test_size': 0.2,
                    'random_state': 0,
                    'n_jobs': 1
                },
                'models': {
                    'random_forest': {'n_estimators': 30, 'max_depth': 8},
                    'svm': {'kernel': 'linear', 'C': 0.5},
                    'xgb': {'n_estimators': 30, 'max_depth': 4}
                }
            }
        }
        
        config = configs.get(self.profile, configs[ConfigProfile.PRODUCTION])
        
        # Adjust based on resource tier
        if resource_tier == ResourceTier.LOW:
            config['vectorizer']['max_features'] = min(
                config['vectorizer']['max_features'], 1000
            )
            config['training']['n_jobs'] = 1
            # Reduce model complexity
            if 'random_forest' in config['models']:
                config['models']['random_forest']['n_estimators'] = min(
                    config['models']['random_forest']['n_estimators'], 50
                )
        
        elif resource_tier == ResourceTier.HIGH:
            # Can handle more complexity
            config['training']['n_jobs'] = -1
        
        self.logger.info(f"Generated configuration for {self.profile.value} profile")
        return config
    
    def get_vectorizer_config(self) -> Dict[str, Any]:
        """
        Get optimized vectorizer configuration.
        
        Returns:
            Dictionary with vectorizer parameters
        """
        return self.config.get('vectorizer', {})
    
    def get_training_config(self) -> Dict[str, Any]:
        """
        Get optimized training configuration.
        
        Returns:
            Dictionary with training parameters
        """
        return self.config.get('training', {})
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific model (one-to-one entity configuration).
        
        Args:
            model_name: Name of the model (e.g., 'random_forest', 'svm', 'xgb')
            
        Returns:
            Dictionary with model-specific parameters
        """
        models = self.config.get('models', {})
        return models.get(model_name, {})
    
    def recommend_models(self, dataset_size: Optional[int] = None) -> List[str]:
        """
        Recommend models based on configuration and dataset size.
        
        Args:
            dataset_size: Optional size of the dataset
            
        Returns:
            List of recommended model names
        """
        resource_tier = self.system_info.get('resource_tier', ResourceTier.MEDIUM)
        
        if self.profile == ConfigProfile.FAST_INFERENCE:
            return ['naive_bayes', 'logistic_regression']
        
        elif self.profile == ConfigProfile.HIGH_ACCURACY:
            return ['random_forest', 'xgb', 'svm', 'logistic_regression']
        
        elif resource_tier == ResourceTier.LOW:
            return ['naive_bayes', 'logistic_regression', 'svm']
        
        # Default recommendations for production
        return ['naive_bayes', 'random_forest', 'svm', 'logistic_regression', 'xgb']
    
    def validate_config(self) -> Tuple[bool, List[str]]:
        """
        Validate the current configuration.
        
        Returns:
            Tuple of (is_valid, list of warnings/issues)
        """
        warnings = []
        
        # Check vectorizer settings
        vectorizer = self.config.get('vectorizer', {})
        if vectorizer.get('max_features', 0) < 500:
            warnings.append("max_features is very low, may impact accuracy")
        
        # Check system resources
        if self.system_info.get('memory_gb', 0) < 2:
            warnings.append("Low memory detected, consider FAST_INFERENCE profile")
        
        # Check n_jobs setting
        training = self.config.get('training', {})
        if training.get('n_jobs', 1) == -1 and self.system_info.get('cpu_count', 1) <= 2:
            warnings.append("n_jobs=-1 with few cores may not improve performance")
        
        is_valid = len([w for w in warnings if 'error' in w.lower()]) == 0
        return is_valid, warnings
    
    def get_summary(self) -> str:
        """
        Get a human-readable summary of the configuration.
        
        Returns:
            Formatted string with configuration summary
        """
        resource_tier = self.system_info.get('resource_tier', ResourceTier.MEDIUM)
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║          Smart Auto-Configuration Summary                      ║
╚════════════════════════════════════════════════════════════════╝

Profile: {self.profile.value}
Resource Tier: {resource_tier.value}

System Information:
  • Memory: {self.system_info.get('memory_gb', 'N/A')} GB
  • CPU Cores: {self.system_info.get('cpu_count', 'N/A')}
  • Platform: {self.system_info.get('platform', 'N/A')}

Vectorizer Configuration:
  • Max Features: {self.config['vectorizer']['max_features']}
  • Min DF: {self.config['vectorizer']['min_df']}
  • Max DF: {self.config['vectorizer']['max_df']}

Training Configuration:
  • Test Size: {self.config['training']['test_size']}
  • N Jobs: {self.config['training']['n_jobs']}
  • Random State: {self.config['training']['random_state']}

Recommended Models: {', '.join(self.recommend_models())}

Validation:
"""
        is_valid, warnings = self.validate_config()
        if is_valid:
            summary += "  ✓ Configuration is valid\n"
        if warnings:
            summary += "  Warnings:\n"
            for warning in warnings:
                summary += f"    • {warning}\n"
        
        return summary
    
    def apply_to_base_classifier(self) -> Dict[str, Any]:
        """
        Get configuration that can be applied to BaseClassifier.
        
        Returns:
            Dictionary with VECTORIZER_PARAMS
        """
        return {
            'VECTORIZER_PARAMS': self.get_vectorizer_config()
        }
    
    def export_config(self, filepath: str) -> None:
        """
        Export configuration to a file for later use.
        
        Args:
            filepath: Path to save the configuration
        """
        import json
        
        export_data = {
            'profile': self.profile.value,
            'system_info': {k: v.value if isinstance(v, Enum) else v 
                           for k, v in self.system_info.items()},
            'config': self.config
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Configuration exported to {filepath}")


def create_auto_config(profile: str = "production", 
                       logger: Optional[logging.Logger] = None) -> AutoConfig:
    """
    Factory function to create AutoConfig with string profile name.
    
    Args:
        profile: Profile name as string
        logger: Optional logger instance
        
    Returns:
        AutoConfig instance
    """
    profile_map = {
        'development': ConfigProfile.DEVELOPMENT,
        'production': ConfigProfile.PRODUCTION,
        'high_accuracy': ConfigProfile.HIGH_ACCURACY,
        'fast_inference': ConfigProfile.FAST_INFERENCE,
        'custom': ConfigProfile.CUSTOM
    }
    
    profile_enum = profile_map.get(profile.lower(), ConfigProfile.PRODUCTION)
    return AutoConfig(profile=profile_enum, logger=logger)


if __name__ == "__main__":
    # Demo usage
    print("=" * 70)
    print("Smart Auto-Configuration System Demo")
    print("=" * 70)
    
    # Test different profiles
    for profile in ConfigProfile:
        if profile != ConfigProfile.CUSTOM:
            config = AutoConfig(profile=profile)
            print(config.get_summary())
            print("\n")
