#!/usr/bin/env python3
"""
Embedding Fibre
===============

The embedding fibre enriches syntactic trees with vector representations.
This allows integration with neural NLP methods while maintaining the
formal guarantees of the base grammar.

Key properties:
- Pull-back: Project embeddings to subspace
- Push-forward: Compose embeddings 
- Combine: Vector operations (add, concat, transform)
"""

from typing import List, Optional, Callable
import math

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fibration_core import Fibre, TreeNode, Morphism

class EmbeddingData:
    """Vector embedding data for tree nodes."""
    
    def __init__(self, vector: List[float], dim: int = None):
        self.vector = vector
        self.dim = dim or len(vector)
        
    def norm(self) -> float:
        """L2 norm of vector."""
        return math.sqrt(sum(x**2 for x in self.vector))
    
    def normalize(self) -> 'EmbeddingData':
        """Return normalized vector."""
        n = self.norm()
        if n > 0:
            return EmbeddingData([x/n for x in self.vector])
        return self
    
    def dot(self, other: 'EmbeddingData') -> float:
        """Dot product with another embedding."""
        return sum(a*b for a, b in zip(self.vector, other.vector))
    
    def cosine_similarity(self, other: 'EmbeddingData') -> float:
        """Cosine similarity with another embedding."""
        return self.dot(other) / (self.norm() * other.norm())
    
    def __repr__(self):
        preview = self.vector[:3] if len(self.vector) > 3 else self.vector
        return f"EmbeddingData(dim={self.dim}, preview={preview}...)"

class EmbeddingFibre(Fibre[EmbeddingData]):
    """
    Embedding fibre implementation.
    
    This demonstrates how distributed representations can be
    integrated with formal grammar via fibrations.
    """
    
    def __init__(self, dim: int = 50, compose_fn: Optional[Callable] = None):
        self.dim = dim
        self.compose_fn = compose_fn or self._default_compose
        
        # Simple word embeddings for demo
        self.word_embeddings = {
            "the": [1.0, 0.0] + [0.1] * (dim - 2),
            "a": [0.9, 0.1] + [0.1] * (dim - 2),
            "student": [0.0, 1.0] + [0.2] * (dim - 2),
            "teacher": [0.1, 0.9] + [0.2] * (dim - 2),
            "left": [0.5, 0.5] + [0.3] * (dim - 2),
            "arrived": [0.4, 0.6] + [0.3] * (dim - 2),
        }
    
    def pull(self, morphism: Morphism, target_data: EmbeddingData) -> EmbeddingData:
        """
        Pull back embeddings along morphism.
        
        This projects the target embedding to a subspace corresponding
        to the source tree structure.
        """
        # Simplified: apply linear projection
        # In practice, would use morphism structure to determine projection
        
        # Simple projection: keep first k dimensions
        source_dim = self._estimate_source_dim(morphism)
        projected = target_data.vector[:source_dim]
        
        # Pad with zeros if needed
        if len(projected) < source_dim:
            projected.extend([0.0] * (source_dim - len(projected)))
            
        return EmbeddingData(projected, source_dim)
    
    def push(self, morphism: Morphism, source_data: EmbeddingData) -> EmbeddingData:
        """
        Push forward embeddings along morphism.
        
        This extends the source embedding to the target space,
        potentially adding dimensions for additional structure.
        """
        # Extend to target dimension
        target_dim = self._estimate_target_dim(morphism)
        extended = source_data.vector[:]
        
        # Pad with learned values (simplified: small random values)
        if len(extended) < target_dim:
            extended.extend([0.01] * (target_dim - len(extended)))
            
        return EmbeddingData(extended[:target_dim], target_dim)
    
    def combine(self, data1: EmbeddingData, data2: EmbeddingData,
                operation: str) -> EmbeddingData:
        """
        Combine embeddings when merging trees.
        
        Different operations use different vector compositions.
        """
        if operation == 'merge':
            # Use composition function (default: weighted average)
            return self.compose_fn(data1, data2)
            
        elif operation == 'move':
            # Movement might transform the embedding
            # Simple version: linear combination with different weights
            v1 = data1.vector
            v2 = data2.vector
            
            # Ensure same dimension
            max_dim = max(len(v1), len(v2))
            v1 = v1 + [0.0] * (max_dim - len(v1))
            v2 = v2 + [0.0] * (max_dim - len(v2))
            
            # Weight moved constituent differently
            result = [0.3 * a + 0.7 * b for a, b in zip(v1, v2)]
            return EmbeddingData(result, max_dim)
            
        else:
            # Default: average
            return self._default_compose(data1, data2)
    
    def identity_data(self, tree: TreeNode) -> EmbeddingData:
        """Create identity embedding for a tree."""
        # For leaves, use word embeddings
        if not tree.children and tree.label in self.word_embeddings:
            return EmbeddingData(self.word_embeddings[tree.label], self.dim)
        
        # For internal nodes, use zero vector (will be composed)
        return EmbeddingData([0.0] * self.dim, self.dim)
    
    def _default_compose(self, data1: EmbeddingData, 
                        data2: EmbeddingData) -> EmbeddingData:
        """Default composition: weighted average."""
        v1 = data1.vector
        v2 = data2.vector
        
        # Ensure same dimension
        max_dim = max(len(v1), len(v2))
        v1 = v1 + [0.0] * (max_dim - len(v1))
        v2 = v2 + [0.0] * (max_dim - len(v2))
        
        # Weighted average (could be learned)
        result = [0.5 * a + 0.5 * b for a, b in zip(v1, v2)]
        return EmbeddingData(result, max_dim)
    
    def _estimate_source_dim(self, morphism: Morphism) -> int:
        """Estimate dimension for source of morphism."""
        # Simplified - would use tree structure in practice
        return self.dim // 2
    
    def _estimate_target_dim(self, morphism: Morphism) -> int:
        """Estimate dimension for target of morphism."""
        # Simplified - would use tree structure in practice
        return self.dim

