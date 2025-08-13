# 🧪 Practical Tutorials & Examples

> **Hands-on tutorials to master recursive language processing with real-world applications**

Learn by building! These goal-oriented tutorials show how to use the Atomic Language Model for practical applications, from simple text processing to advanced linguistic analysis.

## 🎯 Tutorial 1: Building a Grammar Checker

**Goal**: Create a command-line grammar checker that validates sentences using our formal grammar.

### Step 1: Set Up the Validator
```bash
cd atomic-lang-model
```

Create `grammar_checker.rs`:
```rust
use atomic_lang_model::{parse_sentence, test_lexicon, DerivationError};

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} \"sentence to check\"", args[0]);
        return;
    }
    
    let sentence = &args[1];
    let lexicon = test_lexicon();
    
    match parse_sentence(sentence, &lexicon) {
        Ok(result) => {
            println!("✅ VALID: '{}'", sentence);
            println!("   Category: {}", result.label);
            println!("   Structure: {}", result.linearize());
        }
        Err(e) => {
            println!("❌ INVALID: '{}'", sentence);
            println!("   Error: {:?}", e);
        }
    }
}
```

### Step 2: Test Your Checker
```bash
# Compile the checker
rustc --edition 2021 -L target/release/deps grammar_checker.rs -o grammar_checker

# Test valid sentences
./grammar_checker "the student left"
# ✅ VALID: 'the student left'

./grammar_checker "every teacher who arrived smiled"
# ✅ VALID: 'every teacher who arrived smiled'

# Test invalid sentences
./grammar_checker "the the student left"
# ❌ INVALID: 'the the student left'

./grammar_checker "student left the"
# ❌ INVALID: 'student left the'
```

### Step 3: Batch Processing
Create a file checker script:
```bash
cat > check_file.sh << 'EOF'
#!/bin/bash
while IFS= read -r line; do
    echo "Checking: $line"
    ./grammar_checker "$line"
    echo "---"
done < "$1"
EOF

chmod +x check_file.sh
```

Test with a sentence file:
```bash
# Create test sentences
cat > sentences.txt << EOF
the student left
every teacher smiled
the student the left
book red the
the student who the teacher praised left
EOF

# Check all sentences
./check_file.sh sentences.txt
```

---

## 🎯 Tutorial 2: Building a Next-Token Predictor

**Goal**: Create a probabilistic text completion system using the hybrid model.

### Step 1: Python Predictor
```python
# predictor.py
from tiny_lm import ProbGrammar
from hybrid_model import HybridLanguageModel
import sys

class SmartPredictor:
    def __init__(self):
        self.prob_model = ProbGrammar()
        self.hybrid_model = HybridLanguageModel()
    
    def predict_next(self, prefix, k=5000, top_k=5):
        """Predict most likely next tokens"""
        print(f"Analyzing: '{prefix}'")
        print("=" * 50)
        
        # Get predictions
        predictions = self.hybrid_model.predict_next(prefix, k=k, validate=True)
        
        print("Top predictions (grammatically valid only):")
        for i, (token, prob) in enumerate(predictions[:top_k]):
            bar = "█" * int(prob * 30)  # Visual probability bar
            print(f"{i+1:2d}. {token:10} {prob:.3f} {bar}")
        
        # Show some completions
        print("\nSample completions:")
        for i in range(3):
            completion = self.hybrid_model.get_valid_continuations(prefix, beam_size=1)[0]
            print(f"   • {completion}")
    
    def interactive_mode(self):
        """Interactive prediction session"""
        print("🤖 Smart Predictor - Type prefixes to get predictions")
        print("Commands: 'quit' to exit, 'help' for usage")
        print()
        
        while True:
            try:
                prefix = input("Enter prefix: ").strip()
                if prefix.lower() == 'quit':
                    break
                elif prefix.lower() == 'help':
                    print("Enter a sentence beginning (e.g., 'the student who')")
                    continue
                elif prefix:
                    self.predict_next(prefix)
                    print()
            except KeyboardInterrupt:
                break
        
        print("\nGoodbye! 👋")

if __name__ == "__main__":
    predictor = SmartPredictor()
    
    if len(sys.argv) > 1:
        # Command line mode
        prefix = " ".join(sys.argv[1:])
        predictor.predict_next(prefix)
    else:
        # Interactive mode
        predictor.interactive_mode()
```

