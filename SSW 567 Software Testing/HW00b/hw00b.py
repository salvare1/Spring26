def classify_triangle(a, b, c):
    sides = sorted([a, b, c])

    if sides[0] <= 0 or sides[0] + sides[1] <= sides[2]:
        return "Not a valid triangle"

    if a == b == c:
        triangle_type = "equilateral"
    elif a == b or b == c or a == c:
        triangle_type = "isosceles"
    else:
        triangle_type = "scalene"

    if sides[0]**2 + sides[1]**2 == sides[2]**2:
        return f"{triangle_type} right triangle"

    return triangle_type
