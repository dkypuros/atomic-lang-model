#!/usr/bin/env python3
"""
BM-25 Retrieval Fibre
====================

The BM-25 fibre enriches syntactic trees with information retrieval scores.
This shows how the fibration naturally extends to IR tasks - query trees
get scored against document collections, with scores propagating compositionally.

Key insight: BM-25 scores are just another type of empirical annotation
that lives coherently over syntactic structure.
"""

from typing import Dict, List, Set
from collections import defaultdict
import math

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fibration_core import Fibre, TreeNode, Morphism

class BM25Data:
    """BM-25 relevance scores over documents."""
    
    def __init__(self, scores: Dict[str, float] = None):
        self.scores = scores or {}
        
    def top_k(self, k: int) -> List[tuple[str, float]]:
        """Get top k highest-scoring documents."""
        sorted_scores = sorted(self.scores.items(), 
                             key=lambda x: x[1], reverse=True)
        return sorted_scores[:k]
    
    def normalized(self) -> 'BM25Data':
        """Return normalized scores in [0,1] range (creates new instance)."""
        if not self.scores:
            return BM25Data({})
        
        max_score = max(self.scores.values())
        if max_score > 0:
            normalized = {doc: score/max_score 
                         for doc, score in self.scores.items()}
            return BM25Data(normalized)
        return BM25Data(self.scores.copy())
    
    def filter_threshold(self, threshold: float) -> 'BM25Data':
        """Keep only documents scoring above threshold."""
        filtered = {doc: score for doc, score in self.scores.items()
                   if score >= threshold}
        return BM25Data(filtered)
    
    def __repr__(self):
        top = self.top_k(3)
        return f"BM25Data({len(self.scores)} docs, top: {top})"

class BM25Fibre(Fibre[BM25Data]):
    """
    BM-25 retrieval fibre implementation.
    
    This demonstrates how IR scoring integrates with syntactic parsing:
    - Query trees get scored against document collections
    - Syntactic transformations update scores coherently
    - Complex queries compose scores from constituents
    """
    
    def __init__(self, k1: float = 1.2, b: float = 0.75, 
                 combine_weights: Dict[str, float] = None,
                 tokenizer = None):
        """
        Initialize with BM-25 parameters.
        
        k1: controls term frequency saturation
        b: controls length normalization
        combine_weights: weights for combining scores in different operations
        tokenizer: optional custom tokenizer function
        """
        self.k1 = k1
        self.b = b
        self.combine_weights = combine_weights or {
            'merge_left': 0.6,
            'merge_right': 0.4
        }
        self.tokenizer = tokenizer or self._default_tokenizer
        
        # Mock document collection for demo
        self.documents = {
            "doc1": "the student studies machine learning",
            "doc2": "the teacher explains recursion theory", 
            "doc3": "students learn about formal grammars",
            "doc4": "recursive functions in programming",
            "doc5": "the professor teaches linguistics"
        }
        
        # Precompute IDF scores
        self._compute_idf()
    
    def _default_tokenizer(self, text: str) -> List[str]:
        """Default tokenizer: lowercase and split, removing punctuation."""
        import re
        # Simple regex tokenizer that handles punctuation
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens
        
    def _compute_idf(self):
        """Compute inverse document frequency scores."""
        doc_freq = defaultdict(int)
        self.doc_lengths = {}
        
        for doc_id, text in self.documents.items():
            terms = self.tokenizer(text)
            self.doc_lengths[doc_id] = len(terms)
            seen = set()
            for term in terms:
                if term not in seen:
                    doc_freq[term] += 1
                    seen.add(term)
        
        n_docs = len(self.documents)
        self.idf = {}
        for term, df in doc_freq.items():
            self.idf[term] = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)
        
        self.avg_doc_length = sum(self.doc_lengths.values()) / n_docs
    
    def _bm25_score(self, query_terms: List[str], doc_id: str) -> float:
        """Calculate BM-25 score for query against document."""
        doc_text = self.documents.get(doc_id, "")
        doc_terms = self.tokenizer(doc_text)
        doc_length = self.doc_lengths.get(doc_id, 0)
        
        score = 0.0
        term_freqs = defaultdict(int)
        for term in doc_terms:
            term_freqs[term] += 1
        
        for query_term in query_terms:
            if query_term in term_freqs:
                tf = term_freqs[query_term]
                idf = self.idf.get(query_term, 0)
                
                # BM-25 formula
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
                
                score += idf * (numerator / denominator)
        
        return score
    
    def pull(self, morphism: Morphism, target_data: BM25Data) -> BM25Data:
        """
        Pull back BM-25 scores along morphism.
        
        Scores are mostly invariant to syntactic reduction, but
        we might filter based on morphism properties.
        """
        # For IR, scores typically don't change with syntax
        # But we could filter documents based on syntactic constraints
        pulled_scores = {}
        
        for doc_id, score in target_data.scores.items():
            # Could check if document is compatible with source syntax
            if self._is_compatible_doc(doc_id, morphism):
                pulled_scores[doc_id] = score
        
        return BM25Data(pulled_scores)
    
    def push(self, morphism: Morphism, source_data: BM25Data) -> BM25Data:
        """
        Push forward BM-25 scores along morphism.
        
        Extending query syntax might change relevance.
        """
        # Scores generally propagate unchanged
        # Could reweight based on syntactic expansion
        return BM25Data(source_data.scores.copy())
    
    def combine(self, data1: BM25Data, data2: BM25Data, 
                operation: str) -> BM25Data:
        """
        Combine BM-25 scores when merging trees.
        
        Different operations use different score aggregations.
        """
        combined_scores = defaultdict(float)
        
        if operation == 'merge':
            # For merged queries, aggregate scores
            # Could use max, sum, or weighted combination
            all_docs = set(data1.scores.keys()) | set(data2.scores.keys())
            
            for doc_id in all_docs:
                score1 = data1.scores.get(doc_id, 0)
                score2 = data2.scores.get(doc_id, 0)
                
                # Use configurable weights
                w_left = self.combine_weights.get('merge_left', 0.6)
                w_right = self.combine_weights.get('merge_right', 0.4)
                combined_scores[doc_id] = w_left * score1 + w_right * score2
                
        elif operation == 'move':
            # Movement doesn't change IR scores typically
            combined_scores.update(data1.scores)
            
        return BM25Data(dict(combined_scores))
    
    def identity_data(self, tree: TreeNode) -> BM25Data:
        """Create identity BM-25 data for a tree."""
        # For leaves, compute BM-25 scores
        if not tree.children:
            query_term = tree.label.lower()
            scores = {}
            
            for doc_id in self.documents:
                score = self._bm25_score([query_term], doc_id)
                if score > 0:
                    scores[doc_id] = score
                    
            return BM25Data(scores)
        
        # For internal nodes, start with empty scores
        return BM25Data({})
    
    def _is_compatible_doc(self, doc_id: str, morphism: Morphism) -> bool:
        """Check if document is compatible with morphism source."""
        # TODO: Implement syntactic compatibility checking
        # For now, all documents are considered compatible
        return True

