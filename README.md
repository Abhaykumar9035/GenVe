****GenVe (Generative Video Explainers)****

**Overview**

GenVe is a tool designed to automate the generation of Manim-based explainer videos using a scene description. It takes detailed descriptions of mathematical concepts or processes and creates animated visuals through the Manim library. It allows seamless integration with large language models to generate the required animation code.




**Workflow**

Input: A detailed scene description including text, visual cues, and transcript.
Processing: The scene description is passed to a pre-configured large language model.
Output: The model generates the corresponding Manim code for animation.




**Installation**

Clone the repository:


Run this in terminal of code editor
git clone <repository_url>
(Here url is: https://github.com/Abhaykumar9035/GenVe )

cd <repository_directory>
(Here repository dir is: GenVe)

Install dependencies:

pip install -r requirements.txt
Ensure the config.py file is properly configured with your LLM (Ollama or others).

All files must be visible in your local machine filebar.
Run the project:

python <filename.py>
(Here it is : manim_generation)
