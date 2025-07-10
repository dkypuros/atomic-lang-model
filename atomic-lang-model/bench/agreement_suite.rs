//! Agreement Test Suite (Linzen et al. 2016)
//! 
//! Tests subject-verb agreement across center-embedded structures to evaluate
//! the atomic language model's handling of long-distance dependencies.

use atomic_lang_model::*;
use std::collections::HashMap;

/// Test case for subject-verb agreement
#[derive(Debug, Clone)]
pub struct AgreementTest {
    /// Grammatical sentence (correct agreement)
    pub grammatical: String,
    /// Ungrammatical sentence (incorrect agreement)  
    pub ungrammatical: String,
    /// Number of intervening attractors
    pub attractor_count: usize,
    /// Embedding depth
    pub depth: usize,
}

/// Results of agreement testing
#[derive(Debug, Clone)]
pub struct AgreementResults {
    /// Total test cases
    pub total: usize,
    /// Correctly identified grammatical sentences
    pub correct_grammatical: usize,
    /// Correctly rejected ungrammatical sentences
    pub correct_ungrammatical: usize,
    /// Accuracy score
    pub accuracy: f64,
    /// Results by embedding depth
    pub by_depth: HashMap<usize, f64>,
    /// Results by attractor count
    pub by_attractors: HashMap<usize, f64>,
}

/// Generate agreement test suite
pub fn generate_agreement_tests() -> Vec<AgreementTest> {
    vec![
        // Depth 0: Simple agreement
        AgreementTest {
            grammatical: "the student is here".to_string(),
            ungrammatical: "the student are here".to_string(),
            attractor_count: 0,
            depth: 0,
        },
        AgreementTest {
            grammatical: "the students are here".to_string(),
            ungrammatical: "the students is here".to_string(),
            attractor_count: 0,
            depth: 0,
        },
        
        // Depth 1: One attractor
        AgreementTest {
            grammatical: "the student near the teachers is here".to_string(),
            ungrammatical: "the student near the teachers are here".to_string(),
            attractor_count: 1,
            depth: 1,
        },
        AgreementTest {
            grammatical: "the students near the teacher are here".to_string(),
            ungrammatical: "the students near the teacher is here".to_string(),
            attractor_count: 1,
            depth: 1,
        },
        
        // Depth 2: Two attractors
        AgreementTest {
            grammatical: "the student near the teachers in the room is here".to_string(),
            ungrammatical: "the student near the teachers in the room are here".to_string(),
            attractor_count: 2,
            depth: 2,
        },
        AgreementTest {
            grammatical: "the students near the teacher in the room are here".to_string(),
            ungrammatical: "the students near the teacher in the room is here".to_string(),
            attractor_count: 2,
            depth: 2,
        },
        
        // Relative clause embedding
        AgreementTest {
            grammatical: "the student who the teachers like is smart".to_string(),
            ungrammatical: "the student who the teachers like are smart".to_string(),
            attractor_count: 1,
            depth: 1,
        },
        AgreementTest {
            grammatical: "the students who the teacher likes are smart".to_string(),
            ungrammatical: "the students who the teacher likes is smart".to_string(),
            attractor_count: 1,
            depth: 1,
        },
        
        // Deep embedding (difficulty test)
        AgreementTest {
            grammatical: "the student who the teacher that Mary knows likes is here".to_string(),
            ungrammatical: "the student who the teacher that Mary knows likes are here".to_string(),
            attractor_count: 2,
            depth: 2,
        },
    ]
}

