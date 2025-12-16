#!/usr/bin/env python3
# examples/auto_config_usage.py
"""
Example demonstrating the Smart Auto-Configuration System
for Spam Detection with human-friendly interface
"""

from spam_detector_ai.auto_config import AutoConfig, ConfigProfile, create_auto_config


def demo_basic_usage():
    """Basic usage of AutoConfig"""
    print("=" * 70)
    print("BASIC USAGE: Creating AutoConfig with different profiles")
    print("=" * 70)
    
    # Create configuration with different profiles
    profiles = ['development', 'production', 'high_accuracy', 'fast_inference']
    
    for profile_name in profiles:
        config = create_auto_config(profile=profile_name)
        print(f"\n{profile_name.upper()} Profile:")
        print(f"  Vectorizer max_features: {config.get_vectorizer_config()['max_features']}")
        print(f"  Training test_size: {config.get_training_config()['test_size']}")
        print(f"  Recommended models: {', '.join(config.recommend_models())}")
    
    print("\n")


def demo_detailed_summary():
    """Show detailed configuration summary"""
    print("=" * 70)
    print("DETAILED SUMMARY: Production Configuration")
    print("=" * 70)
    
    config = AutoConfig(profile=ConfigProfile.PRODUCTION)
    print(config.get_summary())
    print("\n")


def demo_model_specific_config():
    """Get configuration for specific models (one-to-one entity)"""
    print("=" * 70)
    print("ONE-TO-ONE ENTITY CONFIGURATION: Model-Specific Settings")
    print("=" * 70)
    
    config = AutoConfig(profile=ConfigProfile.HIGH_ACCURACY)
    
    print("\nRandom Forest Configuration:")
    rf_config = config.get_model_config('random_forest')
    for key, value in rf_config.items():
        print(f"  {key}: {value}")
    
    print("\nSVM Configuration:")
    svm_config = config.get_model_config('svm')
    for key, value in svm_config.items():
        print(f"  {key}: {value}")
    
    print("\nXGBoost Configuration:")
    xgb_config = config.get_model_config('xgb')
    for key, value in xgb_config.items():
        print(f"  {key}: {value}")
    
    print("\n")


def demo_adaptive_config():
    """Show how configuration adapts to system resources"""
    print("=" * 70)
    print("ADAPTIVE CONFIGURATION: Resource-Based Optimization")
    print("=" * 70)
    
    config = AutoConfig(profile=ConfigProfile.PRODUCTION)
    
    print("\nSystem Resource Detection:")
    print(f"  Memory: {config.system_info['memory_gb']} GB")
    print(f"  CPU Cores: {config.system_info['cpu_count']}")
    print(f"  Resource Tier: {config.system_info['resource_tier'].value}")
    
    print("\nAdaptive Settings:")
    training_config = config.get_training_config()
    print(f"  Parallel jobs (n_jobs): {training_config['n_jobs']}")
    print(f"  Test size: {training_config['test_size']}")
    
    print("\n")


def demo_export_import():
    """Demonstrate exporting configuration"""
    print("=" * 70)
    print("EXPORT CONFIGURATION: Save for Later Use")
    print("=" * 70)
    
    import tempfile
    import os
    
    config = AutoConfig(profile=ConfigProfile.PRODUCTION)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
        tmp_path = tmp.name
    
    try:
        config.export_config(tmp_path)
        print(f"\n✓ Configuration exported to: {tmp_path}")
        
        # Show file contents
        with open(tmp_path, 'r') as f:
            content = f.read()
        print(f"\nExported content preview (first 500 chars):")
        print(content[:500] + "...")
        
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    print("\n")


def demo_validation():
    """Demonstrate configuration validation"""
    print("=" * 70)
    print("CONFIGURATION VALIDATION: Automatic Checks")
    print("=" * 70)
    
    config = AutoConfig(profile=ConfigProfile.PRODUCTION)
    is_valid, warnings = config.validate_config()
    
    print(f"\nConfiguration valid: {is_valid}")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  • {warning}")
    else:
        print("No warnings - configuration is optimal!")
    
    print("\n")


def demo_human_interface():
    """Demonstrate the human-friendly interface"""
    print("=" * 70)
    print("HUMAN-FRIENDLY INTERFACE: Interactive Configuration")
    print("=" * 70)
    
    print("\nAvailable Profiles:")
    profiles = {
        'development': 'Fast training, lower accuracy - for development/testing',
        'production': 'Balanced performance and accuracy - recommended default',
        'high_accuracy': 'Maximum accuracy, slower - for production use',
        'fast_inference': 'Quick predictions, lower accuracy - for high-volume'
    }
    
    for profile, description in profiles.items():
        print(f"  • {profile}: {description}")
    
    print("\nExample: Creating a production configuration")
    print("  config = create_auto_config(profile='production')")
    
    config = create_auto_config(profile='production')
    print("\n✓ Configuration created successfully!")
    print(f"  Resource tier detected: {config.system_info['resource_tier'].value}")
    print(f"  Recommended models: {', '.join(config.recommend_models())}")
    
    print("\n")


def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "Smart Auto-Configuration System Demonstration" + " " * 12 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    demo_human_interface()
    demo_basic_usage()
    demo_detailed_summary()
    demo_model_specific_config()
    demo_adaptive_config()
    demo_validation()
    demo_export_import()
    
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nFor more information, see the documentation or:")
    print("  from spam_detector_ai import AutoConfig, ConfigProfile")
    print("  help(AutoConfig)")
    print("\n")


if __name__ == "__main__":
    main()