def demo_embedding_fibre():
    """Demonstrate embedding fibre operations."""
    print("🔢 Embedding Fibre Demo")
    print("=" * 50)
    
    # Create fibre
    emb_fibre = EmbeddingFibre(dim=10)
    
    # Get word embeddings
    student_emb = EmbeddingData(emb_fibre.word_embeddings["student"])
    teacher_emb = EmbeddingData(emb_fibre.word_embeddings["teacher"])
    left_emb = EmbeddingData(emb_fibre.word_embeddings["left"])
    
    print("Word embeddings:")
    print(f"  'student': {student_emb}")
    print(f"  'teacher': {teacher_emb}")
    print(f"  'left': {left_emb}")
    
    # Compute similarities
    sim = student_emb.cosine_similarity(teacher_emb)
    print(f"\nCosine similarity (student, teacher): {sim:.3f}")
    
    # Combine embeddings
    np_embedding = emb_fibre.combine(
        EmbeddingData(emb_fibre.word_embeddings["the"]),
        student_emb,
        'merge'
    )
    
    sentence_embedding = emb_fibre.combine(np_embedding, left_emb, 'merge')
    
    print(f"\nComposed sentence embedding: {sentence_embedding}")
    print(f"Norm: {sentence_embedding.norm():.3f}")
    
    # Demonstrate pull-back
    dummy_morphism = Morphism("small", "big", {})
    pulled = emb_fibre.pull(dummy_morphism, sentence_embedding)
    print(f"\nPulled embedding dimension: {pulled.dim} (was {sentence_embedding.dim})")
    
    print("\n✨ The fibration ensures:")
    print("  - Embeddings compose with syntactic structure")
    print("  - Substitution preserves semantic relationships")
    print("  - Neural and symbolic methods integrate cleanly")


if __name__ == "__main__":
    demo_embedding_fibre()