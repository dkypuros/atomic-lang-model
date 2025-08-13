# 📖 Glossary of Concepts

> **A comprehensive guide to all key terms and concepts in the Atomic Language Model documentation**

This glossary provides quick definitions and links to detailed explanations throughout the documentation. Terms are organized alphabetically for easy reference.

---

## A

### **Agreement Suite**
A set of linguistic tests from [Linzen et al. 2016](nlp-verification-methods.md) that evaluate subject-verb agreement across various syntactic constructions. Used to validate our model's handling of grammatical dependencies.
- 📍 Found in: [Specification](../atomic-lang-model/spec.md), [Implementation Report](../atomic-lang-model/REPORT.md)

### **Atomic Language Model**
Our ultra-lightweight (<50KB) implementation of universal grammar with provable recursion and zero dependencies. The "atomic" refers to its minimal, indivisible nature.
- 📍 Found in: [Overview](index.md), [Walkthrough](walkthrough.md)

### **Abstract Algebra**
The mathematical framework defining our grammar's operations (Merge and Move) as algebraic transformations on syntactic objects.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#2-abstract-algebra-the-grammars-operations), [Specification](../atomic-lang-model/spec.md)

### **Attractors**
Intervening nouns between a subject and verb that can cause agreement errors in language processing. Our model correctly handles these distractors.
- 📍 Found in: [Implementation Report](../atomic-lang-model/REPORT.md)

### **aⁿbⁿ Generation**
A classic pattern (equal numbers of a's followed by b's) that proves a language is non-regular. Our model generates this pattern, demonstrating true recursion.
- 📍 Found in: [Mathematical Proofs](chomsky-mathematical-proofs.md), [Quick Start](../atomic-lang-model/QUICKSTART.md)

---

## B

### **Base Category**
In our [Grothendieck fibration](../atomic-lang-model/experiments/fibration-bridge/theory.md), the category of pure syntactic structures without empirical annotations.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#3-category-theory-the-fibration-architecture), [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md)

### **Beck-Chevalley Condition**
A coherence condition in category theory ensuring that pull-backs commute with push-forwards in our fibration architecture.
- 📍 Found in: [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md)

### **Binary Size Optimization**
Techniques used to achieve our <50KB binary size, including link-time optimization (LTO) and dead code elimination.
- 📍 Found in: [Specification](../atomic-lang-model/spec.md), [Size Comparison](size-comparison.md)

### **BM25Fibre**
A fibre implementation for information retrieval using BM-25 scoring, demonstrating how IR integrates with our fibration architecture.
- 📍 Found in: [BM-25 Implementation](../atomic-lang-model/experiments/fibration-bridge/fibres/bm25_fibre.py)

---

## C

### **Cartesian Morphism**
A morphism in a fibration that provides the "best" way to lift structures along syntactic transformations.
- 📍 Found in: [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md), [Fibre Contracts](../atomic-lang-model/experiments/fibration-bridge/docs/fibre_contracts.md)

### **Category Features (CAT)**
Basic syntactic categories like N (noun), V (verb), D (determiner) that label constituents in our grammar.
- 📍 Found in: [Specification](../atomic-lang-model/spec.md), [Formal Verification](../atomic-lang-model/Coq/Minimalist.v)

### **Center-embedding**
Recursive structures where constituents are nested within other constituents (e.g., "the student [who the teacher [that I know] praised] left"). Tests true recursive capability.
- 📍 Found in: [Recursive Overview](recursive-language-overview.md), [Examples](examples.md)

### **Chomsky, Noam**
Linguist whose theories of universal grammar and recursive syntax form the mathematical foundation of our implementation.
- 📍 Found in: [Mathematical Proofs](chomsky-mathematical-proofs.md), [The Story](the-recursive-story.md)

### **Claude-Flow**
AI orchestration platform we explored for coordinating the implementation process.
- 📍 Found in: [Implementation Report](../atomic-lang-model/REPORT.md)

### **Colorless Green Suite**
Tests from [Gulordava et al. 2018](nlp-verification-methods.md) using semantically anomalous but syntactically correct sentences to evaluate pure grammatical processing.
- 📍 Found in: [NLP Verification](nlp-verification-methods.md), [Benchmarks](../atomic-lang-model/bench/)

### **Complexity Penalty**
A scoring mechanism that balances parsing accuracy with computational efficiency in our implementation.
- 📍 Found in: [Specification](../atomic-lang-model/spec.md)

### **Chomsky Hierarchy**
A classification of languages by computational complexity (Regular ⊂ Context-Free ⊂ Context-Sensitive ⊂ Recursively Enumerable). Our model operates at the context-free level and beyond.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#1-formal-language-theory--the-chomsky-hierarchy), [Formal Language Theory](formal-language-theory.md)

