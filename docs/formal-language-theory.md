# Formal Language Theory and Grammar Hierarchies

> **Note**: This document provides detailed technical specifications. For a comprehensive overview of the mathematical foundations including abstract algebra and category theory, see our [Mathematical Foundations](mathematical-foundations.md) guide.

## The Mathematical Framework Behind Language

Formal language theory provides the mathematical foundation for understanding how recursive structures in human language can be precisely characterized and computed. This forms the first pillar of our three-part mathematical framework, alongside [abstract algebra](mathematical-foundations.md#2-abstract-algebra-the-grammars-operations) and [category theory](mathematical-foundations.md#3-category-theory-the-fibration-architecture).

## The Chomsky Hierarchy

Languages are classified by the power of grammars needed to generate them:

### Type 3: Regular Languages
**Grammar Form**: A → aB or A → a
```
Finite-state automaton
Memory: Constant
Example: (ab)*
```

**Limitations**: Cannot handle center-embedding like aⁿbⁿ

### Type 2: Context-Free Languages  
**Grammar Form**: A → α (where α is any string)
```
Push-down automaton
Memory: Stack (unbounded)
Example: aⁿbⁿ, balanced parentheses
```

**Power**: Handles nested structures but not cross-serial dependencies

### Type 1: Context-Sensitive Languages
**Grammar Form**: αAβ → αγβ (where |γ| ≥ 1)
```
Linear-bounded automaton
Memory: Polynomial in input length
Example: aⁿbⁿcⁿ
```

### Type 0: Recursively Enumerable
**Grammar Form**: α → β (unrestricted)
```
Turing machine
Memory: Unlimited
Example: Any computable language
```

## Where Human Language Fits

### Mildly Context-Sensitive Languages

Human language appears to require grammars slightly more powerful than context-free but much less than fully context-sensitive:

```
Regular ⊂ Context-Free ⊂ Mildly Context-Sensitive ⊂ Context-Sensitive
```

**Properties of Mildly Context-Sensitive:**
- Polynomial parsing time
- Constant growth property  
- Limited cross-serial dependencies
- Semilinear Parikh images

## Minimalist Grammars (MGs)

### Algebraic Formulation

Stabler (1997) formalized Chomsky's Merge operation, creating the algebraic system we implement:

```
MG = ⟨V, C, Lex, F⟩
```

Where:
- **V**: Feature values
- **C**: Syntactic categories  
- **Lex ⊂ V***: Finite lexicon of feature strings
- **F**: Structure-building functions (Merge and Move)

This algebraic formulation is the foundation of our implementation. For a detailed explanation of how these operations work as an algebraic system, see [Abstract Algebra: The Grammar's Operations](mathematical-foundations.md#2-abstract-algebra-the-grammars-operations).

### Core Operations

**Merge**: 
```
Merge(X, Y) = {X, Y}
```

**Move**:
```
Move±f(X) = rearrange X based on feature ±f
```

### Mathematical Properties

**Theorem** (Stabler 1997): Every MG language is equivalent to a multiple context-free language.

This places human syntax in a mathematically precise complexity class that is:
- More powerful than context-free
- Polynomial-time parsable
- Empirically adequate for natural language

## Recursive Definition Examples

### Simple Recursive Grammar
```
S → aSb | ε
```
Generates: {ε, ab, aabb, aaabbb, ...} = {aⁿbⁿ | n ≥ 0}

### Natural Language Recursion
```
NP → Det N (CP)
CP → C S
S → NP VP
```

Enables unlimited embedding:
"The student [who the professor [that Mary knows] taught] left"

## Tree-Adjoining Grammars (TAGs)

### Definition
TAGs consist of:
- **Elementary trees**: Minimal linguistic structures
- **Adjunction operation**: Inserts trees into other trees
- **Substitution operation**: Replaces frontier nodes

### Mathematical Properties
- **Weak generative capacity**: Mildly context-sensitive
- **Strong generative capacity**: Between CFG and CSG
- **Recognition complexity**: O(n⁶) worst case

### Example TAG Derivation
```
Initial tree: [S [NP John] [VP [V sleeps]]]
Auxiliary tree: [VP [Adv often] [VP* ]]
Result: [S [NP John] [VP [Adv often] [VP [V sleeps]]]]
```

## Computational Complexity

### Recognition Problems

| Grammar Class | Recognition Time | Memory Model |
|---------------|------------------|--------------|
| Regular | O(n) | Finite automaton |
| Context-free | O(n³) | Push-down automaton |
| TAG | O(n⁶) | Embedded push-down |
| Context-sensitive | PSPACE-complete | Linear-bounded |

### Parsing Algorithms

**Earley Parser** (Context-free):
```
Chart[i,j] = {A → α • β | A derives span from i to j}
```

**CKY Algorithm**:
```
For each span length l = 1 to n:
  For each start position i:
    For each split point k:
      Combine(i,k) ∪ Combine(k,j) → Combine(i,j)
```

## Feature-Based Grammars

### Head-Driven Phrase Structure Grammar (HPSG)

Uses typed feature structures:
```
[PHON: "cats"
 HEAD: [AGR: [NUM: pl]]
 SUBCAT: ⟨⟩]
```

### Lexical Functional Grammar (LFG)

Separates constituent structure (c-structure) from functional structure (f-structure):
```
C-structure: [S [NP Mary] [VP [V sees] [NP John]]]
F-structure: [PRED: 'see⟨SUBJ,OBJ⟩'
              SUBJ: [PRED: 'Mary']
              OBJ: [PRED: 'John']]
```

## Universal Grammar as Mathematical Object

### The Minimalist View
All syntactic computation reduces to:
```
⟨PHON-F, SYN-F, SEM-F, Select, Merge, Transfer⟩
```

Where Merge(x,y) = {x,y} provides the recursive engine.

### Formal Properties
- **Closure**: Merge output can re-enter Merge
- **Compositionality**: Meaning determined by constituent meanings
- **Displacement**: Move operations create dependencies
- **Phases**: Computational domains for Transfer operations

## Connection to Automata Theory

### Push-Down Automata and Context-Free Grammars
**Equivalence**: Every CFG has an equivalent PDA, and vice versa.

**Stack operations**:
- Push symbols for left-recursive rules
- Pop symbols for right-recursive completion
- Empty stack indicates successful parse

### The Role of Memory
Different grammar classes require different memory architectures:
- **Regular**: Finite memory (current state)
- **Context-free**: Stack memory (LIFO)
- **Mildly context-sensitive**: Multiple stacks or tree stack
- **Context-sensitive**: Tape memory (bounded)

This mathematical progression from simple to complex memory models parallels the evolution from basic pattern recognition to human-level language understanding.