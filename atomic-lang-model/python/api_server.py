#!/usr/bin/env python3
"""
Atomic Language Model API Server
================================

Ultra-lightweight Flask API for the probabilistic language model.
Provides RESTful endpoints for next-token prediction, sentence generation,
and syntax validation.

Features:
- <100kB when zipped with standard Python runtime
- JSON API with comprehensive responses
- Built-in CORS support for web applications
- Health checks and model information endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import time
from typing import Dict, Any, List
from hybrid_model import HybridLanguageModel
from tiny_lm import ProbGrammar

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web applications

# Initialize models
prob_model = ProbGrammar()
hybrid_model = HybridLanguageModel()

# Model metadata
MODEL_INFO = {
    "name": "Atomic Language Model",
    "version": "1.0.0",
    "type": "hybrid_probabilistic_cfg",
    "size": "<100kB",
    "guarantees": {
        "grammaticality": True,
        "recursion": True,
        "formal_verification": True,
        "non_regularity": True
    },
    "capabilities": [
        "next_token_prediction",
        "sentence_generation",
        "syntax_validation",
        "recursive_parsing"
    ],
    "endpoints": {
        "/": "Model information",
        "/health": "Health check",
        "/predict": "Next token prediction",
        "/generate": "Sentence generation",
        "/validate": "Syntax validation",
        "/complete": "Text completion"
    }
}

@app.route('/')
def info():
    """Return model information."""
    return jsonify(MODEL_INFO)

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "model_loaded": True
    })

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    """
    Predict next token probabilities.
    
    GET: /predict?prefix=the+student
    POST: {"prefix": "the student", "k": 3000, "validate": true}
    """
    if request.method == 'GET':
        prefix = request.args.get('prefix', '')
        k = int(request.args.get('k', 1000))
        validate = request.args.get('validate', 'true').lower() == 'true'
    else:
        data = request.get_json()
        prefix = data.get('prefix', '')
        k = data.get('k', 1000)
        validate = data.get('validate', True)
    
    # Get predictions
    start_time = time.time()
    predictions = hybrid_model.predict_next(prefix, k=k, validate=validate)
    inference_time = time.time() - start_time
    
    # Format response
    return jsonify({
        "prefix": prefix,
        "predictions": [
            {"token": token, "probability": prob}
            for token, prob in predictions[:10]  # Top 10
        ],
        "total_predictions": len(predictions),
        "inference_time_ms": round(inference_time * 1000, 2),
        "validated": validate,
        "model_type": "hybrid_probabilistic_cfg"
    })

@app.route('/generate', methods=['POST', 'GET'])
def generate():
    """
    Generate grammatically valid sentences.
    
    GET: /generate?count=5
    POST: {"count": 5, "max_length": 20}
    """
    if request.method == 'GET':
        count = int(request.args.get('count', 1))
        max_length = int(request.args.get('max_length', 20))
    else:
        data = request.get_json()
        count = data.get('count', 1)
        max_length = data.get('max_length', 20)
    
    # Generate sentences
    sentences = []
    start_time = time.time()
    
    for _ in range(count):
        sentence = hybrid_model.generate_sentence()
        if sentence and len(sentence.split()) <= max_length:
            sentences.append(sentence)
    
    generation_time = time.time() - start_time
    
    return jsonify({
        "sentences": sentences,
        "count": len(sentences),
        "generation_time_ms": round(generation_time * 1000, 2),
        "guaranteed_grammatical": True,
        "model_type": "hybrid_probabilistic_cfg"
    })

@app.route('/validate', methods=['POST'])
def validate():
    """
    Validate syntactic correctness of sentences.
    
    POST: {"sentences": ["the student left", "student the left"]}
    """
    data = request.get_json()
    sentences = data.get('sentences', [])
    
    if isinstance(sentences, str):
        sentences = [sentences]
    
    # Validate each sentence
    results = []
    start_time = time.time()
    
    for sentence in sentences:
        is_valid = hybrid_model.validate_syntax(sentence)
        results.append({
            "sentence": sentence,
            "valid": is_valid,
            "tokens": len(sentence.split())
        })
    
    validation_time = time.time() - start_time
    
    return jsonify({
        "results": results,
        "validation_time_ms": round(validation_time * 1000, 2),
        "validator": "rust_atomic_language_model"
    })

@app.route('/complete', methods=['POST'])
def complete():
    """
    Complete a sentence prefix with beam search.
    
    POST: {"prefix": "the student who", "beam_size": 5}
    """
    data = request.get_json()
    prefix = data.get('prefix', '')
    beam_size = data.get('beam_size', 5)
    
    # Get completions
    start_time = time.time()
    completions = hybrid_model.get_valid_continuations(prefix, beam_size=beam_size)
    completion_time = time.time() - start_time
    
    # Also get token probabilities
    predictions = hybrid_model.predict_next(prefix, k=1000, validate=True)
    
    return jsonify({
        "prefix": prefix,
        "completions": completions,
        "next_tokens": [
            {"token": token, "probability": prob}
            for token, prob in predictions[:5]
        ],
        "beam_size": beam_size,
        "completion_time_ms": round(completion_time * 1000, 2),
        "guaranteed_grammatical": True
    })

@app.route('/grammar', methods=['GET'])
def grammar():
    """Return the probabilistic grammar rules."""
    return jsonify({
        "grammar": prob_model.rules,
        "type": "weighted_cfg",
        "normalized": True,
        "recursive": True
    })

@app.route('/benchmark', methods=['POST'])
def benchmark():
    """
    Run benchmarks on provided sentences.
    
    POST: {"sentences": ["the student left", ...]}
    """
    data = request.get_json()
    sentences = data.get('sentences', [])
    
    if not sentences:
        return jsonify({"error": "No sentences provided"}), 400
    
    # Calculate perplexity
    start_time = time.time()
    perplexity = hybrid_model.evaluate_perplexity(sentences)
    benchmark_time = time.time() - start_time
    
    # Additional metrics
    total_tokens = sum(len(s.split()) for s in sentences)
    
    return jsonify({
        "perplexity": round(perplexity, 2),
        "sentences_evaluated": len(sentences),
        "total_tokens": total_tokens,
        "benchmark_time_ms": round(benchmark_time * 1000, 2),
        "model_type": "hybrid_probabilistic_cfg"
    })

# Error handlers
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request", "message": str(e)}), 400

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Development server
if __name__ == '__main__':
    print("🚀 Atomic Language Model API Server")
    print("=" * 50)
    print("Endpoints:")
    for endpoint, desc in MODEL_INFO["endpoints"].items():
        print(f"  {endpoint:20} - {desc}")
    print("\nStarting server on http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)