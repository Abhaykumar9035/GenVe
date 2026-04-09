from manim import *

class SVDAnimation(Scene):
    def construct(self):
        # Introduction to SVD
        text1 = Text("Introduction to SVD", font_size=48)
        self.play(Write(text1))
        self.wait(2)
        self.play(FadeOut(text1))

        # Matrix Decomposition
        text2 = Text("Matrix Decomposition", font_size=48)
        self.play(Write(text2))
        self.wait(1)

        A = Matrix([[1, 2], [3, 4]], fill_color=YELLOW)
        A.animate.to_edge(UP)
        U = Matrix([[1, 0], [0, 1]], fill_color=BLUE)
        S = Matrix([[2, 0], [0, 3]], fill_color=GREEN)
        V = Matrix([[1, 1], [1, -1]], fill_color=RED)
        V_T = V.copy()

        eq = MathTex(r"A = U \cdot S \cdot V^T", font_size=60).next_to(A, DOWN, buff=0.5)
        self.play(A.animate.to_edge(UP), U.animate.to_edge(UP), S.animate.to_edge(UP), V.animate.to_edge(UP), Write(eq))
        self.wait(2)

        # Singular Values
        text3 = Text("Singular Values", font_size=48)
        self.play(Write(text3))
        self.wait(1)

        s1 = MathTex("\sigma_1 = 2", font_size=48).move_to(S)
        s2 = MathTex("\sigma_2 = 3", font_size=48).move_to(S)
        self.play(s1.animate.to_edge(UP), s2.animate.to_edge(UP))
        self.wait(2)

        # Animated SVD Process
        text4 = Text("Animated SVD Process", font_size=48)
        self.play(Write(text4))
        self.wait(1)

        # Simulate SVD algorithm transformation
        self.play(A.animate.shift(DOWN * 500))
        U.animate.shift(DOWN * 500)
        S.animate.shift(DOWN * 500)
        V.animate.shift(DOWN * 500)

        self.wait(3)

        # Summary
        text5 = Text("Summary", font_size=48)
        self.play(Write(text5))
        self.wait(1)

        U.to_edge(UP)
        S.to_edge(UP)
        V.to_edge(UP)
        self.play(U.animate.scale(1.5).shift(DOWN*400), S.animate.scale(1.5).shift(DOWN*400), V.animate.scale(1.5).shift(DOWN*400))

        applications = VGroup(
            Text("Dimensionality Reduction", font_size=36),
            Text("Noise Reduction", font_size=36),
            Text("Recommendation Systems", font_size=36)
        ).arrange(DOWN)
        applications.to_edge(DOWN)

        self.play(Write(applications))
        self.wait(3)

        self.play(FadeOut(*self.mobjects))
