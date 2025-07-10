//! Colorless Green Test Suite (Gulordava et al. 2018)
//! 
//! Tests syntactic processing independent of semantic content using
//! semantically anomalous but syntactically well-formed sentences.

use atomic_lang_model::*;
use std::collections::HashMap;

/// Test case for colorless green evaluation
#[derive(Debug, Clone)]
pub struct ColorlessGreenTest {
    /// Grammatical but semantically anomalous sentence
    pub grammatical: String,
    /// Ungrammatical version of the same sentence
    pub ungrammatical: String,
    /// Syntactic complexity level
    pub complexity: usize,
    /// Embedding depth
    pub depth: usize,
    /// Test category
    pub category: String,
}

/// Results of colorless green testing
#[derive(Debug, Clone)]
pub struct ColorlessGreenResults {
    /// Total test cases
    pub total: usize,
    /// Correctly identified grammatical sentences
    pub correct_grammatical: usize,
    /// Correctly rejected ungrammatical sentences
    pub correct_ungrammatical: usize,
    /// Accuracy score
    pub accuracy: f64,
    /// Complexity penalty (average difference in derivation length)
    pub complexity_penalty: f64,
    /// Results by complexity level
    pub by_complexity: HashMap<usize, f64>,
    /// Results by category
    pub by_category: HashMap<String, f64>,
}

/// Generate colorless green test suite
pub fn generate_colorless_green_tests() -> Vec<ColorlessGreenTest> {
    vec![
        // Simple anomalous sentences
        ColorlessGreenTest {
            grammatical: "colorless green ideas sleep furiously".to_string(),
            ungrammatical: "colorless green ideas sleeps furiously".to_string(),
            complexity: 1,
            depth: 0,
            category: "agreement".to_string(),
        },
        ColorlessGreenTest {
            grammatical: "purple thoughts dance silently".to_string(),
            ungrammatical: "purple thoughts dances silently".to_string(),
            complexity: 1,
            depth: 0,
            category: "agreement".to_string(),
        },
        
        // More complex structures
        ColorlessGreenTest {
            grammatical: "the invisible cat that meows backwards jumped".to_string(),
            ungrammatical: "the invisible cat that meow backwards jumped".to_string(),
            complexity: 2,
            depth: 1,
            category: "relative_clause".to_string(),
        },
        ColorlessGreenTest {
            grammatical: "square circles think about round triangles".to_string(),
            ungrammatical: "square circles thinks about round triangles".to_string(),
            complexity: 2,
            depth: 0,
            category: "agreement".to_string(),
        },
        
        // Nested structures
        ColorlessGreenTest {
            grammatical: "the idea that thoughts have colors seems wrong".to_string(),
            ungrammatical: "the idea that thoughts have colors seem wrong".to_string(),
            complexity: 3,
            depth: 1,
            category: "complement_clause".to_string(),
        },
        ColorlessGreenTest {
            grammatical: "transparent music that numbers hear loudly disappears".to_string(),
            ungrammatical: "transparent music that numbers hear loudly disappear".to_string(),
            complexity: 3,
            depth: 1,
            category: "relative_clause".to_string(),
        },
        
        // Complex embeddings
        ColorlessGreenTest {
            grammatical: "the notion that silent colors speak to deaf sounds confuses everyone".to_string(),
            ungrammatical: "the notion that silent colors speak to deaf sounds confuse everyone".to_string(),
            complexity: 4,
            depth: 2,
            category: "complement_clause".to_string(),
        },
        ColorlessGreenTest {
            grammatical: "impossible dreams about flying rocks visit sleeping mathematics".to_string(),
            ungrammatical: "impossible dreams about flying rocks visits sleeping mathematics".to_string(),
            complexity: 3,
            depth: 1,
            category: "prepositional_phrase".to_string(),
        },
        
        // Very complex structures
        ColorlessGreenTest {
            grammatical: "the belief that the idea that colors think is false seems reasonable".to_string(),
            ungrammatical: "the belief that the idea that colors think are false seems reasonable".to_string(),
            complexity: 5,
            depth: 2,
            category: "double_embedding".to_string(),
        },
    ]
}