### Step 2: Try the Predictor
```bash
cd ../python

# Command line usage
python predictor.py "the student"
python predictor.py "the student who"
python predictor.py "every teacher"

# Interactive mode
python predictor.py
# Then type: the book that Mary
# Then type: every student who
```

### Step 3: Batch Prediction
Create a batch predictor:
```python
# batch_predictor.py
import json
from predictor import SmartPredictor

def batch_predict(input_file, output_file):
    predictor = SmartPredictor()
    
    with open(input_file) as f:
        prefixes = [line.strip() for line in f if line.strip()]
    
    results = []
    for prefix in prefixes:
        predictions = predictor.hybrid_model.predict_next(prefix, k=3000)
        results.append({
            'prefix': prefix,
            'predictions': [{'token': token, 'probability': float(prob)} 
                          for token, prob in predictions[:5]]
        })
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Processed {len(prefixes)} prefixes → {output_file}")

if __name__ == "__main__":
    # Create test prefixes
    with open('test_prefixes.txt', 'w') as f:
        f.write("the student\n")
        f.write("every teacher who\n")
        f.write("the book that\n")
        f.write("some students\n")
    
    batch_predict('test_prefixes.txt', 'predictions.json')
```

---

## 🎯 Tutorial 3: Building a Simple DSL Parser

**Goal**: Extend the grammar to handle a domain-specific language for mathematical expressions.

### Step 1: Define Math Grammar Rules
```rust
// math_grammar.rs - Add to src/lib.rs or create separate module

use crate::{SyntacticObject, Feature, Category, LexItem};

pub fn math_lexicon() -> Vec<LexItem> {
    vec![
        // Numbers
        LexItem::new("1", &[Feature::Cat(Category::N)]),
        LexItem::new("2", &[Feature::Cat(Category::N)]),
        LexItem::new("42", &[Feature::Cat(Category::N)]),
        
        // Operators
        LexItem::new("+", &[Feature::Cat(Category::V), Feature::Sel(Category::N), Feature::Sel(Category::N)]),
        LexItem::new("*", &[Feature::Cat(Category::V), Feature::Sel(Category::N), Feature::Sel(Category::N)]),
        LexItem::new("=", &[Feature::Cat(Category::V), Feature::Sel(Category::N), Feature::Sel(Category::N)]),
        
        // Parentheses (for recursion)
        LexItem::new("(", &[Feature::Cat(Category::D), Feature::Sel(Category::N)]),
        LexItem::new(")", &[Feature::Cat(Category::D)]),
    ]
}

pub fn parse_math_expression(expr: &str) -> Result<SyntacticObject, DerivationError> {
    // Tokenize the expression
    let tokens: Vec<&str> = expr.split_whitespace().collect();
    let lexicon = math_lexicon();
    
    // Use our standard parsing with math lexicon
    parse_sentence(&tokens.join(" "), &lexicon)
}
```

### Step 2: Math Expression Parser
```python
# math_parser.py
import sys
sys.path.append('../atomic-lang-model/target/release')  # Adjust path as needed

class MathExpressionParser:
    def __init__(self):
        # You would call the Rust function here
        # For demo, we'll simulate the parsing logic
        pass
    
    def parse(self, expression):
        """Parse mathematical expression"""
        print(f"Parsing: {expression}")
        
        # Simulate recursive descent parsing
        tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()
        
        try:
            result = self.parse_expression(tokens, 0)
            print(f"✅ Valid expression")
            print(f"   Structure: {result['tree']}")
            print(f"   Evaluation: {result['value']}")
        except Exception as e:
            print(f"❌ Invalid expression: {e}")
    
    def parse_expression(self, tokens, pos):
        """Simple recursive parser for demo"""
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")
        
        # Handle parentheses
        if tokens[pos] == '(':
            pos += 1
            result = self.parse_expression(tokens, pos)
            pos = result['next_pos']
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Missing closing parenthesis")
            return {'tree': f"({result['tree']})", 'value': result['value'], 'next_pos': pos + 1}
        
        # Handle numbers
        if tokens[pos].isdigit():
            return {'tree': tokens[pos], 'value': int(tokens[pos]), 'next_pos': pos + 1}
        
        # Handle operators (simplified)
        if pos + 2 < len(tokens) and tokens[pos + 1] in ['+', '*']:
            left = self.parse_expression(tokens, pos)
            op = tokens[left['next_pos']]
            right = self.parse_expression(tokens, left['next_pos'] + 1)
            
            if op == '+':
                value = left['value'] + right['value']
            else:  # *
                value = left['value'] * right['value']
            
            return {
                'tree': f"{left['tree']} {op} {right['tree']}",
                'value': value,
                'next_pos': right['next_pos']
            }
        
        raise ValueError(f"Unexpected token: {tokens[pos]}")

# Example usage
if __name__ == "__main__":
    parser = MathExpressionParser()
    
    # Test expressions
    test_expressions = [
        "2 + 3",
        "( 2 + 3 ) * 4",
        "1 + 2 * 3",
        "( ( 1 + 2 ) * 3 ) + 4",
        "2 + + 3",  # Invalid
        "( 2 + 3",   # Invalid
    ]
    
    for expr in test_expressions:
        parser.parse(expr)
        print()
```

