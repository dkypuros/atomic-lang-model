# NLP Testing and Verification Methods for Recursion

## From Theory to Practice: Testing Recursive Language Processing

How do we know if a computational system truly handles linguistic recursion? This requires moving from abstract proofs to concrete, measurable tests using real language data.

## The Challenge of Empirical Validation

### What We Need to Test

1. **Structural Understanding**: Does the system build correct hierarchical representations?
2. **Long-Distance Dependencies**: Can it track relationships across embedded clauses?
3. **Recursive Depth**: How does performance degrade with increasing embedding?
4. **Compositional Semantics**: Are meanings computed correctly from structure?

### The Token-Level Translation

Abstract recursion theory must be converted into:
- **Specific test sentences** with known grammatical properties
- **Quantitative metrics** (accuracy, surprisal, reaction time)
- **Controlled comparisons** between grammatical and ungrammatical variants

## Subject-Verb Agreement Challenge Sets

### The Linzen et al. (2016) Framework

**Basic Paradigm**:
```
The N_sg near the N_pl verb_? 
```

**Examples**:
- "The key to the cabinets is/*are here"
- "The author of these books is/*are famous"

**Measurement**:
```
Accuracy = #correct_predictions / #test_items
```

### Recursive Extensions

**Multiple Attractors**:
```
The N_sg [that the N_pl [who the N_pl knew] liked] verb_?
```

**Results Pattern**:
- 1 attractor: ~90% accuracy (humans and LSTMs)
- 2 attractors: ~70% accuracy  
- 3+ attractors: Near chance performance

**Mathematical Relationship**:
```
Accuracy ≈ baseline_accuracy × decay_rate^(num_attractors)
```

## "Colorless Green" Nonsense Tests

### Gulordava et al. (2018) Methodology

**Purpose**: Remove lexical and semantic cues, isolate syntactic processing

**Example Pairs**:
```
Grammatical:   The colorless green ideas sleep furiously
Ungrammatical: The colorless green ideas sleeps furiously  
```

**Surprisal Measurement**:
```
Surprisal(w_i) = -log₂ P(w_i | w₁...w_{i-1})
```

**Hypothesis**: Lower surprisal for grammatical continuations

### Cross-Linguistic Validation

**Languages Tested**: English, Italian, Hebrew, Russian

**Recursive Patterns**:
- **English**: Subject-relative clauses
- **Italian**: Pro-drop with agreement
- **Hebrew**: Discontinuous constituents  
- **Russian**: Case marking with free word order

**Universal Finding**: Performance degrades with embedding depth across all languages

## Center-Embedding Evaluation

### Graduated Difficulty Scale

**Level 1**: "The student smiled"
```
[S [NP The student] [VP smiled]]
```

**Level 2**: "The student [who left] smiled"  
```
[S [NP The student [CP who [S left]]] [VP smiled]]
```

**Level 3**: "The student [who the teacher [who arrived] knew] smiled"
```
[S [NP The student [CP who [S [NP the teacher [CP who [S arrived]]] knew]]] [VP smiled]]
```

### Performance Metrics

**Human Processing**:
- Reading time increases exponentially: RT ∝ e^(depth)
- Accuracy drops sharply after depth 2
- Garden-path effects increase with embedding

**Neural Models**:
```python
def measure_recursive_performance(model, test_set):
    results = {}
    for depth in range(1, 6):
        sentences = filter_by_depth(test_set, depth)
        accuracy = evaluate_agreement(model, sentences)
        results[depth] = accuracy
    return results
```

## Formal Language Learning Tests

### aⁿbⁿ Recognition

**Training Set**: 
```
ab, aabb, aaabbb, aaaabbbb, ...
```

**Test Set**:
```
Positive: a⁵b⁵, a¹⁰b¹⁰
Negative: a⁵b⁶, a⁴b⁵, abab
```

**Models Tested**:
- Simple RNNs: Fail beyond short sequences
- LSTMs: Learn up to training length, don't generalize
- Stack-augmented networks: Perfect generalization
- Transformers: Length-dependent performance

### Dyck Language Tests

**Balanced Parentheses**:
```
Valid: (), (()), (())(), ((()()))
Invalid: )(, (((), ())(
```

**Measurement**: Exact match accuracy on test strings

**Results**:
- Vanilla RNNs: ~60% accuracy
- LSTMs: ~85% accuracy  
- Stack RNNs: ~98% accuracy
- Transformers: 95%+ with position encoding

