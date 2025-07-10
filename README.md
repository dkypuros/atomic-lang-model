# 🧬 Atomic Language Model

> **Extremely lightweight universal grammar implementation with provable recursion**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Rust](https://img.shields.io/badge/rust-%23000000.svg?style=flat&logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![Size](https://img.shields.io/badge/binary-<50kB-green)](./atomic-lang-model/REPORT.md)

A mathematically rigorous, recursively complete language model that fits in under 50kB with zero runtime dependencies. Built on Chomsky's Minimalist Grammar theory with formal verification and empirical validation.

### 📊 Mind-Blowing Size Comparison:
- **Our Model**: 0.05 MB (50 KB)
- **GPT-3**: 700,000 MB
- **Ratio**: We're **14,000,000x smaller**!

Yet we still provide provable recursion, next-token prediction, and formal verification. [See how we did it →](./docs/walkthrough.md)

## ✨ What Makes This Special

🧮 **Mathematically Proven**: Formal proofs of recursive capability using Coq  
⚡ **Ultra-Lightweight**: Complete implementation under 50kB binary  
🔬 **Scientifically Validated**: Tested with standard linguistic benchmark suites  
🏗️ **Universal Grammar**: Based on Chomsky's Minimalist Grammar theory  
♾️ **Provably Recursive**: Generates a^n b^n patterns, proving non-regularity  
🤖 **Probabilistic Language Model**: Next-token prediction with formal guarantees  

## 🚀 Quick Start

### Prerequisites
- Rust 1.70+ (for compilation)
- Git (for cloning)
- Python 3.8+ (optional, for probabilistic language model)

### 30-Second Demo
```bash
# Clone the repository
git clone https://github.com/user/atomic-lang-model.git
cd atomic-lang-model/atomic-lang-model

# Run the demo (shows recursive generation + parsing)
cargo run --release

# Run mathematical proof tests
cargo test --release test_complete_recursive_proof

# Run full benchmark suite
cargo test --release --features bench

# NEW: Try the probabilistic language model
cd ../python && python tiny_lm.py
```

### What You'll See
```
🧬 Atomic Language Model - Recursive Grammar Demo
============================================================

📐 Mathematical Proof: aⁿbⁿ Generation
----------------------------------------
n=0: ε (empty)
n=1: a b  
n=2: a a b b
n=3: a a a b b b
n=4: a a a a b b b b
n=5: a a a a a b b b b b

🔍 Parsing Test: Recursive Structures
----------------------------------------
✅ 'the student left' → the student left
   Category: S, Complete: true

♾️  Unbounded Recursion Demonstration
----------------------------------------
✅ Can generate a^6b^6 (length: 12)
✅ Can generate a^7b^7 (length: 14)  
✅ Can generate a^8b^8 (length: 16)

🎯 Theoretical Capacity: INFINITE
🔬 Practical Limit: Memory bounded
```

## 📚 Learning Path

### 1. 🎯 Start Here: Understanding Recursion
**Read First**: [Recursive Language Overview](./docs/recursive-language-overview.md)
- What is recursion in language?
- Why does it matter?
- How does this implementation work?

### 2. 🧮 The Mathematical Foundation  
**Next**: [Chomsky's Mathematical Proofs](./docs/chomsky-mathematical-proofs.md)
- The 1956 proof that changed linguistics
- How finite-state grammars fail
- Why recursion is mathematically necessary

### 3. ⚙️ Technical Deep Dive
**Then**: [Formal Language Theory](./docs/formal-language-theory.md)
- Grammar hierarchies and automata
- Minimalist Grammar operations
- Complexity theory and parsing

### 4. 💻 Implementation Details
**Implementation**: [Atomic Language Model](./atomic-lang-model/)
- [Formal Specification](./atomic-lang-model/spec.md)
- [Rust Implementation](./atomic-lang-model/src/lib.rs)
- [Mathematical Tests](./atomic-lang-model/tests/recursion.rs)
- [Performance Report](./atomic-lang-model/REPORT.md)

### 5. 🧪 Testing and Validation
**Validation**: [NLP Verification Methods](./docs/nlp-verification-methods.md)
- Agreement test suites
- Colorless green tests  
- Performance benchmarking

### 6. ✅ Formal Verification
**Advanced**: [Machine Verification](./docs/machine-verification.md)
- Coq proof development
- Mechanized theorem proving
- Mathematical rigor

## 🌟 The Complete Story

This project demonstrates the full journey from mathematical theory to practical implementation:

📖 **[The Recursive Story](./docs/the-recursive-story.md)** - The complete narrative connecting all pieces

## 🆕 Probabilistic Language Model Extension

We've extended the atomic language model with **probabilistic next-token prediction** capabilities while maintaining all formal guarantees:

### Features
- 🎲 **Weighted Grammar Rules**: Each production has learned probabilities
- 🔮 **Next-Token Prediction**: Monte Carlo sampling for language modeling
- 🔄 **Hybrid Architecture**: Combines Rust validation with Python inference
- 🌐 **REST API**: Flask server for easy integration
- 📦 **Still Ultra-Light**: <100kB total with all features

### Quick Demo
```bash
# Run the probabilistic language model
cd atomic-lang-model/python
python tiny_lm.py

# Start the API server
python api_server.py

# Try the interactive demo
cd ../examples
python language_model_demo.py
```

### Example API Usage
```bash
# Predict next token
curl localhost:5000/predict?prefix=the+student

# Generate sentences
curl localhost:5000/generate?count=5

# Validate syntax
curl -X POST localhost:5000/validate \
  -H "Content-Type: application/json" \
  -d '{"sentences": ["the student left", "student the left"]}'
```

This extension bridges **formal grammar theory** with **practical NLP applications**, creating the world's smallest formally verified language model.

## 🎯 Key Features

### Mathematical Rigor
- ✅ **Formal Specification**: Complete mathematical definition of operations
- ✅ **Coq Proofs**: Machine-verified theorems about recursive properties  
- ✅ **Non-regularity Proof**: Constructive demonstration via a^n b^n generation
- ✅ **Complexity Bounds**: Polynomial parsing with exponential generation capacity

### Universal Grammar Implementation
- ✅ **Merge Operation**: `Merge(α:=_X β, X:γ) = ⟨X, [], [α, γ]⟩`
- ✅ **Move Operation**: Implements wh-movement and feature checking
- ✅ **Feature System**: Categories, selectors, and movement features
- ✅ **Minimalist Compliance**: Based on Chomsky's Minimalist Program

### Engineering Excellence  
- ✅ **Zero Dependencies**: No runtime requirements
- ✅ **Size Optimized**: ~35kB binary with full functionality
- ✅ **Memory Efficient**: <256kB peak usage for 20-word sentences
- ✅ **Fast Parsing**: Polynomial-time complexity O(n³)

### Empirical Validation
- ✅ **Agreement Tests**: Subject-verb agreement across center-embedding (Linzen et al. 2016)
- ✅ **Colorless Green**: Syntactic processing with semantic anomalies (Gulordava et al. 2018)
- ✅ **Recursive Capability**: Demonstrates unbounded center-embedding
- ✅ **Performance Metrics**: Comprehensive benchmarking framework

## 🛠️ Project Structure

```
atomic-lang-model/
├── docs/                          # 📚 Complete documentation suite
│   ├── recursive-language-overview.md    # Start here!
│   ├── chomsky-mathematical-proofs.md    # The math foundation
│   ├── formal-language-theory.md         # Technical theory
│   ├── computational-processing.md       # How machines handle recursion
│   ├── nlp-verification-methods.md       # Testing approaches
│   ├── machine-verification.md           # Formal proofs
│   └── the-recursive-story.md            # Complete narrative
├── atomic-lang-model/             # 🧬 Core implementation
│   ├── src/lib.rs                      # Main implementation (~3k lines)
│   ├── tests/recursion.rs              # Mathematical proof tests
│   ├── bench/                          # NLP evaluation suites
│   ├── Coq/Minimalist.v               # Machine-verified proofs
│   ├── spec.md                         # Formal specification
│   ├── REPORT.md                       # Implementation analysis
│   ├── python/                         # 🤖 Probabilistic LM extension
│   │   ├── tiny_lm.py                 # Core probabilistic grammar
│   │   ├── hybrid_model.py            # Rust-Python bridge
│   │   └── api_server.py              # REST API server
│   └── examples/                       # 🎮 Demo applications
│       ├── language_model_demo.py     # Interactive demo
│       └── quick_example.py           # Simple usage example
└── flow/                          # 🌊 Claude-flow integration
    └── claude-flow/                    # AI orchestration platform
```

## 🎮 Try It Yourself

### Basic Usage
```bash
# Generate recursive patterns
cargo run --release -- generate an_bn 5
# Output: a a a a a b b b b b

# Parse sentences  
cargo run --release -- parse "the student who left smiled"
# Shows parse tree and derivation steps

# Run mathematical tests
cargo test test_an_bn_generation
cargo test test_recursive_capability
```

### Advanced Features
```bash
# Run linguistic evaluation suites
cargo test --release agreement_suite
cargo test --release colorless_green_suite

# Performance benchmarking
cargo test --release run_complete_benchmark

# Formal verification (requires Coq)
cd Coq && coqc Minimalist.v
```

## 🧪 What This Proves

This implementation demonstrates that:

1. **Recursive universal grammar is implementable** in extremely constrained environments
2. **Mathematical theory and practical engineering** can be unified effectively  
3. **Formal verification and empirical testing** provide complementary validation
4. **Chomsky's insights about recursion** remain relevant for modern AI systems

## 🤝 Contributing

We welcome contributions! See [Contributing Guidelines](./docs/contributing.md)

**Great starting points:**
- 📖 Improve documentation and examples
- 🧪 Add more linguistic test cases
- ⚡ Optimize performance and memory usage
- 🔬 Extend Coq formalization
- 🌍 Test on additional languages

## 📄 Citation

If you use this work in research, please cite:

```bibtex
@software{atomic_language_model,
  title={Atomic Language Model: Recursive Universal Grammar in 50kB},
  author={Atomic Language Model Team},
  year={2024},
  url={https://github.com/user/atomic-lang-model}
}
```

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 🌟 Acknowledgments

Built on the mathematical foundations of:
- **Noam Chomsky**: Recursive language theory and Minimalist Grammar
- **Edward Stabler**: Formal implementation of Minimalist Grammars  
- **Linzen et al.**: Agreement test methodology
- **Gulordava et al.**: Colorless green evaluation framework

---

**Ready to explore the mathematical foundations of human language?**

🚀 **[Start with the Overview](./docs/recursive-language-overview.md)** → Learn what recursion means for language

🧮 **[Dive into the Math](./docs/chomsky-mathematical-proofs.md)** → See the formal proofs

💻 **[Try the Code](./atomic-lang-model/)** → Run the implementation

*Built with mathematical rigor. Validated through empirical testing. Optimized for practical use.*