def demo_bm25_fibre():
    """Demonstrate BM-25 fibre for information retrieval."""
    print("🔍 BM-25 Retrieval Fibre Demo")
    print("=" * 50)
    
    # Create fibre
    bm25_fibre = BM25Fibre()
    
    print("Document collection:")
    for doc_id, text in bm25_fibre.documents.items():
        print(f"  {doc_id}: {text}")
    
    # Score single terms
    print("\n📊 Single term queries:")
    for term in ["student", "teacher", "recursion"]:
        tree = TreeNode(id=f"q_{term}", label=term, children=[])
        scores = bm25_fibre.identity_data(tree)
        
        print(f"\nQuery: '{term}'")
        for doc_id, score in scores.top_k(3):
            print(f"  {doc_id}: {score:.3f}")
    
    # Combine queries
    print("\n🔗 Combined query: 'student' AND 'learning'")
    
    student_tree = TreeNode(id="q1", label="student", children=[])
    learning_tree = TreeNode(id="q2", label="learning", children=[])
    
    student_scores = bm25_fibre.identity_data(student_tree)
    learning_scores = bm25_fibre.identity_data(learning_tree)
    
    combined = bm25_fibre.combine(student_scores, learning_scores, 'merge')
    
    print("Combined scores:")
    for doc_id, score in combined.top_k(3):
        print(f"  {doc_id}: {score:.3f}")
    
    # Demonstrate syntax-aware retrieval
    print("\n🌳 Syntax-aware query processing:")
    print("Query structure: [NP the student] [VP studies]")
    
    # This would integrate with the parser to build structured queries
    # that respect syntactic relationships while computing IR scores
    
    print("\n✨ The fibration ensures:")
    print("  - IR scores compose with query syntax")
    print("  - Syntactic query refinement preserves relevance")
    print("  - Complex queries build from simple term scores")


if __name__ == "__main__":
    demo_bm25_fibre()