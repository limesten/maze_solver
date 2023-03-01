from tkinter import Tk, BOTH, Canvas
import time

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)

    def run(self):
        self.__root.mainloop()

    def redraw(self):
        self.__canvas.update_idletasks()

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(
        self,
        p1,
        p2,
    ):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
        canvas.pack(fill=BOTH, expand=1)

class Cell:
    def __init__(self, _x1, _y1, _x2, _y2, _win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1
        self._y2 = _y2
        self._win = _win

    def __str__(self):
        return f"{self._x1, self._y1}"

    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)))
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)))
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)))
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)))
    
    def draw_move(self, to_cell, undo=False):
        this_cell_x_center = self._x1 + ((self._x2 - self._x1) / 2)
        this_cell_y_center = self._x1 + ((self._x2 - self._x1) / 2)

        to_cell_x_center = to_cell._x1 + ((to_cell._x2 - to_cell._x1) / 2)
        to_cell_y_center = to_cell._y2 + ((to_cell._y1 - to_cell._y2) / 2)

        line_color = "red"
        if undo == True:
            line_color = "gray"

        self._win.draw_line(Line(Point(this_cell_x_center, this_cell_y_center), Point(to_cell_x_center, to_cell_y_center)), line_color)

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells(num_rows, num_cols, cell_size_x, cell_size_y, win)

    def __str__(self):
        return f"num rows are {self._cells}"

    def _create_cells(self, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self._cells = []
        for c in range(num_cols):
            column_list = []
            for r in range(num_rows):
                x1 = self._x1 + c * cell_size_x
                y1 = self._y1 + r * cell_size_y

                x2 = x1 + cell_size_x
                y2 = y1 + cell_size_y

                cell = Cell(x1, y1, x2, y2, win)
                column_list.append(cell)
            self._cells.append(column_list)
        
        self._draw_cells(self._cells)

    def _draw_cells(self, column_list):
        for column in column_list:
            for cell in column:
                cell.draw()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
   
                


def main():
    win = Window(2000, 1000)
    # Start X, Start Y, Number of Rows, Number of Columns, Cell size X, Cell size Y
    maze = Maze(100, 100, 10, 10, 50, 50, win)
    win.run()

main()