### **Context-Free Languages**
Languages that can be generated by context-free grammars. Our model generates languages beyond this class (multiple context-free).
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#language-classes), [Formal Language Theory](formal-language-theory.md)

### **Coq**
A proof assistant used to formally verify the mathematical properties of our grammar implementation.
- 📍 Found in: [Machine Verification](machine-verification.md), [Coq Proofs](../atomic-lang-model/Coq/Minimalist.v)

---

## D

### **Derivation**
The process of building a syntactic structure from lexical items through merge and move operations.
- 📍 Found in: [Specification](../atomic-lang-model/spec.md), [Computational Processing](computational-processing.md)

### **DFA (Deterministic Finite Automaton)**
A finite-state machine that our grammar provably exceeds in computational power through recursive generation.
- 📍 Found in: [Mathematical Proofs](chomsky-mathematical-proofs.md)

### **Discrete Infinity**
The property of human language to generate infinitely many distinct sentences from finite means.
- 📍 Found in: [Recursive Overview](recursive-language-overview.md), [Implementation Report](../atomic-lang-model/REPORT.md)

---

## E

### **Earley Parser**
An efficient parsing algorithm for context-free grammars that we reference but don't use (we use a custom approach).
- 📍 Found in: [Specification](../atomic-lang-model/spec.md)

### **EmbeddingFibre**
A fibre that enriches syntactic trees with vector representations, bridging symbolic and neural approaches.
- 📍 Found in: [Embedding Fibre](../atomic-lang-model/experiments/fibration-bridge/fibres/embedding_fibre.py)

---

## F

### **Feature Checking**
The process of verifying that syntactic features match correctly during merge operations (e.g., selector =N matches category N).
- 📍 Found in: [Implementation](../atomic-lang-model/src/lib.rs), [Specification](../atomic-lang-model/spec.md)

### **Feature System**
The formal system of syntactic features including categories (N, V), selectors (=N), and movement triggers (+wh, -wh).
- 📍 Found in: [Specification](../atomic-lang-model/spec.md), [Theory](formal-language-theory.md)

### **Fibre/Fibration**
Mathematical structure that cleanly separates pure syntax from empirical enrichments (probabilities, embeddings, proofs).
- 📍 Found in: [Fibration Experiment](../atomic-lang-model/experiments/fibration-bridge/), [Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md)

### **Functoriality**
The property that composition of morphisms is preserved: pull(g∘f) = pull(f, pull(g, ·)).
- 📍 Found in: [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md), [Tests](../atomic-lang-model/experiments/fibration-bridge/tests/)

---

## G

### **Grothendieck Fibration**
A category-theoretic structure connecting syntax (base) with data layers (fibres). Provides mathematical coherence in our hybrid architecture.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#grothendieck-fibration), [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md)
A category-theoretic construction that relates pure grammar (base) to empirical data (fibres) in a mathematically coherent way.
- 📍 Found in: [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md), [Experiments](../atomic-lang-model/experiments/fibration-bridge/)

### **Gulordava et al. 2018**
Authors of the "colorless green" test suite for evaluating syntactic capabilities independent of semantics.
- 📍 Found in: [NLP Verification](nlp-verification-methods.md)

---

## H

### **Halting Condition**
Mechanism to prevent infinite recursion in parsing by limiting derivation depth or workspace size.
- 📍 Found in: [Specification](../atomic-lang-model/spec.md)

### **Hybrid Architecture**
Our design combining Rust (formal grammar) with Python (probabilistic modeling) for best of both worlds.
- 📍 Found in: [Hybrid Model](../atomic-lang-model/python/hybrid_model.py), [Tutorial](language-model-tutorial.md)

---

## L

### **Lexical Items**
Basic units in the lexicon consisting of a phonological form and syntactic features (e.g., "student" with features [N]).
- 📍 Found in: [Specification](../atomic-lang-model/spec.md), [Implementation](../atomic-lang-model/src/lib.rs)

### **Lexicon**
The collection of lexical items available for building syntactic structures.
- 📍 Found in: [Quick Start](../atomic-lang-model/QUICKSTART.md), [Examples](examples.md)

### **Link-Time Optimization (LTO)**
Compiler optimization that helps achieve our <50KB binary size by eliminating dead code across compilation units.
- 📍 Found in: [Build Configuration](../atomic-lang-model/Cargo.toml), [Report](../atomic-lang-model/REPORT.md)

### **Linzen et al. 2016**
Authors of the agreement test suite we use to validate grammatical dependency handling.
- 📍 Found in: [NLP Verification](nlp-verification-methods.md), [Benchmarks](../atomic-lang-model/bench/)

