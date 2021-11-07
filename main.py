from manim import *
from manim.mobject.geometry import ArrowTriangleTip


class MainOne(Scene):
    def construct(self):
        x_range = [0, 3]
        y_range = [0, np.exp(x_range[1])]
        graph = NumberPlane(
            x_range=x_range,
            x_length=10,
            y_range=y_range,
            y_length=5,
            axis_config={
                'font_size': 12
            },
            background_line_style={
                'stroke_width': 0
            }
        ).center()
        x_label = graph.get_x_axis_label('X')
        y_label = graph.get_y_axis_label('Y')
        graph_labels = VGroup(x_label, y_label)
        self.play(Create(graph), Write(graph_labels))
        self.wait()

        g1 = graph.get_graph(
            function=lambda t:
            np.exp(t),
            # np.abs(np.sin(np.power(t, t)) / np.power(2, (np.power(t, t) - (pi / 2)) / pi)),
            color=RED
        )

        dx_halving = 5
        riemann = [
            graph.get_riemann_rectangles(
                graph=graph.get_graph(lambda t: 0),
                dx=1,
                x_range=[x_range[0], x_range[1]]
            )
        ]
        for i1 in range(dx_halving):
            riemann.append(graph.get_riemann_rectangles(
                graph=g1,
                dx=np.power(0.5, i1),
                # input_sample_type='right',
                x_range=[x_range[0], x_range[1]],
                stroke_width=0)
            )

        self.play(Create(g1))
        self.wait()
        for i2 in range(dx_halving):
            self.play(ReplacementTransform(riemann[i2], riemann[i2 + 1]))
        self.wait()


class MainPlain(Scene):
    def construct(self):
        x_range = [-5, 5]
        y_range = [-5, 5]
        axis_lines = NumberPlane(
            x_range=x_range,
            y_range=y_range,
            x_length=7,
            y_length=7,
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 4,
                "include_ticks": False,
                "include_tip": False,
                "line_to_number_buff": SMALL_BUFF,
                "label_direction": DR,
                "font_size": 24
            },
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 1
            }
        ).center()
        axis_box = SurroundingRectangle(
            mobject=axis_lines,
            buff=0,
            color=BLUE,
            stroke_width=2
        )
        x_axis_label = axis_lines.get_x_axis_label(label='x')
        y_axis_label = axis_lines.get_y_axis_label(label='y')
        axis = VGroup(axis_box, axis_lines, x_axis_label, y_axis_label)
        self.play(Create(axis))
        self.wait()


class Main(Scene):
    def construct(self):
        series_big = MathTex(r"\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n}")
        series_big_box = SurroundingRectangle(series_big)
        series_small = MathTex(
            r"\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n}"
        ).scale(0.75).move_to([-3.25, 2, 0], aligned_edge=RIGHT)
        self.play(Write(series_big))
        self.wait()
        self.play(Create(series_big_box))
        self.wait()
        self.play(FadeOut(series_big_box))
        self.play(TransformMatchingTex(series_big, series_small))
        self.wait()

        times_to_iterate = 15
        line_range = [[-2, 4, 6], [3, -3, 6]]

        series_array = np.array([
            0 if x == 0 else -1 / x if x % 2 == 0 else 1 / x for x in range(times_to_iterate + 2)
        ])
        partial_sum_array = np.cumsum(series_array)
        points_array = np.array([
            [
                [
                    line_range[0][0] + partial_sum_array[x] * line_range[0][2],
                    line_range[1][0] - x * line_range[1][2] / times_to_iterate,
                    0
                ],
                [
                    line_range[0][0] + partial_sum_array[x + 1] * line_range[0][2],
                    line_range[1][0] - x * line_range[1][2] / times_to_iterate,
                    0
                ]
            ]
            if x % 2 == 0 else
            [
                [
                    line_range[0][0] + partial_sum_array[x] * line_range[0][2],
                    line_range[1][0] - x * line_range[1][2] / times_to_iterate,
                    0
                ],
                [
                    line_range[0][0] + partial_sum_array[x + 1] * line_range[0][2],
                    line_range[1][0] - x * line_range[1][2] / times_to_iterate,
                    0
                ]
            ]
            for x in range(times_to_iterate + 1)
        ])

        all_segments = VGroup()
        for i in range(times_to_iterate):
            segment_dot_one = Dot(points_array[i][0], radius=0.06)
            segment_dot_two = Dot(points_array[i][1], radius=0.06)
            segment_line = Line(points_array[i][0], points_array[i][1], color=BLUE)
            segment_label = MathTex(
                r"S_{" + str(i + 1) + r"}",
                font_size=line_range[1][2] * 100 / times_to_iterate
            ).move_to(
                [line_range[0][0] - 0.5, points_array[i][0][1], 0]
            )
            segment = VGroup(segment_line, segment_dot_two, segment_dot_one)
            VGroup.add(all_segments, segment_line, segment_dot_two, segment_dot_one, segment_label)
            self.play(Write(segment_label), Create(segment), run_time=1 / (i + 1))
            self.wait(1 / (i + 1))
        self.wait()
        ln_two_line = DashedLine([
            line_range[0][0] + np.log(2) * line_range[0][2], 10, 0],
            [line_range[0][0] + np.log(2) * line_range[0][2], -10, 0],
            color=RED_B
        )
        self.play(FadeIn(ln_two_line))
        self.wait()

        series_small_answer = MathTex(
            r"\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n} = ln(2)"
        ).scale(0.75).move_to(series_small, aligned_edge=RIGHT)
        self.play(ReplacementTransform(series_small, series_small_answer))
        self.wait()
        self.play(FadeOut(all_segments, ln_two_line))
        self.wait()

        series_small_center = MathTex(
            r"\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n} = ln(2)"
        ).scale(0.75).move_to([0, 2.5, 0])
        number_line = NumberLine(x_range=[0, 1], length=8).center()
        self.play(Create(number_line), TransformMatchingTex(series_small_answer, series_small_center))
        self.wait()
        all_arrows = VGroup()
        for i in range(times_to_iterate + 1):
            arrow_start_dot = Dot(number_line.number_to_point(partial_sum_array[i]), radius=0.075)
            arrow_to_next = CurvedArrow(
                start_point=number_line.number_to_point(partial_sum_array[i]),
                end_point=number_line.number_to_point(partial_sum_array[i + 1]),
                tip_shape=ArrowTriangleTip,
                tip_length=0.25
            )
            VGroup.add(all_arrows, arrow_to_next, arrow_start_dot)
            arrow = VGroup(arrow_start_dot, arrow_to_next)
            self.play(Create(arrow), run_time=1 / (i + 1))
            self.wait(1 / (i + 1))
        self.wait()
        ln_two_dot = Dot(number_line.number_to_point(np.log(2)), color=RED_B, radius=0.1)
        # ln_two_dot_label =
        self.play(FadeIn(ln_two_dot))
        self.wait()
        self.play(FadeOut(all_arrows))
        self.wait()

