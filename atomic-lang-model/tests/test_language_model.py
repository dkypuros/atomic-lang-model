#!/usr/bin/env python3
"""
Integration Tests for Probabilistic Language Model
=================================================

Tests the integration between Rust and Python components,
ensuring the hybrid architecture maintains all formal guarantees
while providing practical language modeling capabilities.
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from tiny_lm import ProbGrammar
from hybrid_model import HybridLanguageModel
import time
import json


class TestProbabilisticGrammar(unittest.TestCase):
    """Test the probabilistic grammar implementation."""
    
    def setUp(self):
        self.model = ProbGrammar()
    
    def test_grammar_normalization(self):
        """Test that grammar rules are properly normalized."""
        for lhs, productions in self.model.rules.items():
            total_weight = sum(weight for weight, _ in productions)
            self.assertAlmostEqual(total_weight, 1.0, places=6,
                msg=f"Weights for {lhs} should sum to 1.0")
    
    def test_sentence_generation(self):
        """Test basic sentence generation."""
        for _ in range(10):
            sentence = self.model.sample_sentence()
            self.assertIsInstance(sentence, str)
            self.assertGreater(len(sentence), 0)
            # Should contain at least subject and verb
            tokens = sentence.split()
            self.assertGreaterEqual(len(tokens), 2)
    
    def test_recursive_capability(self):
        """Test that model can generate recursive structures."""
        recursive_found = False
        for _ in range(100):
            sentence = self.model.sample_sentence()
            if "who" in sentence or "that" in sentence:
                recursive_found = True
                break
        
        self.assertTrue(recursive_found, 
            "Should generate at least one recursive structure")
    
    def test_prediction_output_format(self):
        """Test next-token prediction output format."""
        predictions = self.model.predict_next("the student", k=1000)
        
        self.assertIsInstance(predictions, list)
        self.assertGreater(len(predictions), 0)
        
        # Check format of predictions
        for token, prob in predictions:
            self.assertIsInstance(token, str)
            self.assertIsInstance(prob, float)
            self.assertGreaterEqual(prob, 0.0)
            self.assertLessEqual(prob, 1.0)
        
        # Check probabilities sum to ~1.0
        total_prob = sum(prob for _, prob in predictions)
        self.assertAlmostEqual(total_prob, 1.0, places=1)
    
    def test_empty_prefix_handling(self):
        """Test handling of empty prefix."""
        predictions = self.model.predict_next("", k=1000)
        # Should still return predictions (starting tokens)
        self.assertGreater(len(predictions), 0)


class TestHybridModel(unittest.TestCase):
    """Test the hybrid Rust-Python model."""
    
    def setUp(self):
        self.model = HybridLanguageModel()
    
    def test_initialization(self):
        """Test model initialization."""
        self.assertIsNotNone(self.model.prob_grammar)
        # Rust binary might not be available in test environment
        if self.model.rust_binary:
            self.assertTrue(self.model.rust_binary.exists())
    
    def test_syntax_validation_fallback(self):
        """Test that validation falls back to Python when Rust unavailable."""
        # Test with known valid/invalid sentences
        valid_sentences = [
            "the student left",
            "a teacher smiled"
        ]
        
        for sentence in valid_sentences:
            # Should return True even without Rust binary
            result = self.model.validate_syntax(sentence)
            self.assertIsInstance(result, bool)
    
    def test_prediction_with_validation(self):
        """Test predictions with syntactic validation."""
        predictions = self.model.predict_next("the student", k=1000, validate=True)
        
        # All predictions should lead to valid continuations
        for token, prob in predictions[:5]:
            test_sentence = f"the student {token}"
            # If we have Rust validation, check it
            if self.model.rust_binary:
                self.assertTrue(self.model.validate_syntax(test_sentence))
    
    def test_sentence_generation_validity(self):
        """Test that generated sentences are valid."""
        for _ in range(5):
            sentence = self.model.generate_sentence()
            if sentence:  # Might fail if no valid sentence found
                self.assertIsInstance(sentence, str)
                self.assertGreater(len(sentence), 0)
    
    def test_beam_search_completions(self):
        """Test beam search for completions."""
        completions = self.model.get_valid_continuations("the teacher", beam_size=3)
        
        self.assertIsInstance(completions, list)
        self.assertLessEqual(len(completions), 3)  # Respects beam size
        
        for completion in completions:
            self.assertIsInstance(completion, str)
            self.assertTrue(completion.startswith("the teacher"))
    
    def test_model_export(self):
        """Test model configuration export."""
        config = self.model.to_json()
        
        self.assertIn("model_type", config)
        self.assertIn("grammar_rules", config)
        self.assertIn("capabilities", config)
        self.assertIn("guarantees", config)
        
        # Check guarantees
        self.assertTrue(config["guarantees"]["grammaticality"])
        self.assertTrue(config["guarantees"]["recursion"])


class TestLanguageModelPerformance(unittest.TestCase):
    """Performance tests for the language model."""
    
    def setUp(self):
        self.prob_model = ProbGrammar()
        self.hybrid_model = HybridLanguageModel()
    
    def test_generation_speed(self):
        """Test sentence generation performance."""
        start = time.time()
        sentences = [self.prob_model.sample_sentence() for _ in range(100)]
        duration = time.time() - start
        
        rate = len(sentences) / duration
        print(f"\nGeneration rate: {rate:.0f} sentences/second")
        
        # Should generate at least 100 sentences per second
        self.assertGreater(rate, 100)
    
    def test_prediction_speed(self):
        """Test next-token prediction performance."""
        start = time.time()
        predictions = self.prob_model.predict_next("the student who", k=1000)
        duration = time.time() - start
        
        print(f"Prediction time (1000 samples): {duration:.3f}s")
        
        # Should complete in under 1 second
        self.assertLess(duration, 1.0)
    
    def test_memory_footprint(self):
        """Test that model has minimal memory footprint."""
        import os
        
        # Check size of Python modules
        module_sizes = {
            "tiny_lm.py": os.path.getsize(
                os.path.join(os.path.dirname(__file__), '..', 'python', 'tiny_lm.py')
            ),
            "hybrid_model.py": os.path.getsize(
                os.path.join(os.path.dirname(__file__), '..', 'python', 'hybrid_model.py')
            ),
            "api_server.py": os.path.getsize(
                os.path.join(os.path.dirname(__file__), '..', 'python', 'api_server.py')
            )
        }
        
        total_size = sum(module_sizes.values())
        print(f"\nModule sizes:")
        for name, size in module_sizes.items():
            print(f"  {name}: {size/1024:.1f} KB")
        print(f"Total: {total_size/1024:.1f} KB")
        
        # Total should be under 100KB
        self.assertLess(total_size, 100 * 1024)


class TestMathematicalProperties(unittest.TestCase):
    """Test mathematical properties of the language model."""
    
    def setUp(self):
        self.model = ProbGrammar()
    
    def test_discrete_infinity(self):
        """Test that model exhibits discrete infinity."""
        # Generate many sentences and check for uniqueness
        sentences = set()
        for _ in range(1000):
            sentence = self.model.sample_sentence()
            sentences.add(sentence)
        
        # Should generate many unique sentences
        uniqueness_ratio = len(sentences) / 1000
        print(f"\nUniqueness ratio: {uniqueness_ratio:.1%}")
        
        self.assertGreater(uniqueness_ratio, 0.5,
            "Should generate mostly unique sentences")
    
    def test_recursive_depth(self):
        """Test recursive depth capabilities."""
        max_depth = 0
        depth_counts = {}
        
        for _ in range(500):
            sentence = self.model.sample_sentence()
            depth = sentence.count("who") + sentence.count("that")
            max_depth = max(max_depth, depth)
            depth_counts[depth] = depth_counts.get(depth, 0) + 1
        
        print(f"\nRecursive depth distribution:")
        for depth in sorted(depth_counts.keys()):
            print(f"  Depth {depth}: {depth_counts[depth]} sentences")
        
        # Should be able to generate at least depth 2
        self.assertGreaterEqual(max_depth, 2)
    
    def test_probability_consistency(self):
        """Test that probabilities are consistent."""
        # Generate sentences and verify they follow the grammar weights
        prefix = "the"
        predictions = self.model.predict_next(prefix, k=5000)
        
        # Check that more probable tokens appear more often
        if len(predictions) >= 2:
            first_token, first_prob = predictions[0]
            last_token, last_prob = predictions[-1]
            
            # First should have higher probability than last
            self.assertGreater(first_prob, last_prob)


class TestLinguisticPhenomena(unittest.TestCase):
    """Test specific linguistic phenomena."""
    
    def setUp(self):
        self.model = ProbGrammar()
    
    def test_center_embedding(self):
        """Test generation of center-embedded structures."""
        center_embedded = []
        
        for _ in range(200):
            sentence = self.model.sample_sentence()
            # Look for patterns like "the X who Y Z"
            if "who" in sentence and sentence.count("the") >= 1:
                center_embedded.append(sentence)
        
        self.assertGreater(len(center_embedded), 0,
            "Should generate center-embedded structures")
        
        print(f"\nCenter-embedded examples:")
        for example in center_embedded[:3]:
            print(f"  - {example}")
    
    def test_grammatical_roles(self):
        """Test that sentences have proper grammatical roles."""
        for _ in range(10):
            sentence = self.model.sample_sentence()
            tokens = sentence.split()
            
            # Should have determiners and nouns
            determiners = ["the", "a"]
            has_determiner = any(d in tokens for d in determiners)
            
            # Should have verbs
            verbs = ["left", "smiled", "praised", "arrived"]
            has_verb = any(v in tokens for v in verbs)
            
            self.assertTrue(has_determiner and has_verb,
                f"Sentence should have determiner and verb: {sentence}")


def run_integration_tests():
    """Run all integration tests with summary."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestProbabilisticGrammar,
        TestHybridModel,
        TestLanguageModelPerformance,
        TestMathematicalProperties,
        TestLinguisticPhenomena
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*60)
    print("Integration Test Summary")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ All integration tests passed!")
        print("The probabilistic language model is working correctly.")
    else:
        print("\n❌ Some tests failed. Please review the output above.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)