### Step 3: Interactive Math Shell
```python
# math_shell.py
from math_parser import MathExpressionParser

class MathShell:
    def __init__(self):
        self.parser = MathExpressionParser()
        self.variables = {}
    
    def run(self):
        print("🧮 Mathematical Expression Parser")
        print("Based on Atomic Language Model formal grammar")
        print("Commands: 'quit' to exit, 'vars' to show variables")
        print("Examples: '2 + 3', '( 1 + 2 ) * 4', 'x = 5 + 3'")
        print()
        
        while True:
            try:
                expr = input("math> ").strip()
                
                if expr.lower() == 'quit':
                    break
                elif expr.lower() == 'vars':
                    print("Variables:", self.variables)
                    continue
                elif '=' in expr and not expr.startswith('('):
                    # Variable assignment
                    var, value_expr = expr.split('=', 1)
                    var = var.strip()
                    value_expr = value_expr.strip()
                    
                    # Parse the value expression
                    self.parser.parse(value_expr)
                    # In real implementation, store the parsed result
                    print(f"Variable '{var}' assigned")
                    continue
                elif expr:
                    self.parser.parse(expr)
                
                print()
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                print()
        
        print("\nGoodbye! 🔢")

if __name__ == "__main__":
    shell = MathShell()
    shell.run()
```

---

## 🎯 Tutorial 4: Integrating with Neural Embeddings

**Goal**: Show how the Fibration Bridge can integrate word embeddings with formal grammar.

