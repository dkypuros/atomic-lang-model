#!/usr/bin/env python3
"""
Atomic Language Model Demo
==========================

Interactive demonstration of the probabilistic language model capabilities.
Shows how to use the model for various NLP tasks while maintaining
formal guarantees of grammaticality and recursion.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from tiny_lm import ProbGrammar
from hybrid_model import HybridLanguageModel
import json

def separator(title: str):
    """Print a formatted section separator."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def demo_basic_generation():
    """Demonstrate basic sentence generation."""
    separator("Basic Sentence Generation")
    
    model = ProbGrammar()
    print("Generating 10 random sentences from the grammar:\n")
    
    for i in range(10):
        sentence = model.sample_sentence()
        print(f"{i+1:2}. {sentence}")
    
    print("\n✅ All sentences are guaranteed grammatical by construction")

def demo_next_token_prediction():
    """Demonstrate next-token prediction capabilities."""
    separator("Next-Token Prediction")
    
    model = ProbGrammar()
    test_prefixes = [
        "the",
        "the student",
        "the student who",
        "the teacher",
        "a"
    ]
    
    for prefix in test_prefixes:
        print(f"\nPrefix: '{prefix}'")
        predictions = model.predict_next(prefix, k=5000)
        
        print("  Top predictions:")
        for token, prob in predictions[:5]:
            bar = '█' * int(prob * 30)
            print(f"    {token:10} {prob:6.3f} {bar}")

def demo_recursive_capability():
    """Demonstrate recursive sentence generation."""
    separator("Recursive Generation Capability")
    
    model = ProbGrammar()
    print("Generating sentences with increasing embedding depth:\n")
    
    # Generate sentences and sort by complexity
    sentences = []
    for _ in range(100):
        s = model.sample_sentence()
        depth = s.count("who") + s.count("that")
        sentences.append((depth, s))
    
    # Show examples at each depth
    sentences.sort()
    shown_depths = set()
    
    for depth, sentence in sentences:
        if depth not in shown_depths and depth <= 3:
            print(f"Depth {depth}: {sentence}")
            shown_depths.add(depth)
            if len(shown_depths) >= 4:
                break
    
    print("\n✅ Model generates recursive structures naturally")

def demo_hybrid_validation():
    """Demonstrate hybrid model with syntax validation."""
    separator("Hybrid Model: Probabilistic + Formal Validation")
    
    try:
        model = HybridLanguageModel()
        print("Hybrid model initialized with Rust validation\n")
    except:
        print("⚠️  Rust binary not found - using Python-only mode\n")
        model = HybridLanguageModel()
    
    # Test valid and invalid sentences
    test_sentences = [
        ("the student left", True),
        ("the teacher who arrived smiled", True),
        ("student the left", False),
        ("the the student", False),
        ("who student left", False)
    ]
    
    print("Validating test sentences:")
    for sentence, expected in test_sentences:
        is_valid = model.validate_syntax(sentence)
        symbol = "✓" if is_valid else "✗"
        status = "PASS" if is_valid == expected else "FAIL"
        print(f"  {symbol} '{sentence}' - {status}")

def demo_beam_search_completion():
    """Demonstrate beam search for sentence completion."""
    separator("Beam Search Sentence Completion")
    
    model = HybridLanguageModel()
    
    prefixes = [
        "the student",
        "the teacher who",
        "a book"
    ]
    
    for prefix in prefixes:
        print(f"\nCompleting: '{prefix}'")
        completions = model.get_valid_continuations(prefix, beam_size=5)
        
        for i, completion in enumerate(completions[:5], 1):
            print(f"  {i}. {completion}")

def demo_model_comparison():
    """Compare pure probabilistic vs hybrid model."""
    separator("Model Comparison: Pure vs Hybrid")
    
    pure_model = ProbGrammar()
    hybrid_model = HybridLanguageModel()
    
    prefix = "the student who"
    
    # Pure probabilistic predictions
    print(f"Predictions for '{prefix}':\n")
    print("Pure Probabilistic Model:")
    pure_preds = pure_model.predict_next(prefix, k=3000)
    for token, prob in pure_preds[:5]:
        print(f"  {token:10} {prob:.3f}")
    
    # Hybrid model predictions (with validation)
    print("\nHybrid Model (with validation):")
    hybrid_preds = hybrid_model.predict_next(prefix, k=3000, validate=True)
    for token, prob in hybrid_preds[:5]:
        print(f"  {token:10} {prob:.3f}")
    
    print("\n✅ Hybrid model ensures all predictions are grammatical")

