import curses
from time import sleep
from threading import Thread


class Controller:

    def __init__(self, terminal, game):
        self.terminal = terminal
        self.game = game

    def handle_input(self):
        key = self.terminal.getch()
        if key == ord("\n"):
            return self.game.next_game_mode()
        if key == 127:
            return self.game.next_game_mode(dec=True)
        if self.game.game_mode == 0:
            if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                self.game.move_cursor(key)
            if key == ord(" "):
                self.game.flip_cell()
        if self.game.game_mode == 1:
            if key == ord(" "):
                self.game.tick()
        if self.game.game_mode == 2:
            self.game.tick()
            sleep(.2)
