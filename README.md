# GenVe — Generative Video Explainers

GenVe is an automation tool that converts descriptive mathematical explanations into fully animated **Manim** videos.  
It enables educators, creators, and developers to generate high-quality explainer videos using **natural-language scene descriptions**, powered by Large Language Models (LLMs).

Whether you want to animate algebraic derivations, geometric constructions, or conceptual visualizations, GenVe handles the Manim code generation for you—end-to-end.

---

## 🚀 Key Features

- **Automated Manim Code Generation**  
  Convert detailed scene descriptions into ready-to-run Manim animation scripts.

- **LLM-Powered Workflow**  
  Integrates seamlessly with LLMs (Ollama or others) for code generation.

- **Robust Scene Description Format**  
  Accepts text, narrative audio transcript, visual cues, and mathematical expressions.

- **Developer-Friendly**  
  Simple API, clean project structure, and full local control.

---

## 🛠️ How It Works

1. **Input:**  
   Provide a detailed scene description including:
   - Explanation text  
   - Visual instructions  
   - Timing or narration cues  
   - Transcript (optional)

2. **Processing:**  
   The description is forwarded to your configured LLM backend.  
   The LLM generates Manim-compatible Python code.

3. **Output:**  
   A runnable `.py` file that uses Manim to render the animated explainer video.

---

## 📦 Installation & Setup

Follow these steps to install and run GenVe locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Abhaykumar9035/GenVe
cd GenVe
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your LLM
Open config.py in the project root and set:

LLM backend (Ollama or custom)

Model name

API endpoint

API keys (if applicable)

▶️ Running the Project
After configuration, run:

``` bash
python manim_generation.py
```
Generated Manim scene files will appear in the project workspace.

📁 Project Structure
``` bash

graphql

GenVe/
│── config.py                # LLM configuration  
│── manim_generation.py      # Main script for generating Manim code  
│── prompts/                 # Prompt templates for LLM  
│── scenes/                  # Generated Manim scene files  
│── requirements.txt         # Project dependencies  
│── README.md                # Documentation  
```

### 🧠 Recommended Scene Description Format
A good description includes:

- Scene title
- Concept summary
- Mathematical expressions
- Transitions (fade in, move, scale, highlight)
- Color or layout cues
- Exact narration text

Example:

```bash
vbnet

Title: Explaining the Pythagorean Theorem
Visual: Show a right triangle with sides a, b, and c. Highlight the square on each side.
Narration: "The Pythagorean theorem states that a² + b² = c²."
Animation: Move squares, transform labels, show area equivalence.
```
