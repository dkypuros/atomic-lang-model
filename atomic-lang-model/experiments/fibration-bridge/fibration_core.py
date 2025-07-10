#!/usr/bin/env python3
"""
Fibration Core
==============

Core implementation of Grothendieck fibration for relating pure grammar 
and empirical NLP layers. This provides the mathematical machinery to
cleanly separate syntax from statistics while maintaining compositionality.

The key insight: Every empirical annotation "lives over" exactly one 
syntactic object, with coherent pull-back/push-forward operations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List, Optional, Generic, TypeVar
from dataclasses import dataclass
import json

# Type variables for generic fibration
BaseObj = TypeVar('BaseObj')  # Objects in base category (trees)
FibreData = TypeVar('FibreData')  # Data in fibres (probs, vectors, etc)

@dataclass
class TreeNode:
    """Basic tree structure for base category objects."""
    id: str
    label: str
    children: List['TreeNode']
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'label': self.label,
            'children': [c.to_dict() for c in self.children]
        }
    
    @classmethod
    def from_dict(cls, d: Dict) -> 'TreeNode':
        return cls(
            id=d['id'],
            label=d['label'],
            children=[cls.from_dict(c) for c in d.get('children', [])]
        )

@dataclass
class Morphism:
    """Morphism in base category (tree homomorphism)."""
    source_id: str
    target_id: str
    mapping: Dict[str, str]  # node_id -> node_id
    
    def compose(self, other: 'Morphism') -> 'Morphism':
        """Composition of morphisms."""
        if self.target_id != other.source_id:
            raise ValueError("Cannot compose: target != source")
        
        # Compose mappings
        new_mapping = {}
        for k, v in self.mapping.items():
            if v in other.mapping:
                new_mapping[k] = other.mapping[v]
        
        return Morphism(
            source_id=self.source_id,
            target_id=other.target_id,
            mapping=new_mapping
        )

class Fibre(ABC, Generic[FibreData]):
    """
    Abstract base class for fibres.
    
    A fibre provides empirical data (probabilities, embeddings, proofs)
    that lives over syntactic objects, with coherent pull/push operations.
    """
    
    @abstractmethod
    def pull(self, morphism: Morphism, target_data: FibreData) -> FibreData:
        """
        Pull back data along a morphism.
        
        Given f: A → B and data over B, compute data over A.
        This is the *cartesian* operation that makes substitution work.
        """
        pass
    
    @abstractmethod
    def push(self, morphism: Morphism, source_data: FibreData) -> FibreData:
        """
        Push forward data along a morphism.
        
        Given f: A → B and data over A, compute data over B.
        """
        pass
    
    @abstractmethod
    def combine(self, data1: FibreData, data2: FibreData, 
                operation: str) -> FibreData:
        """
        Combine data from two fibres (e.g., when merging subtrees).
        
        Operation could be 'merge', 'move', etc. based on grammar rules.
        """
        pass
    
    @abstractmethod
    def identity_data(self, tree: TreeNode) -> FibreData:
        """Create identity/neutral data for a tree."""
        pass

class GrammarFibration:
    """
    Main fibration class connecting base category and fibres.
    
    This implements the Grothendieck construction, managing:
    - Base category: syntactic trees and their morphisms
    - Total category: trees with empirical annotations
    - Fibration: the projection and cartesian structure
    """
    
    def __init__(self):
        self.trees: Dict[str, TreeNode] = {}
        self.morphisms: Dict[Tuple[str, str], Morphism] = {}
        self.annotations: Dict[str, Dict[str, Any]] = {}
        
    def add_tree(self, tree: TreeNode) -> str:
        """Add a tree to the base category."""
        self.trees[tree.id] = tree
        return tree.id
    
    def add_morphism(self, morphism: Morphism) -> None:
        """Add a morphism to the base category."""
        key = (morphism.source_id, morphism.target_id)
        self.morphisms[key] = morphism
    
    def annotate(self, tree_id: str, fibre_name: str, data: Any, 
                 instance_id: Optional[str] = None) -> None:
        """
        Attach fibre data to a tree.
        
        Args:
            tree_id: ID of the tree to annotate
            fibre_name: Name of the fibre type
            data: The annotation data
            instance_id: Optional instance identifier to avoid key clashes
        """
        if tree_id not in self.annotations:
            self.annotations[tree_id] = {}
        
        # Use instance_id if provided to avoid clashes
        key = f"{fibre_name}:{instance_id}" if instance_id else fibre_name
        self.annotations[tree_id][key] = data
    
    def get_annotation(self, tree_id: str, fibre_name: str) -> Optional[Any]:
        """Retrieve fibre data for a tree."""
        return self.annotations.get(tree_id, {}).get(fibre_name)
    
    def parse_with_fibre(self, sentence: str, fibre: Fibre[FibreData]) -> Tuple[TreeNode, FibreData]:
        """
        Parse a sentence and compute fibre data compositionally.
        
        This demonstrates the key advantage: parsing and empirical
        enrichment happen together, with fibration ensuring coherence.
        """
        # This is a simplified example - real implementation would use
        # the full grammar from tiny_lm.py
        
        tokens = sentence.split()
        
        # Build parse tree bottom-up (simplified)
        leaves = []
        for i, token in enumerate(tokens):
            leaf = TreeNode(
                id=f"leaf_{i}",
                label=token,
                children=[]
            )
            self.add_tree(leaf)
            leaves.append(leaf)
        
        # Combine leaves (simplified binary tree)
        current_level = leaves
        level_num = 0
        
        while len(current_level) > 1:
            next_level = []
            
            for i in range(0, len(current_level) - 1, 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else None
                
                if right:
                    # Create parent node
                    parent = TreeNode(
                        id=f"node_{level_num}_{i//2}",
                        label="merge",
                        children=[left, right]
                    )
                    self.add_tree(parent)
                    
                    # Create morphisms for the merge
                    left_morph = Morphism(
                        source_id=left.id,
                        target_id=parent.id,
                        mapping={left.id: parent.id}
                    )
                    right_morph = Morphism(
                        source_id=right.id,
                        target_id=parent.id,
                        mapping={right.id: parent.id}
                    )
                    
                    self.add_morphism(left_morph)
                    self.add_morphism(right_morph)
                    
                    # Compute fibre data compositionally
                    left_data = self.get_annotation(left.id, fibre.__class__.__name__)
                    right_data = self.get_annotation(right.id, fibre.__class__.__name__)
                    
                    if left_data is None:
                        left_data = fibre.identity_data(left)
                        self.annotate(left.id, fibre.__class__.__name__, left_data)
                    
                    if right_data is None:
                        right_data = fibre.identity_data(right)
                        self.annotate(right.id, fibre.__class__.__name__, right_data)
                    
                    # Combine data
                    parent_data = fibre.combine(left_data, right_data, 'merge')
                    self.annotate(parent.id, fibre.__class__.__name__, parent_data)
                    
                    next_level.append(parent)
                else:
                    next_level.append(left)
            
            # Handle odd number of nodes
            if len(current_level) % 2 == 1:
                next_level.append(current_level[-1])
            
            current_level = next_level
            level_num += 1
        
        # Return root and its fibre data
        root = current_level[0]
        root_data = self.get_annotation(root.id, fibre.__class__.__name__)
        
        return root, root_data
    
    def substitute(self, tree_id: str, subtree_id: str, 
                   new_subtree: TreeNode, fibre: Fibre[FibreData]) -> Tuple[TreeNode, FibreData]:
        """
        Substitute a subtree and coherently update fibre data.
        
        This demonstrates the key property of fibrations: when we
        modify syntax, empirical data updates automatically and coherently.
        """
        # Get original tree
        tree = self.trees[tree_id]
        
        # Create new tree with substitution (simplified)
        new_tree = self._substitute_tree(tree, subtree_id, new_subtree)
        new_tree.id = f"{tree_id}_subst"
        self.add_tree(new_tree)
        
        # Create substitution morphism
        morph = Morphism(
            source_id=new_tree.id,
            target_id=tree_id,
            mapping={new_tree.id: tree_id}  # Simplified
        )
        self.add_morphism(morph)
        
        # Pull back fibre data
        original_data = self.get_annotation(tree_id, fibre.__class__.__name__)
        if original_data:
            new_data = fibre.pull(morph, original_data)
            self.annotate(new_tree.id, fibre.__class__.__name__, new_data)
            return new_tree, new_data
        else:
            return new_tree, fibre.identity_data(new_tree)
    
    def _substitute_tree(self, tree: TreeNode, target_id: str, 
                         new_subtree: TreeNode) -> TreeNode:
        """Helper to perform tree substitution."""
        if tree.id == target_id:
            return new_subtree
        
        new_children = [
            self._substitute_tree(child, target_id, new_subtree)
            for child in tree.children
        ]
        
        return TreeNode(
            id=tree.id,
            label=tree.label,
            children=new_children
        )
    
    def verify_functoriality(self, f: Morphism, g: Morphism, 
                            fibre: Fibre[FibreData], data: FibreData) -> bool:
        """
        Verify that pull-back respects composition:
        pull(g∘f, data) = pull(f, pull(g, data))
        
        This is a key coherence property of fibrations.
        """
        # Compose morphisms
        gf = f.compose(g)
        
        # Method 1: Pull back along composition
        result1 = fibre.pull(gf, data)
        
        # Method 2: Pull back in sequence
        temp = fibre.pull(g, data)
        result2 = fibre.pull(f, temp)
        
        # In a proper implementation, we'd define equality for fibre data
        # For now, we'll assume they're equal if string representations match
        return str(result1) == str(result2)
    
    def to_json(self) -> str:
        """Export fibration to JSON for visualization."""
        return json.dumps({
            'trees': {k: v.to_dict() for k, v in self.trees.items()},
            'morphisms': [
                {
                    'source': m.source_id,
                    'target': m.target_id,
                    'mapping': m.mapping
                }
                for m in self.morphisms.values()
            ],
            'annotations': self.annotations
        }, indent=2)


def demo_fibration():
    """Demonstrate basic fibration usage."""
    print("🔬 Grothendieck Fibration Demo")
    print("=" * 50)
    
    # Create fibration
    fib = GrammarFibration()
    
    # Create a simple tree
    tree = TreeNode(
        id="root",
        label="S",
        children=[
            TreeNode(id="np", label="NP", children=[
                TreeNode(id="det", label="the", children=[]),
                TreeNode(id="n", label="student", children=[])
            ]),
            TreeNode(id="vp", label="VP", children=[
                TreeNode(id="v", label="left", children=[])
            ])
        ]
    )
    
    fib.add_tree(tree)
    print(f"Added tree: {tree.label}")
    print(f"Tree structure: {json.dumps(tree.to_dict(), indent=2)}")
    
    # The magic happens when we add fibres (see probability_fibre.py)
    print("\n✨ The fibration structure allows clean separation of:")
    print("  - Syntax (base category)")
    print("  - Statistics (fibres)")
    print("  - With coherent composition!")


if __name__ == "__main__":
    demo_fibration()