from tkinter import Tk, Canvas

RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"

X = 0
Y = 1

width, height = None, None
rectangles = []

field = None

tk = Tk()


with open("lab3.txt") as f:
    width, height = f.readline().split("x")
    width, height = int(width), int(height)

    field = [[False for _ in range(width)] for _ in range(height)]

    rectangles.append([1, 1, width, height])
    for line in f.readlines():
        rectangle = [int(i) for i in line.split(", ")]
        rectangles.append(rectangle)


canvas = Canvas(width=width, height=height, bg="white")

for rectangle in rectangles:
    canvas.create_rectangle(*rectangle)


def fill(x, y, color="red", type="full"):
    # print(x, y)

    # if x in [0, width + 1, height + 1] or y in [0, height + 1, width + 1]:
    #     print(x, y, " in [0, {}, {}]".format(width, height))
    #     return

    if is_black_point(x, y) or field[y][x]:
        return

    field[y][x] = True

    # canvas.
    if x % 5 == 0:# or y % 5 == 0:
        canvas.create_line(x, y, x, y, fill=color)

    fill(x + 1, y, color=color, type="full")
    fill(x - 1, y, color=color, type="full")
    fill(x, y + 1, color=color, type="full")
    fill(x, y - 1, color=color, type="full")


def is_black_point(x, y):
    def is_point_on_the_border(x, y, x1, y1, x2, y2):
        if y1 > y2:
            y1, y2 = y2, y1

        if x1 > x2:
            x1, x2, = x2, x1

        if x in [x1, x2] and y1 <= y <= y2:
            return True

        if y in [y1, y2] and x1 <= x <= x2:
            return True

        return False

    for rectangle in rectangles:
        if is_point_on_the_border(x, y, *rectangle):
            return True

    return False


def find_corner(_x, _y):
    x, y = _x, _y
    if is_black_point(x, y):
        raise Exception

    without_move = True
    while True:
        if not is_black_point(x + 1, y - 1):
            x, y = x + 1, y - 1
            without_move = False
            continue

        if not is_black_point(x + 1, y):
            x = x + 1
            without_move = False
            continue

        if not is_black_point(x, y - 1):
            y = y - 1
            without_move = False
            continue

        if without_move:
            return x, y
        else:
            without_move = True


def fill2(_x, _y, color="gray"):
    def is_equal_points(a, b):
        return a[0] == b[0] and a[1] == b[1]

    point = list(find_corner(_x, _y))
    polygon = [point, point]

    direction = DOWN

    while not (is_equal_points(polygon[0], polygon[-1]) and len(polygon) >= 4):
        print(polygon)

        x, y = point

        if direction == DOWN:
            if not is_black_point(x + 1, y):
                point = [point[0], point[1]]
                polygon.append(point)
                direction = RIGHT
                continue

            if is_black_point(x, y + 1):
                point = [point[0], point[1]]
                polygon.append(point)
                direction = LEFT
                continue

            point[Y] = y + 1

        if direction == LEFT:
            if not is_black_point(x, y + 1):
                point = [point[0], point[1]]
                polygon.append(point)
                direction = DOWN
                continue

            if is_black_point(x, y + 1):
                point = [point[0], point[1]]
                polygon.append(point)
                direction = UP
                continue

            point[X] = x - 1

        if direction == UP:
            if not is_black_point(x - 1, y):
                point = [point[0], point[1]]
                polygon.append(point)
                direction = LEFT
                continue

            if is_black_point(x, y - 1):
                point = [point[0], point[1]]
                polygon.append(point)
                direction = RIGHT
                continue

            point[Y] = y - 1

        if direction == RIGHT:
            if not is_black_point(x, y - 1):
                point = [point[0], point[1]]
                polygon.append(point)
                direction = UP
                continue

            if is_black_point(x + 1, y):
                point = [point[0], point[1]]
                polygon.append(point)
                direction = DOWN
                continue

            point[X] = x + 1

    canvas.create_polygon(*polygon, fill=color)



# canvas.create_line(24, 55, 24, 55)

# fill2(24, 61)

fill(11, 22, "red")
# fill(11, 31)
fill(71, 71)


canvas.pack()
tk.mainloop()