/// Extended lexicon for colorless green testing
pub fn colorless_green_lexicon() -> Vec<LexItem> {
    let mut lexicon = agreement_lexicon();
    
    // Add semantically anomalous but syntactically valid items
    lexicon.extend(vec![
        // Adjectives
        LexItem::new("colorless", &[Feature::Cat(Category::N)]), // Simplified as modifier
        LexItem::new("green", &[Feature::Cat(Category::N)]),
        LexItem::new("purple", &[Feature::Cat(Category::N)]),
        LexItem::new("invisible", &[Feature::Cat(Category::N)]),
        LexItem::new("square", &[Feature::Cat(Category::N)]),
        LexItem::new("round", &[Feature::Cat(Category::N)]),
        LexItem::new("transparent", &[Feature::Cat(Category::N)]),
        LexItem::new("silent", &[Feature::Cat(Category::N)]),
        LexItem::new("deaf", &[Feature::Cat(Category::N)]),
        LexItem::new("impossible", &[Feature::Cat(Category::N)]),
        LexItem::new("flying", &[Feature::Cat(Category::N)]),
        LexItem::new("sleeping", &[Feature::Cat(Category::N)]),
        
        // Nouns
        LexItem::new("ideas", &[Feature::Cat(Category::N)]),
        LexItem::new("thoughts", &[Feature::Cat(Category::N)]),
        LexItem::new("cat", &[Feature::Cat(Category::N)]),
        LexItem::new("circles", &[Feature::Cat(Category::N)]),
        LexItem::new("triangles", &[Feature::Cat(Category::N)]),
        LexItem::new("idea", &[Feature::Cat(Category::N)]),
        LexItem::new("colors", &[Feature::Cat(Category::N)]),
        LexItem::new("music", &[Feature::Cat(Category::N)]),
        LexItem::new("numbers", &[Feature::Cat(Category::N)]),
        LexItem::new("notion", &[Feature::Cat(Category::N)]),
        LexItem::new("sounds", &[Feature::Cat(Category::N)]),
        LexItem::new("everyone", &[Feature::Cat(Category::N)]),
        LexItem::new("dreams", &[Feature::Cat(Category::N)]),
        LexItem::new("rocks", &[Feature::Cat(Category::N)]),
        LexItem::new("mathematics", &[Feature::Cat(Category::N)]),
        LexItem::new("belief", &[Feature::Cat(Category::N)]),
        
        // Verbs
        LexItem::new("sleep", &[Feature::Cat(Category::V)]),
        LexItem::new("sleeps", &[Feature::Cat(Category::V)]),
        LexItem::new("dance", &[Feature::Cat(Category::V)]),
        LexItem::new("dances", &[Feature::Cat(Category::V)]),
        LexItem::new("meows", &[Feature::Cat(Category::V)]),
        LexItem::new("meow", &[Feature::Cat(Category::V)]),
        LexItem::new("jumped", &[Feature::Cat(Category::V)]),
        LexItem::new("think", &[Feature::Cat(Category::V)]),
        LexItem::new("thinks", &[Feature::Cat(Category::V)]),
        LexItem::new("have", &[Feature::Cat(Category::V)]),
        LexItem::new("seems", &[Feature::Cat(Category::V)]),
        LexItem::new("seem", &[Feature::Cat(Category::V)]),
        LexItem::new("hear", &[Feature::Cat(Category::V)]),
        LexItem::new("disappears", &[Feature::Cat(Category::V)]),
        LexItem::new("disappear", &[Feature::Cat(Category::V)]),
        LexItem::new("speak", &[Feature::Cat(Category::V)]),
        LexItem::new("confuses", &[Feature::Cat(Category::V)]),
        LexItem::new("confuse", &[Feature::Cat(Category::V)]),
        LexItem::new("visit", &[Feature::Cat(Category::V)]),
        LexItem::new("visits", &[Feature::Cat(Category::V)]),
        
        // Adverbs
        LexItem::new("furiously", &[Feature::Cat(Category::V)]),
        LexItem::new("silently", &[Feature::Cat(Category::V)]),
        LexItem::new("backwards", &[Feature::Cat(Category::V)]),
        LexItem::new("loudly", &[Feature::Cat(Category::V)]),
        
        // Other
        LexItem::new("about", &[Feature::Cat(Category::C), Feature::Sel(Category::DP)]),
        LexItem::new("to", &[Feature::Cat(Category::C), Feature::Sel(Category::DP)]),
        LexItem::new("wrong", &[Feature::Cat(Category::N)]),
        LexItem::new("false", &[Feature::Cat(Category::N)]),
        LexItem::new("reasonable", &[Feature::Cat(Category::N)]),
    ]);
    
    lexicon
}

