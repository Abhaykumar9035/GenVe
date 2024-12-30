import dspy
from config import config


class PreambleGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.llm_choice = config['module_assignments']["script_generation"]
        self.llm_config = config['llms'][self.llm_choice]

    def forward(self, topic):
        dspy.configure(lm=self.get_llm_instance())
        preamble = dspy.ChainOfThought("topic -> context")(topic=topic)
        return dspy.Prediction(context=preamble.context)
    
    def get_llm_instance(self):
        """Instantiates the appropriate LLM based on configuration."""
        if self.llm_choice == "ollama":
            # Assuming you have a way to interact with Ollama via an API or a library
            return dspy.OllamaLocal(model=self.llm_config["model"], api_base=self.llm_config["api_base"], api_key=self.llm_config["api_key"])
            # return dspy.Ollama(url=self.llm_config["url"], model=self.llm_config["model"])
        # elif self.llm_choice == "google":
        #     genai.configure(api_key=self.llm_config["api_key"])
        #     return genai.GenerativeModel(self.llm_config["model"])
        else:
            return dspy.LM(api_key=self.llm_config["api_key"], model=self.llm_config["model"])
        


class ScriptGeneration(dspy.Module):
    def __init__(self, generate_preamble):
        super().__init__()
        self.generate_preamble = generate_preamble
        self.llm_choice = config['module_assignments']["script_generation"]
        self.llm_config = config['llms'][self.llm_choice]
        self.generate_section = dspy.ChainOfThought(
            "context, query -> answer"
        )
        self.generate_script = dspy.ChainOfThought(
            "topic, refined_prompt, script_sections -> final_script"
        )

    def forward(self, topic, refined_prompt):

        dspy.configure(lm=self.get_llm_instance())

        preamble = self.generate_preamble(topic=topic)
        context = preamble.context

        sections = [
            "Introduction",
            "Core Explanation",
            "Visual Cues with concreate examples to improve understanding (We are using manim for animations)",
            "Conclusion",
            "Naration Script",
            "Final Script fot Video Explainer using Narration Script and Visual Cues"
            
        ]
        script_sections = []

        for section in sections:
            query = f"Generate the {section} section for the topic: {topic}."
            section_content = self.generate_section(context=context, query=query).answer
            script_sections.append(f"{section}:\n{section_content}")

        final_script = "\n\n".join(script_sections)
        return dspy.Prediction(final_script=final_script)
    
    def get_llm_instance(self):
        """Instantiates the appropriate LLM based on configuration."""
        if self.llm_choice == "ollama":
            # Assuming you have a way to interact with Ollama via an API or a library
            return dspy.OllamaLocal(model=self.llm_config["model"], api_base=self.llm_config["api_base"], api_key=self.llm_config["api_key"])
            # return dspy.Ollama(url=self.llm_config["url"], model=self.llm_config["model"])
        # elif self.llm_choice == "google":
        #     genai.configure(api_key=self.llm_config["api_key"])
        #     return genai.GenerativeModel(self.llm_config["model"])
        else:
            return dspy.LM(api_key=self.llm_config["api_key"], model=self.llm_config["model"])
  
        

if __name__ == "__main__":
    preamble = PreambleGenerator()

    module = ScriptGeneration(preamble)
    prediction = module("Explain the concept of Singular Value decompsotion", "Create a script for a short explainer video (approximately 4-5 minutes) about Singular Value Decomposition (SVD). The target audience is high school students with a basic understanding of matrices. The video should explain what SVD is, why it's useful, and how it works at a high level, without getting bogged down in complex mathematical details. Use clear, concise language and visual aids (e.g., animations, diagrams) to illustrate the concepts. Include an analogy or real-world example to help students understand the practical applications of SVD. The tone should be engaging and informative.")
    print(prediction.final_script)
