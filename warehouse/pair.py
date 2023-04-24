import constants


class Pair:
    def __init__(self, cell1, cell2):
        self.cell1 = cell1
        self.cell2 = cell2
        self.value = 0
        # if cell1 is agent
        if self.cell1 == constants.FORKLIFT:
            if self.cell2.column -1 == constants.EMPTY:
                self.value = abs(self.cell2.column -1 - self.cell1.column) + abs(self.cell2.line - self.cell1.line)
            else :
                self.value = abs(self.cell2.column +1 - self.cell1.column) + abs(self.cell2.line - self.cell1.line)
        else:
            if self.cell1.column - 1 == constants.EMPTY:
                self.value = abs(self.cell2.column - self.cell1.column) + abs(self.cell2.line - self.cell1.line)
            else:
                self.value = abs(self.cell2.column - self.cell1.column) + abs(self.cell2.line - self.cell1.line)


        #calculate the value of the pair
        self.value = abs(self.cell2.column - self.cell1.column) + abs(self.cell2.line - self.cell1.line)



    def hash(self):
        return str(self.cell1.line) + "_" + str(self.cell1.column) + "_" + str(
            self.cell2.line) + "_" + str(self.cell2.column)

    def __str__(self):
        return str(self.cell1.line) + "-" + str(self.cell1.column) + " / " + str(self.cell2.line) + "-" + str(self.cell2.column) + ": " + str(self.value) + "\n"

