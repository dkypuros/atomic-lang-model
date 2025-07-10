#!/usr/bin/env python3
"""
Base Category
=============

The base category B consists of syntactic objects (derivation trees)
and structure-preserving morphisms between them. This is the pure,
mathematical side of our fibration - no probabilities or empirical
data, just tree structures and their relationships.
"""

from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Import grammar rules from main implementation
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'python'))
from tiny_lm import PG_RULES

@dataclass
class Feature:
    """Syntactic feature (simplified from Rust implementation)."""
    name: str
    value: str
    
@dataclass 
class SyntacticObject:
    """Core syntactic object in minimalist grammar."""
    label: str
    features: List[Feature]
    left_child: Optional['SyntacticObject'] = None
    right_child: Optional['SyntacticObject'] = None
    
    def to_tree_node(self, id_prefix: str = "") -> 'TreeNode':
        """Convert to generic tree node for fibration."""
        from fibration_core import TreeNode
        
        node_id = f"{id_prefix}_{self.label}_{id(self)}"
        children = []
        
        if self.left_child:
            children.append(self.left_child.to_tree_node(f"{id_prefix}_L"))
        if self.right_child:
            children.append(self.right_child.to_tree_node(f"{id_prefix}_R"))
            
        return TreeNode(id=node_id, label=self.label, children=children)

class BaseCategory:
    """
    The base category of syntactic derivations.
    
    Objects: Derivation trees
    Morphisms: Structure-preserving maps (tree homomorphisms)
    
    This provides the pure syntactic backbone that fibres enrich.
    """
    
    def __init__(self):
        self.grammar_rules = self._convert_pg_rules()
        
    def _convert_pg_rules(self) -> Dict[str, List[List[str]]]:
        """Convert probabilistic rules to pure syntactic rules."""
        pure_rules = {}
        for lhs, productions in PG_RULES.items():
            pure_rules[lhs] = [rhs for _, rhs in productions]
        return pure_rules
    
    def merge(self, obj1: SyntacticObject, obj2: SyntacticObject) -> Optional[SyntacticObject]:
        """
        Merge operation from Minimalist Grammar.
        
        This is the pure syntactic operation - no probabilities involved.
        """
        # Simplified merge: check if obj1 selects category of obj2
        for feature in obj1.features:
            if feature.name == "sel" and feature.value == obj2.label:
                # Create merged object
                return SyntacticObject(
                    label=obj1.label,
                    features=[f for f in obj1.features if f.name != "sel"],
                    left_child=obj1,
                    right_child=obj2
                )
        return None
    
    def move(self, obj: SyntacticObject, feature: str) -> Optional[SyntacticObject]:
        """
        Move operation for handling displacement.
        
        Again, pure syntax - the empirical aspects live in fibres.
        """
        # Simplified: would implement proper movement here
        return obj
    
    def is_complete(self, obj: SyntacticObject) -> bool:
        """Check if derivation is complete (no outstanding features)."""
        return len(obj.features) == 0
    
    def derive_all(self, tokens: List[str], max_derivations: int = 10) -> List[SyntacticObject]:
        """
        Generate all possible derivations for a token sequence.
        
        This gives us the base objects that fibres can annotate.
        """
        # Simplified: in reality would use CKY or similar
        derivations = []
        
        # For demo, create a simple left-branching structure
        if not tokens:
            return []
            
        current = SyntacticObject(label=tokens[0], features=[])
        
        for token in tokens[1:]:
            next_obj = SyntacticObject(label=token, features=[])
            current = SyntacticObject(
                label="merge",
                features=[],
                left_child=current,
                right_child=next_obj
            )
            
        derivations.append(current)
        return derivations[:max_derivations]

class TreeMorphism:
    """
    Morphism in the base category (tree homomorphism).
    
    These preserve tree structure and are used for:
    - Subtree substitution
    - Tree composition  
    - Adjunction operations
    """
    
    def __init__(self, source: SyntacticObject, target: SyntacticObject):
        self.source = source
        self.target = target
        self.node_mapping: Dict[int, int] = {}
        
    def is_structure_preserving(self) -> bool:
        """Verify this is a valid tree homomorphism."""
        # Check that parent-child relationships are preserved
        # Simplified for demo
        return True
    
    def compose(self, other: 'TreeMorphism') -> 'TreeMorphism':
        """Composition of tree morphisms."""
        if id(self.target) != id(other.source):
            raise ValueError("Cannot compose: target != source")
            
        composed = TreeMorphism(self.source, other.target)
        # Compose the node mappings
        for src, mid in self.node_mapping.items():
            if mid in other.node_mapping:
                composed.node_mapping[src] = other.node_mapping[mid]
                
        return composed

class BaseCategoryOps:
    """Operations in the base category."""
    
    @staticmethod
    def graft(tree: SyntacticObject, position: str, 
              subtree: SyntacticObject) -> Tuple[SyntacticObject, TreeMorphism]:
        """
        Graft a subtree at a position.
        
        Returns the new tree and the morphism from new to old.
        """
        # Implementation would traverse tree to find position
        # and create appropriate morphism
        pass
    
    @staticmethod
    def prune(tree: SyntacticObject, position: str) -> Tuple[SyntacticObject, TreeMorphism]:
        """
        Remove a subtree.
        
        Returns the pruned tree and morphism.
        """
        pass
    
    @staticmethod
    def adjoin(tree: SyntacticObject, position: str,
               auxiliary: SyntacticObject) -> Tuple[SyntacticObject, TreeMorphism]:
        """
        Tree adjunction operation.
        
        Used for modifiers and recursive structures.
        """
        pass


def demo_base_category():
    """Demonstrate base category operations."""
    print("🌳 Base Category Demo")
    print("=" * 50)
    
    base = BaseCategory()
    
    # Create some syntactic objects
    the = SyntacticObject(label="D", features=[])
    student = SyntacticObject(label="N", features=[])
    left = SyntacticObject(label="V", features=[])
    
    print("Created syntactic objects:")
    print(f"  - {the.label}: 'the'")
    print(f"  - {student.label}: 'student'") 
    print(f"  - {left.label}: 'left'")
    
    # Derive a simple sentence
    derivations = base.derive_all(["the", "student", "left"])
    print(f"\nDerived {len(derivations)} tree(s) for 'the student left'")
    
    if derivations:
        tree = derivations[0]
        print(f"Tree structure: {tree.label}")
        print("  (In a real implementation, this would be a proper syntax tree)")
    
    print("\n✨ This pure syntactic layer is enriched by fibres for:")
    print("  - Probabilities (probability_fibre.py)")
    print("  - Embeddings (embedding_fibre.py)")
    print("  - Proofs (proof_fibre.py)")


if __name__ == "__main__":
    demo_base_category()