---

## M

### **Memoization**
Caching technique to avoid recomputing results, especially important for base category operations in our fibration.
- 📍 Found in: [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md), [Performance](../atomic-lang-model/REPORT.md)

### **Memory Profiling**
Analysis of memory usage showing our model uses <256KB peak for 20-word sentences.
- 📍 Found in: [Performance Analysis](../atomic-lang-model/REPORT.md), [Examples](examples.md)

### **Merge Operation**
Core binary algebraic operation that combines two syntactic objects: Merge(α:=ₓβ, X:γ) = ⟨X, [], [α, γ]⟩. Models function application in syntax.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#1-merge), [Specification](../atomic-lang-model/spec.md)
- 📍 Found in: [Mathematical Proofs](chomsky-mathematical-proofs.md), [Implementation](../atomic-lang-model/src/lib.rs)

### **Minimalist Grammar**
Chomsky's algebraic theory reducing language to minimal operations (Merge and Move) that we implement. Forms the abstract algebra foundation of our system.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#2-abstract-algebra-the-grammars-operations), [Formal Language Theory](formal-language-theory.md)
- 📍 Found in: [Overview](recursive-language-overview.md), [Theory](formal-language-theory.md)

### **Monte Carlo**
Sampling method used in our probabilistic extension to estimate next-token distributions.
- 📍 Found in: [Probabilistic LM](../atomic-lang-model/python/tiny_lm.py), [Tutorial](language-model-tutorial.md)

### **Morphism**
Structure-preserving map between syntactic trees in our category-theoretic framework.
- 📍 Found in: [Fibration Core](../atomic-lang-model/experiments/fibration-bridge/fibration_core.py)

### **Move Operation**
Unary algebraic operation handling syntactic displacement (e.g., wh-movement): Move(+f, ...-f...) moves -f constituent. Models transformations like question formation.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#2-move), [Specification](../atomic-lang-model/spec.md)
- 📍 Found in: [Specification](../atomic-lang-model/spec.md), [Theory](formal-language-theory.md)

### **Multiple Context-Free Languages (MCFLs)**
Language class more powerful than CFLs that our grammar generates, allowing crossing dependencies.
- 📍 Found in: [Formal Language Theory](formal-language-theory.md), [Specification](../atomic-lang-model/spec.md)

---

## N

### **Negative Features (-f)**
Features that trigger movement when matched with corresponding positive features.
- 📍 Found in: [Feature System](../atomic-lang-model/spec.md), [Coq Proofs](../atomic-lang-model/Coq/Minimalist.v)

### **Non-regularity**
Property of languages that cannot be recognized by finite-state machines, proven by aⁿbⁿ generation.
- 📍 Found in: [Mathematical Proofs](chomsky-mathematical-proofs.md), [Tests](../atomic-lang-model/tests/recursion.rs)

### **no_std**
Rust attribute indicating no standard library dependency, enabling our minimal binary size.
- 📍 Found in: [Implementation](../atomic-lang-model/src/lib.rs), [Size Comparison](size-comparison.md)

---

## P

### **Polynomial Complexity**
Our parsing algorithm runs in O(n³) time, making it practical for real-world use.
- 📍 Found in: [Specification](../atomic-lang-model/spec.md), [Performance](../atomic-lang-model/REPORT.md)

### **Positive Features (+f)**
Features that attract constituents with matching negative features for movement.
- 📍 Found in: [Feature System](../atomic-lang-model/spec.md), [Theory](formal-language-theory.md)

### **ProbabilityFibre**
A fibre implementation assigning probability distributions to syntactic structures in our fibration architecture.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#fibres-f), [Fibration Bridge](../atomic-lang-model/experiments/fibration-bridge/)

### **Pullback**
The category-theoretic operation ensuring coherent transformation of data when syntax changes. Central to our fibration architecture.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#grothendieck-fibration), [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md)

