from manim import *
# from hopital_rule_solver import solver
from math_functions import *


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 8)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation


class AlignedEquation(Scene):
    def construct(self):
        steps = steps_to_solve('(2+5)^(2+1)*(3+1)')
        # steps = steps_to_solve('(1+2^2)/3+4')
        # steps = steps_to_solve('(1^4*2^2+3^3)-2^5/4')
        # steps = steps_to_solve('24-16/4*2+3')
        # steps = steps_to_solve('((2+5)^(2+1)*(3+1)+2)/(4+1)-6')
        all_steps = [latex_for_visual(str(expression)) for expression in steps[:-1]]
        all_steps.append(str(steps[-1]))
        VERTICAL_SPACING = 1.5 * UP
        LAG_RATIO = 0.4

        formatted_steps = []
        eq_left = MathTex(all_steps[0])
        eq_equal = MathTex('=')
        eq_left.next_to(eq_equal, LEFT)
        for step in all_steps[1:]:
            eq_right = MathTex(step)
            eq_right.next_to(eq_equal, RIGHT)
            formatted_steps.append([eq_equal.copy(), eq_right])
        formatted_steps[0] = [eq_left] + formatted_steps[0]

        entire_equation = []
        for n, step in enumerate(formatted_steps):
            self.play(AnimationGroup(*[Write(x) for x in step], lag_ratio=LAG_RATIO))
            entire_equation += step
            if n + 1 < len(formatted_steps):
                self.play(AnimationGroup(*[x.animate.shift(VERTICAL_SPACING) for x in entire_equation]))


# class WholeEquation(Scene):
#     def construct(self):
#         # expression = '3^(2+1)*(3+1)+2/(4+1)-6'
#         # latex = order_operations(expression).latex()
#         latex = latex_for_visual()
#         eq1_left = MathTex(latex)
#         self.add(eq1_left)


class VectorArrow(Scene):
    def construct(self):
        dot = Dot(ORIGIN)
        arrow = Arrow(ORIGIN, [2, 2, 0], buff=0, color=GOLD)
        numberplane = NumberPlane()
        origin_text = Text('(0, 0)').next_to(dot, DOWN)
        tip_text = Text('(2, 2)').next_to(arrow.get_end(), RIGHT)
        self.add(numberplane, dot, arrow, origin_text, tip_text)

        arrow2 = Arrow(ORIGIN, [5, 2, 0], buff=0)
        tip_text2 = Text('(5, 2)').next_to(arrow2.get_end(), RIGHT)
        self.play(Transform(arrow, arrow2), Transform(tip_text, tip_text2))


class ThreeDLightSourcePosition(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        plane = Surface(
            lambda x, y: np.array([x, y, x+y]), v_range=[-2, +2],
            u_range=[-2, +2]
        )
        plane1 = Surface(
            lambda x, y: np.array([-x, y, x + y]), v_range=[-2, +2],
            u_range=[-2, +2]
        )
        # self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        plane.set_style(fill_opacity=1,stroke_color=GREEN)
        plane1.set_style(fill_opacity=1,stroke_color=RED)
        self.set_camera_orientation(phi=120 * DEGREES, theta=30 * DEGREES)
        self.add(axes, plane, plane1)
        self.begin_ambient_camera_rotation(rate=1)
        self.wait(3)