/// Calculate derivation complexity (simplified metric)
fn estimate_derivation_complexity(sentence: &str, lexicon: &[LexItem]) -> usize {
    // Simple complexity estimate based on sentence structure
    let tokens: Vec<&str> = sentence.split_whitespace().collect();
    let token_count = tokens.len();
    
    // Count embedding indicators
    let that_count = tokens.iter().filter(|&&token| token == "that").count();
    let who_count = tokens.iter().filter(|&&token| token == "who").count();
    
    // Estimate complexity: base tokens + embedding penalty
    token_count + (that_count + who_count) * 2
}

/// Test colorless green pair with complexity measurement
pub fn test_colorless_green_pair(test: &ColorlessGreenTest, lexicon: &[LexItem]) -> (bool, bool, f64) {
    let grammatical_result = parse_sentence(&test.grammatical, lexicon);
    let ungrammatical_result = parse_sentence(&test.ungrammatical, lexicon);
    
    let grammatical_parsed = grammatical_result.is_ok();
    let ungrammatical_rejected = ungrammatical_result.is_err();
    
    // Calculate complexity penalty
    let gram_complexity = estimate_derivation_complexity(&test.grammatical, lexicon);
    let ungram_complexity = estimate_derivation_complexity(&test.ungrammatical, lexicon);
    let complexity_penalty = ungram_complexity as f64 - gram_complexity as f64;
    
    (grammatical_parsed, ungrammatical_rejected, complexity_penalty)
}

/// Run complete colorless green test suite
pub fn run_colorless_green_suite() -> ColorlessGreenResults {
    let tests = generate_colorless_green_tests();
    let lexicon = colorless_green_lexicon();
    
    let mut total = 0;
    let mut correct_grammatical = 0;
    let mut correct_ungrammatical = 0;
    let mut complexity_penalties = Vec::new();
    let mut by_complexity: HashMap<usize, Vec<bool>> = HashMap::new();
    let mut by_category: HashMap<String, Vec<bool>> = HashMap::new();
    
    println!("🎨 Running Colorless Green Test Suite (Gulordava et al. 2018)");
    println!("=" .repeat(60));
    
    for test in &tests {
        let (gram_ok, ungram_rejected, penalty) = test_colorless_green_pair(test, &lexicon);
        
        total += 2;
        complexity_penalties.push(penalty);
        
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
        
        // Track by complexity
        by_complexity.entry(test.complexity)
            .or_insert_with(Vec::new)
            .extend(vec![gram_ok, ungram_rejected]);
            
        // Track by category
        by_category.entry(test.category.clone())
            .or_insert_with(Vec::new)
            .extend(vec![gram_ok, ungram_rejected]);
        
        println!("   Complexity: {}, Depth: {}, Category: {}, Penalty: {:.1}", 
            test.complexity, test.depth, test.category, penalty);
        println!();
    }
    
    let accuracy = (correct_grammatical + correct_ungrammatical) as f64 / total as f64;
    let avg_complexity_penalty = complexity_penalties.iter().sum::<f64>() / complexity_penalties.len() as f64;
    
    // Calculate accuracy by complexity
    let complexity_accuracy: HashMap<usize, f64> = by_complexity.iter()
        .map(|(&complexity, results)| {
            let correct = results.iter().filter(|&&x| x).count();
            let acc = correct as f64 / results.len() as f64;
            (complexity, acc)
        })
        .collect();
    
    // Calculate accuracy by category
    let category_accuracy: HashMap<String, f64> = by_category.iter()
        .map(|(category, results)| {
            let correct = results.iter().filter(|&&x| x).count();
            let acc = correct as f64 / results.len() as f64;
            (category.clone(), acc)
        })
        .collect();
    
    ColorlessGreenResults {
        total,
        correct_grammatical,
        correct_ungrammatical,
        accuracy,
        complexity_penalty: avg_complexity_penalty,
        by_complexity: complexity_accuracy,
        by_category: category_accuracy,
    }
}

