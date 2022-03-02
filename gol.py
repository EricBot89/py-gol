import curses
from Game import Game
from Renderer import Renderer
from Controller import Controller


def gol(term):
    curses.curs_set(0)
    y, x = term.getmaxyx()
    Game.set_param(size_x=x - 21, size_y=y-1)
    gol = Game(term)
    ren = Renderer(term, gol)

    ren.render()

    con = Controller(term, gol)

    while True:
        con.handle_input()
        ren.render()


if __name__ == "__main__":
    curses.wrapper(gol)
    curses.wrapper()
