"""

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|                                            |
| DEVELOPER   : VIKAS BHASKAR VOORADI        |
|                                            |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
| 1.   vertical_single_line(n=10)                                                   |
| 2.   vertical_left_bar_line(width=5,n=10)                                         |
| 3.   vertical_right_bar_line(width=5,n=10,space=50)                               |
| 4.   horizontal_single_line(n=10,row=1)                                           | 
| 5.   horizontal_upper_bar_line(width=20,row=5)                                    |
| 6.   left_angle_triangle(row=8)                                                   |
| 7.   left_angle_up_side_down_triangle(row=8)                                      | 
| 8.   right_angle_triangle(row=8)                                                  | 
| 9.   right_angle_up_side_down_triangle(row=8)                                     |
| 10.  pyramid(row=8)                                                               |
| 11.  pyramid_up_side_down(row=8)                                                  |
| 12.  square(row=5)                                                                |
| 13.  diamond(row=8)                                                               |
| 14.  left_angle_triangle_flip_up_down(row=8)                                      |
| 15 . right_angle_triangle_flip_up_down(row=8)                                     | 
| 16.  right_shankarpali(row=8)                                                     |
| 17.  left_shankarpali(row=8)                                                      | 
| 18.  empty_square(row=8)                                                          |
| 19.  empty_left_side_triangle(row=8)                                              |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


"""


def vertical_single_line(n=10):
    for i in range(n):
        print("*")


def vertical_left_bar_line(width=5, n=10):
    for i in range(n):
        print(width * "*")


def vertical_right_bar_line(width=5, n=10, space=50):
    for i in range(n):
        print(space * " " + width * "*")


def horizontal_single_line(n=10, row=1):
    for i in range(row):
        print(n * "*")


def horizontal_upper_bar_line(width=20, row=5):
    for i in range(row):
        print(width * "*")


def left_angle_triangle(row=8):
    for i in range(row):
        print(i * "* ")


def left_angle_up_side_down_triangle(row=8):
    cnt = 0
    for i in range(row):
        print((row - cnt) * "* ")
        cnt = cnt + 1


def right_angle_triangle(row=8):
    for i in range(1, row + 1):
        print(((row - 1) * 2) * " " + i * "* ")
        row = row - 1


def right_angle_up_side_down_triangle(row=8):
    space = 0
    for i in range(row + 1):
        print(space * " " + row * "* ")
        row = row - 1
        space = space + 2


def pyramid(row=8):
    for i in range(row):
        print(((row * 2) - 2) * " " + i * "*   ")
        row = row - 1


def pyramid_up_side_down(row=8):
    cnt = 0
    space = 0
    for i in range(row):
        print(space * " " + (row - cnt) * "*   ")
        cnt = cnt + 1
        space = space + 2


def square(row=5):
    for i in range(row):
        print(row * 2 * "*")


def diamond(row=8):
    row_1 = row
    space = 2
    for i in range(row):
        print(((row * 2) - 2) * " " + i * "*   ")
        row = row - 1

    for i in reversed(range(row_1 - 1)):
        print(space * " " + i * "*   ")
        space = space + 2


def left_angle_triangle_flip_up_down(row=8):
    for i in range(row + 1):
        print(i * "* ")

    for i in reversed(range(row)):
        print(i * "* ")


def right_angle_triangle_flip_up_down(row=8):
    row_1 = row
    space = 2
    for i in range(1, row + 1):
        print(((row - 1) * 2) * " " + i * "* ")
        row = row - 1

    for i in reversed(range(row_1)):
        print(space * " " + i * "* ")
        space = space + 2


def right_shankarpali(row=8):

    row_1 = row

    for i in range(1, row + 1):
        print(((row - 1) * 2) * " " + i * "* ")
        row = row - 1

    for i in reversed(range(row_1)):
        print(i * "* ")


def left_shankarpali(row=8):

    row_1 = row
    space = 2

    for i in range(row):
        print(i * "* ")

    for i in reversed(range(row_1 - 1)):
        print(space * " " + i * "* ")
        space = space + 2


def empty_box(row=8):
    space = row - 2
    for i in range(1, row + 1):
        if i == 1:
            print(row * "* ")
        elif i < row:
            print("*" + (space * 2) * " " + " *")
        else:
            print(row * "* ")


def empty_left_side_triangle(row=8):
    space = 0
    for i in range(1, row + 1):
        if i == 1:
            print(i * "*")
        elif i < row:
            print("*" + space * " " + " *")
            space = space + 2
        else:
            print(row * "* ")
