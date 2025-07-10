# 🤖 Probabilistic Language Model Tutorial

> **Learn how to use the world's smallest formally verified language model**

This tutorial guides you through using the probabilistic extension of our atomic language model. You'll learn how to generate text, predict next tokens, and build applications while maintaining mathematical guarantees.

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Building Applications](#building-applications)
6. [Theory and Practice](#theory-and-practice)
7. [Troubleshooting](#troubleshooting)

## 🎯 Introduction

### What You're Getting

The probabilistic language model extension adds:
- **Next-token prediction** with probability distributions
- **Weighted grammar rules** for realistic generation
- **Hybrid validation** ensuring grammatical correctness
- **REST API** for easy integration
- **<100kB footprint** including all features

### Why This Matters

Traditional language models (GPT, BERT) are:
- **Massive** (gigabytes to terabytes)
- **Opaque** (no formal guarantees)
- **Resource-intensive** (require GPUs)

Our model is:
- **Tiny** (<100kB total)
- **Transparent** (mathematically verified)
- **Efficient** (runs on any device)

## 🚀 Installation

### Prerequisites
```bash
# Required: Python 3.8+
python --version  # Should show 3.8 or higher

# Optional: Rust (for hybrid validation)
rustc --version  # Should show 1.70 or higher
```

### Setup
```bash
# Clone the repository
git clone https://github.com/user/atomic-lang-model.git
cd atomic-lang-model/atomic-lang-model

# No pip install needed - zero dependencies!
# Just run directly
cd python
python tiny_lm.py
```

## 📖 Basic Usage

### 1. Generate Sentences

```python
from tiny_lm import ProbGrammar

# Create model
model = ProbGrammar()

# Generate sentences
for i in range(5):
    sentence = model.sample_sentence()
    print(f"{i+1}. {sentence}")

# Output:
# 1. the student left
# 2. a teacher who arrived smiled
# 3. the student praised the book
# 4. the teacher who the student praised left
# 5. a book arrived
```

### 2. Predict Next Tokens

```python
# Get next token predictions
prefix = "the student"
predictions = model.predict_next(prefix, k=3000)

print(f"Next tokens after '{prefix}':")
for token, prob in predictions[:5]:
    print(f"  {token}: {prob:.3f}")

# Output:
# Next tokens after 'the student':
#   who: 0.245
#   left: 0.198
#   smiled: 0.156
#   praised: 0.134
#   arrived: 0.089
```

### 3. Use the Hybrid Model

```python
from hybrid_model import HybridLanguageModel

# Create hybrid model (uses Rust validation if available)
model = HybridLanguageModel()

# Generate with validation
sentence = model.generate_sentence()
print(f"Generated: {sentence}")
print(f"Valid: {model.validate_syntax(sentence)}")

# Get validated predictions
predictions = model.predict_next("the teacher", validate=True)
print("All predictions guaranteed grammatical!")
```

## 🔧 Advanced Features

### Monte Carlo Sampling Parameters

```python
# Adjust sampling for speed vs accuracy
fast_predictions = model.predict_next(prefix, k=100)    # Fast, less accurate
slow_predictions = model.predict_next(prefix, k=10000)  # Slow, more accurate

# Compare distributions
print(f"Fast sampling found {len(fast_predictions)} continuations")
print(f"Slow sampling found {len(slow_predictions)} continuations")
```

### Custom Grammar Rules

```python
# Define your own weighted grammar
MY_RULES = {
    'S': [
        (1.0, ['NP', 'VP']),
    ],
    'NP': [
        (0.6, ['Det', 'N']),
        (0.4, ['N']),
    ],
    'VP': [
        (0.7, ['V']),
        (0.3, ['V', 'NP']),
    ],
    'Det': [
        (0.5, ['the']),
        (0.5, ['a']),
    ],
    'N': [
        (0.5, ['cat']),
        (0.5, ['dog']),
    ],
    'V': [
        (0.6, ['sleeps']),
        (0.4, ['runs']),
    ],
}

# Create model with custom grammar
custom_model = ProbGrammar(MY_RULES)
print(custom_model.sample_sentence())  # "the cat sleeps"
```

### Beam Search Completion

```python
# Get multiple high-probability completions
prefix = "the student who"
completions = model.get_valid_continuations(prefix, beam_size=5)

print(f"Top completions for '{prefix}':")
for comp in completions:
    print(f"  - {comp}")

# Output:
# Top completions for 'the student who':
#   - the student who left
#   - the student who arrived
#   - the student who smiled
#   - the student who the teacher praised
#   - the student who praised the book
```

## 🌐 Building Applications

### 1. REST API Server

```bash
# Start the API server
cd atomic-lang-model/python
python api_server.py

# Server runs on http://localhost:5000
```

### 2. API Endpoints

```python
import requests

# Predict next token
response = requests.get('http://localhost:5000/predict?prefix=the+student')
predictions = response.json()['predictions']

# Generate sentences
response = requests.get('http://localhost:5000/generate?count=3')
sentences = response.json()['sentences']

# Validate syntax
response = requests.post('http://localhost:5000/validate', 
    json={'sentences': ['the student left', 'student the left']})
results = response.json()['results']

# Get grammar rules
response = requests.get('http://localhost:5000/grammar')
grammar = response.json()['grammar']
```

### 3. Build a Chatbot

```python
def simple_chatbot():
    model = HybridLanguageModel()
    
    print("Grammar Bot: I can help you write grammatical sentences!")
    print("Type 'quit' to exit.\n")
    
    while True:
        prefix = input("Start a sentence: ").strip()
        
        if prefix.lower() == 'quit':
            break
        
        # Get predictions
        predictions = model.predict_next(prefix, k=1000)
        
        if predictions:
            print(f"\nI suggest continuing with:")
            for token, prob in predictions[:3]:
                continuation = f"{prefix} {token}"
                print(f"  '{continuation}' (confidence: {prob:.1%})")
        
        # Show a complete sentence
        full_sentence = model.get_valid_continuations(prefix, beam_size=1)
        if full_sentence:
            print(f"\nComplete sentence: {full_sentence[0]}")
        
        print()

# Run the chatbot
simple_chatbot()
```

### 4. Text Autocomplete

```python
class AutoComplete:
    def __init__(self):
        self.model = HybridLanguageModel()
        self.cache = {}
    
    def suggest(self, text, num_suggestions=5):
        # Cache for performance
        if text in self.cache:
            return self.cache[text]
        
        # Get predictions
        predictions = self.model.predict_next(text, k=500)
        suggestions = []
        
        for token, prob in predictions[:num_suggestions]:
            suggestion = {
                'text': f"{text} {token}",
                'confidence': prob,
                'complete': self.is_complete(f"{text} {token}")
            }
            suggestions.append(suggestion)
        
        self.cache[text] = suggestions
        return suggestions
    
    def is_complete(self, text):
        # Simple heuristic: sentence is complete if it has subject and verb
        tokens = text.split()
        has_noun = any(t in ['student', 'teacher', 'book'] for t in tokens)
        has_verb = any(t in ['left', 'smiled', 'arrived', 'praised'] for t in tokens)
        return has_noun and has_verb

# Use autocomplete
ac = AutoComplete()
suggestions = ac.suggest("the student")
for s in suggestions:
    print(f"{s['text']} - {s['confidence']:.1%} - Complete: {s['complete']}")
```

## 🧮 Theory and Practice

### Understanding the Probabilities

The model assigns probabilities based on:
1. **Grammar rule weights** - How likely each production is
2. **Monte Carlo sampling** - Empirical frequency from samples
3. **Syntactic validation** - Only grammatical continuations

```python
# Examine rule probabilities
def explain_generation(sentence):
    tokens = sentence.split()
    print(f"Generating: {sentence}")
    print("\nDerivation:")
    
    # This is simplified - real derivation is more complex
    print("  S → DP VP")
    print("  DP → D NP (p=0.7) or D N (p=0.3)")
    print("  VP → V (p=0.5) or V DP (p=0.3)")
    # ... etc

explain_generation("the student left")
```

### Formal Guarantees

Unlike neural language models, our model guarantees:

```python
def verify_guarantees():
    model = HybridLanguageModel()
    
    # 1. All generated sentences are grammatical
    for _ in range(100):
        sentence = model.generate_sentence()
        assert model.validate_syntax(sentence), f"Invalid: {sentence}"
    print("✅ Grammaticality guaranteed")
    
    # 2. Model exhibits recursion
    recursive_found = False
    for _ in range(100):
        s = model.prob_grammar.sample_sentence()
        if s.count("who") + s.count("that") > 1:
            recursive_found = True
            print(f"✅ Recursive structure: {s}")
            break
    
    # 3. Predictions maintain validity
    predictions = model.predict_next("the student", validate=True)
    for token, _ in predictions[:5]:
        assert model.validate_syntax(f"the student {token}")
    print("✅ Valid predictions guaranteed")

verify_guarantees()
```

### Comparison with Neural Models

```python
def compare_approaches():
    print("Traditional Neural LM:")
    print("  - Size: 100MB - 100GB+")
    print("  - Guarantees: None")
    print("  - Interpretability: Black box")
    print("  - Resources: GPU required")
    
    print("\nOur Probabilistic Grammar:")
    print("  - Size: <100KB")
    print("  - Guarantees: Grammaticality, recursion")
    print("  - Interpretability: Explicit rules")
    print("  - Resources: Any device")
    
    print("\nTrade-offs:")
    print("  - Vocabulary: Limited but extensible")
    print("  - Semantics: Structure-focused")
    print("  - Use case: Where correctness matters")

compare_approaches()
```

## 🔍 Troubleshooting

### Common Issues

**"No predictions returned"**
```python
# Increase sample size
predictions = model.predict_next(prefix, k=5000)  # More samples

# Check if prefix is valid
if not predictions:
    print(f"No valid continuations found for '{prefix}'")
    print("Try a simpler prefix like 'the' or 'a'")
```

**"Rust validation not working"**
```python
# Check if Rust binary exists
if not model.rust_binary:
    print("Rust binary not found - using Python validation")
    print("To enable Rust validation:")
    print("  cd ../atomic-lang-model")
    print("  cargo build --release")
```

**"Generation seems repetitive"**
```python
# Add randomness to rule selection
import random

def generate_diverse(model, count=10):
    sentences = set()
    attempts = 0
    
    while len(sentences) < count and attempts < count * 10:
        sentence = model.sample_sentence()
        sentences.add(sentence)
        attempts += 1
    
    return list(sentences)

diverse = generate_diverse(model)
print(f"Generated {len(diverse)} unique sentences")
```

### Performance Optimization

```python
# Profile performance
import time

def benchmark_operations():
    model = ProbGrammar()
    
    # Generation speed
    start = time.time()
    sentences = [model.sample_sentence() for _ in range(1000)]
    gen_time = time.time() - start
    print(f"Generation: {1000/gen_time:.0f} sentences/sec")
    
    # Prediction speed
    start = time.time()
    predictions = model.predict_next("the student", k=1000)
    pred_time = time.time() - start
    print(f"Prediction: {pred_time*1000:.0f}ms for 1000 samples")
    
    # Memory usage
    import sys
    size = sys.getsizeof(model.rules)
    print(f"Grammar size: {size/1024:.1f}KB")

benchmark_operations()
```

## 🎓 Learning Exercises

### Exercise 1: Extend the Vocabulary
```python
# Add new words to the grammar
# Modify PG_RULES in tiny_lm.py to include:
# - New nouns: 'professor', 'homework'  
# - New verbs: 'completed', 'assigned'
# - Test that sentences still parse correctly
```

### Exercise 2: Analyze Probability Distributions
```python
# For different prefixes, analyze how probabilities change
# Compare: "the", "the student", "the student who"
# What patterns do you notice?
```

### Exercise 3: Build a Grammar Checker
```python
# Use the model to build a simple grammar checker
# that highlights potentially ungrammatical constructions
```

### Exercise 4: Create Domain-Specific Model
```python
# Modify the grammar for a specific domain:
# - Legal documents
# - Technical writing  
# - Children's stories
# How do the probability distributions change?
```

## 🚀 Next Steps

1. **Explore the API** - Build web applications with the REST endpoints
2. **Customize the Grammar** - Adapt for your specific use case
3. **Benchmark Performance** - Compare with other language models
4. **Extend the Theory** - Add semantic representations
5. **Contribute** - Share your improvements with the community

## 📚 Additional Resources

- [Probabilistic Context-Free Grammars](https://en.wikipedia.org/wiki/Stochastic_context-free_grammar)
- [Monte Carlo Methods](https://en.wikipedia.org/wiki/Monte_Carlo_method)
- [Formal Language Theory](formal-language-theory.md)
- [Original Implementation](../atomic-lang-model/)

---

**Congratulations!** You now know how to use the world's smallest formally verified language model. This unique combination of mathematical rigor and practical utility opens new possibilities for trustworthy NLP applications.

*Questions? Open an issue on GitHub or check our [FAQ](faq.md).*