"""
Fibres for the Grothendieck fibration.

Each fibre provides a different type of empirical enrichment:
- ProbabilityFibre: Statistical weights
- EmbeddingFibre: Vector representations  
- ProofFibre: Formal verification data
- BM25Fibre: Information retrieval scores
"""

from .probability_fibre import ProbabilityFibre
from .embedding_fibre import EmbeddingFibre
from .proof_fibre import ProofFibre
from .bm25_fibre import BM25Fibre

__all__ = ['ProbabilityFibre', 'EmbeddingFibre', 'ProofFibre', 'BM25Fibre']