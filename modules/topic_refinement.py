import dspy
from config import config



class TopicRefinement(dspy.Module):
    def __init__(self):
        super().__init__()
        self.llm_choice = config['module_assignments']["topic_refinement"]
        self.llm_config = config['llms'][self.llm_choice]
        self.generate_refined_prompt = dspy.ChainOfThought(
            "topic: str -> refined_prompt: str",
        )
        
    def forward(self, topic):
        
        # Dynamically select the LLM based on configuration
        dspy.configure(lm=self.get_llm_instance())

        # Define the instruction for prompt refinement
        refinement_instruction = (
            "Transform the following topic into a clear, concise prompt "
            "suitable for generating a script for an explainer video. "
            "Consider the target audience (e.g., high school students) "
            "and ensure the prompt is specific enough to guide the script generation."
        )

        # Execute the ChainOfThought module to generate the refined prompt
        prediction = self.generate_refined_prompt(
            topic=f"{refinement_instruction}\nTopic: {topic}"
        )
        return dspy.Prediction(refined_prompt=prediction.refined_prompt)

    def get_llm_instance(self):
        """Instantiates the appropriate LLM based on configuration."""
        if self.llm_choice == "openai":
            return dspy.LM(api_key=self.llm_config["api_key"], model=self.llm_config["model"])
        elif self.llm_choice == "google":
            return dspy.Google(api_key=self.llm_config["api_key"], model=self.llm_config["model"])
        elif self.llm_choice == "ollama":
            # Assuming you have a way to interact with Ollama via an API or a library
            return dspy.OllamaLocal(model=self.llm_config["model"], api_base=self.llm_config["api_base"], api_key=self.llm_config["api_key"])
            # return dspy.Ollama(url=self.llm_config["url"], model=self.llm_config["model"])
        else:
            raise ValueError(f"Unknown LLM choice: {self.llm_choice}")
        

if __name__ == "__main__":
    module = TopicRefinement()
    prediction = module("How to build a chatbot using Python")
    print(prediction.refined_prompt)