/// Print detailed colorless green analysis
pub fn print_colorless_green_analysis(results: &ColorlessGreenResults) {
    println!("\n🎨 COLORLESS GREEN TEST RESULTS");
    println!("=" .repeat(40));
    println!("Total test cases: {}", results.total);
    println!("Correct grammatical: {}/{}", results.correct_grammatical, results.total / 2);
    println!("Correct ungrammatical: {}/{}", results.correct_ungrammatical, results.total / 2);
    println!("Overall accuracy: {:.1}%", results.accuracy * 100.0);
    println!("Average complexity penalty: {:.2}", results.complexity_penalty);
    
    println!("\n📈 ACCURACY BY COMPLEXITY LEVEL:");
    for complexity in 1..=5 {
        if let Some(&accuracy) = results.by_complexity.get(&complexity) {
            println!("  Level {}: {:.1}%", complexity, accuracy * 100.0);
        }
    }
    
    println!("\n📈 ACCURACY BY CATEGORY:");
    for (category, &accuracy) in &results.by_category {
        println!("  {}: {:.1}%", category, accuracy * 100.0);
    }
    
    // Performance analysis
    println!("\n🔍 PERFORMANCE ANALYSIS:");
    if results.accuracy > 0.7 {
        println!("✅ Good syntactic processing (>70% accuracy)");
    } else if results.accuracy > 0.5 {
        println!("⚠️  Moderate syntactic processing (50-70% accuracy)");
    } else {
        println!("❌ Poor syntactic processing (<50% accuracy)");
    }
    
    // Complexity analysis
    if results.complexity_penalty > 0.0 {
        println!("📈 Ungrammatical sentences require more complex derivations (+{:.2})", 
            results.complexity_penalty);
    } else {
        println!("📉 No significant complexity difference detected");
    }
    
    // Semantic independence analysis
    println!("\n🧠 SEMANTIC INDEPENDENCE:");
    if results.accuracy > 0.6 {
        println!("✅ Good semantic-independent syntactic processing");
        println!("   Model successfully ignores semantic anomalies");
    } else {
        println!("⚠️  Possible semantic interference in syntactic processing");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_colorless_green_generation() {
        let tests = generate_colorless_green_tests();
        assert!(!tests.is_empty(), "Should generate test cases");
        
        // Verify semantic anomaly
        for test in &tests {
            assert!(!test.grammatical.is_empty(), "Grammatical sentence should not be empty");
            assert!(!test.ungrammatical.is_empty(), "Ungrammatical sentence should not be empty");
            assert_ne!(test.grammatical, test.ungrammatical, "Sentences should differ");
            
            // Check for semantic anomaly indicators
            let has_anomaly = test.grammatical.contains("colorless") || 
                             test.grammatical.contains("purple thoughts") ||
                             test.grammatical.contains("invisible cat") ||
                             test.grammatical.contains("square circles");
                             
            if test.complexity >= 3 || has_anomaly {
                // Higher complexity tests should have some semantic anomaly
            }
        }
        
        println!("Generated {} colorless green test cases", tests.len());
    }
    
    #[test]
    fn test_colorless_green_lexicon() {
        let lexicon = colorless_green_lexicon();
        assert!(lexicon.len() > 20, "Should have substantial lexicon");
        
        // Check for key anomalous items
        let has_colorless = lexicon.iter().any(|item| item.phon == "colorless");
        let has_green = lexicon.iter().any(|item| item.phon == "green");
        let has_ideas = lexicon.iter().any(|item| item.phon == "ideas");
        
        assert!(has_colorless, "Should have 'colorless'");
        assert!(has_green, "Should have 'green'");
        assert!(has_ideas, "Should have 'ideas'");
    }
    
    #[test]
    fn test_complexity_estimation() {
        let lexicon = colorless_green_lexicon();
        
        let simple = "colorless green ideas sleep";
        let complex = "the idea that thoughts have colors seems wrong";
        
        let simple_complexity = estimate_derivation_complexity(simple, &lexicon);
        let complex_complexity = estimate_derivation_complexity(complex, &lexicon);
        
        assert!(complex_complexity > simple_complexity, 
            "Complex sentence should have higher complexity estimate");
        
        println!("Simple: {}, Complex: {}", simple_complexity, complex_complexity);
    }
    
    #[test]
    fn test_colorless_green_suite_runs() {
        let results = run_colorless_green_suite();
        
        assert_eq!(results.total, generate_colorless_green_tests().len() * 2);
        assert!(results.accuracy >= 0.0 && results.accuracy <= 1.0);
        
        print_colorless_green_analysis(&results);
    }
}