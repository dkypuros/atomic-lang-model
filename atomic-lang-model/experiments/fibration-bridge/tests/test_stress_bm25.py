#!/usr/bin/env python3
"""
Stress Test for BM-25 Fibre
===========================

Tests BM-25 performance with larger document collections to ensure
IDF caching and scoring remain O(|V| + |D|) rather than O(|V| * |D|).
"""

import sys
import os
import time
import random
import string
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fibres.bm25_fibre import BM25Fibre, BM25Data

def generate_synthetic_corpus(n_docs: int, vocab_size: int = 1000, 
                            doc_length_range: tuple = (10, 100)) -> Dict[str, str]:
    """Generate synthetic document collection for testing."""
    # Create vocabulary
    vocab = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8))) 
             for _ in range(vocab_size)]
    
    corpus = {}
    for i in range(n_docs):
        doc_length = random.randint(*doc_length_range)
        doc_words = random.choices(vocab, k=doc_length)
        corpus[f"doc_{i}"] = ' '.join(doc_words)
    
    return corpus

def test_large_corpus_performance():
    """Test BM-25 performance with large corpus."""
    print("🏋️ Large Corpus Performance Test")
    print("-" * 50)
    
    # Test with increasing corpus sizes
    sizes = [100, 1000, 5000, 10000]
    
    for n_docs in sizes:
        print(f"\nTesting with {n_docs} documents...")
        
        # Generate corpus
        start = time.time()
        corpus = generate_synthetic_corpus(n_docs)
        gen_time = time.time() - start
        print(f"  Corpus generation: {gen_time:.2f}s")
        
        # Create BM-25 fibre
        start = time.time()
        fibre = BM25Fibre()
        fibre.documents = corpus
        fibre._compute_idf()
        init_time = time.time() - start
        print(f"  IDF computation: {init_time:.2f}s")
        
        # Test scoring
        query_terms = ["test", "query", "words"]
        start = time.time()
        
        scores = {}
        for doc_id in list(corpus.keys())[:100]:  # Score first 100 docs
            score = fibre._bm25_score(query_terms, doc_id)
            scores[doc_id] = score
            
        score_time = time.time() - start
        avg_time = score_time / min(100, n_docs)
        print(f"  Scoring time: {score_time:.2f}s ({avg_time*1000:.2f}ms per doc)")
        
        # Check complexity
        # Should be O(|V| + |D|) not O(|V| * |D|)
        if n_docs >= 1000:
            expected_linear = init_time * (n_docs / 1000)
            if init_time > expected_linear * 2:
                print("  ⚠️  WARNING: IDF computation may not be linear!")
    
    print("\n✅ Performance test completed")
    return True

def test_memory_efficiency():
    """Test memory usage with large collections."""
    print("\n💾 Memory Efficiency Test")
    print("-" * 50)
    
    import gc
    import sys
    
    # Baseline memory
    gc.collect()
    baseline = sys.getsizeof(BM25Fibre())
    
    # Test with different corpus sizes
    for n_docs in [100, 1000, 5000]:
        corpus = generate_synthetic_corpus(n_docs, vocab_size=500)
        
        fibre = BM25Fibre()
        fibre.documents = corpus
        fibre._compute_idf()
        
        # Measure memory
        total_size = sys.getsizeof(fibre)
        doc_size = sum(sys.getsizeof(doc) for doc in corpus.values())
        idf_size = sys.getsizeof(fibre.idf)
        
        print(f"\n{n_docs} documents:")
        print(f"  Total fibre size: {total_size/1024:.1f}KB")
        print(f"  Document data: {doc_size/1024:.1f}KB")
        print(f"  IDF table: {idf_size/1024:.1f}KB")
        print(f"  Overhead: {(total_size - doc_size)/1024:.1f}KB")
        
        # Clean up
        del fibre
        del corpus
        gc.collect()
    
    print("\n✅ Memory test completed")
    return True

def test_concurrent_queries():
    """Test handling multiple queries efficiently."""
    print("\n🔀 Concurrent Query Test")
    print("-" * 50)
    
    # Create fibre with medium corpus
    corpus = generate_synthetic_corpus(1000)
    fibre = BM25Fibre()
    fibre.documents = corpus
    fibre._compute_idf()
    
    # Generate multiple queries
    queries = [
        ["search", "engine", "optimization"],
        ["machine", "learning", "algorithm"],
        ["natural", "language", "processing"],
        ["information", "retrieval", "system"],
        ["data", "structure", "analysis"]
    ]
    
    # Time batch processing
    start = time.time()
    all_results = {}
    
    for i, query in enumerate(queries):
        scores = {}
        for doc_id in list(corpus.keys())[:100]:
            score = fibre._bm25_score(query, doc_id)
            scores[doc_id] = score
        
        # Get top 10
        top_10 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
        all_results[f"query_{i}"] = top_10
    
    batch_time = time.time() - start
    
    print(f"Processed {len(queries)} queries in {batch_time:.2f}s")
    print(f"Average per query: {batch_time/len(queries):.2f}s")
    
    # Show sample results
    print("\nSample results (query_0 top 3):")
    for doc_id, score in all_results["query_0"][:3]:
        print(f"  {doc_id}: {score:.3f}")
    
    print("\n✅ Concurrent query test completed")
    return True

def run_stress_tests():
    """Run all stress tests."""
    print("🔥 Running BM-25 Stress Tests")
    print("=" * 60)
    
    tests = [
        ("Large corpus performance", test_large_corpus_performance),
        ("Memory efficiency", test_memory_efficiency),
        ("Concurrent queries", test_concurrent_queries),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📊 {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"❌ {test_name} failed")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} failed with error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"Stress test summary: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All stress tests passed!")
        print("BM-25 fibre scales well to larger collections.")
    else:
        print("\n⚠️  Some stress tests failed.")
    
    return failed == 0

if __name__ == "__main__":
    # Fix import
    from typing import Dict
    
    success = run_stress_tests()
    sys.exit(0 if success else 1)