from tkinter import Tk, BOTH, Canvas
import time
import random

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
    def __init__(self, _win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = _win
        self.visited = False

    def __str__(self):
        return f"{self._x1, self._y1}"

    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)))
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), fill_color="white")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)))
        else:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), fill_color="white")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)))
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), fill_color="white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)))
        else:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), fill_color="white")
    
    def draw_move(self, to_cell, undo=False):
        this_cell_x_center = self._x1 + ((self._x2 - self._x1) / 2)
        this_cell_y_center = self._y1 + ((self._y2 - self._y1) / 2)

        to_cell_x_center = to_cell._x1 + ((to_cell._x2 - to_cell._x1) / 2)
        to_cell_y_center = to_cell._y2 + ((to_cell._y1 - to_cell._y2) / 2)

        line_color = "red"
        if undo == True:
            line_color = "grey"

        self._win.draw_line(
                Line(
                    Point(this_cell_x_center, this_cell_y_center), 
                    Point(to_cell_x_center, to_cell_y_center)
                    ), 
                line_color
                )

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed

        if self._seed is not None:
            self._random = random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def __str__(self):
        return f"num rows are {self._cells}"

    def _create_cells(self):
        self._cells = []
        for c in range(self._num_cols):
            column_list = []
            for r in range(self._num_rows):
                column_list.append(Cell(self._win))
            self._cells.append(column_list)

        for c in range(self._num_cols):
            for r in range(self._num_rows):
                self._draw_cell(c, r)


    def _draw_cell(self, c, r):
        if self._win is None:
            return

        cell = self._cells[c][r]

        cell._x1 = self._x1 + c * self._cell_size_x
        cell._y1 = self._y1 + r * self._cell_size_y

        cell._x2 = cell._x1 + self._cell_size_x
        cell._y2 = cell._y1 + self._cell_size_y

        self._cells[c][r].draw()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.10)
   
    def _break_entrance_and_exit(self):
        first_cell = self._cells[0][0]
        last_cell = self._cells[-1][-1]

        first_cell.has_left_wall = False
        first_cell.draw()
        last_cell.has_bottom_wall = False
        last_cell.draw()

    def _break_walls_r(self, i, j):

        self._cells[i][j].visited = True


        while True:
            possible_visits = []

            # check up
            if j > 0 and self._cells[i][j - 1].visited == False:
                possible_visits.append((i, j - 1))
            # check right
            if i < self._num_cols - 1 and self._cells[i + 1][j].visited == False:
                possible_visits.append((i + 1, j))
            # check down
            if j < self._num_rows - 1 and self._cells[i][j + 1].visited == False:
                possible_visits.append((i, j + 1))
            # check left
            if i > 0 and self._cells[i - 1][j].visited == False:
                possible_visits.append((i - 1, j))
            
            if len(possible_visits) == 0:
                self._draw_cell(i, j)
                return
            
            # pick random direction
            next_direction = random.choice(possible_visits)

            # find which direction it is  

            # up
            if j - 1 == next_direction[1]:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            # right
            if i + 1 == next_direction[0]: 
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # down
            if j + 1 == next_direction[1]:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # left 
            if i - 1 == next_direction[0]:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False

            self._break_walls_r(next_direction[0], next_direction[1])

    def _reset_cells_visited(self):

        for column in self._cells:
            for cell in column:
                cell.visited = False

    def solve(self):
        print("solving maze...")
        solved = self._solve_r(0, 0)
        if solved:
            print("solved! =)")
            return True
        else:
            print("not solved =(")
            return False

    def _solve_r(self, i, j):
        curr = self._cells[i][j]

        self._animate()
        self._cells[i][j].visited = True

        # at the end
        if self._cells[i][j] == self._cells[-1][-1]:
            return True

        # check up
        if j > 0 and not self._cells[i][j - 1].visited and not self._cells[i][j].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            solved = self._solve_r(i, j-1)
            if solved:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
            
        # check right
        if i < self._num_cols - 1 and not self._cells[i + 1][j].visited and not self._cells[i][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            solved = self._solve_r(i + 1, j)
            if solved:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # check down
        if j < self._num_rows - 1 and not self._cells[i][j + 1].visited and not self._cells[i][j].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            solved = self._solve_r(i, j + 1)
            if solved:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # check left
        if i > 0 and not self._cells[i - 1][j].visited and not self._cells[i][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            solved = self._solve_r(i - 1, j)
            if solved:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        
        # if end was not found
        return False

def main():
    win = Window(750, 750)
    # Start X, Start Y, Number of Rows, Number of Columns, Cell size X, Cell size Y
    maze = Maze(100, 100, 10, 10, 50, 50, win)
    maze.solve()
    win.run()

main()