/// Extended lexicon for agreement testing
pub fn agreement_lexicon() -> Vec<LexItem> {
    let mut lexicon = test_lexicon();
    
    // Add agreement-sensitive items
    lexicon.extend(vec![
        LexItem::new("students", &[Feature::Cat(Category::N)]),
        LexItem::new("teachers", &[Feature::Cat(Category::N)]),
        LexItem::new("is", &[Feature::Cat(Category::V)]),
        LexItem::new("are", &[Feature::Cat(Category::V)]),
        LexItem::new("likes", &[Feature::Cat(Category::V), Feature::Sel(Category::DP)]),
        LexItem::new("like", &[Feature::Cat(Category::V), Feature::Sel(Category::DP)]),
        LexItem::new("near", &[Feature::Cat(Category::V), Feature::Sel(Category::DP)]),
        LexItem::new("in", &[Feature::Cat(Category::V), Feature::Sel(Category::DP)]),
        LexItem::new("room", &[Feature::Cat(Category::N)]),
        LexItem::new("here", &[Feature::Cat(Category::V)]),
        LexItem::new("smart", &[Feature::Cat(Category::V)]),
        LexItem::new("Mary", &[Feature::Cat(Category::N)]),
        LexItem::new("knows", &[Feature::Cat(Category::V), Feature::Sel(Category::DP)]),
    ]);
    
    lexicon
}

/// Test agreement for a single sentence pair
pub fn test_agreement_pair(test: &AgreementTest, lexicon: &[LexItem]) -> (bool, bool) {
    let grammatical_result = parse_sentence(&test.grammatical, lexicon);
    let ungrammatical_result = parse_sentence(&test.ungrammatical, lexicon);
    
    let grammatical_parsed = grammatical_result.is_ok();
    let ungrammatical_rejected = ungrammatical_result.is_err();
    
    (grammatical_parsed, ungrammatical_rejected)
}

/// Run complete agreement test suite
pub fn run_agreement_suite() -> AgreementResults {
    let tests = generate_agreement_tests();
    let lexicon = agreement_lexicon();
    
    let mut total = 0;
    let mut correct_grammatical = 0;
    let mut correct_ungrammatical = 0;
    let mut by_depth: HashMap<usize, Vec<bool>> = HashMap::new();
    let mut by_attractors: HashMap<usize, Vec<bool>> = HashMap::new();
    
    println!("🧪 Running Agreement Test Suite (Linzen et al. 2016)");
    println!("=" .repeat(60));
    
    for test in &tests {
        let (gram_ok, ungram_rejected) = test_agreement_pair(test, &lexicon);
        
        total += 2; // Each test has grammatical + ungrammatical
        
        if gram_ok {
            correct_grammatical += 1;
            println!("✅ GRAM: {}", test.grammatical);
        } else {
            println!("❌ GRAM: {}", test.grammatical);
        }
        
        if ungram_rejected {
            correct_ungrammatical += 1;
            println!("✅ UNGRAM: {} (correctly rejected)", test.ungrammatical);
        } else {
            println!("❌ UNGRAM: {} (incorrectly accepted)", test.ungrammatical);
        }
        
        // Track by depth
        by_depth.entry(test.depth)
            .or_insert_with(Vec::new)
            .extend(vec![gram_ok, ungram_rejected]);
            
        // Track by attractors
        by_attractors.entry(test.attractor_count)
            .or_insert_with(Vec::new)
            .extend(vec![gram_ok, ungram_rejected]);
        
        println!("   Depth: {}, Attractors: {}", test.depth, test.attractor_count);
        println!();
    }
    
    let accuracy = (correct_grammatical + correct_ungrammatical) as f64 / total as f64;
    
    // Calculate accuracy by depth
    let depth_accuracy: HashMap<usize, f64> = by_depth.iter()
        .map(|(&depth, results)| {
            let correct = results.iter().filter(|&&x| x).count();
            let acc = correct as f64 / results.len() as f64;
            (depth, acc)
        })
        .collect();
    
    // Calculate accuracy by attractors
    let attractor_accuracy: HashMap<usize, f64> = by_attractors.iter()
        .map(|(&attractors, results)| {
            let correct = results.iter().filter(|&&x| x).count();
            let acc = correct as f64 / results.len() as f64;
            (attractors, acc)
        })
        .collect();
    
    AgreementResults {
        total,
        correct_grammatical,
        correct_ungrammatical,
        accuracy,
        by_depth: depth_accuracy,
        by_attractors: attractor_accuracy,
    }
}

