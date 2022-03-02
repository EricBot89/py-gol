import curses


class Renderer:

    mode_map = [
        "EDITING",
        "STEPPING",
        "RUNNING"
    ]

    def __init__(self, terminal, game):
        self.game = game
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.COLOR_LIVE = curses.color_pair(1)
        self.COLOR_DEAD = curses.color_pair(2)
        self.COLOR_INVERTED = curses.color_pair(3)
        self.MAX_Y, self.MAX_X = terminal.getmaxyx()
        self.terminal = terminal
        self.game_pad = curses.newpad(game.SIZE_Y + 2, game.SIZE_X + 2)

    def render(self):
        if self.game.update_menu:
            self.game.update_menu = False
            self.terminal.erase()
            self.terminal.addstr(1, 1, "MODE")
            self.terminal.addstr(
                1, 6, self.mode_map[self.game.game_mode], self.COLOR_INVERTED)
            self.terminal.addstr(2, 1, "SIZE")
            self.terminal.addstr(
                2, 6, f"{self.game.SIZE_X}x{self.game.SIZE_Y}", self.COLOR_INVERTED)
            self.terminal.addstr(3, 1, "WRAP")
            self.terminal.addstr(
                3, 6, f"{self.game.TORUS}", self.COLOR_INVERTED)
            self.terminal.addstr(4, 1, "GROW")
            self.terminal.addstr(
                4, 6, self.game.GROW_RULE, self.COLOR_INVERTED)
            self.terminal.addstr(5, 1, "LIVE")
            self.terminal.addstr(
                5, 6, self.game.LIVE_RULE, self.COLOR_INVERTED)
            self.terminal.addstr(6, 1, "TIME")
            self.terminal.addstr(
                6, 6, f"{self.game.TICK_TIME}s", self.COLOR_INVERTED)
            for y in range(self.MAX_Y-1):
                self.terminal.addch(y, 19, "╏", self.COLOR_INVERTED)
            self.terminal.refresh()
        for i, row in enumerate(self.game.cells):
            for j, cell in enumerate(row):
                tile_char = "X" if self.game.game_mode == 0 and self.game.cursor == (
                    i, j) else " "
                color = self.COLOR_LIVE if cell.status else self.COLOR_DEAD
                self.game_pad.addch(i, j, tile_char, color)
        self.game_pad.refresh(0, 0, 0, 20, self.MAX_Y - 1, self.MAX_X - 1)
