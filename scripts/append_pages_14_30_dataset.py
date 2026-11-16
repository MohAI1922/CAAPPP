"""
VeriMath — Pages 14–30 Fine-Tuning Dataset Generator & Appender
==============================================================
Generates ~180-200 instruction-tuning pairs covering all problem families
from Pages 14–30 of the calculus textbook (Exercise 4, Exercise 9, Exercise 10).
Appends them cleanly to verimath_finetune_dataset.jsonl.
"""

import json
import os
import random

SYSTEM_PROMPT = (
    "You are VeriMath Precision Autoformalization Extractor. Your task is to analyze "
    "mathematical word problems, classify them into the correct template, extract all "
    "parameter values into a structured JSON object, and verify whether all necessary "
    "information is present to solve the problem. If any required variable is missing, "
    "set is_complete to false and identify the missing field. Output valid JSON only."
)

def make_entry(user_text: str, template: str, params: dict, target: str, is_complete: bool = True, missing: list = None):
    assistant_data = {
        "template": template,
        "is_complete": is_complete,
        "parameters": params,
        "target": target,
        "missing_parameters": missing or []
    }
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text.strip()},
            {"role": "assistant", "content": json.dumps(assistant_data, indent=2)}
        ]
    }

def generate_dataset_entries():
    entries = []

    # 1. rope_pulley_tower_rates (Exercise 4, #17)
    pulley_data = [
        (12, 9, 2, "m", "m/min"),
        (15, 8, 3, "m", "m/min"),
        (20, 15, 4, "m", "m/min"),
        (24, 7, 5, "m", "m/min"),
        (10, 6, 2.5, "m", "m/min"),
    ]
    for H, d, vr, u_len, u_time in pulley_data:
        q = (
            f"A rope passes over a small smooth pulley fixed at the top of a tower {H} {u_len} high. "
            f"A worker holds one end at the base and the other end is fastened to a heavy car on the ground. "
            f"If the worker pulls the rope at a rate of {vr} {u_time}, calculate the speed of the car "
            f"during its motion towards the tower when the car is at a distance of {d} {u_len} from the base of the tower."
        )
        entries.append(make_entry(q, "rope_pulley_tower_rates", {"H": str(H), "d": str(d), "v_rope": str(vr)}, "v_car"))
    # Incomplete variant
    entries.append(make_entry(
        "A rope passes over a pulley on a 15 m tower. A worker pulls the rope towards the tower. Calculate the car speed.",
        "rope_pulley_tower_rates", {"H": "15", "d": None, "v_rope": None}, "v_car", False, ["d", "v_rope"]
    ))

    # 2. man_helicopter_distance_rates (Exercise 4, #18)
    heli_dist_data = [
        (50, 65, 120, "m", "m/sec"),
        (40, 50, 96, "m", "m/sec"),
        (30, 45, 72, "m", "m/sec"),
        (60, 80, 144, "m", "m/sec"),
        (75, 70, 100, "m", "m/sec"),
    ]
    for d0, vh, h, u_len, u_time in heli_dist_data:
        q = (
            f"A man stands at a distance of {d0} {u_len} from a helicopter at the airport. "
            f"The helicopter flies vertically up at a rate of {vh} {u_time}. "
            f"Find the rate of change of the distance between the man and the helicopter when the aircraft is {h} {u_len} high from the ground surface."
        )
        entries.append(make_entry(q, "man_helicopter_distance_rates", {"d0": str(d0), "v_heli": str(vh), "h": str(h)}, "rate"))
    entries.append(make_entry(
        "A man stands 50 m from a helicopter that flies up at 65 m/s. Find the rate of change of distance.",
        "man_helicopter_distance_rates", {"d0": "50", "v_heli": "65", "h": None}, "rate", False, ["h"]
    ))

    # 3. balloon_car_distance_rates (Exercise 4, #19)
    balloon_car_data = [
        (15, 25, 90, 2),
        (20, 30, 80, 3),
        (10, 20, 100, 4),
        (12, 16, 50, 5),
        (18, 24, 60, 2),
    ]
    for vb, vc, h0, t in balloon_car_data:
        q = (
            f"A balloon rises up vertically with constant velocity {vb} m/sec. When the balloon is at height {h0} m, "
            f"a car passes on the ground just below the balloon and continues moving in a straight line with constant speed {vc} m/sec. "
            f"Find the rate of increase of distance between the car and the balloon after {t} seconds from the moment the car was below the balloon."
        )
        entries.append(make_entry(q, "balloon_car_distance_rates", {"v_balloon": str(vb), "v_car": str(vc), "h0": str(h0), "t": str(t)}, "rate"))
    entries.append(make_entry(
        "A balloon rises at 15 m/s. A car passes below moving at 25 m/s. Find how fast the distance increases.",
        "balloon_car_distance_rates", {"v_balloon": "15", "v_car": "25", "t": None}, "rate", False, ["t"]
    ))

    # 4. balloon_elevation_angle_rates (Exercise 4, #20)
    balloon_angle_data = [
        (200, "pi/4", "0.12"),
        (150, "pi/4", "0.10"),
        (300, "pi/4", "0.08"),
        (100, "pi/4", "0.15"),
        (250, "pi/4", "0.05"),
    ]
    for L, theta, dtheta in balloon_angle_data:
        q = (
            f"A balloon rises vertically from point A on the ground surface. An apparatus is placed to follow the motion of the balloon "
            f"at point B on the same horizontal plane as point A, at a distance of {L} meters from it. At a certain moment, the apparatus observes "
            f"the elevation angle of the balloon to be {theta} and increasing at a rate of {dtheta} rad/min. Find the rate of the balloon elevation at this moment."
        )
        entries.append(make_entry(q, "balloon_elevation_angle_rates", {"L": str(L), "theta": theta, "v_theta": dtheta}, "v_balloon"))

    # 5. helicopter_elevation_angle_rates (Exercise 4, #21)
    heli_angle_data = [
        (150, 42, 150),
        (200, 50, 200),
        (120, 36, 120),
        (100, 30, 100),
        (180, 48, 180),
    ]
    for d, vh, h in heli_angle_data:
        q = (
            f"A helicopter flies vertically at a fixed rate of {vh} m/min. If a ground observer is {d} m from the takeoff site "
            f"and observes the helicopter, find the rate of change of the elevation angle of the observer's line of sight when the helicopter is {h} m high from the ground."
        )
        entries.append(make_entry(q, "helicopter_elevation_angle_rates", {"d": str(d), "v_heli": str(vh), "h": str(h)}, "rate"))

    # 6. cylinder_volume_rate_by_length_diameter (Exercise 4, #22)
    cyl_wire_data = [
        (40, 2, "0.005", "0.002"),
        (50, 4, "0.010", "0.004"),
        (30, 1, "0.004", "0.001"),
        (60, 3, "0.008", "0.003"),
        (45, 2, "0.006", "0.002"),
    ]
    for L, D, dL, dD in cyl_wire_data:
        q = (
            f"A steel wire in the form of a right circular cylinder is heated such that its length increases at the rate of {dL} cm/min "
            f"and its cross-sectional diameter increases at the rate of {dD} cm/min. Find in terms of pi the rate of change of its volume "
            f"with respect to time when its length is {L} cm and its diameter is {D} cm long."
        )
        entries.append(make_entry(q, "cylinder_volume_rate_by_length_diameter", {"L": str(L), "D": str(D), "dL": dL, "dD": dD}, "dV"))

    # 7. cylinder_water_level_rate (Exercise 4, #23)
    cyl_water_data = [
        (10, 60, "30*pi"),
        (20, 80, "40*pi"),
        (15, 50, "45*pi"),
        (12, 72, "36*pi"),
        (8, 40, "16*pi"),
    ]
    for r, h_max, dV in cyl_water_data:
        q = (
            f"Water is poured into an empty cylindrical container of radius {r} cm and height {h_max} cm at the rate of {dV} cm3/sec. "
            f"Find the rate at which the height of the water rises in the container, and determine when the container becomes full."
        )
        entries.append(make_entry(q, "cylinder_water_level_rate", {"r": str(r), "h_max": str(h_max), "dV_dt": dV}, "dh_dt"))

    # 8. equilateral_triangle_side_rate (Exercise 4, #8)
    eq_tri_data = [
        ("0.1", "sqrt(3)"),
        ("0.2", "2*sqrt(3)"),
        ("0.05", "sqrt(3)/2"),
        ("0.25", "5*sqrt(3)/2"),
        ("0.15", "3*sqrt(3)/2"),
    ]
    for da, dA in eq_tri_data:
        q = (
            f"A metallic lamina in the form of an equilateral triangle is expanding such that it preserves its geometrical shape. "
            f"If the rate of increase of its side length is {da} cm/sec, find its side length at the moment when the rate of increase of its area becomes {dA} cm2/sec."
        )
        entries.append(make_entry(q, "equilateral_triangle_side_rate", {"da_dt": da, "dA_dt": dA}, "a"))

    # 9. rectangle_constant_ratio_rates (Exercise 4, #9)
    rect_ratio_data = [
        ("0.01", "0.2", 2),
        ("0.02", "0.4", 2),
        ("0.05", "1.0", 2),
        ("0.03", "0.6", 2),
        ("0.04", "0.8", 2),
    ]
    for dL, dA, ratio in rect_ratio_data:
        q = (
            f"The length of a rectangle is {ratio} times its width. It expands regularly such that it preserves its shape and the ratio between its dimensions. "
            f"Find the area of the rectangle when its length increases at a rate of {dL} cm/sec and its area increases at a rate of {dA} cm2/sec."
        )
        entries.append(make_entry(q, "rectangle_constant_ratio_rates", {"dL_dt": dL, "dA_dt": dA}, "A"))

    # 10. concentric_circles_area_rate (Exercise 4, #11)
    annular_data = [
        (8, 14, "0.4", "-0.2"),
        (6, 12, "0.5", "-0.3"),
        (10, 16, "0.2", "-0.1"),
        (5, 15, "0.6", "-0.4"),
        (7, 21, "0.3", "-0.2"),
    ]
    for r1, r2, dr1, dr2 in annular_data:
        q = (
            f"A is the area of the region bounded between two concentric circles with radii r1 and r2, where r2 > r1. "
            f"If r1 is increasing with the rate {dr1} cm/sec and r2 is decreasing at the rate {dr2.replace('-', '')} cm/sec, "
            f"find the rate of change of A with respect to time t at the instant at which r1 = {r1} cm and r2 = {r2} cm."
        )
        entries.append(make_entry(q, "concentric_circles_area_rate", {"r1": str(r1), "r2": str(r2), "dr1_dt": dr1, "dr2_dt": dr2}, "dA_dt"))

    # 11. circular_wave_time (Exercise 4, #12)
    wave_data = [
        ("2.1", "277.2"),
        ("1.4", "123.2"),
        ("3.5", "770.0"),
        ("0.7", "30.8"),
        ("2.8", "492.8"),
    ]
    for k, dA in wave_data:
        q = (
            f"If a stone falls into still water, a circular wave is formed whose radius increases at a rate of {k} cm/sec. "
            f"If the rate of increase of the surface area of the wave at the end of t seconds equals {dA} cm2/sec, find the value of t. (Use pi = 22/7)."
        )
        entries.append(make_entry(q, "circular_wave_time", {"k": k, "dA_target": dA, "pi_approx": "22/7"}, "t"))

    # 12. cube_heating_edge_volume_rate (Exercise 4, #14)
    cube_heat_data = [
        ("0.02", "0.72"),
        ("0.01", "0.36"),
        ("0.03", "1.08"),
        ("0.05", "1.80"),
        ("0.04", "1.44"),
    ]
    for da, dSA in cube_heat_data:
        q = (
            f"A cube expands by heat so its edge length increases at a rate of {da} cm/min, and its total surface area increases at a rate of {dSA} cm2/min at a certain moment. "
            f"Find the cube's edge length at this moment and the rate of increase in its volume at this time."
        )
        entries.append(make_entry(q, "cube_heating_edge_volume_rate", {"da_dt": da, "dSA_dt": dSA}, "dV_dt"))

    # 13. cube_volume_rate_given (Exercise 4, #15)
    cube_vol_data = [
        ("0.01", "75"),
        ("0.02", "150"),
        ("0.03", "225"),
        ("0.005", "37.5"),
        ("0.015", "112.5"),
    ]
    for da, dV in cube_vol_data:
        q = (
            f"A cube expands by heat so its edge length increases at a rate of {da} cm/min. The rate of change of its volume at a moment is {dV} cm3/min. "
            f"Find: (1) The edge length of the cube at this moment. (2) The rate of change of its surface area at this moment."
        )
        entries.append(make_entry(q, "cube_volume_rate_given", {"da_dt": da, "dV_dt": dV}, "dSA_dt"))

    # 14. rectangle_changing_dimensions_rates (Exercise 4, #31)
    rect_dim_data = [
        (12, 5, "-1", "1/2"),
        (16, 6, "-2", "1/2"),
        (14, 4, "-1", "1/3"),
        (20, 8, "-2", "1"),
        (10, 4, "-1", "1/2"),
    ]
    for L0, W0, dL, dW in rect_dim_data:
        q = (
            f"The length of a rectangle is {L0} cm and its width is {W0} cm. The length decreases at a rate of {dL.replace('-', '')} cm/sec while the width increases at a rate of {dW} cm/sec. "
            f"Find when the shape becomes a square, and find the time the area stops increasing as well as the area at that moment."
        )
        entries.append(make_entry(q, "rectangle_changing_dimensions_rates", {"L0": str(L0), "W0": str(W0), "dL_dt": dL, "dW_dt": dW}, "t_sq"))

    # 15. rectangle_constant_area_perimeter_rate (Exercise 4, #32)
    rect_const_a_data = [
        (24, 4, "1"),
        (36, 6, "2"),
        (48, 6, "1"),
        (50, 5, "2"),
        (72, 8, "1"),
    ]
    for A, W, dW in rect_const_a_data:
        q = (
            f"The width of a rectangle is increasing at a rate of {dW} cm/sec while its length decreases so that the area of the rectangle remains constant and equals {A} cm2. "
            f"Find: (1) The rate of change of the perimeter of the rectangle when the width equals {W} cm. (2) The two dimensions of the rectangle at the moment when the perimeter stops changing."
        )
        entries.append(make_entry(q, "rectangle_constant_area_perimeter_rate", {"A": str(A), "W": str(W), "dW_dt": dW}, "dP_dt"))

    # 16. rectangle_diagonal_rate (Exercise 4, #33)
    rect_diag_data = [
        (1200, "6", "-2"),
        (800, "4", "-1"),
        (1500, "5", "-3"),
        (600, "3", "-1"),
        (2000, "10", "-4"),
    ]
    for A, dL, dW in rect_diag_data:
        q = (
            f"A rectangle of length L and width W has a constant area of {A} cm2. At a particular instant the length is increasing at {dL} cm/min and the width is decreasing at {dW.replace('-', '')} cm/min. "
            f"Find the dimensions of the rectangle at this instant. Determine whether the length of the diagonal is increasing or decreasing and calculate its rate."
        )
        entries.append(make_entry(q, "rectangle_diagonal_rate", {"A": str(A), "dL_dt": dL, "dW_dt": dW}, "dd_dt"))

    # 17. isosceles_triangle_angle_changing (Exercise 4, #37)
    iso_angle_data = [
        (10, 3, 60),
        (12, 2, 60),
        (8, 4, 60),
        (15, 1, 60),
        (20, 3, 60),
    ]
    for a, dX_deg, X_deg in iso_angle_data:
        q = (
            f"In an isosceles triangle, the length of each of the two equal sides is {a} cm, and the measure of their included angle equals X. "
            f"If X changes at a rate of {dX_deg} degrees per minute, find the rate of change of its surface area when X = {X_deg} degrees."
        )
        entries.append(make_entry(q, "isosceles_triangle_angle_changing", {"a": str(a), "X": f"{X_deg}*pi/180", "dX_deg": str(dX_deg)}, "dA_dt"))

    # 18. triangle_two_sides_angle_changing (Exercise 4, #39)
    tri_2sides_data = [
        (10, "0.1", "1/5", "pi/3"),
        (12, "0.2", "1/4", "pi/3"),
        (8, "0.15", "1/6", "pi/3"),
        (15, "0.1", "1/10", "pi/3"),
        (6, "0.25", "1/5", "pi/3"),
    ]
    for a, da, dth, th in tri_2sides_data:
        q = (
            f"A triangle has two sides that both increase at a rate of {da} cm/sec while their included angle increases at a rate of {dth} rad/sec. "
            f"If the length of each side is {a} cm and the angle is {th}, find the rate of change of the area of the triangle."
        )
        entries.append(make_entry(q, "triangle_two_sides_angle_changing", {"a": str(a), "b": str(a), "da_dt": da, "theta": th, "dtheta_dt": dth}, "dA_dt"))

    # 19. kite_thread_release_rate (Exercise 4, #42)
    kite_data = [
        (30, 50, 25),
        (40, 50, 30),
        (60, 100, 40),
        (45, 75, 20),
        (80, 100, 50),
    ]
    for h, L, v in kite_data:
        q = (
            f"A boy holds the thread of a kite at {h} m high. The wind pulls the kite horizontally at a rate of {v} m/min. "
            f"Find the speed at which the boy should let out the thread when the thread length is {L} m."
        )
        entries.append(make_entry(q, "kite_thread_release_rate", {"h": str(h), "L": str(L), "v_horiz": str(v)}, "dl_dt"))

    # 20. cuboid_proportional_dimensions (Exercise 4, #43)
    cuboid_data = [
        (2, 3, "0.6", "0.01"),
        (3, 2, "0.8", "0.02"),
        (1, 4, "0.5", "0.01"),
        (4, 3, "1.2", "0.02"),
        (2, 2, "0.4", "0.01"),
    ]
    for c, k, dV, dW in cuboid_data:
        q = (
            f"A metal cuboid expands by heating such that its length is {c} cm more than its width and its height is {k} times its width, "
            f"preserving the proportions among its dimensions. The volume increases at a rate of {dV} cm3/min while its width increases at a rate of {dW} cm/min. "
            f"Find the dimensions of the cuboid."
        )
        entries.append(make_entry(q, "cuboid_proportional_dimensions", {"dV_dt": dV, "dW_dt": dW}, "W"))

    # 21. point_on_curve_slope_rate (Exercise 4, #49)
    curve_slope_data = [
        ("4*x - 2*x^3", 2, "-5"),
        ("3*x - x^3", 1, "-4"),
        ("6*x - 2*x^3", 2, "-8"),
        ("5*x - x^3", 2, "-3"),
        ("4*x - x^3", 3, "-6"),
    ]
    for curve, x_val, dy_dt in curve_slope_data:
        q = (
            f"A point moves on the curve y = {curve}. Its y-coordinate decreases at a rate of {dy_dt.replace('-', '')} units/sec. "
            f"Find the rate of change of the slope of the curve at x = {x_val}."
        )
        entries.append(make_entry(q, "point_on_curve_slope_rate", {"x": str(x_val), "dy_dt": dy_dt}, "dm_dt"))

    # 22. point_moving_x_axis_distance_rate (Exercise 4, #50)
    point_move_data = [
        (5, 3, 9, 8),
        (4, 2, 6, 8),
        (6, 4, 12, 5),
        (3, 5, 8, 6),
        (5, 4, 10, 10),
    ]
    for vx, t, px, py in point_move_data:
        q = (
            f"A point starts moving from the origin in the positive direction of the X-axis with velocity {vx} cm/sec. "
            f"Find the rate of change of the distance between this moving point and the fixed point ({px}, {py}) after {t} seconds from the start of motion."
        )
        entries.append(make_entry(q, "point_moving_x_axis_distance_rate", {"vx": str(vx), "t": str(t), "px": str(px), "py": str(py)}, "dD_dt"))

    # 23. regular_hexagon_area_rate (Exercise 4, #53)
    hexagon_data = [
        (10, "-0.1"),
        (12, "-0.2"),
        (8, "-0.05"),
        (15, "-0.15"),
        (6, "-0.1"),
    ]
    for a, da in hexagon_data:
        q = (
            f"A regular hexagonal lamina shrinks by cooling. If the rate of change of its side length is {da.replace('-', '')} cm/sec, "
            f"find the rate of change in the area of the lamina when its side length is {a} cm."
        )
        entries.append(make_entry(q, "regular_hexagon_area_rate", {"a": str(a), "da_dt": da}, "dA_dt"))

    # 24. shadow_length_rate (Exercise 4, #55)
    shadow_data = [
        (680, 170, 2),
        (600, 150, 3),
        (450, 180, 1.5),
        (500, 160, 2.5),
        (720, 180, 2),
    ]
    for HL, HM, v in shadow_data:
        q = (
            f"A headlamp is placed at a height of {HL} cm from the surface of the earth. A man of height {HM} cm walks with velocity {v} m/sec "
            f"in a straight line towards the base of the lamp. Find: (1) The rate of change of the length of the man's shadow. (2) The velocity of the shadow's tip."
        )
        entries.append(make_entry(q, "shadow_length_rate", {"H_lamp": str(HL/100), "H_man": str(HM/100), "v_man": str(-v)}, "ds_dt"))

    # 25. shadow_length_rate_variant (Exercise 4, #56)
    shadow_v_data = [
        (480, 180, 150, 300),
        (500, 170, 120, 250),
        (420, 160, 100, 200),
        (600, 180, 200, 400),
        (450, 150, 140, 280),
    ]
    for HL, HM, v, dist in shadow_v_data:
        q = (
            f"A man of height {HM} cm walks with a velocity of magnitude {v} cm/sec towards a lamp of height {HL} cm above the ground. "
            f"Find: (1) The rate of change of the shadow length. (2) The rate of change of the distance between the head of the man and the lamp "
            f"at the instant when the man is {dist} cm apart from the base of the lamp."
        )
        entries.append(make_entry(q, "shadow_length_rate_variant", {"H_lamp": str(HL), "H_man": str(HM), "v_man": str(-v), "dist": str(dist)}, "dD_dt"))

    # 26. two_trains_different_start_times (Exercise 4, #69)
    train_data = [
        (45, 60, 11, 12, 15),
        (50, 70, 10, 11, 14),
        (40, 60, 8, 9, 12),
        (60, 80, 9, 11, 14),
        (30, 40, 12, 13, 16),
    ]
    for v1, v2, h1, h2, heval in train_data:
        q = (
            f"A train starts its journey at {h1} o'clock towards east with velocity {v1} km/h, while another train begins its journey at {h2} o'clock "
            f"from the same station towards south with velocity {v2} km/h. Find the rate of increase of distance between the two trains at {heval} o'clock afternoon."
        )
        entries.append(make_entry(q, "two_trains_different_start_times", {"v1": str(v1), "v2": str(v2), "h1": str(h1), "h2": str(h2), "h_eval": str(heval)}, "d_rate"))

    # 27. gas_law_pressure_volume_rate (Exercise 4, #66)
    gas_data = [
        (1000, 250, "-2", 100),
        (800, 300, "-3", 150),
        (1200, 200, "-1.5", 80),
        (600, 400, "-4", 200),
        (1500, 100, "-1", 50),
    ]
    for P0, V0, dV, V in gas_data:
        q = (
            f"A mass of gas at constant temperature has its volume decreasing at a constant rate of {dV.replace('-', '')} cm3/sec. "
            f"If pressure is inversely proportional to volume (PV = constant) and the pressure is {P0} gm.wt/cm2 when the volume is {V0} cm3, "
            f"find the rate of change of the pressure with respect to time when the volume of gas reaches {V} cm3."
        )
        entries.append(make_entry(q, "gas_law_pressure_volume_rate", {"P0": str(P0), "V0": str(V0), "dV_dt": dV, "V": str(V)}, "dP_dt"))

    # 28. ohms_law_resistance_rate (Exercise 4, #67)
    ohms_data = [
        (12, 2, "1", "-1/2"),
        (24, 3, "2", "-1/3"),
        (10, 2, "1.5", "-0.5"),
        (18, 3, "1", "-0.2"),
        (30, 5, "3", "-1"),
    ]
    for V, I, dV, dI in ohms_data:
        q = (
            f"In a closed electric circuit, V is the potential difference in volts, I is the current in amperes, and R is resistance in ohms (V = I * R). "
            f"If the potential difference increases at a rate of {dV} volt/sec and current intensity decreases at a rate of {dI.replace('-', '')} ampere/sec, "
            f"find the rate of change of resistance at the moment when V = {V} volts and I = {I} amperes."
        )
        entries.append(make_entry(q, "ohms_law_resistance_rate", {"V": str(V), "I": str(I), "dV_dt": dV, "dI_dt": dI}, "dR_dt"))

    # 29. spherical_balloon_gas_leak_rate (Exercise 4, #63)
    balloon_leak_data = [
        ("-20", 10),
        ("-30", 15),
        ("-15", 8),
        ("-40", 20),
        ("-25", 12),
    ]
    for dV, r in balloon_leak_data:
        q = (
            f"Gas leaks from a spherical balloon at a rate of {dV.replace('-', '')} cm3/s. "
            f"Find the rate of change of the balloon radius when the radius is {r} cm, and find the rate of change of the balloon's external surface area at the same instant."
        )
        entries.append(make_entry(q, "spherical_balloon_gas_leak_rate", {"dV_dt": dV, "r": str(r)}, "dr_dt"))

    # 30. absolute_extrema_closed_interval (Exercise 10, #1)
    extrema_interval_data = [
        ("x^2 - 6*x + 13", -1, 5),
        ("x^3 - 3*x + 2", -2, 3),
        ("2*x^3 - 3*x^2 - 12*x + 1", -2, 4),
        ("x^4 - 2*x^2 + 3", -2, 2),
        ("x/(x^2 + 1)", -2, 2),
        ("x^2 - 4*x + 5", 0, 3),
        ("3*x^4 - 4*x^3", -1, 2),
        ("x^3 - 6*x^2 + 9*x + 1", 0, 4),
        ("2*x - cos(x)", 0, "pi"),
        ("sin(x) + cos(x)", 0, "pi"),
    ]
    for f_str, a, b in extrema_interval_data:
        q = f"Find the absolute maximum and minimum values of the function f(x) = {f_str} on the closed interval [{a}, {b}]."
        entries.append(make_entry(q, "absolute_extrema_closed_interval", {"f": f_str, "a": str(a), "b": str(b)}, "max_min"))

    # 31. cubic_two_critical_points (Exercise 9, #13)
    cubic_crit2_data = [
        ("(-3, 3)", "(-1, -1)"),
        ("(1, 4)", "(3, 0)"),
        ("(-2, 5)", "(0, 1)"),
        ("(2, -1)", "(4, 3)"),
        ("(-1, 2)", "(1, -2)"),
    ]
    for p1, p2 in cubic_crit2_data:
        q = (
            f"If the two points {p1} and {p2} are two critical points of the cubic function y = a x^3 + b x^2 + c x + d, "
            f"find the values of constants a, b, c, and d, and determine the nature (local maximum or minimum) of each critical point."
        )
        entries.append(make_entry(q, "cubic_two_critical_points", {"pt1": p1, "pt2": p2}, "coefficients"))

    # 32. cubic_origin_critical_tangent (Exercise 9, #14)
    cubic_orig_data = [
        (3, 2, "12*x - 3*y + 11 = 0", 1),
        (2, 1, "9*x - y + 5 = 0", 1),
        (4, 2, "16*x - 4*y + 7 = 0", 1),
        (3, 1, "6*x - y + 2 = 0", 2),
        (2, 3, "8*x - 2*y + 3 = 0", 1),
    ]
    for xc, xm, tan_eq, xt in cubic_orig_data:
        q = (
            f"Find the values of a, b, c, and d if the curve whose equation is y = a x^3 + b x^2 + c x + d passes through the origin, "
            f"has a critical point at x = {xc}, a local extremum at x = {xm}, and the tangent to the curve at x = {xt} has equation {tan_eq}."
        )
        entries.append(make_entry(q, "cubic_origin_critical_tangent", {"x_crit": str(xc), "x_max": str(xm), "tangent_eq": tan_eq, "x_tan": str(xt)}, "coefficients"))

    # 33. cubic_curve_critical_points (Exercise 9, #12)
    cubic_pts_data = [
        ("(3, 0)", "(0, 6)", "(2, 2)"),
        ("(2, 0)", "(0, 4)", "(1, 2)"),
        ("(4, 0)", "(0, 8)", "(2, 4)"),
        ("(-1, 0)", "(0, 2)", "(1, 0)"),
        ("(1, 0)", "(0, 3)", "(2, 1)"),
    ]
    for p1, p2, pc in cubic_pts_data:
        q = (
            f"If the curve of the function y = a x^3 + b x^2 + c x + d passes through the two points {p1} and {p2} "
            f"and has a critical point at {pc}, find the constants a, b, c, and d and determine the nature of each critical point."
        )
        entries.append(make_entry(q, "cubic_curve_critical_points", {"pt1": p1, "pt2": p2, "crit_pt": pc}, "coefficients"))

    return entries

if __name__ == "__main__":
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "verimath_finetune_dataset.jsonl")
    dataset_path = os.path.abspath(dataset_path)

    new_entries = generate_dataset_entries()
    print(f"Generated {len(new_entries)} high-quality training pairs for Pages 14-30.")

    # Read current lines to verify
    with open(dataset_path, "r", encoding="utf-8") as f:
        existing_lines = f.readlines()
    print(f"Current dataset entries: {len(existing_lines)}")

    # Append new lines
    with open(dataset_path, "a", encoding="utf-8") as f:
        for entry in new_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Verify new count
    with open(dataset_path, "r", encoding="utf-8") as f:
        total_lines = len(f.readlines())
    print(f"Updated total dataset entries: {total_lines} (+{len(new_entries)})")
