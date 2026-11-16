import asyncio
import sys
sys.path.insert(0, ".")
from backend.templates.registry import TEMPLATES, classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.lean_runner import _verify_with_sympy

sample_problems = [
    {
        "id": "P17",
        "prob": "A rope passes over a small smooth pulley fixed at the top of a tower 12 m. high. A worker holds one end at the base and the other end fastens at a heavy car on the ground. If the worker can pull the rope at a rate 2 m/min., calculate the speed of the car during its motion towards the tower when the car is at a distance 9 m. from the base of the tower.",
        "cat": "rope_pulley_tower_rates",
    },
    {
        "id": "P18",
        "prob": "A man stands at a distance 50 m. from a helicopter at the airport. The helicopter flies vertically up at a rate 65 m./sec. Find the rate of change of the distance between the man and helicopter when the plane 120 m. high from the ground surface.",
        "cat": "man_helicopter_distance_rates",
    },
    {
        "id": "P19",
        "prob": "A balloon rises up vertically with constant velocity 15 m./sec., when the balloon at height 90 m. a car passes on the ground just below the balloon and remains moving in a straight line with constant speed 25 m./sec. Find the rate of increasing of distance between the car and the balloon after 2 seconds from the moment that the car was below the balloon.",
        "cat": "balloon_car_distance_rates",
    },
    {
        "id": "P20",
        "prob": "A balloon rises vertically from point A on the ground surface. An apparatus is placed to follow up the motion of the balloon at point B at the same horizontal plane of point A and distant 200 meters from it. At a moment the apparatus observed the elevation angle of the balloon to find it pi/4 and it increases at a rate of 0.12 rad /min. Find the rate of the balloon elevation at this moment.",
        "cat": "balloon_elevation_angle_rates",
    },
    {
        "id": "P21",
        "prob": "A helicopter flies vertically at a fixed rate of 42 m./min. If a ground observer is 150 m. of the taking off site and observes the helicopter, find the rate of change of the elevation angle of the observer eyesight when the helicopter is 150 m. high from the ground.",
        "cat": "helicopter_elevation_angle_rates",
    },
    {
        "id": "P22",
        "prob": "A steel wire in the form of a right circular cylinder is heated such that its length increases at the rate of 0.005 cm./min. and its cross sectional diameter increases at the rate of 0.002 cm./min. Find in terms of pi the rate of change of its volume with respect to the time t when its length is of 40 cm. and its diameter is of 2 cm. long.",
        "cat": "cylinder_volume_rate_by_length_diameter",
    },
    {
        "id": "P23",
        "prob": "Water is poured into an empty cylindrical container of radius 10 cm. and height 60 cm. at the rate of 30pi cm2/sec. Find the rate at which the height of the water rises in the container. When does the container become full?",
        "cat": "cylinder_water_level_rate",
    },
    {
        "id": "P08",
        "prob": "A metallic lamina in the form of an equilateral triangle is expanding such that it preserves its geometrical shape. If the rate of increase of its side length is 0.1 cm./sec., find its side length at the moment when the rate of increase of its area becomes sqrt(3) cm2/sec.",
        "cat": "equilateral_triangle_side_rate",
    },
    {
        "id": "P09",
        "prob": "The length of a rectangle is twice its width. It expands regularly such that it preserves its shape and the ratio between its dimensions. Find the area of the rectangle when its length increases at rate of 0.01 cm./sec. and its area increase at rate of 0.2 cm2/sec.",
        "cat": "rectangle_constant_ratio_rates",
    },
    {
        "id": "P11",
        "prob": "A is the area of the region bounded between two concentric circles with radii r_1 and r_2, where r_2 > r_1. If r_1 is increasing with the rate 0.4 cm./sec. and r_2 is decreasing to the rate 0.2 cm./sec., find the rate of change of A with respect to time t at the instant at which r_1 = 8 cm. and r_2 = 14 cm.",
        "cat": "concentric_circles_area_rate",
    },
    {
        "id": "P12",
        "prob": "If stone fell in still water then a circular wave is formed whose radius increases at a rate of 2.1 cm./sec. If the rate of increase of the surface area of the wave at the end of t seconds from the beginning equals 277.2 cm2/sec. Find the value of t. (pi = 22/7)",
        "cat": "circular_wave_time",
    },
    {
        "id": "P14",
        "prob": "A cube extends by heat so its edge length increases at a rate 0.02 cm./min., and its surface area increases at a rate of 0.72 cm2/min., at a moment. Find the cube edge length at this moment and the rate of the increase in its volume at this time.",
        "cat": "cube_heating_edge_volume_rate",
    },
    {
        "id": "P15",
        "prob": "A cube extends by heat so its edge length increases at rate 0.01 cm./min., the rate of change of its volume at a moment is 75 cm3/min. find: (1) The edge length of the cube at this moment. (2) The rate of change of its surface area at this moment.",
        "cat": "cube_volume_rate_given",
    },
    {
        "id": "P31",
        "prob": "The length of rectangle 12 cm. and its width 5 cm. the length decreases at a rate 1 cm./sec. while the width increases at a rate 1/2 cm./sec., find when does the shape become a square. Hence find the time the area stop increasing and find the area at this moment.",
        "cat": "rectangle_changing_dimensions_rates",
    },
    {
        "id": "P32",
        "prob": "The width of a rectangle is increasing at a rate 1 cm./sec. while its length is decreasing so that the area of the rectangle remains constant and equals 24 cm2. Find: (1) The rate of change of the perimeter of the rectangle at the moment when the width equals 4 cm. (2) The two dimensions of the rectangle at the moment when the perimeter stops changing.",
        "cat": "rectangle_constant_area_perimeter_rate",
    },
    {
        "id": "P33",
        "prob": "A rectangle of length L and width W has a constant area of 1200 cm2 at a particular instant the length is increasing at 6 cm./min. and the width is decreasing at 2 cm./min. Find the dimensions of the rectangle at this instant. Is the length of the diagonal of the rectangle increasing or decreasing? At what rate?",
        "cat": "rectangle_diagonal_rate",
    },
    {
        "id": "P37",
        "prob": "An isosceles triangle, the length of each of the two equal sides is 10 cm., and the measure of their included angle equals (X) if X change at a rate of 3 degree per minute, find the rate of change of its surface area when X = 60 degree",
        "cat": "isosceles_triangle_angle_changing",
    },
    {
        "id": "P42",
        "prob": "A boy holds a thread of a kite at 30 high, the wind pulls the kite horizontally at a rate 25 m./min. find the speed the boy should leave the thread when the thread length = 50 m.",
        "cat": "kite_thread_release_rate",
    },
    {
        "id": "P43",
        "prob": "A metal cuboid expands, its length 2 cm. more than its width and its height is 3 times its width by heating such that it preserves the ratio among its dimensions. The volume increases at a rate 0.6 cm3/min. while its width increases at a rate 0.01 cm./min.. Find the dimensions of the cuboid.",
        "cat": "cuboid_proportional_dimensions",
    },
    {
        "id": "P49",
        "prob": "A point moves on the curve: y = 4x - 2x3, its y-coordinate is decreasing at a rate of 5 units/sec. Find the rate of change of the slope of the curve at x = 2",
        "cat": "point_on_curve_slope_rate",
    },
    {
        "id": "P50",
        "prob": "A point starts to move from origin in the positive direction of X-axis with velocity 5 cm./sec. find the rate of change of the distance between this point and the point (9, 8) after 3 seconds from the beginning of motion.",
        "cat": "point_moving_x_axis_distance_rate",
    },
    {
        "id": "P53",
        "prob": "A regular hexagonal - like lamina shrinks by cold. if the rate of change of its side length is 0.1 cm./sec. find the rate of change in the area of the lamina when its side length is 10 cm.",
        "cat": "regular_hexagon_area_rate",
    },
    {
        "id": "P55",
        "prob": "A head lamp is placed at a height of 680 cm. from the surface of the earth. A man of a height 170 cm. walks with velocity 2 m./sec. in a straight line towards the base of the lamp. Find: (1) The rate of change of length of the man shadow. (2) The velocity of the man end of shadow",
        "cat": "shadow_length_rate",
    },
    {
        "id": "P56",
        "prob": "A man of a height 180 cm. is walking with a velocity of magnitude 150 cm./sec. towards a lamp of height 480 cm. over the ground. Find: (1) The rate of change of the length of the shadow of the man. (2) The rate of change of the distance between the head of the man and the lamp at the instant at which the man is 300 cm. apart from the base of the lamp.",
        "cat": "shadow_length_rate_variant",
    },
    {
        "id": "P69",
        "prob": "A train starts its journey at 11 o clock towards east with velocity 45 km./h., while another train began its journey at 12 o clock from the same point towards south with velocity 60 km./h. find the rate of increasing of distance between the two trains at 3 o clock afternoon.",
        "cat": "two_trains_different_start_times",
    },
    {
        "id": "P66",
        "prob": "A known mass of gas with a constant temperature whose volume decreases at a constant rate of 2 cm3/sec. If the pressure is inversely proportional to the volume and the pressure equals 1000 gm.wt/cm2 when the volume is 250 cm3, find the rate of change of the pressure with respect to time when the volume of gas is 100 cm3.",
        "cat": "gas_law_pressure_volume_rate",
    },
    {
        "id": "P67",
        "prob": "In a closed electric circuit, if v is the potential difference (volt), I is the current intensity (Ampere), R is the resistance (ohm). If the potential difference increases at a rate of 1 volt/sec. and the current intensity decreases at a rate of 1/2 Ampere/sec., find the rate of the resistance at the moment which v = 12 volt and I = 2 Amperes.",
        "cat": "ohms_law_resistance_rate",
    },
    {
        "id": "P63",
        "prob": "If the gas leaks from a spherical balloon at a rate of 20 cm3/s., find the rate of change of the balloon radius length at the moment in which the radius length is 10 cm. and find the rate of change of the balloon external surface area at the same moment.",
        "cat": "spherical_balloon_gas_leak_rate",
    },
    {
        "id": "P_extrema",
        "prob": "Find the extrema values of f(X) = X^2 - 6X + 13 on [-1, 5].",
        "cat": "absolute_extrema_closed_interval",
    },
    {
        "id": "P_crit2",
        "prob": "If the two points (-3, 3), (-1, -1) are two critical points of the function y = a x^3 + b x^2 + c x + d. Find a, b, c and d and determine the type of each of the critical points.",
        "cat": "cubic_two_critical_points",
    },
    {
        "id": "P_crit_origin",
        "prob": "Find the values of a, b, c, d if the curve whose equation y = a x^3 + b x^2 + c x + d passes through the origin and it has a critical point at x = 3 and local maximum value = f(2) and the tangent at x = 1 has equation 12 x - 3 y + 11 = 0",
        "cat": "cubic_origin_critical_tangent",
    },
]

print(f"Total problems to test: {len(sample_problems)}")
for item in sample_problems:
    prob = item["prob"]
    exp_cat = item["cat"]
    got_cat = classify_problem(prob)
    cat_match = (got_cat == exp_cat)
    
    solver_res = solve(prob)
    cand_ans = solver_res.candidate_answer
    
    lean_stmt = None
    verify_ok = False
    if got_cat:
        try:
            form_res = formalize(prob, solver_res, got_cat)
            lean_stmt = form_res.lean_statement
            verify_ok = _verify_with_sympy(lean_stmt)
        except Exception as e:
            lean_stmt = f"ERROR: {e}"
            
    print(f"{item['id']} [{exp_cat}]:")
    print(f"   classify: {'OK' if cat_match else f'FAIL (got {got_cat})'}")
    safe_cand = str(cand_ans).encode('ascii', 'backslashreplace').decode('ascii')
    print(f"   cand_ans: {safe_cand}")
    safe_lean = lean_stmt[:80].encode('ascii', 'backslashreplace').decode('ascii') if lean_stmt else 'None'
    print(f"   lean: {safe_lean}")
    print(f"   verify: {'PASS' if verify_ok else 'FAIL'}")