def demo_linguistic_phenomena():
    """Demonstrate specific linguistic phenomena."""
    separator("Linguistic Phenomena")
    
    model = ProbGrammar()
    
    print("1. Subject-Verb Agreement:")
    print("   (Model generates matching singular/plural forms)\n")
    
    # Generate sentences and check patterns
    agreement_examples = []
    for _ in range(50):
        s = model.sample_sentence()
        if "student" in s and ("left" in s or "smiled" in s):
            agreement_examples.append(s)
        if len(agreement_examples) >= 3:
            break
    
    for ex in agreement_examples:
        print(f"   - {ex}")
    
    print("\n2. Center Embedding:")
    print("   (Recursive structures with 'who' and 'that')\n")
    
    # Find center-embedded examples
    embedded = []
    for _ in range(100):
        s = model.sample_sentence()
        if s.count("who") + s.count("that") >= 1:
            embedded.append(s)
        if len(embedded) >= 3:
            break
    
    for ex in embedded:
        print(f"   - {ex}")

def demo_performance_metrics():
    """Show performance metrics and model size."""
    separator("Performance Metrics")
    
    import time
    model = ProbGrammar()
    
    # Generation speed
    start = time.time()
    sentences = [model.sample_sentence() for _ in range(1000)]
    gen_time = time.time() - start
    
    print(f"Generation Performance:")
    print(f"  - 1000 sentences in {gen_time:.2f}s")
    print(f"  - {1000/gen_time:.0f} sentences/second")
    
    # Prediction speed
    start = time.time()
    predictions = model.predict_next("the student", k=1000)
    pred_time = time.time() - start
    
    print(f"\nPrediction Performance:")
    print(f"  - 1000 samples in {pred_time:.2f}s")
    print(f"  - Found {len(predictions)} unique continuations")
    
    # Model size
    import os
    script_size = os.path.getsize(os.path.join(os.path.dirname(__file__), '..', 'python', 'tiny_lm.py'))
    
    print(f"\nModel Size:")
    print(f"  - Core implementation: {script_size/1024:.1f} KB")
    print(f"  - No external dependencies")
    print(f"  - Total with Flask API: <100 KB")

def interactive_demo():
    """Interactive demonstration mode."""
    separator("Interactive Language Model Demo")
    
    model = HybridLanguageModel()
    
    print("\nCommands:")
    print("  predict <prefix>  - Get next token predictions")
    print("  generate         - Generate a random sentence")
    print("  complete <prefix> - Get sentence completions")
    print("  validate <sentence> - Check if sentence is grammatical")
    print("  quit             - Exit demo")
    
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if cmd == "quit":
                break
            elif cmd == "generate":
                sentence = model.generate_sentence()
                print(f"Generated: {sentence}")
            elif cmd.startswith("predict "):
                prefix = cmd[8:]
                predictions = model.predict_next(prefix, k=1000)
                print(f"Predictions for '{prefix}':")
                for token, prob in predictions[:5]:
                    print(f"  {token:10} {prob:.3f}")
            elif cmd.startswith("complete "):
                prefix = cmd[9:]
                completions = model.get_valid_continuations(prefix, beam_size=3)
                print(f"Completions for '{prefix}':")
                for comp in completions:
                    print(f"  - {comp}")
            elif cmd.startswith("validate "):
                sentence = cmd[9:]
                valid = model.validate_syntax(sentence)
                print(f"'{sentence}' is {'valid' if valid else 'invalid'}")
            else:
                print("Unknown command. Try 'predict', 'generate', 'complete', 'validate', or 'quit'")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Run all demonstrations."""
    print("🤖 Atomic Language Model - Comprehensive Demo")
    print("=" * 60)
    print("\nThis demo showcases a probabilistic language model that:")
    print("  • Generates only grammatical sentences")
    print("  • Provides next-token predictions")
    print("  • Supports recursive structures")
    print("  • Fits in <100KB with zero dependencies")
    
    # Run demos
    demo_basic_generation()
    demo_next_token_prediction()
    demo_recursive_capability()
    demo_hybrid_validation()
    demo_beam_search_completion()
    demo_model_comparison()
    demo_linguistic_phenomena()
    demo_performance_metrics()
    
    # Optional interactive mode
    print("\n" + "="*60)
    response = input("\nRun interactive demo? (y/n): ").strip().lower()
    if response == 'y':
        interactive_demo()
    
    print("\n✅ Demo complete! The model combines:")
    print("   - Mathematical rigor (proven non-regular)")
    print("   - Practical utility (next-token prediction)")
    print("   - Minimal footprint (<100KB)")
    print("   - Formal guarantees (validated syntax)")

if __name__ == "__main__":
    main()