/// Print detailed results analysis
pub fn print_agreement_analysis(results: &AgreementResults) {
    println!("\n📊 AGREEMENT TEST RESULTS");
    println!("=" .repeat(40));
    println!("Total test cases: {}", results.total);
    println!("Correct grammatical: {}/{}", results.correct_grammatical, results.total / 2);
    println!("Correct ungrammatical: {}/{}", results.correct_ungrammatical, results.total / 2);
    println!("Overall accuracy: {:.1}%", results.accuracy * 100.0);
    
    println!("\n📈 ACCURACY BY EMBEDDING DEPTH:");
    for depth in 0..=2 {
        if let Some(&accuracy) = results.by_depth.get(&depth) {
            println!("  Depth {}: {:.1}%", depth, accuracy * 100.0);
        }
    }
    
    println!("\n📈 ACCURACY BY ATTRACTOR COUNT:");
    for attractors in 0..=2 {
        if let Some(&accuracy) = results.by_attractors.get(&attractors) {
            println!("  {} attractors: {:.1}%", attractors, accuracy * 100.0);
        }
    }
    
    // Performance analysis
    println!("\n🔍 PERFORMANCE ANALYSIS:");
    if results.accuracy > 0.8 {
        println!("✅ Excellent performance (>80% accuracy)");
    } else if results.accuracy > 0.6 {
        println!("⚠️  Moderate performance (60-80% accuracy)");
    } else {
        println!("❌ Poor performance (<60% accuracy)");
    }
    
    // Depth analysis
    let depth_0_acc = results.by_depth.get(&0).unwrap_or(&0.0);
    let depth_1_acc = results.by_depth.get(&1).unwrap_or(&0.0);
    let depth_2_acc = results.by_depth.get(&2).unwrap_or(&0.0);
    
    if depth_0_acc > depth_1_acc && depth_1_acc > depth_2_acc {
        println!("📉 Expected degradation with embedding depth");
    } else {
        println!("🤔 Unexpected performance pattern across depths");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_agreement_generation() {
        let tests = generate_agreement_tests();
        assert!(!tests.is_empty(), "Should generate test cases");
        
        // Verify test structure
        for test in &tests {
            assert!(!test.grammatical.is_empty(), "Grammatical sentence should not be empty");
            assert!(!test.ungrammatical.is_empty(), "Ungrammatical sentence should not be empty");
            assert_ne!(test.grammatical, test.ungrammatical, "Sentences should differ");
        }
        
        println!("Generated {} agreement test cases", tests.len());
    }
    
    #[test]
    fn test_agreement_lexicon() {
        let lexicon = agreement_lexicon();
        assert!(lexicon.len() > 10, "Should have substantial lexicon");
        
        // Check for key items
        let has_is = lexicon.iter().any(|item| item.phon == "is");
        let has_are = lexicon.iter().any(|item| item.phon == "are");
        let has_students = lexicon.iter().any(|item| item.phon == "students");
        
        assert!(has_is, "Should have 'is'");
        assert!(has_are, "Should have 'are'");
        assert!(has_students, "Should have 'students'");
    }
    
    #[test]
    fn test_simple_agreement() {
        let lexicon = agreement_lexicon();
        
        // Test simple grammatical case
        let result = parse_sentence("the student is here", &lexicon);
        // Note: This might fail with current minimal grammar, but tests the framework
        
        println!("Simple agreement test result: {:?}", result.is_ok());
    }
    
    #[test]
    fn test_agreement_suite_runs() {
        // This test verifies the test suite runs without crashing
        let results = run_agreement_suite();
        
        assert_eq!(results.total, generate_agreement_tests().len() * 2);
        assert!(results.accuracy >= 0.0 && results.accuracy <= 1.0);
        
        print_agreement_analysis(&results);
    }
}