## Structural Probe Evaluation

### Hewitt & Manning (2019) Framework

**Hypothesis**: Neural representations encode syntactic tree distances

**Linear Probe**:
```
d_syntax(w_i, w_j) = √((h_i - h_j)ᵀ B (h_i - h_j))
```

Where B is learned transformation matrix

**Evaluation**: Spearman correlation between predicted and gold tree distances

**Results**: 
- BERT layers 6-8 best capture syntax
- Performance correlates with downstream task success
- Recursive structures emerge without explicit supervision

## Compositional Generalization Tests

### SCAN Benchmark

**Task**: Map natural language to action sequences
```
"walk twice" → WALK WALK
"walk and run twice" → WALK RUN RUN  
"walk around right twice" → LTURN WALK RTURN LTURN WALK RTURN
```

**Challenge**: Compositional combinations not seen in training

**Recursive Extension**:
```
"walk around left and walk around right twice"
```

### CFQ (Compositional Freebase Questions)

**Systematic Splits**: 
- Train on simple compositions
- Test on complex recursive combinations

**Example**:
```
Training: "What movies did M0 direct?"
Testing: "What movies did directors who were born in M1 direct?"
```

## Quantitative Metrics for Recursion

### Embedding Depth Analysis

**Automatic Depth Extraction**:
```python
def calculate_embedding_depth(parse_tree):
    def max_depth(node):
        if node.is_leaf():
            return 0
        return 1 + max(max_depth(child) for child in node.children)
    return max_depth(parse_tree.root)
```

**Performance Curves**:
```
accuracy_by_depth = {
    depth: accuracy_at_depth(model, test_sentences[depth])
    for depth in range(1, max_depth + 1)
}
```

### Processing Difficulty Prediction

**Surprisal-Based Metrics**:
```
Processing_Difficulty = Σᵢ Surprisal(wᵢ) × Integration_Cost(wᵢ)
```

**Memory-Based Metrics**:
```
Memory_Load = max(stack_depth_during_parsing)
```

## Large-Scale Evaluation Frameworks

### BLiMP (Benchmark of Linguistic Minimal Pairs)

**Coverage**: 67 linguistic phenomena across 12 categories
**Format**: Binary forced choice between grammatical/ungrammatical
**Recursive Phenomena**: 
- Center embedding
- Filler-gap dependencies  
- Coordinate structures

### CoLA (Corpus of Linguistic Acceptability)

**Task**: Binary classification of sentence acceptability
**Data**: 10K English sentences from linguistics literature
**Evaluation**: Matthews correlation coefficient

**Recursive Examples**:
```
Acceptable: "The fact that John left surprised Mary"
Unacceptable: "*The fact John left surprised Mary"
```

## Adversarial Testing

### Syntactic Transformations

**Passive Voice**:
```
"The dog chased the cat" → "The cat was chased by the dog"
```

**Relative Clause Conversion**:
```
"The student solved the problem" → "The student who solved the problem"
```

**Recursive Embedding**:
```
Base: "Mary thinks John left"
Embedded: "Mary thinks that John said that Bill left"
```

### Semantic Invariance Tests

**Hypothesis**: Recursive transformations shouldn't change core meaning

**Test Cases**:
```
"John believes Mary is smart"
"John believes that Mary is smart"  
"It is John's belief that Mary is smart"
```

**Evaluation**: Semantic similarity scores should remain high

## Practical Implementation

### Test Suite Construction

```python
class RecursionTestSuite:
    def __init__(self):
        self.agreement_tests = load_agreement_data()
        self.embedding_tests = generate_embedding_tests()
        self.formal_lang_tests = create_formal_language_tests()
    
    def evaluate_model(self, model):
        results = {}
        results['agreement'] = self.test_agreement(model)
        results['embedding'] = self.test_embedding(model)  
        results['formal'] = self.test_formal_languages(model)
        return self.aggregate_results(results)
```

### Statistical Analysis

**Significance Testing**:
- McNemar's test for paired binary outcomes
- Mann-Whitney U for non-parametric comparisons
- Bootstrap confidence intervals for robustness

**Effect Size Measurement**:
- Cohen's d for continuous metrics
- Odds ratios for binary classifications
- Correlation coefficients for relationships

The empirical validation of recursive language processing bridges the gap between elegant mathematical theory and messy real-world performance, providing the quantitative foundation needed to evaluate and improve both human and machine language understanding.