### **Pushdown Automaton**
A computational model with stack memory required to recognize context-free languages. Our model exceeds this class.
- 📍 Found in: [Mathematical Foundations](mathematical-foundations.md#language-classes), [Formal Language Theory](formal-language-theory.md)
Fibre enriching syntactic trees with probability distributions for language modeling.
- 📍 Found in: [Probability Fibre](../atomic-lang-model/experiments/fibration-bridge/fibres/probability_fibre.py)

### **ProofFibre**
Fibre carrying formal verification data and proof obligations through syntactic derivations.
- 📍 Found in: [Proof Fibre](../atomic-lang-model/experiments/fibration-bridge/fibres/proof_fibre.py)

### **Pull-back/Pull Operation**
Categorical operation that lifts empirical data along syntactic morphisms, ensuring coherence.
- 📍 Found in: [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md), [Fibre Contracts](../atomic-lang-model/experiments/fibration-bridge/docs/fibre_contracts.md)

### **Push-forward/Push Operation**
Dual to pull-back, propagating empirical data forward along syntactic transformations.
- 📍 Found in: [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md)

---

## R

### **Recursion/Recursive**
The property of language allowing infinite expression through self-referential rules, central to our implementation.
- 📍 Found in: [Recursive Overview](recursive-language-overview.md), [Mathematical Proofs](chomsky-mathematical-proofs.md)

### **Relative Clauses**
Syntactic structures like "who arrived" that modify nouns and demonstrate recursive embedding.
- 📍 Found in: [Examples](examples.md), [Tests](../atomic-lang-model/tests/recursion.rs)

### **Rust**
Systems programming language used for our core implementation, providing safety and zero-cost abstractions.
- 📍 Found in: [Implementation](../atomic-lang-model/src/lib.rs), [Walkthrough](walkthrough.md)

---

## S

### **Selector Features (=CAT)**
Features that select complements of specific categories during merge (e.g., =N selects a noun).
- 📍 Found in: [Feature System](../atomic-lang-model/spec.md), [Implementation](../atomic-lang-model/src/lib.rs)

### **Stabler 1997**
Edward Stabler's formalization of minimalist grammars that our implementation follows.
- 📍 Found in: [References](formal-language-theory.md), [Specification](../atomic-lang-model/spec.md)

### **Subject-verb Agreement**
Grammatical constraint requiring subjects and verbs to match in number, tested extensively in our benchmarks.
- 📍 Found in: [NLP Verification](nlp-verification-methods.md), [Agreement Tests](../atomic-lang-model/bench/agreement_suite.rs)

### **Syntactic Objects**
Tree structures built from lexical items through merge and move operations.
- 📍 Found in: [Implementation](../atomic-lang-model/src/lib.rs), [Theory](formal-language-theory.md)

---

## T

### **TokenLattice**
Data structure for efficient token representation in our implementation (referenced in source).
- 📍 Found in: Source code

### **Total Category**
In our fibration, the category containing syntactic structures enriched with empirical data.
- 📍 Found in: [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md)

---

## U

### **Universal Grammar**
Chomsky's theory that all human languages share fundamental structural principles, which we implement.
- 📍 Found in: [Overview](recursive-language-overview.md), [The Story](the-recursive-story.md)

### **Universal Property**
Category-theoretic property ensuring unique factorization through cartesian morphisms in our fibration.
- 📍 Found in: [Fibration Theory](../atomic-lang-model/experiments/fibration-bridge/theory.md)

---

## W

### **Workspace**
Memory-bounded storage for syntactic objects during derivation, preventing infinite recursion.
- 📍 Found in: [Specification](../atomic-lang-model/spec.md), [Implementation](../atomic-lang-model/src/lib.rs)

### **Workspace Management**
System for efficiently storing and accessing syntactic objects during parsing within memory constraints.
- 📍 Found in: [Implementation Report](../atomic-lang-model/REPORT.md)

---

## Quick Reference

### Most Important Concepts
1. **[Recursion](#recursionrecursive)** - Core property of human language
2. **[Minimalist Grammar](#minimalist-grammar)** - Theoretical foundation
3. **[Merge](#merge-operation)** & **[Move](#move-operation)** - Fundamental operations
4. **[Atomic Language Model](#atomic-language-model)** - Our implementation
5. **[Hybrid Architecture](#hybrid-architecture)** - Rust + Python design

### Size & Performance
- **<50KB binary** - See [Size Comparison](size-comparison.md)
- **Zero dependencies** - See [no_std](#no_std)
- **O(n³) parsing** - See [Polynomial Complexity](#polynomial-complexity)
- **<256KB memory** - See [Memory Profiling](#memory-profiling)

### Theoretical Foundations
- **[Mathematical Foundations](mathematical-foundations.md)** - Complete guide to the mathematics
- **[Universal Grammar](#universal-grammar)** - Chomsky's theory
- **[Chomsky Hierarchy](#chomsky-hierarchy)** - Language classification
- **[Abstract Algebra](#abstract-algebra)** - Grammar operations
- **[Non-regularity](#non-regularity)** - Beyond finite-state
- **[Discrete Infinity](#discrete-infinity)** - Infinite from finite
- **[Grothendieck Fibration](#grothendieck-fibration)** - Advanced architecture

---

*This glossary is a living document. As the project evolves, new terms will be added and definitions refined.*