### Step 1: Simple Embedding Integration
```python
# embedding_integration.py
import numpy as np
from collections import defaultdict

class EmbeddingGrammarBridge:
    """Demonstrates Fibration Bridge with embeddings"""
    
    def __init__(self):
        # Simple word embeddings (in practice, use pre-trained)
        self.embeddings = {
            'the': np.array([0.1, 0.2, 0.3]),
            'student': np.array([0.4, 0.5, 0.6]),
            'teacher': np.array([0.4, 0.6, 0.5]),  # Similar to student
            'left': np.array([0.7, 0.1, 0.2]),
            'arrived': np.array([0.7, 0.2, 0.1]),  # Similar to left
            'who': np.array([0.2, 0.3, 0.4]),
        }
        
        # Syntax categories (from our formal grammar)
        self.categories = {
            'the': 'DP',
            'student': 'N', 
            'teacher': 'N',
            'left': 'V',
            'arrived': 'V',
            'who': 'C',
        }
    
    def pullback_transform(self, base_transformation, embeddings):
        """
        Demonstrate pullback: when syntax transforms, embeddings transform coherently
        
        Example: student → teacher transformation
        """
        print("🔄 Fibration Pullback Operation")
        print("=" * 40)
        
        # Base transformation (syntax level)
        old_word, new_word = base_transformation
        print(f"Base transformation: {old_word} → {new_word}")
        print(f"Syntax category preserved: {self.categories[old_word]} → {self.categories[new_word]}")
        
        # Fibre transformation (embedding level)
        old_embedding = embeddings[old_word]
        new_embedding = embeddings[new_word]
        
        print(f"\nEmbedding pullback:")
        print(f"  {old_word}: {old_embedding}")
        print(f"  {new_word}: {new_embedding}")
        print(f"  Similarity: {np.dot(old_embedding, new_embedding):.3f}")
        
        # Show coherence: similar syntax → similar embeddings
        syntax_similar = self.categories[old_word] == self.categories[new_word]
        embed_similar = np.dot(old_embedding, new_embedding) > 0.7
        
        print(f"\nCoherence check:")
        print(f"  Syntax similar: {syntax_similar}")
        print(f"  Embeddings similar: {embed_similar}")
        print(f"  Pullback preserves structure: {syntax_similar == embed_similar}")
    
    def demonstrate_fibration(self):
        """Show the complete fibration architecture"""
        print("🏗️ Fibration Architecture Demonstration")
        print("=" * 50)
        
        # Show base category (syntax)
        print("Base Category (Pure Syntax):")
        for word, category in self.categories.items():
            print(f"  {word} : {category}")
        
        print("\nFibre (Embeddings):")
        for word, embedding in self.embeddings.items():
            print(f"  {word} → {embedding}")
        
        print("\nPullback transformations:")
        # Demonstrate several coherent transformations
        transformations = [
            ('student', 'teacher'),  # Same category: N → N
            ('left', 'arrived'),     # Same category: V → V
        ]
        
        for transformation in transformations:
            print(f"\n{'─' * 30}")
            self.pullback_transform(transformation, self.embeddings)
    
    def semantic_grammar_parsing(self, sentence):
        """Parse sentence with both syntax and semantics"""
        words = sentence.split()
        
        print(f"📝 Parsing with Grammar + Embeddings: '{sentence}'")
        print("=" * 50)
        
        # Check if all words are in our lexicon
        missing_words = [w for w in words if w not in self.categories]
        if missing_words:
            print(f"❌ Unknown words: {missing_words}")
            return
        
        # Show syntactic analysis
        print("Syntactic structure:")
        for word in words:
            category = self.categories[word]
            embedding = self.embeddings[word]
            print(f"  {word:10} | {category:3} | {embedding}")
        
        # Semantic similarity analysis
        print(f"\nSemantic analysis:")
        if len(words) >= 2:
            word1, word2 = words[0], words[-1]  # First and last word
            emb1, emb2 = self.embeddings[word1], self.embeddings[word2]
            similarity = np.dot(emb1, emb2)
            print(f"  '{word1}' ↔ '{word2}' similarity: {similarity:.3f}")
        
        # In real implementation, this would:
        # 1. Use Rust core for syntactic validation
        # 2. Use embeddings for semantic plausibility
        # 3. Combine both scores for overall sentence quality
        print("✅ Hybrid parsing complete")

if __name__ == "__main__":
    bridge = EmbeddingGrammarBridge()
    
    # Demonstrate fibration architecture
    bridge.demonstrate_fibration()
    
    print("\n" + "="*60 + "\n")
    
    # Parse sentences with hybrid approach
    test_sentences = [
        "the student left",
        "the teacher arrived",
        "the student who left",
    ]
    
    for sentence in test_sentences:
        bridge.semantic_grammar_parsing(sentence)
        print()
```

---

## 🎯 Tutorial 5: Building a Web Interface

**Goal**: Create a simple web interface for the language model using the REST API.

