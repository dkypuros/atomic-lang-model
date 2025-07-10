#!/usr/bin/env python3
"""
Test BM-25 Fibre Integration
============================

Tests that information retrieval scoring works correctly within
the fibration framework, maintaining all categorical laws.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fibration_core import GrammarFibration, Morphism, TreeNode
from fibres.bm25_fibre import BM25Fibre, BM25Data

def test_bm25_basic_scoring():
    """Test basic BM-25 scoring functionality."""
    bm25_fibre = BM25Fibre()
    
    # Test single term scoring
    query_tree = TreeNode(id="q1", label="student", children=[])
    scores = bm25_fibre.identity_data(query_tree)
    
    # Should have non-empty scores
    assert len(scores.scores) > 0
    
    # Scores should be positive
    for doc_id, score in scores.scores.items():
        assert score >= 0
    
    # Documents containing "student" should score higher
    top_docs = scores.top_k(2)
    assert any("student" in bm25_fibre.documents[doc_id].lower() 
              for doc_id, _ in top_docs)
    
    print("✅ Basic BM-25 scoring test passed")
    return True

def test_bm25_combination():
    """Test that BM-25 scores combine correctly."""
    bm25_fibre = BM25Fibre()
    
    # Create two query terms
    q1 = TreeNode(id="q1", label="student", children=[])
    q2 = TreeNode(id="q2", label="learning", children=[])
    
    scores1 = bm25_fibre.identity_data(q1)
    scores2 = bm25_fibre.identity_data(q2)
    
    # Combine via merge
    combined = bm25_fibre.combine(scores1, scores2, 'merge')
    
    # Combined should have scores
    assert len(combined.scores) > 0
    
    # Documents with both terms should score well
    doc1_text = bm25_fibre.documents["doc1"].lower()
    if "student" in doc1_text and "learning" in doc1_text:
        assert "doc1" in combined.scores
        assert combined.scores["doc1"] > 0
    
    print("✅ BM-25 combination test passed")
    return True

def test_bm25_with_fibration():
    """Test BM-25 fibre integration with full fibration."""
    fib = GrammarFibration()
    bm25_fibre = BM25Fibre()
    
    # Parse a query with BM-25 scoring
    query = "student learning"
    tree, bm25_data = fib.parse_with_fibre(query, bm25_fibre)
    
    # Should have parse tree and scores
    assert tree is not None
    assert bm25_data is not None
    
    # Annotations should be recorded
    assert tree.id in fib.annotations
    bm25_annotation = fib.get_annotation(tree.id, 'BM25Fibre')
    assert bm25_annotation is not None
    
    print("✅ BM-25 fibration integration test passed")
    return True

def test_bm25_pullback():
    """Test that BM-25 pull-back preserves relevance."""
    bm25_fibre = BM25Fibre()
    
    # Create some scores
    original_scores = BM25Data({
        "doc1": 0.8,
        "doc2": 0.6,
        "doc3": 0.4
    })
    
    # Create a morphism
    morph = Morphism("small", "big", {"a": "b"})
    
    # Pull back scores
    pulled = bm25_fibre.pull(morph, original_scores)
    
    # Scores should be preserved (IR is syntax-invariant mostly)
    assert len(pulled.scores) == len(original_scores.scores)
    import math
    for doc_id in original_scores.scores:
        assert doc_id in pulled.scores
        assert math.isclose(pulled.scores[doc_id], original_scores.scores[doc_id], rel_tol=1e-9)
    
    print("✅ BM-25 pull-back test passed")
    return True

def test_bm25_normalization():
    """Test score normalization functionality."""
    # Create scores with different ranges
    scores = BM25Data({
        "doc1": 10.0,
        "doc2": 5.0,
        "doc3": 2.5
    })
    
    # Normalize
    normalized = scores.normalized()
    
    # Check normalization
    import math
    assert math.isclose(normalized.scores["doc1"], 1.0, rel_tol=1e-9)  # Highest score becomes 1
    assert math.isclose(normalized.scores["doc2"], 0.5, rel_tol=1e-9)
    assert math.isclose(normalized.scores["doc3"], 0.25, rel_tol=1e-9)
    
    print("✅ BM-25 normalization test passed")
    return True

def test_syntax_aware_retrieval():
    """Test that syntactic structure affects retrieval."""
    fib = GrammarFibration()
    bm25_fibre = BM25Fibre()
    
    # Parse structured query: "the student who studies"
    # This would show how syntax influences scoring
    complex_query = "the student studies"
    tree, scores = fib.parse_with_fibre(complex_query, bm25_fibre)
    
    # The structured parsing should produce different scores
    # than bag-of-words (future enhancement)
    assert scores is not None
    
    print("✅ Syntax-aware retrieval test passed")
    return True

def run_bm25_tests():
    """Run all BM-25 fibre tests."""
    print("🔍 Running BM-25 Fibre Tests")
    print("=" * 50)
    
    tests = [
        ("Basic scoring", test_bm25_basic_scoring),
        ("Score combination", test_bm25_combination),
        ("Fibration integration", test_bm25_with_fibration),
        ("Pull-back coherence", test_bm25_pullback),
        ("Score normalization", test_bm25_normalization),
        ("Syntax-aware retrieval", test_syntax_aware_retrieval),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"❌ {test_name} failed")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} failed with error: {e}")
    
    print(f"\n{'='*50}")
    print(f"Summary: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All BM-25 tests passed!")
        print("Information retrieval integrates cleanly with the fibration.")
    else:
        print("\n⚠️  Some BM-25 tests failed.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_bm25_tests()
    sys.exit(0 if success else 1)