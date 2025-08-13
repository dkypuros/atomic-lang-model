This project, the **Atomic Language Model**, is a hybrid system that combines a formal, rule-based grammar engine with a probabilistic language model. Its main goal is to create an extremely lightweight (<50kB) and efficient language model that has mathematically provable properties, particularly regarding its ability to handle the recursive nature of human language.

The procect addresses a key challenge in AI by bridging the gap between symbolic reasoning (which provides structure and guarantees) and statistical learning (which provides flexibility and real-world performance). This hybrid approach aims for the best of both worlds: a model that doesn't make basic grammatical mistakes but can still generate plausible and creative text.

---

## What the Project Does

The project has two main components that work together: a Rust core and a Python layer.

### 1. The Rust Core: A Formal Grammar Engine ⚙️
The heart of the project is a tiny, ultra-fast engine written in Rust that implements principles from a linguistic theory called **Minimalist Grammar**.

* **It's a validator, not a guesser.** Its job is to determine with 100% certainty whether a sentence is grammatically possible according to its rules. It doesn't deal in probabilities.
* **It handles complex syntax.** It's built around core linguistic operations called "Merge" and "Move" that allow it to understand complex, nested sentences like *"the student who the teacher praised left"*.
* **It's provably powerful.** The project includes tests and formal proofs (using the Coq theorem prover) to demonstrate that this core engine can handle infinitely recursive patterns—a key feature of human language that simpler models can't manage.

### 2. The Python Layer: A Probabilistic Model 🎲
This part is a simple, standard language model that learns statistical patterns from grammar rules.

* **It predicts and generates.** Like other language models, it can generate new sentences or predict the most likely next word in a sequence (e.g., after "the student," it might predict "left" with 40% probability and "smiled" with 30%).
* **It's lightweight.** The implementation is self-contained in a single file (`tiny_lm.py`) with no external dependencies.

### How They Work Together: The Hybrid Approach
The project's cleverness lies in how it combines these two parts. The Python model acts as the creative engine, while the Rust core is the strict editor.

1.  **Generation:** The Python model generates a sentence.
2.  **Validation:** The Rust core checks if the sentence is grammatically valid. If not, it's thrown out, and the process repeats.
3.  **Prediction:** The Python model suggests a list of possible next words with probabilities. The Rust core filters this list, removing any words that would result in a grammatical error. The probabilities of the remaining valid words are then recalculated.

This ensures that all output is not only statistically likely but also **formally correct**.

---

## What Makes It Special

This isn't just another language model. It has several unique and powerful features.

### Mathematical Rigor
The project is built on a foundation of formal proofs. It uses tests to demonstrate its ability to generate patterns like $a^nb^n$ (e.g., `a a a b b b`), which is a classic way to prove a grammar is more powerful than simple finite-state machines. The included Coq file (`Minimalist.v`) takes this a step further by formalizing these properties in a machine-checkable proof system.

### Advanced Linguistic Evaluation
It doesn't just check for correctness; it evaluates its syntactic capabilities against established linguistic benchmarks:
* **Agreement Suite:** Tests its ability to handle long-distance dependencies, like making sure a subject agrees with its verb even when many words separate them (e.g., "the **student** near the teachers **is** here," not "are here").
* **Colorless Green Suite:** Tests its understanding of syntax independent of meaning, using sentences like Noam Chomsky's famous "Colorless green ideas sleep furiously."

### An Experiment in Category Theory 🤯
The project includes a forward-thinking experiment called the **"Fibration Bridge."** This uses a high-level mathematical concept (Grothendieck fibrations) to create a clean, modular architecture.
* **Base:** The pure syntax from the Rust core.
* **Fibres:** Different kinds of data that "live on top of" the syntax. The project implements several fibres:
    * **ProbabilityFibre:** Statistical weights.
    * **EmbeddingFibre:** Vector representations for neural networks.
    * **ProofFibre:** Formal verification data.
    * **BM25Fibre:** Relevance scores for information retrieval (search).

This architecture provides a principled way to combine many different types of models (symbolic, statistical, neural, search) while guaranteeing they remain coherent and consistent.