### Step 1: Simple HTML Interface
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Atomic Language Model Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        textarea { width: 100%; height: 100px; }
        button { padding: 10px 20px; margin: 5px; }
        .result { background: #f0f0f0; padding: 15px; margin: 10px 0; }
        .valid { background: #d4edda; color: #155724; }
        .invalid { background: #f8d7da; color: #721c24; }
        .prediction { margin: 5px 0; }
        .probability-bar { display: inline-block; height: 20px; background: #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 Atomic Language Model</h1>
        <p>The world's smallest language model with mathematical guarantees!</p>
        
        <h2>Sentence Validation</h2>
        <textarea id="sentences" placeholder="Enter sentences to validate (one per line)">the student left
student the left
the student who the teacher praised left</textarea>
        <br>
        <button onclick="validateSentences()">Validate Grammar</button>
        
        <div id="validation-results"></div>
        
        <h2>Next-Token Prediction</h2>
        <input type="text" id="prefix" placeholder="Enter sentence prefix..." value="the student who">
        <button onclick="predictNext()">Predict Next Tokens</button>
        
        <div id="prediction-results"></div>
        
        <h2>Sentence Generation</h2>
        <label>Number of sentences: <input type="number" id="count" value="5" min="1" max="10"></label>
        <button onclick="generateSentences()">Generate</button>
        
        <div id="generation-results"></div>
    </div>

    <script>
        const API_BASE = 'http://localhost:5000';
        
        async function validateSentences() {
            const textarea = document.getElementById('sentences');
            const sentences = textarea.value.split('\\n').filter(s => s.trim());
            
            const response = await fetch(`${API_BASE}/validate`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sentences: sentences})
            });
            
            const results = await response.json();
            
            let html = '<h3>Validation Results:</h3>';
            results.results.forEach(result => {
                const className = result.valid ? 'valid' : 'invalid';
                const icon = result.valid ? '✅' : '❌';
                html += `<div class="result ${className}">
                    ${icon} "${result.sentence}" (${result.tokens} tokens)
                </div>`;
            });
            
            document.getElementById('validation-results').innerHTML = html;
        }
        
        async function predictNext() {
            const prefix = document.getElementById('prefix').value;
            
            const response = await fetch(`${API_BASE}/predict`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prefix: prefix, k: 3000})
            });
            
            const results = await response.json();
            
            let html = `<h3>Predictions for "${prefix}":</h3>`;
            results.predictions.forEach((pred, i) => {
                const barWidth = Math.round(pred.probability * 200);
                html += `<div class="prediction">
                    ${i+1}. <strong>${pred.token}</strong> 
                    (${(pred.probability * 100).toFixed(1)}%)
                    <span class="probability-bar" style="width: ${barWidth}px;"></span>
                </div>`;
            });
            
            html += `<p><small>Generated from ${results.total_predictions} predictions in ${results.inference_time_ms}ms</small></p>`;
            
            document.getElementById('prediction-results').innerHTML = html;
        }
        
        async function generateSentences() {
            const count = document.getElementById('count').value;
            
            const response = await fetch(`${API_BASE}/generate`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({count: parseInt(count)})
            });
            
            const results = await response.json();
            
            let html = '<h3>Generated Sentences:</h3>';
            results.sentences.forEach((sentence, i) => {
                html += `<div class="result valid">✅ ${sentence}</div>`;
            });
            
            html += `<p><small>Generated ${results.count} sentences in ${results.generation_time_ms}ms (all grammatically guaranteed!)</small></p>`;
            
            document.getElementById('generation-results').innerHTML = html;
        }
    </script>
</body>
</html>
```

### Step 2: Start Everything
```bash
# Terminal 1: Start the API server
cd atomic-lang-model/python
python api_server.py

# Terminal 2: Serve the HTML file
cd /path/to/html/file
python -m http.server 8080

# Open browser to http://localhost:8080
```

---

## 🏆 Challenge Exercises

### Challenge 1: Extend the Grammar
Add support for adjectives and adverbs to the lexicon. Test sentences like:
- "the tall student left quickly"
- "every smart teacher who arrived early smiled"

### Challenge 2: Build a Poetry Validator  
Create a system that validates both grammar AND poetic meter (iambic pentameter).

### Challenge 3: Multi-Language Support
Extend the grammar to handle basic sentences in another language while maintaining the same formal properties.

### Challenge 4: Performance Optimization
Can you make the parsing even faster? Try different optimization techniques and measure the results.

### Challenge 5: Advanced Fibration
Implement a full fibration with multiple fibres (probabilities, embeddings, and BM-25 scores) that stay coherent across transformations.

## 📚 Related Documentation

- **[API Reference](../DEVELOPER_GUIDE/01-api-reference.md)** - Complete function documentation
- **[Mathematical Foundations](../THEORY/01-mathematical-foundations.md)** - Understand the theory
- **[Interactive Walkthrough](03-interactive-walkthrough.md)** - Guided tour of all features

---

**🎉 Congratulations! You've built real applications using the world's smallest formally verified language model. What will you create next?**