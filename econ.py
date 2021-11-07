from manim import *
from helper import clamp


class Main(Scene):
    def construct(self):
        x_range = [0, 8]
        y_range = [0, 8]
        axis_lines = NumberPlane(
            x_range=x_range,
            y_range=y_range,
            x_length=6.5,
            y_length=6.5,
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
                "stroke_color": BLUE_C,
                "stroke_width": 2,
                "stroke_opacity": 1
            }
        ).center().move_to(UP / 5)
        axis_box = SurroundingRectangle(
            mobject=axis_lines,
            buff=0,
            color=BLUE_D,
            stroke_width=2
        )
        y_axis_label = axis_lines.get_y_axis_label(label="Price", edge=UL, direction=LEFT)
        x_axis_label = axis_lines.get_x_axis_label(label="Quantity", edge=DR, direction=RIGHT)
        axis = VGroup(axis_box, axis_lines, x_axis_label, y_axis_label)
        self.play(Create(axis))
        self.wait()

        demand_elasticity = 1
        supply_elasticity = 1

        supply_shift = 0
        demand_shift = 1
        line_buffer = 0.5

        eq_not_cords = [
            ((y_range[1] - demand_elasticity * demand_shift - supply_elasticity * supply_shift) /
             (supply_elasticity + demand_elasticity)),
            (((y_range[1] - demand_elasticity * demand_shift - supply_elasticity * supply_shift) /
              (supply_elasticity + demand_elasticity) + supply_shift) * supply_elasticity),
            0
        ]
        eq_one_cords = [
            ((y_range[1] + demand_elasticity * demand_shift + supply_elasticity * supply_shift) /
             (supply_elasticity + demand_elasticity)),
            (((y_range[1] + demand_elasticity * demand_shift + supply_elasticity * supply_shift) /
              (supply_elasticity + demand_elasticity) - supply_shift) * supply_elasticity),
            0
        ]

        supply_labels = [f"S_{x}" if supply_shift != 0 else "S" for x in range(2)]
        demand_labels = [f"D_{x}" if demand_shift != 0 else "D" for x in range(2)]
        x_axis_labels = [f"Q_{x}" if eq_not_cords[0] - eq_one_cords[0] != 0 else "Q" for x in range(2)]
        y_axis_labels = [f"P_{x}" if eq_not_cords[1] - eq_one_cords[1] != 0 else "P" for x in range(2)]

        supply_not_x_range = [
            clamp(
                num=(y_range[0] + line_buffer) / supply_elasticity - supply_shift,
                max_value=x_range[1] - line_buffer,
                min_value=x_range[0] + line_buffer
            ),
            clamp(
                num=(y_range[1] - line_buffer) / supply_elasticity - supply_shift,
                max_value=x_range[1] - line_buffer,
                min_value=x_range[0] + line_buffer
            )
        ]
        demand_not_x_range = [
            clamp(
                num=(y_range[1] - line_buffer - y_range[1]) / (-demand_elasticity) - demand_shift,
                max_value=x_range[1] - line_buffer,
                min_value=x_range[0] + line_buffer
            ),
            clamp(
                num=(y_range[0] + line_buffer - y_range[1]) / (-demand_elasticity) - demand_shift,
                max_value=x_range[1] - line_buffer,
                min_value=x_range[0] + line_buffer
            )
        ]
        supply_not = axis_lines.get_graph(
            lambda x: supply_elasticity * (x + supply_shift),
            x_range=supply_not_x_range,
            color=RED_B
        )
        demand_not = axis_lines.get_graph(
            lambda x: -demand_elasticity * (x + demand_shift) + y_range[1],
            x_range=demand_not_x_range,
            color=GREEN_B
        )
        supply_not_label = axis_lines.get_graph_label(
            supply_not,
            supply_labels[0],
            buff=SMALL_BUFF,
            color=WHITE,
            x_val=supply_not_x_range[1]
        )
        demand_not_label = axis_lines.get_graph_label(
            demand_not,
            demand_labels[0],
            buff=SMALL_BUFF,
            color=WHITE,
            x_val=demand_not_x_range[1]
        )
        eq_not_point = axis_lines.coords_to_point(
            eq_not_cords[0],
            eq_not_cords[1],
            0
        )
        eq_not_dot = Dot(eq_not_point)
        x_dash_not = axis_lines.get_line_from_axis_to_point(point=eq_not_point, index=0, stroke_width=4)
        y_dash_not = axis_lines.get_line_from_axis_to_point(point=eq_not_point, index=1, stroke_width=4)
        x_dash_not_label = MathTex(x_axis_labels[0], font_size=40).move_to(axis_lines.coords_to_point(
            eq_not_cords[0],
            -line_buffer,
            0
        ))
        y_dash_not_label = MathTex(y_axis_labels[0], font_size=40).move_to(axis_lines.coords_to_point(
            -line_buffer,
            eq_not_cords[1],
            0
        ))
        not_graphs = VGroup(
            supply_not,
            supply_not_label,
            demand_not,
            demand_not_label,
            x_dash_not,
            x_dash_not_label,
            y_dash_not,
            y_dash_not_label,
            eq_not_dot
        )

        supply_one_x_range = [
            clamp(
                num=(y_range[0] + line_buffer) / supply_elasticity + supply_shift,
                max_value=x_range[1] - line_buffer,
                min_value=x_range[0] + line_buffer
            ),
            clamp(
                num=(y_range[1] - line_buffer) / supply_elasticity + supply_shift,
                max_value=x_range[1] - line_buffer,
                min_value=x_range[0] + line_buffer
            )
        ]
        demand_one_x_range = [
            clamp(
                num=(y_range[1] - line_buffer - y_range[1]) / (-demand_elasticity) + demand_shift,
                max_value=x_range[1] - line_buffer,
                min_value=x_range[0] + line_buffer
            ),
            clamp(
                num=(y_range[0] + line_buffer - y_range[1]) / (-demand_elasticity) + demand_shift,
                max_value=x_range[1] - line_buffer,
                min_value=x_range[0] + line_buffer
            )
        ]
        supply_one = axis_lines.get_graph(
            lambda x: supply_elasticity * (x - supply_shift),
            x_range=supply_one_x_range,
            color=RED_D
        )
        demand_one = axis_lines.get_graph(
            lambda x: -demand_elasticity * (x - demand_shift) + y_range[1],
            x_range=demand_one_x_range,
            color=GREEN_D
        )
        supply_one_label = axis_lines.get_graph_label(
            supply_one,
            supply_labels[1],
            buff=SMALL_BUFF,
            color=WHITE,
            x_val=demand_one_x_range[1]
        )
        demand_one_label = axis_lines.get_graph_label(
            demand_one,
            demand_labels[1],
            buff=SMALL_BUFF,
            color=WHITE,
            x_val=demand_one_x_range[1]
        )
        eq_one_point = axis_lines.coords_to_point(
            eq_one_cords[0],
            eq_one_cords[1],
            0
        )
        eq_one_dot = Dot(eq_one_point)
        x_dash_one = axis_lines.get_line_from_axis_to_point(point=eq_one_point, index=0, stroke_width=4)
        y_dash_one = axis_lines.get_line_from_axis_to_point(point=eq_one_point, index=1, stroke_width=4)
        x_dash_one_label = MathTex(x_axis_labels[1], font_size=40).move_to(axis_lines.coords_to_point(
            eq_one_cords[0],
            -line_buffer,
            0
        ))
        y_dash_one_label = MathTex(y_axis_labels[1], font_size=40).move_to(axis_lines.coords_to_point(
            -line_buffer,
            eq_one_cords[1],
            0
        ))
        not_one_arrow_price = Arrow(start=y_dash_not_label.get_center(), end=y_dash_one_label.get_center())
        not_one_arrow_quantity = Arrow(start=x_dash_not_label.get_center(), end=x_dash_one_label.get_center())
        one_graphs = VGroup(
            supply_one,
            supply_one_label,
            demand_one,
            demand_one_label,
            x_dash_one,
            x_dash_one_label,
            y_dash_one,
            y_dash_one_label,
            eq_one_dot,
        )

        self.play(Create(VGroup(supply_not, demand_not)))
        self.play(Write(VGroup(supply_not_label, demand_not_label)))
        self.play(Create(VGroup(x_dash_not, y_dash_not, eq_not_dot)))
        self.play(Write(VGroup(x_dash_not_label, y_dash_not_label)))
        self.wait()

        if eq_not_cords != eq_one_cords:
            self.play(
                TransformFromCopy(not_graphs, one_graphs, run_time=2),
                Create(VGroup(not_one_arrow_price, not_one_arrow_quantity), run_time=2)
            )
            self.wait()
        VGroup.add(one_graphs, not_one_arrow_quantity, not_one_arrow_price)
