# Smart Auto-Configuration System

## Overview

The Smart Auto-Configuration System is an intelligent configuration module that automatically optimizes settings for spam detection models based on:

- **System Resources**: Detects available memory, CPU cores, and adapts settings accordingly
- **Use Case Profiles**: Provides pre-configured profiles for different scenarios
- **One-to-One Entity Configuration**: Configure individual models independently
- **Human-Friendly Interface**: Easy-to-use API with validation and recommendations

## Features

### 1. Automatic Resource Detection
The system automatically detects:
- Available memory (RAM)
- CPU core count and frequency
- Operating system platform
- Resource tier (LOW, MEDIUM, HIGH)

Based on these detections, it adapts configurations to optimize performance.

### 2. Configuration Profiles

Four pre-configured profiles are available:

#### Development Profile
- **Purpose**: Fast training during development and testing
- **Characteristics**: Lower accuracy, faster training
- **Use Case**: When iterating on code or testing changes
- **Settings**:
  - Vectorizer max_features: 1000
  - Test size: 30%
  - Reduced model complexity

#### Production Profile (Default)
- **Purpose**: Balanced performance and accuracy
- **Characteristics**: Good accuracy with reasonable training time
- **Use Case**: Recommended for most production deployments
- **Settings**:
  - Vectorizer max_features: 1500
  - Test size: 20%
  - Standard model complexity

#### High Accuracy Profile
- **Purpose**: Maximum accuracy, slower training
- **Characteristics**: Best possible accuracy, longer training
- **Use Case**: When accuracy is paramount, training time is not critical
- **Settings**:
  - Vectorizer max_features: 2000
  - Test size: 15%
  - Increased model complexity

#### Fast Inference Profile
- **Purpose**: Quick predictions, optimized for speed
- **Characteristics**: Fast predictions, slightly lower accuracy
- **Use Case**: High-volume prediction scenarios
- **Settings**:
  - Vectorizer max_features: 800
  - Simplified models (Naive Bayes, Logistic Regression)
  - Reduced complexity

### 3. One-to-One Entity Configuration

Configure individual models independently:
```python
config = AutoConfig(profile=ConfigProfile.PRODUCTION)

# Get Random Forest specific configuration
rf_config = config.get_model_config('random_forest')
# Returns: {'n_estimators': 100, 'max_depth': None}

# Get SVM specific configuration
svm_config = config.get_model_config('svm')
# Returns: {'kernel': 'rbf', 'C': 1.0}
```

## Usage Examples

### Basic Usage

```python
from spam_detector_ai.auto_config import create_auto_config

# Create configuration with production profile
config = create_auto_config(profile='production')

# Get vectorizer configuration
vectorizer_config = config.get_vectorizer_config()
# {'max_features': 1500, 'min_df': 5, 'max_df': 0.7}

# Get training configuration
training_config = config.get_training_config()
# {'test_size': 0.2, 'random_state': 0, 'n_jobs': -1}
```

### Using Different Profiles

```python
from spam_detector_ai import AutoConfig, ConfigProfile

# Development profile for fast iteration
dev_config = AutoConfig(profile=ConfigProfile.DEVELOPMENT)

# High accuracy for production
prod_config = AutoConfig(profile=ConfigProfile.HIGH_ACCURACY)

# Fast inference for high-volume
fast_config = AutoConfig(profile=ConfigProfile.FAST_INFERENCE)
```

### Getting Configuration Summary

```python
config = AutoConfig(profile=ConfigProfile.PRODUCTION)
print(config.get_summary())
```

Output:
```
╔════════════════════════════════════════════════════════════════╗
║          Smart Auto-Configuration Summary                      ║
╚════════════════════════════════════════════════════════════════╝

Profile: production
Resource Tier: high

System Information:
  • Memory: 16.0 GB
  • CPU Cores: 4
  • Platform: Linux

Vectorizer Configuration:
  • Max Features: 1500
  • Min DF: 5
  • Max DF: 0.7

Training Configuration:
  • Test Size: 0.2
  • N Jobs: -1
  • Random State: 0

Recommended Models: naive_bayes, random_forest, svm, logistic_regression, xgb

Validation:
  ✓ Configuration is valid
```

### Model Recommendations

```python
config = AutoConfig(profile=ConfigProfile.PRODUCTION)

# Get recommended models for your configuration
models = config.recommend_models()
print(models)
# ['naive_bayes', 'random_forest', 'svm', 'logistic_regression', 'xgb']
```

### Configuration Validation

```python
config = AutoConfig(profile=ConfigProfile.PRODUCTION)

# Validate configuration
is_valid, warnings = config.validate_config()

if is_valid:
    print("Configuration is valid!")
    
if warnings:
    print("Warnings:")
    for warning in warnings:
        print(f"  • {warning}")
```

### Export Configuration

```python
config = AutoConfig(profile=ConfigProfile.PRODUCTION)

# Export to JSON file for later use
config.export_config('my_config.json')
```

### Applying to Base Classifier

```python
config = AutoConfig(profile=ConfigProfile.PRODUCTION)

# Get configuration in format compatible with BaseClassifier
base_config = config.apply_to_base_classifier()
# {'VECTORIZER_PARAMS': {'max_features': 1500, 'min_df': 5, 'max_df': 0.7}}
```

