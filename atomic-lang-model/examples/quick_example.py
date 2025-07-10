#!/usr/bin/env python3
"""
Quick Example: Atomic Language Model
====================================

A simple example showing the core capabilities in just a few lines.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

from tiny_lm import ProbGrammar

# Create model
model = ProbGrammar()

# Generate sentences
print("🤖 Generating grammatical sentences:")
for i in range(5):
    sentence = model.sample_sentence()
    print(f"{i+1}. {sentence}")

# Predict next tokens
print("\n🔮 Next token predictions for 'the student':")
predictions = model.predict_next("the student", k=3000)
for token, prob in predictions[:5]:
    print(f"  '{token}': {prob:.3f}")

print("\n✅ Ultra-lightweight language model with formal guarantees!")