import numpy as np
from PIL.ImageEnhance import Color
from numpy import ndarray

import constants
from agentsearch.state import State
from agentsearch.action import Action


class WarehouseState(State[Action]):

    def __init__(self, matrix: ndarray, rows, columns):
        super().__init__()

        self.line_forklift = None
        self.column_forklift = None

        self.rows = rows
        self.columns = columns
        self.matrix = matrix

    def can_move_up(self) -> bool:
        #can move up if the line above the forklift is empty and is not null (not out of bounds)
        if self.line_forklift != 0:
            return self.matrix[self.line_forklift - 1][self.column_forklift] != constants.SHELF and \
                self.matrix[self.line_forklift - 1][self.column_forklift] != constants.PRODUCT
        return False

    def can_move_right(self) -> bool:
        #can move right if the column to the right of the forklift is empty and is not null (not out of bounds)
        if self.column_forklift != self.columns - 1:
            return self.matrix[self.line_forklift][self.column_forklift + 1] != constants.SHELF and \
                self.matrix[self.line_forklift][self.column_forklift + 1] != constants.PRODUCT
        return False

    def can_move_down(self) -> bool:
        #can move down if the line below the forklift is empty and is not null (not out of bounds)
        if self.line_forklift != self.rows - 1:
            return self.matrix[self.line_forklift + 1][self.column_forklift] != constants.SHELF and \
                self.matrix[self.line_forklift + 1][self.column_forklift] != constants.PRODUCT
        return False

    def can_move_left(self) -> bool:
        #can move left if the column to the left of the forklift is empty and is not null (not out of bounds)
        if self.column_forklift != 0:
            return self.matrix[self.line_forklift][self.column_forklift - 1] != constants.SHELF and \
                self.matrix[self.line_forklift][self.column_forklift - 1] != constants.PRODUCT
        return False

    def move_up(self) -> None:
        self.line_forklift -= 1

    def move_right(self) -> None:
        self.column_forklift += 1

    def move_down(self) -> None:
        self.line_forklift += 1

    def move_left(self) -> None:
        self.column_forklift -= 1


    def get_cell_color(self, row: int, column: int) -> Color:
        if self.matrix[row][column] == constants.EXIT:
            return constants.COLOREXIT

        if self.matrix[row][column] == constants.PRODUCT_CATCH:
            return constants.COLORSHELFPRODUCTCATCH

        if self.matrix[row][column] == constants.PRODUCT:
            return constants.COLORSHELFPRODUCT

        switcher = {
            constants.FORKLIFT: constants.COLORFORKLIFT,
            constants.SHELF: constants.COLORSHELF,
            constants.EMPTY: constants.COLOREMPTY
        }
        return switcher.get(self.matrix[row][column], constants.COLOREMPTY)

    def __str__(self):
        matrix_string = str(self.rows) + " " + str(self.columns) + "\n"
        for row in self.matrix:
            for column in row:
                matrix_string += str(int(column)) + " "
            matrix_string += "\n"
        return matrix_string

    def __eq__(self, other):
        if isinstance(other, WarehouseState):
            return self.line_forklift == other.line_forklift and self.column_forklift == other.column_forklift
        return NotImplemented

    def __hash__(self):
        return hash(self.matrix.tostring())