## Advanced Usage

### Custom Logger

```python
import logging

logger = logging.getLogger('MyApp')
logger.setLevel(logging.INFO)

config = AutoConfig(profile=ConfigProfile.PRODUCTION, logger=logger)
```

### Checking System Resources

```python
config = AutoConfig(profile=ConfigProfile.PRODUCTION)

print(f"Memory: {config.system_info['memory_gb']} GB")
print(f"CPU Cores: {config.system_info['cpu_count']}")
print(f"Resource Tier: {config.system_info['resource_tier'].value}")
```

### Model-Specific Configuration

```python
config = AutoConfig(profile=ConfigProfile.HIGH_ACCURACY)

# Configure Random Forest
rf_params = config.get_model_config('random_forest')
# Use these parameters when training

# Configure XGBoost
xgb_params = config.get_model_config('xgb')
# Use these parameters when training
```

## Resource Tier Adaptation

The system automatically adapts to available resources:

### Low Tier (< 4GB RAM, < 2 cores)
- Reduces max_features
- Uses single-threaded processing (n_jobs=1)
- Limits model complexity
- Recommends lighter models

### Medium Tier (4-8GB RAM, 2-4 cores)
- Standard configuration
- Balanced settings

### High Tier (> 8GB RAM, > 4 cores)
- Can handle more complexity
- Enables parallel processing (n_jobs=-1)
- No limitations on model complexity

## Integration Examples

### With Model Training

```python
from spam_detector_ai.auto_config import create_auto_config
from spam_detector_ai.training.train_models import ModelTrainer

# Create auto-configuration
config = create_auto_config(profile='production')

# Use configuration for training
trainer = ModelTrainer(
    data_path='data/spam.csv',
    test_size=config.get_training_config()['test_size']
)

# Apply vectorizer configuration to your models
vectorizer_params = config.get_vectorizer_config()
```

### With Prediction

```python
from spam_detector_ai import AutoConfig, ConfigProfile
from spam_detector_ai.prediction.predict import VotingSpamDetector

# Get recommended models
config = AutoConfig(profile=ConfigProfile.FAST_INFERENCE)
recommended_models = config.recommend_models()

print(f"Using models: {recommended_models}")

# Create detector with all models
detector = VotingSpamDetector()
result = detector.is_spam("Your message here")
```

## API Reference

### AutoConfig Class

#### `__init__(profile: ConfigProfile, logger: Optional[logging.Logger] = None)`
Initialize AutoConfig with a profile.

#### `get_vectorizer_config() -> Dict[str, Any]`
Get optimized vectorizer configuration.

#### `get_training_config() -> Dict[str, Any]`
Get optimized training configuration.

#### `get_model_config(model_name: str) -> Dict[str, Any]`
Get configuration for a specific model (one-to-one entity configuration).

#### `recommend_models(dataset_size: Optional[int] = None) -> List[str]`
Recommend models based on configuration and dataset size.

#### `validate_config() -> Tuple[bool, List[str]]`
Validate the current configuration.

#### `get_summary() -> str`
Get a human-readable summary of the configuration.

#### `export_config(filepath: str) -> None`
Export configuration to a file.

### ConfigProfile Enum

- `DEVELOPMENT`: Fast training, lower accuracy
- `PRODUCTION`: Balanced performance and accuracy
- `HIGH_ACCURACY`: Maximum accuracy, slower
- `FAST_INFERENCE`: Quick predictions, lower accuracy
- `CUSTOM`: User-defined configuration

### Factory Function

#### `create_auto_config(profile: str = "production", logger: Optional[logging.Logger] = None) -> AutoConfig`
Create AutoConfig with string profile name.

## Best Practices

1. **Use production profile by default**: It provides a good balance for most use cases.

2. **Check system resources**: Review the detected resource tier to ensure optimal configuration.

3. **Validate configuration**: Always call `validate_config()` before training to catch potential issues.

4. **Export configurations**: Save successful configurations for reproducibility.

5. **Profile selection**:
   - Development: When iterating and testing
   - Production: For most deployments
   - High Accuracy: When accuracy is critical
   - Fast Inference: For high-volume prediction services

6. **Model-specific tuning**: Use `get_model_config()` to fine-tune individual models.

## Troubleshooting

### Low Memory Warning
If you see a low memory warning, consider:
- Using `FAST_INFERENCE` profile
- Reducing batch sizes
- Processing data in chunks

### CPU Limitation
If you have limited CPU cores:
- System automatically adjusts `n_jobs` setting
- Consider `FAST_INFERENCE` profile for quicker processing

### Configuration Validation Failures
Check the warning messages from `validate_config()` and adjust accordingly.

## Future Enhancements

Planned features:
- Dataset size analysis for dynamic configuration
- GPU detection and optimization
- Custom profile creation and saving
- Configuration templates for specific domains
- A/B testing support for multiple configurations

## Examples

See `examples/auto_config_usage.py` for comprehensive examples of all features.

## Support

For issues or questions:
- Check the configuration summary: `config.get_summary()`
- Validate your configuration: `config.validate_config()`
- Review the recommended models: `config.recommend_models()`
