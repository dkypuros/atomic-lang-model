# 🔬 Fibration Bridge: A Grothendieck Experiment

> **An experimental approach to relating pure grammar and empirical NLP layers using category theory**

This folder contains an experimental implementation of using Grothendieck fibrations to cleanly separate the formal grammar (base category) from empirical enrichments (fibres) like probabilities, embeddings, and proofs.

## 🎯 The Core Idea

- **Base Category B**: The pure syntactic universe (derivation trees)
- **Total Category E**: Statistical/empirical enrichments (probabilities, embeddings)
- **Fibration p: E → B**: Maps every empirical object to exactly one grammar object

This separation allows us to:
1. Keep the formal grammar implementation pure and verified
2. Swap different empirical layers without touching core recursion
3. Guarantee compositionality through categorical laws

## 🚀 Quick Demo

```python
# Basic usage
from fibration_core import GrammarFibration
from fibres import ProbabilityFibre, BM25Fibre

# Create fibration with probability fibre
fib = GrammarFibration()
prob_fibre = ProbabilityFibre()

# Parse with empirical enrichment
tree, probs = fib.parse_with_fibre("the student left", prob_fibre)

# Information retrieval with BM-25
bm25 = BM25Fibre()
tree, scores = fib.parse_with_fibre("student learning", bm25)
print(scores.top_k(5))  # Top 5 relevant documents
```

## 📁 Structure

- `fibration_core.py` - Core fibration implementation
- `base_category.py` - Pure syntactic operations
- `fibres/` - Different fibre implementations
  - `probability_fibre.py` - Probabilistic weights
  - `embedding_fibre.py` - Vector embeddings
  - `proof_fibre.py` - Formal proofs
- `examples/` - Usage examples
- `theory.md` - Mathematical background

## ⚗️ Experimental Status

This is an **experimental research prototype** exploring how category theory can improve the architecture of hybrid formal/empirical NLP systems. It's intentionally kept separate from the main codebase to:

1. Allow rapid experimentation without affecting stability
2. Test advanced mathematical concepts before integration
3. Provide a playground for theoretical ideas

## 🔗 Integration Points

While separate, this experiment connects to the main codebase:
- Uses the same grammar rules from `../../python/tiny_lm.py`
- Compatible with Rust parser via `../../src/lib.rs`
- Can enhance the REST API in `../../python/api_server.py`

---

**Note**: This is research code. For production use, stick to the main implementation.