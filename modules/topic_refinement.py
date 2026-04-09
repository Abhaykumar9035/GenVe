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
        lm_instance = self.get_llm_instance()
        with dspy.context(lm=lm_instance):
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
        if self.llm_choice == "ollama":
            return dspy.LM(
                model=f"ollama_chat/{self.llm_config['model']}",
                api_base=self.llm_config["api_base"],
                api_key=self.llm_config.get("api_key", ""),
            )
        # elif self.llm_choice == "google":
        #     genai.configure(api_key=self.llm_config["api_key"])
        #     return genai.GenerativeModel(self.llm_config["model"])
        else:
            return dspy.LM(api_key=self.llm_config["api_key"], model=self.llm_config["model"])
  
        

if __name__ == "__main__":
    module = TopicRefinement()
    prediction = module("Explain the concept of Singular Value decompsotion")
    print(prediction.refined_prompt)