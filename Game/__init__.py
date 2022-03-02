from threading import Thread
from time import sleep
import curses
from .cell import Cell
from.rule_parser import DefaultRuleParser


class Game:

    GROW_RULE = "EQ:3"
    LIVE_RULE = "LT:4;GT:1"
    SIZE_Y = 20
    SIZE_X = 20
    TORUS = False
    TICK_TIME = .25

    rule_parser = DefaultRuleParser

    def __init__(self, term):
        self.game_mode = 0
        self.cells = [[Cell(i, j) for j in range(self.SIZE_X)]
                      for i in range(self.SIZE_Y)]
        self.cells_list = sum(self.cells, [])
        self.update_neighbors()
        self.cursor = (0, 0)
        self.grow_rule = self.rule_parser.parse_rule(self.GROW_RULE)
        self.live_rule = self.rule_parser.parse_rule(self.LIVE_RULE)
        self.term = term
        self.update_menu = True

    def update_neighbors(self):
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                go_up = i-1 >= 0 or self.TORUS
                go_down = i+1 < self.SIZE_Y or self.TORUS
                go_left = j-1 >= 0 or self.TORUS
                go_right = j+1 < self.SIZE_X or self.TORUS
                down = (i+1) % self.SIZE_Y
                up = (i-1)
                left = j - 1
                right = (j + 1) % self.SIZE_X
                if go_up:
                    cell.neighbors.append(self.cells[up][j])
                if go_down:
                    cell.neighbors.append(self.cells[down][j])
                if go_right:
                    cell.neighbors.append(self.cells[i][right])
                if go_left:
                    cell.neighbors.append(self.cells[i][left])
                if go_up and go_left:
                    cell.neighbors.append(self.cells[up][left])
                if go_up and go_right:
                    cell.neighbors.append(self.cells[up][right])
                if go_down and go_left:
                    cell.neighbors.append(self.cells[down][left])
                if go_down and go_right:
                    cell.neighbors.append(self.cells[down][right])

    def next_game_mode(self, *, dec=False):
        self.update_menu = True
        self.game_mode = (
            self.game_mode - 1) % 3 if dec else (self.game_mode + 1) % 3
        if self.game_mode == 2:
            return self.term.nodelay(True)
        self.term.nodelay(False)

    def move_cursor(self, key):
        y, x = self.cursor
        if key == curses.KEY_UP:
            y = (y - 1) % self.SIZE_Y
        if key == curses.KEY_DOWN:
            y = (y + 1) % self.SIZE_Y
        if key == curses.KEY_LEFT:
            x = (x - 1) % self.SIZE_X
        if key == curses.KEY_RIGHT:
            x = (x + 1) % self.SIZE_X
        self.cursor = (y, x)

    def flip_cell(self):
        y, x = self.cursor
        cell = self.cells[y][x]
        cell.status = (cell.status + 1) % 2

    def tick(self):
        next_grid = [[0 for cell in row] for row in self.cells]
        t_0 = Thread(target=self.min_timer, args=(self.TICK_TIME,))
        threads = []
        for cell in self.cells_list:
            cell_thread = Thread(
                target=self.get_next_status, args=(cell, next_grid))
            cell_thread.start()
            threads.append(cell_thread)
        t_0.start()
        for t in threads:
            t.join()
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                cell.status = next_grid[i][j]
        t.join()

    def get_next_status(self, cell, grid):
        status = cell.status
        live_neighbors = cell.live_neighbors
        y, x = cell.coords
        grid[y][x] = self.live_rule(
            live_neighbors) if status else self.grow_rule(live_neighbors)

    @staticmethod
    def min_timer(time):
        sleep(time)

    @classmethod
    def set_param(cls, *, live_rule=None, grow_rule=None, toriodal=None, size_y=None, size_x=None, tick_time=None):
        if live_rule:
            cls.LIVE_RULE = live_rule
        if grow_rule:
            cls.GROW_RULE = grow_rule
        if toriodal is not None:
            cls.TORUS = toriodal
        if size_x:
            cls.SIZE_X = size_x
        if size_y:
            cls.SIZE_Y = size_y
        if tick_time and tick_time > 0:
            cls.TICK_TIME = tick_time
