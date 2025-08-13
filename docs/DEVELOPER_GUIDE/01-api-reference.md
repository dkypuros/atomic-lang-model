# 📋 API Reference

Complete API documentation for the Atomic Language Model, covering both the Rust core library and Python REST API.

## 🦀 Rust Core Library API

The Rust implementation provides the core grammar operations and parsing functionality. Generate full documentation with:

```bash
cd atomic-lang-model
cargo doc --no-deps --open
```

### Core Types

#### `SyntacticObject`
The fundamental data structure representing linguistic constituents.

```rust
pub struct SyntacticObject {
    pub label: Category,        // Syntactic category (N, V, D, etc.)
    pub features: Vec<Feature>, // Grammatical features
    pub children: Vec<SyntacticObject>, // Sub-constituents
}
```

**Methods:**
- `new(phon: &str, feats: &[Feature]) -> Self` - Create from phonetic string and features
- `from_lex(item: &LexItem) -> Self` - Create from lexical item
- `internal(label: Category, features: Vec<Feature>, children: Vec<SyntacticObject>) -> Self` - Create internal node
- `is_complete() -> bool` - Check if all features are satisfied
- `linearize() -> String` - Convert to surface string

#### `Workspace`
Memory-bounded storage for derivation process.

```rust
pub struct Workspace {
    pub objects: Vec<SyntacticObject>,
    memory_limit: usize,
}
```

**Methods:**
- `new(memory_limit: usize) -> Self` - Create with memory limit
- `add_lex(item: &LexItem)` - Add lexical item to workspace
- `is_successful() -> bool` - Check if derivation succeeded
- `memory_usage() -> usize` - Current memory usage

### Grammar Operations

#### `merge`
**Function**: `pub fn merge(a: SyntacticObject, b: SyntacticObject) -> Result<SyntacticObject, DerivationError>`

Core binary operation that combines two syntactic objects.

**Parameters:**
- `a: SyntacticObject` - First object (typically has selector feature)
- `b: SyntacticObject` - Second object (typically satisfies selector)

**Returns:**
- `Ok(SyntacticObject)` - Successfully merged object
- `Err(DerivationError)` - Incompatible features or other error

**Example:**
```rust
let verb = SyntacticObject::new("left", &[Feature::Cat(Category::V), Feature::Sel(Category::D)]);
let noun = SyntacticObject::new("student", &[Feature::Cat(Category::D)]);
let vp = merge(verb, noun)?;  // Creates VP "left student"
```

#### `move_operation`
**Function**: `pub fn move_operation(obj: SyntacticObject) -> Result<SyntacticObject, DerivationError>`

Unary operation handling syntactic displacement (wh-movement, topicalization, etc.).

**Parameters:**
- `obj: SyntacticObject` - Object with +f/-f feature pair

**Returns:**
- `Ok(SyntacticObject)` - Object with -f constituent moved
- `Err(DerivationError)` - No matching features or other error

### Derivation Functions

#### `derive`
**Function**: `pub fn derive(workspace: &mut Workspace, max_steps: usize) -> Result<SyntacticObject, DerivationError>`

Complete derivation process from lexical items to complete sentence.

**Parameters:**
- `workspace: &mut Workspace` - Workspace containing lexical items
- `max_steps: usize` - Maximum derivation steps (prevents infinite loops)

**Returns:**
- `Ok(SyntacticObject)` - Successfully derived sentence
- `Err(DerivationError)` - Derivation failed

#### `step`
**Function**: `pub fn step(workspace: &mut Workspace) -> Result<(), DerivationError>`

Perform single derivation step (one merge or move operation).

### Utility Functions

#### `generate_an_bn`
**Function**: `pub fn generate_an_bn(n: usize) -> String`

Generate aⁿbⁿ pattern for mathematical verification.

**Parameters:**
- `n: usize` - Number of a's and b's

**Returns:**
- `String` - Pattern like "aaa bbb" for n=3

#### `can_merge`
**Function**: `pub fn can_merge(a: &SyntacticObject, b: &SyntacticObject) -> bool`

Check if two objects are compatible for merging.

---

## 🐍 Python REST API

The Python API server provides HTTP endpoints for language model functionality. Start the server:

```bash
cd atomic-lang-model/python
python api_server.py
```

**Base URL:** `http://localhost:5000`

### Model Information

#### `GET /`
Get model information and available endpoints.

**Response:**
```json
{
  "name": "Atomic Language Model",
  "version": "1.0.0",
  "type": "hybrid_probabilistic_cfg",
  "size": "<100kB",
  "guarantees": {
    "grammaticality": true,
    "recursion": true,
    "formal_verification": true,
    "non_regularity": true
  }
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1672531200.123,
  "model_loaded": true
}
```

### Core Functionality

#### `POST /predict`
Predict next token probabilities for a given prefix.

**Request Body:**
```json
{
  "prefix": "the student who",
  "k": 3000,           // Optional: Monte Carlo samples (default: 1000)
  "validate": true     // Optional: Rust grammar validation (default: true)
}
```

