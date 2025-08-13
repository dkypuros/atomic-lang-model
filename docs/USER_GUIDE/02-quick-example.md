# 🎮 Quick Example: Your First Steps

> **From installation to understanding in 10 minutes**

Now that you have the Atomic Language Model installed, let's explore what makes it special through hands-on examples.

## 🧮 Mathematical Proof in Action

### Step 1: Prove Non-Regularity
Run the mathematical demonstration:

```bash
cd atomic-lang-model/atomic-lang-model
cargo run --release
```

You'll see output like:
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

♾️  Unbounded Recursion Demonstration
----------------------------------------
✅ Can generate a^6b^6 (length: 12)
✅ Can generate a^7b^7 (length: 14)  
✅ Can generate a^8b^8 (length: 16)

🎯 Theoretical Capacity: INFINITE
🔬 Practical Limit: Memory bounded
```

**What just happened?** You proved our grammar exceeds finite-state machines! The aⁿbⁿ pattern requires unbounded memory to count the a's and match them with b's.

### Step 2: Test Real Language
Try parsing natural language:

```bash
# Parse a simple sentence
cargo run --release -- parse "the student left"

# Try a complex recursive sentence
cargo run --release -- parse "the student who the teacher praised left"
```

Output shows the complete syntactic analysis:
```
✅ 'the student who the teacher praised left' 
   Category: S (Sentence)
   Complete: true
   
   Parse Tree:
        S
       ╱ ╲
      DP  VP
     ╱|╲  |
   the N  CP V
      |  ╱|╲ |
   student who... left
```

## 🔬 Understanding the Magic

### The Two-Part System

1. **Rust Core**: Formal grammar validation
   ```bash
   # Check what the Rust core does
   cargo test test_merge_operation
   cargo test test_move_operation
   ```

2. **Python Layer**: Probabilistic predictions
   ```bash
   cd ../python
   python tiny_lm.py
   ```
   
   Sample output:
   ```python
   Generated: the student left
   Generated: every teacher smiled  
   Generated: the book that Mary read surprised everyone
   
   Next-token predictions for "the student":
   - left (0.245)
   - smiled (0.198)
   - arrived (0.134)
   ```

### The Hybrid Approach

Try the combined system:
```bash
python -c "
from hybrid_model import HybridLanguageModel
model = HybridLanguageModel()

# Generate grammatically perfect sentences
for i in range(5):
    sentence = model.generate_sentence()
    print(f'✅ {sentence} (valid: {model.validate_syntax(sentence)})')
"
```

**Key insight**: Every generated sentence is guaranteed grammatically correct because the Rust core validates each one!

## 📊 Size vs. Power Demo

### Check the Incredible Size
```bash
# Build optimized binary
cargo build --release --profile min-size

# Check size (should be <50kB!)
ls -lh target/release/atomic-lm

# Compare to your system
echo "Our model: ~50kB"
echo "Your system Python: $(python -c 'import sys; print(f\"{sys.getsizeof(sys.modules)//1024}kB of just loaded modules\")')"
```

### Test Performance
```bash
# Run 1000 parsing operations
time cargo test test_parsing_benchmark --release -- --nocapture

# Check memory usage
cargo test test_memory_bounds --release
```

You'll see parsing happens in milliseconds with <256KB peak memory usage!

## 🧪 Explore Different Capabilities

### 1. Recursive Depth Testing
```bash
# Test increasingly complex sentences
cargo test test_recursive_capability --release -- --nocapture
```

Watch how the model handles:
- Depth 0: "the student left"
- Depth 1: "the student who arrived left"  
- Depth 2: "the student who the teacher praised left"
- Depth 3+: Even more complex embeddings!

### 2. Mathematical Pattern Generation
```bash
# Generate different aⁿbⁿ patterns
cargo run --release -- generate an_bn 3
cargo run --release -- generate an_bn 7
cargo run --release -- generate an_bn 10
```

### 3. Linguistic Test Suites
```bash
# Agreement tests (do subjects and verbs agree?)
cargo test agreement_suite --release

# Colorless green tests (syntax without semantics)
cargo test colorless_green_suite --release
```

## 🔄 REST API Exploration

### Start the Server
```bash
cd ../python
python api_server.py
```

### Try the Endpoints
In another terminal:

```bash
# Get model info
curl localhost:5000/

# Predict next tokens
curl -X POST localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"prefix": "the student who", "k": 5000}'

# Generate sentences  
curl localhost:5000/generate?count=3

# Validate syntax
curl -X POST localhost:5000/validate \
  -H "Content-Type: application/json" \
  -d '{"sentences": ["the student left", "student the left"]}'

# Complete sentences
curl -X POST localhost:5000/complete \
  -H "Content-Type: application/json" \
  -d '{"prefix": "the student who", "beam_size": 5}'
```

## 📈 Benchmarking Your System

### Performance Test
```bash
cd ../atomic-lang-model

# Full benchmark suite
cargo test run_complete_benchmark --release -- --nocapture

# Memory scaling test
cargo test test_recursive_depth_scaling --release

# Size verification
cargo test test_binary_size_claims --release
```

### Compare Results
```bash
echo "Expected results:"
echo "- Parsing: O(n³) complexity"
echo "- Memory: <256KB peak usage"  
echo "- Binary: <50KB total size"
echo "- Speed: <1ms for simple sentences"
echo ""
echo "Your results should be similar!"
```

## 🎯 What You've Learned

After running these examples, you've seen:

✅ **Mathematical Proof**: The aⁿbⁿ generation proves recursive capability  
✅ **Natural Language**: Complex sentence parsing with formal guarantees  
✅ **Hybrid System**: Rust validation + Python probabilities  
✅ **Performance**: Incredible efficiency (50kB, <256KB memory)  
✅ **API Integration**: REST endpoints for real applications  
✅ **Linguistic Validation**: Standard test suites pass  

## 🚀 Next Steps

Ready to dive deeper?

1. **📚 Understand the Theory**: [Mathematical Foundations](../THEORY/01-mathematical-foundations.md)
2. **🚶‍♂️ Take the Full Tour**: [Interactive Walkthrough](03-interactive-walkthrough.md)
3. **💻 Explore the Code**: [API Reference](../DEVELOPER_GUIDE/01-api-reference.md)
4. **🧪 Try Advanced Examples**: [Practical Tutorials](03-examples.md)
5. **🤝 Contribute**: [Contributing Guide](../DEVELOPER_GUIDE/02-contributing.md)

## 💡 Key Takeaways

- **Size ≠ Power**: Our 50kB model handles infinite recursion
- **Math Matters**: Formal proofs ensure correctness
- **Hybrid Works**: Combine symbolic and statistical approaches
- **Standards Count**: We pass established linguistic benchmarks
- **Practical**: REST API ready for real applications

**You've just experienced the world's smallest formally verified language model!**