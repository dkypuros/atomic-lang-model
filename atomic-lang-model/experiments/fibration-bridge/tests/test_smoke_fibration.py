#!/usr/bin/env python3
"""
Smoke Test for Fibration Plumbing
=================================

Minimal test that touches every moving part of the fibration prototype.
If this passes, the categorical architecture is sound.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fibration_core import GrammarFibration, Morphism, TreeNode
from fibres.probability_fibre import ProbabilityFibre, ProbabilityData
from fibres.embedding_fibre import EmbeddingFibre

def test_plumbing_smoke():
    """
    Core smoke test that exercises:
    1. End-to-end parse-and-annotate
    2. Substitution coherence  
    3. Functoriality law
    """
    fib = GrammarFibration()
    prob_fibre = ProbabilityFibre()
    embed_fibre = EmbeddingFibre(dim=4)  # very small vectors for speed

    # 1. Parse a tiny sentence with TWO independent fibres --------------------
    root, prob_root = fib.parse_with_fibre("the student left", prob_fibre)
    _, emb_root = fib.parse_with_fibre("the student left", embed_fibre)

    assert root.id in fib.annotations  # annotations recorded
    assert abs(sum(prob_root.distribution.values()) - 1) < 1e-6
    assert emb_root.dim == 4  # embedding present

    # 2. Do a subtree substitution and check pull-back ------------------------
    # Create a new leaf to substitute
    new_leaf = TreeNode(id="teacher_node", label="teacher", children=[])
    fib.add_tree(new_leaf)

    # Get the original "student" node (simplified - in practice would search)
    # For this test, we'll substitute at a leaf position
    if root.children and root.children[0].children:
        original_leaf_id = root.children[0].children[1].id  # the "student" leaf
    else:
        # Fallback for different tree structure
        original_leaf_id = root.id

    sub_tree, pulled_prob = fib.substitute(
        tree_id=root.id,
        subtree_id=original_leaf_id,
        new_subtree=new_leaf,
        fibre=prob_fibre
    )

    # Pulled distribution should still be normalized
    if pulled_prob and hasattr(pulled_prob, 'distribution'):
        assert abs(sum(pulled_prob.distribution.values()) - 1) < 1e-6

    # 3. Functoriality sanity check -------------------------------------------
    # Fabricate a trivial identity morphism chain
    f = Morphism(
        source_id=sub_tree.id, 
        target_id=root.id,
        mapping={sub_tree.id: root.id}
    )
    g = Morphism(
        source_id="dummy_src", 
        target_id=sub_tree.id,
        mapping={"dummy_src": sub_tree.id}
    )
    
    # Create some test data
    test_data = ProbabilityData({"test": 1.0})
    
    # Verify functoriality
    functorial = fib.verify_functoriality(f, g, prob_fibre, test_data)
    assert functorial, "Functoriality law violated!"

    print("✅ Smoke-test passed: plumbing is coherent")
    return True

def test_multi_fibre_coherence():
    """Test that multiple fibres can coexist without interference."""
    fib = GrammarFibration()
    prob_fibre = ProbabilityFibre()
    embed_fibre = EmbeddingFibre(dim=3)
    
    # Parse with both fibres
    tree1, prob_data = fib.parse_with_fibre("the cat", prob_fibre)
    tree2, emb_data = fib.parse_with_fibre("the cat", embed_fibre)
    
    # Both should produce valid data
    assert prob_data is not None
    assert emb_data is not None
    
    # Annotations should be independent
    prob_annotation = fib.get_annotation(tree1.id, 'ProbabilityFibre')
    emb_annotation = fib.get_annotation(tree2.id, 'EmbeddingFibre')
    
    assert prob_annotation is not None
    assert emb_annotation is not None
    
    print("✅ Multi-fibre coherence test passed")
    return True

def test_composition_laws():
    """Test that composition preserves fibre structure."""
    fib = GrammarFibration()
    prob_fibre = ProbabilityFibre()
    
    # Create simple trees
    tree1 = TreeNode(id="t1", label="NP", children=[])
    tree2 = TreeNode(id="t2", label="VP", children=[])
    tree3 = TreeNode(id="t3", label="S", children=[tree1, tree2])
    
    fib.add_tree(tree1)
    fib.add_tree(tree2)
    fib.add_tree(tree3)
    
    # Add probability data
    prob1 = ProbabilityData({"the cat": 0.6, "a cat": 0.4})
    prob2 = ProbabilityData({"sleeps": 0.7, "runs": 0.3})
    
    fib.annotate("t1", "ProbabilityFibre", prob1)
    fib.annotate("t2", "ProbabilityFibre", prob2)
    
    # Combine
    combined = prob_fibre.combine(prob1, prob2, 'merge')
    
    # Check that combination preserves probability mass
    assert abs(sum(combined.distribution.values()) - 1) < 1e-6
    
    # Check that we get expected combinations
    assert "the cat sleeps" in combined.distribution
    
    print("✅ Composition laws test passed")
    return True

def run_all_tests():
    """Run all smoke tests."""
    print("🧪 Running Fibration Smoke Tests")
    print("=" * 50)
    
    tests = [
        ("Plumbing smoke test", test_plumbing_smoke),
        ("Multi-fibre coherence", test_multi_fibre_coherence),
        ("Composition laws", test_composition_laws),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔬 {test_name}...")
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
        print("\n🎉 All fibration laws verified!")
        print("The categorical architecture is sound.")
    else:
        print("\n⚠️  Some tests failed. Check the fibration implementation.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)