**GET Alternative:**
```
GET /predict?prefix=the+student&k=3000&validate=true
```

**Response:**
```json
{
  "prefix": "the student who",
  "predictions": [
    {"token": "left", "probability": 0.245},
    {"token": "smiled", "probability": 0.198},
    {"token": "arrived", "probability": 0.134}
  ],
  "total_predictions": 12,
  "inference_time_ms": 45.7,
  "validated": true,
  "model_type": "hybrid_probabilistic_cfg"
}
```

#### `POST /generate`
Generate grammatically valid sentences.

**Request Body:**
```json
{
  "count": 5,          // Number of sentences to generate
  "max_length": 20     // Optional: Maximum sentence length
}
```

**GET Alternative:**
```
GET /generate?count=5&max_length=20
```

**Response:**
```json
{
  "sentences": [
    "the student left",
    "every teacher smiled",
    "the book that Mary read surprised everyone"
  ],
  "count": 3,
  "generation_time_ms": 123.4,
  "guaranteed_grammatical": true,
  "model_type": "hybrid_probabilistic_cfg"
}
```

#### `POST /validate`
Validate syntactic correctness of sentences.

**Request Body:**
```json
{
  "sentences": [
    "the student left",
    "student the left",
    "the student who Mary likes left"
  ]
}
```

**Response:**
```json
{
  "results": [
    {"sentence": "the student left", "valid": true, "tokens": 3},
    {"sentence": "student the left", "valid": false, "tokens": 3},
    {"sentence": "the student who Mary likes left", "valid": true, "tokens": 6}
  ],
  "validation_time_ms": 12.3,
  "validator": "rust_atomic_language_model"
}
```

#### `POST /complete`
Complete a sentence prefix with beam search.

**Request Body:**
```json
{
  "prefix": "the student who",
  "beam_size": 5       // Optional: Number of completions (default: 5)
}
```

**Response:**
```json
{
  "prefix": "the student who",
  "completions": [
    "the student who left arrived",
    "the student who smiled departed",
    "the student who Mary likes left"
  ],
  "next_tokens": [
    {"token": "left", "probability": 0.245},
    {"token": "smiled", "probability": 0.198}
  ],
  "beam_size": 5,
  "completion_time_ms": 67.8,
  "guaranteed_grammatical": true
}
```

### Grammar and Analysis

#### `GET /grammar`
Return the probabilistic grammar rules.

**Response:**
```json
{
  "grammar": {
    "S -> NP VP": 0.8,
    "NP -> D N": 0.6,
    "VP -> V": 0.3,
    "VP -> V NP": 0.7
  },
  "type": "weighted_cfg",
  "normalized": true,
  "recursive": true
}
```

#### `POST /benchmark`
Run benchmark evaluation on provided sentences.

**Request Body:**
```json
{
  "sentences": [
    "the student left",
    "every teacher who arrived smiled",
    "the book that Mary read surprised everyone"
  ]
}
```

**Response:**
```json
{
  "perplexity": 23.45,
  "sentences_evaluated": 3,
  "total_tokens": 14,
  "benchmark_time_ms": 89.2,
  "model_type": "hybrid_probabilistic_cfg"
}
```

### Error Responses

All endpoints return appropriate HTTP status codes and error messages:

**400 Bad Request:**
```json
{
  "error": "Bad request",
  "message": "Invalid parameter format"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error", 
  "message": "Derivation failed"
}
```

## 🔗 Integration Examples

### Using with curl

```bash
# Predict next tokens
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"prefix": "the student", "k": 5000}'

# Generate sentences
curl http://localhost:5000/generate?count=3

# Validate grammar
curl -X POST http://localhost:5000/validate \
  -H "Content-Type: application/json" \
  -d '{"sentences": ["the student left", "left student the"]}'
```

### Using with JavaScript

```javascript
// Predict next tokens
const response = await fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    prefix: "the student who",
    k: 3000,
    validate: true
  })
});
const predictions = await response.json();
```

### Using with Python

```python
import requests

# Generate sentences
response = requests.post('http://localhost:5000/generate', 
  json={'count': 5, 'max_length': 15})
sentences = response.json()['sentences']

# Validate syntax
response = requests.post('http://localhost:5000/validate',
  json={'sentences': ['the student left', 'student the left']})
results = response.json()['results']
```

## 🚀 Performance Notes

- **Rust Core**: O(n³) parsing complexity, <256kB memory usage
- **Python API**: <100ms response times for typical queries
- **Memory**: API server uses <50MB RAM total
- **Concurrency**: Flask development server supports multiple concurrent requests

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

---

## 📚 Related Documentation

- **[Mathematical Foundations](../THEORY/01-mathematical-foundations.md)** - Understand the theory behind the API
- **[User Guide](../USER_GUIDE/01-installation.md)** - Setup and basic usage
- **[Examples](../USER_GUIDE/03-examples.md)** - Practical tutorials and recipes