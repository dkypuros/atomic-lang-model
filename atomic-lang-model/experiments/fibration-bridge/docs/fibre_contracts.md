# Fibre Contracts and Invariants

This document specifies the expected invariants and contracts that all fibres must satisfy to maintain the categorical coherence of the Grothendieck fibration.

## Core Fibre Interface

Every fibre must implement these four operations with the following contracts:

### 1. `identity_data(tree: TreeNode) -> FibreData`
**Contract**: Create neutral/identity data for a tree node.
- For leaves: May compute non-trivial data based on node label
- For internal nodes: Should return a neutral element suitable for combination
- Must be deterministic for the same input

### 2. `pull(morphism: Morphism, target_data: FibreData) -> FibreData`
**Contract**: Pull back data along a morphism (cartesian lift).
- Must preserve the "essential content" of the data
- For probability fibres: Total probability mass should be preserved (or explicitly filtered)
- For embedding fibres: Dimension reduction should preserve relative distances
- For proof fibres: Weakening is allowed but not strengthening
- Must satisfy functoriality: `pull(g∘f, data) = pull(f, pull(g, data))`

### 3. `push(morphism: Morphism, source_data: FibreData) -> FibreData`
**Contract**: Push forward data along a morphism.
- Dual to pull-back
- May extend/enrich data for the larger context
- Should be "conservative" - not add information not implicit in source

### 4. `combine(data1: FibreData, data2: FibreData, operation: str) -> FibreData`
**Contract**: Combine data from two sources based on syntactic operation.
- Operation types: 'merge', 'move', others as needed
- Must be associative for 'merge': `combine(a, combine(b, c)) = combine(combine(a, b), c)`
- Should preserve invariants of the data type

## Specific Fibre Invariants

### ProbabilityFibre
- **Invariant**: Probability distributions must sum to 1.0 (±ε for floating point)
- **Pull-back**: Must preserve total probability mass
- **Combine**: Product for independence, weighted sum for alternatives

### EmbeddingFibre
- **Invariant**: Vectors must have consistent dimension within a parse
- **Pull-back**: Dimension reduction must be linear/projective
- **Combine**: Must preserve metric properties (distances)

### ProofFibre
- **Invariant**: Proof status can only weaken, never strengthen without evidence
- **Pull-back**: PROVEN → ASSUMED, others preserved or weakened
- **Combine**: Take weakest status, union dependencies

### BM25Fibre
- **Invariant**: Scores must be non-negative
- **Pull-back**: Scores generally preserved (IR is syntax-invariant)
- **Combine**: Additive for AND, max for OR, weighted for general

## Testing Requirements

Every fibre implementation should include tests for:

1. **Identity laws**: 
   - `combine(identity_data(tree), data) = data`
   - `combine(data, identity_data(tree)) = data`

2. **Functoriality**:
   - `pull(id, data) = data`
   - `pull(g∘f, data) = pull(f, pull(g, data))`

3. **Invariant preservation**:
   - All operations maintain the fibre's specific invariants
   - No operation violates the data type's constraints

## Adding New Fibres

When implementing a new fibre:

1. Define the data type and its invariants
2. Implement the four required operations
3. Document any operation-specific behaviors
4. Add tests for identity, functoriality, and invariants
5. Update this document with the new fibre's contract

## Performance Considerations

- `identity_data`: Should be O(1) or O(node_size)
- `pull/push`: Should be at most O(data_size)
- `combine`: Should be at most O(data1_size + data2_size)
- Caching/memoization is encouraged for expensive computations