import numpy as np
import random
import PriorityQueue

EMPTY = 0
WALL = 1
GHOST = 2
PACMAN = 3

class Board:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.board = np.zeros(row*column).reshape(row, column)
        self.board[0][0] = PACMAN  #default - can be changed by using method putPacman

    #to randomly place walls and ghosts
    def randomize(self):
        for i in range(self.row):
            for j in range(self.column):
                if self.board[i][j] != PACMAN:
                    self.board[i][j] = random.randint(0,2)

    #to replace pacman
    def putPacman(self, location):
        if location[0] >= self.row or location[1] >= self.column or location[0] < 0 or location[1] < 0 or self.board[location[0]][location[1]] != EMPTY:
            print("Cannot put Pacman in cell: " + location.__str__())
            return

        #delete existing pacman
        for i in range(0, self.row):
            for j in range(0,self.column):
                if self.board[i][j] == PACMAN:
                    self.board[i][j] = 0
                    break

        self.board[location[0]][location[1]] = PACMAN


    def putGhost(self, locations):
        for item in locations:
            if item[0] < self.row and item[1] < self.column and item[0] > 0 and item[1] > 0 and self.board[item[0]][item[1]] == EMPTY:
                self.board[item[0]][item[1]] = GHOST
            else:
                print("Cannot put ghost in cell: " + item.__str__())


    def putWalls(self, locations):
        for item in locations:
            if item[0] < self.row and item[1] < self.column and item[0] > 0 and item[1] > 0 and self.board[item[0]][item[1]] == EMPTY:
                self.board[item[0]][item[1]] = WALL
            else:
                print("Cannot put Wall in cell: " + item.__str__())

    def putEmpty(self, locations):
        for item in locations:
            if item[0] < self.row and item[1] < self.column and item[0] > 0 and item[1] > 0 and self.board[item[0]][item[1]] != PACMAN:
                self.board[item[0]][item[1]] = WALL
            else:
                print("Cannot put Clear cell: " + item.__str__())

    def findPacman(self):
        for i in range(0, self.row):
            for j in range(0,self.column):
                if self.board[i][j] == PACMAN:
                    return [i,j]

    #return a list of possible moves from an exsiting cell in the matrix
    def getSuccessors(self, state):
        x = state[0]
        y = state[1]
        succ = []
        if x > 0 and self.board[x-1, y] != WALL:
            succ.append([x-1, y])
        if x < self.row - 1 and self.board[x+1, y] != WALL:
            succ.append([x+1, y])
        if y > 0 and self.board[x, y-1] != WALL:
            succ.append([x, y-1])
        if y < self.column - 1 and self.board[x, y+1] != WALL:
            succ.append([x, y+1])

        return succ

    #prints out shortest distance of all reachable ghosts
    def findGhosts(self):
        frontier = PriorityQueue.PriorityQueue()
        visited = []
        state = self.findPacman()

        node = {}
        node["state"] = state
        node["cost"] = 0
        frontier.push(node, node["cost"])  # push beginning state with its cost into queue

        # loop through queue using cost method
        while not frontier.isEmpty():
            node = frontier.pop()
            state = node["state"]
            cost = node["cost"]

            if state in visited:
                continue

            visited.append(state)

            if self.board[state[0]][state[1]] == GHOST:
                print("shortest distance to Ghost: " + repr(state) + " is " + repr(node["cost"]))
                continue

            for move in self.getSuccessors(state):  # for each child of the node
                if move not in visited:  # if haven't visit it
                    sub_node = {}  # create a node of it to push it to frontier
                    sub_node["state"] = move
                    sub_node["cost"] = node["cost"] + 1
                    frontier.push(sub_node, sub_node["cost"])


# Example1:
b = Board(10, 10)
b.putPacman([3, 4])
b.putGhost([[3, 5], [1, 7], [6, 6]])
b.putWalls([[4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9]])
print("\n")
print(b.board)
b.findGhosts()

# Example2:
b = Board(10, 10)
b.putPacman([3, 4])
b.randomize()
print("\n")
print(b.board)
b.findGhosts()
