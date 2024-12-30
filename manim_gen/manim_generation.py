import dspy
from config import config

from modules.scene_management import SceneManager

class ManimCodeGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.llm_choice = config['module_assignments']["manim_code_generation"]
        self.llm_config = config['llms'][self.llm_choice]
        self.generate_manim_code = dspy.ChainOfThought(
            "scene_description: list -> manim_code"
        )
        
    def forward(self, scene_description):
        dspy.configure(lm=self.get_llm_instance())

        prompt = (
            "Generate Manim code for the following scene description:\n"
            f"{scene_description}\n\n"
            "We do not import images or videos in this code. "
            "We code visulaztion using manim code only nothing else"
            "Scene Description: incudes text, visual cues and transcript"
            "The code should create an animation that visually explains the concept "
            "and aligns with the provided text and visual cues."
        )
        manim_code = self.generate_manim_code(scene_description=prompt).manim_code
        return dspy.Prediction(manim_code=manim_code)

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

    module = SceneManager()
    prediction = module("""Introduction:
Singular Value Decomposition (SVD) is a powerful mathematical technique used in linear algebra to decompose a matrix into three distinct matrices. This decomposition provides insights into the structure and properties of the original matrix, making SVD an essential tool in various fields such as statistics, signal processing, and machine learning. By identifying the most significant singular values and vectors, SVD facilitates data compression, noise reduction, and the extraction of meaningful patterns from complex datasets. Its applications range from image processing, where it helps compress images while preserving essential features, to natural language processing, where it enhances information retrieval through methods like Latent Semantic Analysis. Understanding the concept of SVD is vital for effectively utilizing its capabilities in data analysis and manipulation.

Background:
Singular Value Decomposition (SVD) is a mathematical technique in linear algebra that decomposes a matrix into three matrices, providing insights into the structure and properties of the original matrix. It is represented as \( A = U \Sigma V^T \), where \( A \) is the original matrix, \( U \) contains the left singular vectors, \( \Sigma \) is a diagonal matrix of singular values, and \( V^T \) contains the right singular vectors. SVD is extensively used in various applications, including image compression, where it reduces data size while preserving essential features, and in natural language processing, where it helps uncover relationships between terms and documents. Its versatility makes SVD a crucial tool in fields such as statistics, signal processing, and machine learning.

Core Explanation:
Singular Value Decomposition (SVD) is a method of decomposing a matrix into three components: U, Σ, and V*, where U and V* are orthogonal matrices and Σ is a diagonal matrix of singular values. This decomposition is useful for various applications, including dimensionality reduction, data compression, and noise reduction, as it highlights the most significant features of the data.

Visual Cues with concreate examples to improve understanding (We are using manim for animations):
1. **Matrix Decomposition Animation**: Start with a 3x3 matrix and animate the process of SVD, showing how it decomposes into three matrices: U (left singular vectors), Σ (singular values), and V^T (right singular vectors). Highlight the significance of each component in the decomposition.

2. **Image Compression Example**: Use a grayscale image and animate the SVD process to show how the image can be reconstructed using only the top k singular values. Display the original image alongside the compressed version to illustrate the reduction in data while maintaining essential features.

3. **Latent Semantic Analysis Visualization**: Create a 2D plot representing documents and terms in a semantic space. Use SVD to reduce the dimensionality of this space and animate how the relationships between terms and documents become clearer, emphasizing the clustering of similar terms and documents.

4. **Real-World Applications**: Show various applications of SVD in fields like statistics, signal processing, and machine learning. Use icons or images to represent each field and animate connections to the SVD process, reinforcing its versatility and importance.

5. **Interactive Component**: Consider adding an interactive element where viewers can manipulate the number of singular values used in the image compression example, allowing them to see firsthand how this affects the quality of the reconstructed image.

Conclusion:
In conclusion, Singular Value Decomposition is a powerful mathematical tool that enables the analysis and manipulation of data across various fields. Its ability to decompose matrices into significant components allows for effective data compression, improved information retrieval, and enhanced text analysis. The applications of SVD in statistics, signal processing, machine learning, and natural language processing highlight its importance in modern data science and engineering. By leveraging SVD, researchers and practitioners can gain deeper insights into complex datasets, making it an essential technique in the toolkit of data analysis.

Naration Script:
Welcome to our exploration of Singular Value Decomposition, commonly known as SVD. Today, we will delve into this powerful mathematical technique that plays a crucial role in various fields, including statistics, signal processing, and machine learning. 

At its core, SVD is a method for decomposing a matrix into three distinct components: two orthogonal matrices and a diagonal matrix containing singular values. This breakdown not only simplifies complex data but also highlights the most significant features, making it easier to analyze and manipulate.

In the realm of image processing, SVD is particularly valuable. It allows us to compress images by retaining only the most important singular values and vectors. This means we can significantly reduce the amount of data needed to represent an image while still preserving its essential characteristics. Imagine being able to store high-quality images using less space—this is the power of SVD in action.

Moreover, in natural language processing, SVD is utilized in techniques like Latent Semantic Analysis, or LSA. This approach helps uncover relationships between terms and documents, enhancing our ability to retrieve information and analyze text effectively. By revealing hidden patterns in data, SVD improves our understanding of language and context.

In summary, Singular Value Decomposition is a versatile tool that aids in data analysis across various scientific and engineering disciplines. Its ability to simplify complex data structures while retaining critical information makes it an invaluable asset in our quest to understand and manipulate data.

Thank you for joining us in this discussion on Singular Value Decomposition. We hope you now have a clearer understanding of this essential concept and its applications.

Final Script fot Video Explainer using Narration Script and Visual Cues:
**[Video Explainer Script: Singular Value Decomposition]**

**[Narration Script]**
"Welcome to our explainer on Singular Value Decomposition, or SVD. SVD is a powerful mathematical technique used in various fields, including statistics, signal processing, and machine learning. 

Imagine you have a large dataset, like an image or a collection of documents. SVD helps us break down this complex data into simpler, more manageable parts. 

In image processing, for instance, SVD can compress images by focusing on the most significant features. By retaining only the most important singular values and vectors, we can reduce the amount of data needed to represent the image while still preserving its essential characteristics. 

[Visual Cue: Show a side-by-side comparison of a high-resolution image and its compressed version, highlighting the key features that remain intact.]

In the realm of natural language processing, SVD plays a crucial role in techniques like Latent Semantic Analysis, or LSA. This method uncovers hidden relationships between terms and documents, enhancing our ability to retrieve information and analyze text effectively.

[Visual Cue: Display a diagram illustrating the relationship between words and documents, with clusters showing related terms.]

Overall, Singular Value Decomposition is a vital tool for understanding and manipulating data across various scientific and engineering disciplines. It allows us to simplify complex datasets, making them easier to analyze and interpret.

[Visual Cue: Conclude with a summary slide that lists the key applications of SVD in image processing and natural language processing.]

Thank you for watching! We hope this video has helped you understand the concept of Singular Value Decomposition.""")
    

    manim_gen = ManimCodeGenerator()
    manim_code = manim_gen(prediction.scenes.scenes)
    print(manim_code.manim_code)