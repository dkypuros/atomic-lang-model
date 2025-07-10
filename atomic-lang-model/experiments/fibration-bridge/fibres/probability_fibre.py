#!/usr/bin/env python3
"""
Probability Fibre
=================

The probability fibre enriches syntactic trees with statistical weights.
This is the most natural starting point since it directly extends our
existing probabilistic grammar implementation.

Key properties:
- Pull-back: Restrict probability distribution to subtree
- Push-forward: Extend local probabilities to larger context
- Combine: Multiply probabilities (for independence) or more complex ops
"""

from typing import Dict, List, Tuple
from collections import defaultdict
import math

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fibration_core import Fibre, TreeNode, Morphism

class ProbabilityData:
    """Probability distribution over tree yield (terminal strings)."""
    
    def __init__(self, distribution: Dict[str, float] = None):
        self.distribution = distribution or {}
        self._normalize()
    
    def _normalize(self):
        """Normalize to ensure probabilities sum to 1."""
        total = sum(self.distribution.values())
        if total > 0:
            self.distribution = {k: v/total for k, v in self.distribution.items()}
    
    def entropy(self) -> float:
        """Calculate entropy of distribution."""
        h = 0.0
        for p in self.distribution.values():
            if p > 0:
                h -= p * math.log2(p)
        return h
    
    def top_k(self, k: int) -> List[Tuple[str, float]]:
        """Get top k most probable yields."""
        sorted_items = sorted(self.distribution.items(), 
                            key=lambda x: x[1], reverse=True)
        return sorted_items[:k]
    
    def __repr__(self):
        top = self.top_k(3)
        return f"ProbabilityData({top}...)"

class ProbabilityFibre(Fibre[ProbabilityData]):
    """
    Probability fibre implementation.
    
    This shows how the abstract fibration structure specializes
    to the concrete case of probabilistic parsing.
    """
    
    def __init__(self, smoothing: float = 1e-6):
        self.smoothing = smoothing
        
    def pull(self, morphism: Morphism, target_data: ProbabilityData) -> ProbabilityData:
        """
        Pull back probability distribution along morphism.
        
        Example: If we have P(yield|big_tree) and f: small_tree → big_tree,
        compute P(yield|small_tree) by restriction.
        """
        # In a full implementation, we'd trace which yields are reachable
        # through the morphism. For now, simplified:
        
        pulled_dist = {}
        
        # Filter to yields compatible with source tree structure
        for yield_str, prob in target_data.distribution.items():
            # Simplified: keep yields that could come from source
            # Real implementation would check morphism mapping
            if self._is_compatible_yield(yield_str, morphism):
                pulled_dist[yield_str] = prob
                
        return ProbabilityData(pulled_dist)
    
    def push(self, morphism: Morphism, source_data: ProbabilityData) -> ProbabilityData:
        """
        Push forward probability distribution along morphism.
        
        Example: If we have P(yield|small_tree) and f: small_tree → big_tree,
        extend to P(yield|big_tree) by composition with other subtrees.
        """
        pushed_dist = defaultdict(float)
        
        # For each yield from source, compute possible yields in target
        for src_yield, src_prob in source_data.distribution.items():
            # Get all possible target yields (simplified)
            target_yields = self._get_target_yields(src_yield, morphism)
            
            # Distribute probability (uniform for simplicity)
            for target_yield in target_yields:
                pushed_dist[target_yield] += src_prob / len(target_yields)
                
        return ProbabilityData(dict(pushed_dist))
    
    def combine(self, data1: ProbabilityData, data2: ProbabilityData, 
                operation: str) -> ProbabilityData:
        """
        Combine probability data when merging trees.
        
        For 'merge' operation, this computes P(yield | tree1 ⊕ tree2).
        """
        combined_dist = defaultdict(float)
        
        if operation == 'merge':
            # Combine yields by concatenation (simplified)
            for yield1, prob1 in data1.distribution.items():
                for yield2, prob2 in data2.distribution.items():
                    combined_yield = f"{yield1} {yield2}".strip()
                    combined_dist[combined_yield] += prob1 * prob2
                    
        elif operation == 'move':
            # Movement changes word order - simplified version
            for yield_str, prob in data1.distribution.items():
                tokens = yield_str.split()
                if len(tokens) >= 2:
                    # Simple movement: swap first two tokens
                    moved = f"{tokens[1]} {tokens[0]}" + " ".join(tokens[2:])
                    combined_dist[moved] += prob * 0.5
                    combined_dist[yield_str] += prob * 0.5
                else:
                    combined_dist[yield_str] += prob
                    
        return ProbabilityData(dict(combined_dist))
    
    def identity_data(self, tree: TreeNode) -> ProbabilityData:
        """Create identity probability data for a tree."""
        # For a leaf, probability 1.0 on its label
        if not tree.children:
            return ProbabilityData({tree.label: 1.0})
        
        # For internal nodes, uniform distribution (simplified)
        return ProbabilityData({"": 1.0})
    
    def _is_compatible_yield(self, yield_str: str, morphism: Morphism) -> bool:
        """Check if yield is compatible with source of morphism."""
        # Simplified - real implementation would check tree structure
        return True
    
    def _get_target_yields(self, src_yield: str, morphism: Morphism) -> List[str]:
        """Get possible target yields for a source yield."""
        # Simplified - real implementation would use morphism mapping
        return [src_yield, f"extended_{src_yield}"]

def demo_probability_fibre():
    """Demonstrate probability fibre operations."""
    print("📊 Probability Fibre Demo")
    print("=" * 50)
    
    # Create fibre
    prob_fibre = ProbabilityFibre()
    
    # Create some probability data
    data1 = ProbabilityData({
        "the student": 0.6,
        "a student": 0.3,
        "the teacher": 0.1
    })
    
    data2 = ProbabilityData({
        "left": 0.5,
        "arrived": 0.3,
        "smiled": 0.2
    })
    
    print("Data 1 (noun phrases):")
    for yield_str, prob in data1.top_k(5):
        print(f"  '{yield_str}': {prob:.3f}")
    
    print("\nData 2 (verb phrases):")
    for yield_str, prob in data2.top_k(5):
        print(f"  '{yield_str}': {prob:.3f}")
    
    # Combine via merge
    merged = prob_fibre.combine(data1, data2, 'merge')
    print("\nMerged distribution (NP + VP):")
    for yield_str, prob in merged.top_k(5):
        print(f"  '{yield_str}': {prob:.3f}")
    
    print(f"\nEntropy: {merged.entropy():.3f} bits")
    
    # Demonstrate pull-back
    dummy_morphism = Morphism("small", "big", {"a": "b"})
    pulled = prob_fibre.pull(dummy_morphism, merged)
    print(f"\nPulled distribution has {len(pulled.distribution)} entries")
    
    print("\n✨ The fibration ensures:")
    print("  - Probabilities transform coherently with syntax")
    print("  - Substitution preserves probability semantics")
    print("  - Parsing computes probabilities compositionally")


if __name__ == "__main__":
    demo_probability_fibre()