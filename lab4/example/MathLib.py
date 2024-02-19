import math

def degree_to_radian(degree):
    return math.radians(degree)

def trapezoid_area(height, base1, base2):
    return (base1 + base2) * height / 2

def regular_polygon_area(sides, length):
    return (sides * length ** 2) / (4 * math.tan(math.pi / sides))

def parallelogram_area(base, height):
    return base * height

if __name__ == "__main__":
    degree = 15
    print(f"{degree} degrees in radians: {degree_to_radian(degree)}")
    height, base1, base2 = 5, 5, 6
    print(f"Area of trapezoid: {trapezoid_area(height, base1, base2)}")
    sides, length = 4, 25
    print(f"Area of regular polygon: {regular_polygon_area(sides, length)}")
    base, height = 5, 6
    print(f"Area of parallelogram: {parallelogram_area(base, height)}")
