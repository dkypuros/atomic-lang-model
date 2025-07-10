# 🚀 Quick Start Guide: Atomic Language Model

> **Get up and running with recursive universal grammar in 5 minutes**

This guide gets you from zero to running mathematical proofs of language recursion in just a few commands.

## 📋 Prerequisites

**Required:**
- **Rust 1.70+** - [Install from rustup.rs](https://rustup.rs/)
- **Git** - For cloning the repository

**Optional (for advanced features):**
- **Coq 8.15+** - For formal verification
- **Python 3.8+** - For additional analysis scripts

## ⚡ Lightning Setup (30 seconds)

```bash
# 1. Clone and enter directory
git clone https://github.com/user/atomic-lang-model.git
cd atomic-lang-model/atomic-lang-model

# 2. Run the mathematical demonstration
cargo run --release

# 3. Run core recursive tests  
cargo test --release test_complete_recursive_proof
```

**That's it!** You've just witnessed mathematical proof of language recursion.

## 🎯 What You Just Saw

### The Demo Output
```
🧬 Atomic Language Model - Recursive Grammar Demo
============================================================

📐 Mathematical Proof: aⁿbⁿ Generation
----------------------------------------
n=0: ε (empty)        # Base case: empty string
n=1: a b              # Simple pattern  
n=2: a a b b          # Growing complexity
n=3: a a a b b b      # Unbounded in principle
n=4: a a a a b b b b  # Mathematical recursion
```

**Why This Matters**: This proves our grammar generates non-regular languages, demonstrating true recursion that finite-state machines cannot handle.

### The Test Output
```
🧮 COMPLETE MATHEMATICAL PROOF OF RECURSION
==================================================

1. Non-regularity proof via aⁿbⁿ: ✅
2. Recursive parsing capability: ✅  
3. Infinite generation from finite grammar: ✅
4. Memory efficiency: ✅

🎯 CONCLUSION: RECURSION MATHEMATICALLY PROVEN
```

## 🧪 Essential Commands

### Basic Operations
```bash
# Generate specific recursive patterns
cargo run --release -- generate an_bn 5
# Output: a a a a a b b b b b

# Parse natural language sentences
cargo run --release -- parse "the student left"
# Shows: parse tree, derivation steps, feature checking

# Test mathematical properties
cargo test test_an_bn_generation
cargo test test_recursive_capability  
cargo test test_unboundedness_witness
```

### Linguistic Evaluation
```bash
# Run agreement test suite (Linzen et al. 2016)
cargo test --release agreement_suite

# Run colorless green tests (Gulordava et al. 2018)  
cargo test --release colorless_green_suite

# Complete benchmark suite
cargo test --release run_complete_benchmark
```

### Advanced Features
```bash
# Build size-optimized binary
cargo build --release --profile min-size

# Run with memory profiling
cargo test --release test_recursive_depth_scaling

# Formal verification (requires Coq)
cd Coq && coqc Minimalist.v
```

## 🔍 Understanding the Output

### Demo Explanation
When you run `cargo run --release`, you see:

1. **aⁿbⁿ Generation**: Mathematical proof that our grammar is non-regular
2. **Parsing Tests**: Natural language sentences processed with recursive rules
3. **Performance Metrics**: Memory usage, parsing speed, binary size
4. **Formal Properties**: Mathematical verification of key claims

### Test Explanation  
When you run the recursive proof test:

1. **Non-regularity**: Proves our language exceeds finite-state capacity
2. **Parsing Capability**: Demonstrates recursive structure processing
3. **Infinite Generation**: Shows unbounded capability from finite means
4. **Memory Efficiency**: Verifies practical constraints are met

## 🎮 Interactive Exploration

### Try Different Patterns
```bash
# Different recursive depths
cargo run --release -- generate an_bn 0    # ε (empty)
cargo run --release -- generate an_bn 1    # a b
cargo run --release -- generate an_bn 10   # a^10 b^10

# Parse complex sentences
cargo run --release -- parse "the student who left smiled"
cargo run --release -- parse "the student who the teacher praised left"
```

### Modify the Grammar
Edit `src/lib.rs` to add new lexical items:

```rust
// Add to test_lexicon() function
LexItem::new("quickly", &[Feature::Cat(Category::V)]),
LexItem::new("book", &[Feature::Cat(Category::N)]),
```

Then test: `cargo run --release -- parse "the student quickly left"`

### Experiment with Features
```bash
# Memory scaling tests
cargo test test_recursive_depth_scaling

# Performance analysis  
cargo test test_derivation_convergence

# Feature system correctness
cargo test test_feature_system_correctness
```

## 📊 Key Metrics to Watch

### Size and Performance
```bash
# Check binary size
cargo build --release && ls -lh target/release/atomic-lm
# Target: <50kB

# Memory usage during tests
cargo test --release test_memory_usage
# Target: <256kB peak

# Parsing performance
cargo test --release test_parsing_speed  
# Target: <1ms average
```

### Mathematical Properties
```bash
# Verify recursion depth
cargo test test_recursive_capability
# Should show: unbounded generation capacity

# Check complexity bounds
cargo test test_complexity_analysis
# Should show: polynomial parsing time
```

## 🚨 Troubleshooting

### Common Issues

**"cargo: command not found"**
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

**Compilation errors**
```bash
# Update Rust
rustup update

# Clean and rebuild
cargo clean && cargo build --release
```

**Tests failing**
```bash
# Run specific test with details
cargo test test_an_bn_generation -- --nocapture

# Check system requirements
cargo test --release -- --list
```

### Performance Issues

**Slow compilation**
```bash
# Use fewer CPU cores
export CARGO_BUILD_JOBS=2
cargo build --release
```

**Memory constraints**
```bash
# Run with smaller test sizes
cargo test --release -- --test-threads=1
```

## 🧭 Next Steps

### Beginner Path
1. **📖 Read**: [Recursive Language Overview](../docs/recursive-language-overview.md)
2. **🧮 Study**: [Chomsky's Mathematical Proofs](../docs/chomsky-mathematical-proofs.md)  
3. **💻 Explore**: Browse `src/lib.rs` to understand implementation
4. **🧪 Experiment**: Modify lexicon and test new sentences

### Advanced Path
1. **⚙️ Theory**: [Formal Language Theory](../docs/formal-language-theory.md)
2. **🔬 Verification**: [Machine Verification](../docs/machine-verification.md)
3. **📊 Testing**: [NLP Verification Methods](../docs/nlp-verification-methods.md)
4. **🚀 Optimize**: Improve performance and add features

### Research Path
1. **📁 Source**: Study the complete implementation
2. **🧪 Benchmarks**: Run full linguistic test suites  
3. **✅ Proofs**: Work with Coq verification
4. **📝 Extend**: Add new features or languages

## 🤝 Getting Help

### Documentation
- **📚 Main docs**: `docs/` directory
- **💻 Implementation**: `src/lib.rs` with extensive comments
- **🧪 Tests**: `tests/` and `bench/` directories
- **🔬 Proofs**: `Coq/Minimalist.v` formal verification

### Community
- **💬 Issues**: [GitHub Issues](https://github.com/user/atomic-lang-model/issues)
- **🔧 Discussions**: [GitHub Discussions](https://github.com/user/atomic-lang-model/discussions)
- **📧 Email**: Contact maintainers for research collaboration

### Contributing
- **🐛 Bug reports**: Always welcome
- **📖 Documentation**: Help improve clarity
- **🧪 Tests**: Add more linguistic test cases
- **⚡ Performance**: Optimize implementation

## 🎉 Success Criteria

You're ready to move beyond quick start when you can:

✅ **Run all basic commands** without errors  
✅ **Understand the output** of recursive generation  
✅ **Explain why aⁿbⁿ proves non-regularity**  
✅ **Modify the lexicon** and test new sentences  
✅ **Navigate the codebase** to find key functions  

**Congratulations!** You've successfully set up and explored a mathematically proven implementation of recursive universal grammar. The mathematical foundations of human language are now at your fingertips.

---

**Ready for the next level?** 
- 🧮 **Understand the math**: [Chomsky's Proofs](../docs/chomsky-mathematical-proofs.md)
- 📖 **Full story**: [The Recursive Story](../docs/the-recursive-story.md)  
- 💻 **Deep dive**: Browse the [source code](src/lib.rs)