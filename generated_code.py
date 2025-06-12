from manim import *

class CoordinateVisualizationScene(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
            axis_config={"include_numbers": True}
        )
        axes.add_coordinate_labels()

        point_xaxis = Dot(axes.c2p(8, 0), color=RED)
        label_point_xaxis = Text("Point on x-axis: (8, 0)", color=RED)
        label_point_xaxis.next_to(point_xaxis, UP)

        point_yaxis = Dot(axes.c2p(0, -8), color=BLUE)
        label_point_yaxis = Text("Point on y-axis: (0, -8)", color=BLUE)
        label_point_yaxis.next_to(point_yaxis, RIGHT)

        reasoning_steps = VGroup(
            Text("[Definition] A point on the x-axis has a y-coordinate of 0."),
            Text("[Assumption] Distance from y-axis is |x|. Given distance=8, |x|=8."),
            Text("[Step] Assuming right of y-axis, x=8."),
            Text("[Conclusion] Coordinates: (8, 0)"),
            Text(""),
            Text("[Definition] A point on the y-axis has an x-coordinate of 0."),
            Text("[Assumption] Distance from x-axis is |y|. Given distance=-8, y=-8."),
            Text("[Step] Point is 8 units below x-axis."),
            Text("[Conclusion] Coordinates: (0, -8)")
        )
        reasoning_steps.arrange(DOWN, buff=0.3)
        reasoning_steps.to_edge(LEFT).shift(UP*0.5)

        self.add(axes, point_xaxis, point_yaxis, label_point_xaxis, label_point_yaxis, reasoning_steps)

if __name__ == '__main__':
    scene = CoordinateVisualizationScene()
    scene.construct()