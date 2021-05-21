from tkinter import *
import time
import random


_black = "#000000"
_red = "#9F0000"
_green = "#009F00"
_blue = "#00009F"
_white = "#9F9F9F"
colors = [_black, _red, _green, _blue, _white]


class TileSet:
    def __init__(self, w, h, tile_size=32, fps=4):
        self.fps = fps
        self.w = w
        self.h = h
        self.root = Tk()
        self.root.title("Game of Colors - a Conway's Game of Life variation")
        self.tile_size = tile_size
        self.field = [[TileOperator(i, j) for i in range(w)] for j in range(h)]
        self.canvas = Canvas(width=tile_size * w + tile_size // 16, height=tile_size * h + tile_size // 16, bg="#303030")
        self.canvas.pack()

        self.screen_wrap = True

        for row in self.field:
            for tile in row:
                tile.Draw(self.canvas, self.tile_size)

        self.Run()
        self.root.mainloop()

    def Prep(self):
        rmap = [[random.randint(0, 4) for i in range(self.w)] for j in range(self.h)]
        for j in range(self.h):
            for i in range(self.w):
                self.SetTileColor(i, j, colors[rmap[i][j]])

    def Run(self):
        self.Prep()
        self.root.update()
        while (True):
            time.sleep(1 / self.fps)
            for row in self.field:
                for tile in row:
                    self.StepAtCoords(tile.x, tile.y)
            self.Update()

    def Update(self):
        for row in self.field:
            for tile in row:
                tile.UpdateImage(self.canvas)
        self.root.update()

    def StepAtCoords(self, x, y):
        neighbors = {}
        neighbors[_black] = 0
        neighbors[_white] = 0
        neighbors[_red] = 0
        neighbors[_green] = 0
        neighbors[_blue] = 0
        for color_hex in self.GetNeigborsColors(x, y):
            neighbors[color_hex] += 1
        self.field[y][x].Step(neighbors)

    def GetNeigborsColors(self, x, y):
        colors = []
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if (i == 0 and j == 0):
                    continue
                nx = x + i
                ny = y + j
                if (self.screen_wrap):
                    nx = nx % self.w
                    ny = ny % self.h
                    colors.append(self.field[ny][nx].color)
                else:
                    if (0 <= nx and nx < w and 0 <= ny and ny < h):
                        colors.append(self.field[ny][nx].color)
        return colors

    def SetTileColor(self, x, y, _col):
        self.field[y][x].next_color = _col
        self.field[y][x].UpdateImage(self.canvas)
        self.root.update()


class TileOperator:
    def __init__(self, grid_x, grid_y):
        self.color = "#000000"
        self.next_color = "#000000"
        self.x = grid_x
        self.y = grid_y
        self.image = -1

        self.survive_if = [2, 3]
        self.produce_if = [3]

    def Draw(self, canvas, tile_size):
        image_size = tile_size - tile_size // 16
        xroot = tile_size * self.x + 2 * tile_size // 16
        yroot = tile_size * self.y + 2 * tile_size // 16
        if (self.image != -1):
            canvas.delete(self.image)
        self.image = canvas.create_rectangle(xroot, yroot, xroot + image_size, yroot + image_size, fill=self.color, outline="")

    def UpdateImage(self, canvas):
        canvas.itemconfig(self.image, fill=self.next_color)
        self.color = self.next_color
        self.next_color = _black

    def Step(self, neighbors):
        if (self.color == _black):
            self.StepBlack(neighbors)
        if (self.color == _red):
            self.StepRed(neighbors)
        if (self.color == _green):
            self.StepGreen(neighbors)
        if (self.color == _blue):
            self.StepBlue(neighbors)
        if (self.color == _white):
            self.StepWhite(neighbors)

    def StepBlack(self, neighbors):
        spread_colors = []
        for _col in [_red, _green, _blue]:
            if (neighbors[_col] in self.produce_if):
                spread_colors.append(_col)
        if (len(spread_colors) == 1):
            self.next_color = spread_colors[0]

    def StepWhite(self, neighbors):
        _col = _black
        power = 0
        spread_colors = []
        for _col in [_red, _green, _blue]:
            if (neighbors[_col] > 0):
                spread_colors.append(_col)
        if (len(spread_colors) == 3):
            self.next_color = _white
        else:
            _color = _black
            power = 0
            for _col in [_red, _green, _blue]:
                if (neighbors[_col] > power):
                    power = neighbors[_col]
                    _color = _col
            self.next_color = _color

    def StepRed(self, neighbors):
        if (neighbors[_green] > 0 and neighbors[_blue] > 0):
            self.next_color = _white
        else:
            spread_color = _black
            for _col in [_green, _blue]:
                if (neighbors[_col] in self.produce_if):
                    spread_color = _col
            if (neighbors[_red] in self.survive_if):
                self.next_color = _red
            else:
                self.next_color = spread_color

    def StepGreen(self, neighbors):
        if (neighbors[_red] > 0 and neighbors[_blue] > 0):
            self.next_color = _white
        else:
            spread_color = _black
            for _col in [_red, _blue]:
                if (neighbors[_col] in self.produce_if):
                    spread_color = _col
            if (neighbors[_green] in self.survive_if):
                self.next_color = _green
            else:
                self.next_color = spread_color

    def StepBlue(self, neighbors):
        if (neighbors[_green] > 0 and neighbors[_red] > 0):
            self.next_color = _white
        else:
            spread_color = _black
            for _col in [_green, _red]:
                if (neighbors[_col] in self.produce_if):
                    spread_color = _col
            if (neighbors[_blue] in self.survive_if):
                self.next_color = _blue
            else:
                self.next_color = spread_color


game = TileSet(25, 25)