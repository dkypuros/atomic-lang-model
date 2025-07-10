#!/usr/bin/env python3
"""
Proof Fibre
===========

The proof fibre enriches syntactic trees with formal verification data.
This connects to the Coq proofs in the main implementation, showing how
mathematical guarantees can be carried through the fibration.

Key properties:
- Pull-back: Restrict proofs to subtrees
- Push-forward: Extend local proofs to larger contexts
- Combine: Compose proof obligations
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fibration_core import Fibre, TreeNode, Morphism

class ProofStatus(Enum):
    """Status of a proof obligation."""
    PROVEN = "proven"
    ASSUMED = "assumed"
    PENDING = "pending"
    FAILED = "failed"

@dataclass
class ProofObligation:
    """A single proof obligation."""
    property: str
    status: ProofStatus
    evidence: Optional[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class ProofData:
    """Proof data attached to syntactic trees."""
    
    def __init__(self):
        self.obligations: Dict[str, ProofObligation] = {}
        self.invariants: Set[str] = set()
        
    def add_obligation(self, name: str, obligation: ProofObligation):
        """Add a proof obligation."""
        self.obligations[name] = obligation
        
    def add_invariant(self, invariant: str):
        """Add an invariant that holds for this tree."""
        self.invariants.add(invariant)
        
    def is_fully_verified(self) -> bool:
        """Check if all obligations are proven."""
        return all(
            ob.status == ProofStatus.PROVEN 
            for ob in self.obligations.values()
        )
    
    def pending_obligations(self) -> List[str]:
        """Get list of pending obligations."""
        return [
            name for name, ob in self.obligations.items()
            if ob.status == ProofStatus.PENDING
        ]
    
    def __repr__(self):
        proven = sum(1 for ob in self.obligations.values() 
                    if ob.status == ProofStatus.PROVEN)
        total = len(self.obligations)
        return f"ProofData({proven}/{total} proven, {len(self.invariants)} invariants)"

class ProofFibre(Fibre[ProofData]):
    """
    Proof fibre implementation.
    
    This shows how formal verification can be integrated with
    syntactic derivations through the fibration structure.
    """
    
    def __init__(self):
        # Standard properties we might want to prove
        self.standard_properties = [
            "well_formed",
            "feature_checked", 
            "agreement_satisfied",
            "movement_licensed",
            "recursion_bounded"
        ]
    
    def pull(self, morphism: Morphism, target_data: ProofData) -> ProofData:
        """
        Pull back proofs along morphism.
        
        If we have proofs about the target tree, what can we
        conclude about the source tree?
        """
        pulled = ProofData()
        
        # Invariants that are preserved by morphism
        for inv in target_data.invariants:
            if self._invariant_preserved(inv, morphism):
                pulled.add_invariant(inv)
        
        # Pull back relevant obligations
        for name, obligation in target_data.obligations.items():
            if self._obligation_relevant(obligation, morphism):
                # Create restricted version
                pulled_ob = ProofObligation(
                    property=obligation.property,
                    status=obligation.status,
                    evidence=f"Pulled from {obligation.evidence}",
                    dependencies=obligation.dependencies
                )
                pulled.add_obligation(name, pulled_ob)
                
        return pulled
    
    def push(self, morphism: Morphism, source_data: ProofData) -> ProofData:
        """
        Push forward proofs along morphism.
        
        If we have proofs about the source tree, what can we
        conclude about the target tree?
        """
        pushed = ProofData()
        
        # Some invariants lift directly
        for inv in source_data.invariants:
            if self._invariant_lifts(inv, morphism):
                pushed.add_invariant(inv)
        
        # Push forward obligations with weakened status
        for name, obligation in source_data.obligations.items():
            pushed_ob = ProofObligation(
                property=obligation.property,
                status=self._weaken_status(obligation.status),
                evidence=f"Pushed from {obligation.evidence}",
                dependencies=obligation.dependencies + [f"morphism_{morphism.source_id}_to_{morphism.target_id}"]
            )
            pushed.add_obligation(name, pushed_ob)
            
        return pushed
    
    def combine(self, data1: ProofData, data2: ProofData,
                operation: str) -> ProofData:
        """
        Combine proof data when merging trees.
        
        The proof obligations for the combined tree depend on
        the proofs of the constituents.
        """
        combined = ProofData()
        
        if operation == 'merge':
            # Invariants that hold for both
            combined.invariants = data1.invariants.intersection(data2.invariants)
            
            # Combine obligations
            for name, ob1 in data1.obligations.items():
                if name in data2.obligations:
                    ob2 = data2.obligations[name]
                    # Combined status is the weaker of the two
                    combined_status = self._combine_status(ob1.status, ob2.status)
                    combined_ob = ProofObligation(
                        property=ob1.property,
                        status=combined_status,
                        evidence=f"Combined: {ob1.evidence} AND {ob2.evidence}",
                        dependencies=ob1.dependencies + ob2.dependencies
                    )
                    combined.add_obligation(name, combined_ob)
                else:
                    combined.add_obligation(name, ob1)
                    
            # Add obligations only in data2
            for name, ob2 in data2.obligations.items():
                if name not in combined.obligations:
                    combined.add_obligation(name, ob2)
                    
            # Add merge-specific obligations
            merge_ob = ProofObligation(
                property="merge_well_formed",
                status=ProofStatus.PENDING,
                evidence="Requires checking merge conditions"
            )
            combined.add_obligation("merge_wf", merge_ob)
            
        elif operation == 'move':
            # Movement requires additional proofs
            combined.invariants = data1.invariants.copy()
            
            # Copy obligations with movement dependencies
            for name, ob in data1.obligations.items():
                moved_ob = ProofObligation(
                    property=ob.property,
                    status=ProofStatus.PENDING,  # Re-verify after movement
                    evidence=f"Movement from {ob.evidence}",
                    dependencies=ob.dependencies + ["movement_licensed"]
                )
                combined.add_obligation(name, moved_ob)
                
            # Add movement-specific obligation
            move_ob = ProofObligation(
                property="movement_licensed",
                status=ProofStatus.PENDING,
                evidence="Requires checking movement features"
            )
            combined.add_obligation("movement", move_ob)
            
        return combined
    
    def identity_data(self, tree: TreeNode) -> ProofData:
        """Create identity proof data for a tree."""
        data = ProofData()
        
        # Basic well-formedness obligation
        wf_ob = ProofObligation(
            property="well_formed",
            status=ProofStatus.PENDING,
            evidence=f"Tree {tree.id} well-formedness"
        )
        data.add_obligation("well_formed", wf_ob)
        
        # For leaves, automatically proven
        if not tree.children:
            wf_ob.status = ProofStatus.PROVEN
            wf_ob.evidence = "Leaf nodes are trivially well-formed"
            data.add_invariant("is_leaf")
            
        return data
    
    def _invariant_preserved(self, invariant: str, morphism: Morphism) -> bool:
        """Check if invariant is preserved by morphism."""
        # Simplified - would check morphism properties
        return invariant in ["well_formed", "feature_checked"]
    
    def _invariant_lifts(self, invariant: str, morphism: Morphism) -> bool:
        """Check if invariant lifts along morphism."""
        # Some invariants always lift
        return invariant == "is_leaf"
    
    def _obligation_relevant(self, obligation: ProofObligation, 
                           morphism: Morphism) -> bool:
        """Check if obligation is relevant to morphism source."""
        # Simplified - would check morphism structure
        return True
    
    def _weaken_status(self, status: ProofStatus) -> ProofStatus:
        """Weaken proof status when pushing forward."""
        if status == ProofStatus.PROVEN:
            return ProofStatus.ASSUMED
        return status
    
    def _combine_status(self, status1: ProofStatus, 
                       status2: ProofStatus) -> ProofStatus:
        """Combine two proof statuses (take weaker)."""
        priority = [ProofStatus.FAILED, ProofStatus.PENDING, 
                   ProofStatus.ASSUMED, ProofStatus.PROVEN]
        
        idx1 = priority.index(status1)
        idx2 = priority.index(status2)
        
        return priority[min(idx1, idx2)]

def demo_proof_fibre():
    """Demonstrate proof fibre operations."""
    print("✅ Proof Fibre Demo")
    print("=" * 50)
    
    # Create fibre
    proof_fibre = ProofFibre()
    
    # Create proof data for constituents
    np_proof = ProofData()
    np_proof.add_obligation("well_formed", ProofObligation(
        property="well_formed",
        status=ProofStatus.PROVEN,
        evidence="NP structure verified"
    ))
    np_proof.add_obligation("agreement", ProofObligation(
        property="agreement_satisfied",
        status=ProofStatus.PROVEN,
        evidence="Determiner-noun agreement checked"
    ))
    np_proof.add_invariant("has_determiner")
    
    vp_proof = ProofData()
    vp_proof.add_obligation("well_formed", ProofObligation(
        property="well_formed",
        status=ProofStatus.PROVEN,
        evidence="VP structure verified"
    ))
    vp_proof.add_obligation("theta", ProofObligation(
        property="theta_roles_assigned",
        status=ProofStatus.PENDING,
        evidence="Awaiting argument structure"
    ))
    
    print("NP proof data:")
    print(f"  {np_proof}")
    print(f"  Invariants: {np_proof.invariants}")
    
    print("\nVP proof data:")
    print(f"  {vp_proof}")
    print(f"  Pending: {vp_proof.pending_obligations()}")
    
    # Combine via merge
    sentence_proof = proof_fibre.combine(np_proof, vp_proof, 'merge')
    
    print("\nMerged sentence proof data:")
    print(f"  {sentence_proof}")
    print(f"  Fully verified: {sentence_proof.is_fully_verified()}")
    print(f"  Pending obligations: {sentence_proof.pending_obligations()}")
    
    # Demonstrate movement
    moved_proof = proof_fibre.combine(sentence_proof, ProofData(), 'move')
    
    print("\nAfter movement:")
    print(f"  {moved_proof}")
    print(f"  New obligations: {list(moved_proof.obligations.keys())}")
    
    print("\n✨ The fibration ensures:")
    print("  - Proofs compose with syntactic operations")
    print("  - Verification obligations track dependencies")
    print("  - Formal guarantees propagate through derivations")


if __name__ == "__main__":
    demo_proof_fibre()