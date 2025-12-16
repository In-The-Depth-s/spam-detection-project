# spam_detector_ai/tests/test_auto_config.py

import pytest
import tempfile
import os
import json

from spam_detector_ai.auto_config import (
    AutoConfig, ConfigProfile, ResourceTier, create_auto_config
)


class TestAutoConfig:
    """Tests for the AutoConfig smart configuration system"""
    
    def test_auto_config_initialization(self):
        """Test that AutoConfig initializes correctly"""
        config = AutoConfig(profile=ConfigProfile.PRODUCTION)
        assert config is not None
        assert config.profile == ConfigProfile.PRODUCTION
        assert config.config is not None
        assert config.system_info is not None
    
    def test_development_profile(self):
        """Test development profile configuration"""
        config = AutoConfig(profile=ConfigProfile.DEVELOPMENT)
        vectorizer_config = config.get_vectorizer_config()
        
        assert vectorizer_config['max_features'] == 1000
        assert vectorizer_config['min_df'] == 5
        assert vectorizer_config['max_df'] == 0.8
    
    def test_production_profile(self):
        """Test production profile configuration"""
        config = AutoConfig(profile=ConfigProfile.PRODUCTION)
        vectorizer_config = config.get_vectorizer_config()
        training_config = config.get_training_config()
        
        assert vectorizer_config['max_features'] == 1500
        assert training_config['test_size'] == 0.2
        assert training_config['random_state'] == 0
    
    def test_high_accuracy_profile(self):
        """Test high accuracy profile configuration"""
        config = AutoConfig(profile=ConfigProfile.HIGH_ACCURACY)
        vectorizer_config = config.get_vectorizer_config()
        training_config = config.get_training_config()
        
        assert vectorizer_config['max_features'] == 2000
        assert training_config['test_size'] == 0.15
    
    def test_fast_inference_profile(self):
        """Test fast inference profile configuration"""
        config = AutoConfig(profile=ConfigProfile.FAST_INFERENCE)
        vectorizer_config = config.get_vectorizer_config()
        
        assert vectorizer_config['max_features'] == 800
        assert vectorizer_config['min_df'] == 10
    
    def test_system_resource_detection(self):
        """Test system resource detection"""
        config = AutoConfig(profile=ConfigProfile.PRODUCTION)
        
        assert 'memory_gb' in config.system_info
        assert 'cpu_count' in config.system_info
        assert 'resource_tier' in config.system_info
        assert isinstance(config.system_info['resource_tier'], ResourceTier)
    
    def test_get_model_config(self):
        """Test getting configuration for specific models"""
        config = AutoConfig(profile=ConfigProfile.PRODUCTION)
        
        rf_config = config.get_model_config('random_forest')
        assert 'n_estimators' in rf_config
        assert 'max_depth' in rf_config
        
        svm_config = config.get_model_config('svm')
        assert 'kernel' in svm_config
        assert 'C' in svm_config
    
    def test_recommend_models(self):
        """Test model recommendations"""
        config_prod = AutoConfig(profile=ConfigProfile.PRODUCTION)
        models_prod = config_prod.recommend_models()
        assert len(models_prod) > 0
        
        config_fast = AutoConfig(profile=ConfigProfile.FAST_INFERENCE)
        models_fast = config_fast.recommend_models()
        assert 'naive_bayes' in models_fast
        assert 'logistic_regression' in models_fast
    
    def test_validate_config(self):
        """Test configuration validation"""
        config = AutoConfig(profile=ConfigProfile.PRODUCTION)
        is_valid, warnings = config.validate_config()
        
        assert isinstance(is_valid, bool)
        assert isinstance(warnings, list)
    
    def test_get_summary(self):
        """Test getting configuration summary"""
        config = AutoConfig(profile=ConfigProfile.PRODUCTION)
        summary = config.get_summary()
        
        assert isinstance(summary, str)
        assert 'Profile:' in summary
        assert 'Resource Tier:' in summary
        assert 'Vectorizer Configuration:' in summary
    
    def test_apply_to_base_classifier(self):
        """Test applying configuration to BaseClassifier"""
        config = AutoConfig(profile=ConfigProfile.PRODUCTION)
        base_config = config.apply_to_base_classifier()
        
        assert 'VECTORIZER_PARAMS' in base_config
        assert 'max_features' in base_config['VECTORIZER_PARAMS']
    
    def test_export_config(self):
        """Test exporting configuration to file"""
        config = AutoConfig(profile=ConfigProfile.PRODUCTION)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name
        
        try:
            config.export_config(tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r') as f:
                exported_data = json.load(f)
            
            assert 'profile' in exported_data
            assert 'system_info' in exported_data
            assert 'config' in exported_data
            assert exported_data['profile'] == 'production'
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_create_auto_config_factory(self):
        """Test factory function for creating AutoConfig"""
        config = create_auto_config(profile='production')
        assert config is not None
        assert config.profile == ConfigProfile.PRODUCTION
        
        config_dev = create_auto_config(profile='development')
        assert config_dev.profile == ConfigProfile.DEVELOPMENT
    
    def test_different_profiles_have_different_configs(self):
        """Test that different profiles produce different configurations"""
        config_dev = AutoConfig(profile=ConfigProfile.DEVELOPMENT)
        config_prod = AutoConfig(profile=ConfigProfile.PRODUCTION)
        config_high = AutoConfig(profile=ConfigProfile.HIGH_ACCURACY)
        
        dev_features = config_dev.get_vectorizer_config()['max_features']
        prod_features = config_prod.get_vectorizer_config()['max_features']
        high_features = config_high.get_vectorizer_config()['max_features']
        
        assert dev_features != prod_features or prod_features != high_features


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
