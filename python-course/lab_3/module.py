from errors import OutOfTheBoundsException

width, height = None, None
rectangles = []
field = None


def draw_rectagles_and_return_array(Canvas, filename):
    with open(filename) as f:
        _width, _height = f.readline().split("x")
        global width, height
        width, height = int(_width), int(_height)

        global field
        field = [[False for _ in range(width)] for _ in range(height)]

        rectangles.append([1, 1, width, height])

        for line in f.readlines():
            rectangle = [int(i) for i in line.split(", ")]

            validate_rectangle(rectangle)
            
            rectangles.append(rectangle)

    canvas = Canvas(width=width, height=height, bg="white")

    for rectangle in rectangles:
        canvas.create_rectangle(*rectangle)

    return canvas


def validate_rectangle(rectangle):
    x1, y1, x2, y2 = rectangle

    if 0 <= x1 <= height and 0 <= y1 <= width and 0 <= x2 <= height and 0 <= y2 <= width:
        return

    raise OutOfTheBoundsException("Check data.txt")


def is_point_on_the_border(x, y):
    def _is_point_on_the_border(_x, _y, x1, y1, x2, y2):
        if y1 > y2:
            y1, y2 = y2, y1

        if x1 > x2:
            x1, x2, = x2, x1

        if _x in [x1, x2] and y1 <= y <= y2:
            return True

        if _y in [y1, y2] and x1 <= x <= x2:
            return True

        return False

    for rectangle in rectangles:
        if _is_point_on_the_border(x, y, *rectangle):
            return True

    return False


def fill(canvas, _x, _y, color="red", fill_type="full"):
    queue = [(_x, _y)]

    while queue:
        (x, y), queue = queue[0], queue[1:]

        if is_point_on_the_border(x, y) or field[y][x]:
            continue

        field[y][x] = True

        if fill_type == "full":
            canvas.create_line(x, y, x+1, y, fill=color)
        elif fill_type == "vert" and x % 5 == 0:
            canvas.create_line(x, y, x+1, y, fill=color)
        elif fill_type == "horiz" and y % 5 == 0:
            canvas.create_line(x, y, x+1, y, fill=color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))
