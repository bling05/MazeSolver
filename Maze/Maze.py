import time
import random

class bcolors:
    ENDC = '\033[0m'
    BLACK = '\033[1;30;40m'
    WHITE = '\033[1;37;47m'
    RED = '\033[1;31;41m'
    GREEN = '\033[1;32;42m'
def clearTerminal():
    print('\033[2J')
def gotoTop():
    print('\033[1;1H')

def makeMaze(filename):
    file1 = open(filename, encoding="cp1252")
    temp = file1.read()
    maze = [[char for char in i] for i in temp.split('\n')] # Convert string into 2d list of chars
    return maze

def generateMaze(maze, startRow, startCol):
    generateHelper(maze, startRow, startCol)
    maze[startRow][startCol] = 'S'
    row = startRow
    col = startCol
    maxDist = 0
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            if maze[i][j] == ' ':
                if abs(i-row) + abs(j-col) > maxDist:
                    maxDist = abs(i-row) + abs(j-col)
                    row = i
                    col = j
    maze[row][col] = 'E'


def generateHelper(maze, startRow, startCol):
    if startRow < 1 or startRow > len(maze) - 2 or startCol < 1 or startCol > len(maze[0]) - 2:
        return
    openNeighbors = 0
    if maze[startRow + 1][startCol] == ' ': openNeighbors += 1
    if maze[startRow - 1][startCol] == ' ': openNeighbors += 1
    if maze[startRow][startCol + 1] == ' ': openNeighbors += 1
    if maze[startRow][startCol - 1] == ' ': openNeighbors += 1
    if openNeighbors >= 2: return
    maze[startRow][startCol] = ' '

    directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]
    for k in range(1, 6):
        for i in range(0, 4):
            rand = random.randint(0,3)
            directions[i], directions[rand] = directions[rand], directions[i]
    for i in range(0, 4):
        generateHelper(maze, startRow + directions[i][1], startCol + directions[i][0])

def toString(maze):
    str = ""
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            if maze[i][j] == '#': str += "" + bcolors.BLACK+maze[i][j]+bcolors.ENDC
            elif maze[i][j] == '.': str += "" + bcolors.WHITE+maze[i][j]+bcolors.ENDC
            elif maze[i][j] == '@': str += "" + bcolors.RED+maze[i][j]+bcolors.ENDC
            elif maze[i][j] == 'E': str += "" + bcolors.GREEN+maze[i][j]+bcolors.ENDC
            else: str += maze[i][j]
        if i != len(maze)-1:
            str += '\n'
    return str

def solve(maze):
    if animate:
        clearTerminal()
    startRow, startCol = 0, 0
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            if maze[i][j] == 'S':
                startRow = i
                startCol = j
    return startRow, startCol

def solve2(row, col):
    if maze[row][col] == 'E':
        return 0
    elif maze[row][col] == '#' or maze[row][col] == '.' or maze[row][col] == '@':
        return -1
    maze[row][col] = '@'

    if animate:
        gotoTop()
        print(toString(maze))
        time.sleep(delay)

    down = solve2(row+1, col)
    if down>-1:
        return down+1
    right = solve2(row, col + 1)
    if right > -1:
        return right + 1
    up = solve2(row-1, col)
    if up>-1:
        return up+1
    left = solve2(row, col-1)
    if left>-1:
        return left+1

    maze[row][col] = '.'

    if animate:
        gotoTop()
        print(toString(maze))
        time.sleep(delay)

    return -1

def solved(maze):
    clearTerminal()
    gotoTop()
    str = toString(maze)
    print(str.replace("@", bcolors.GREEN+'@'+bcolors.ENDC))


# DRIVER
retry = True
while retry:
    importQuery = input('Import or Generate? ').lower()
    if importQuery == 'import':
        filename = input('Input filename: ')
        maze = makeMaze(filename)
        retry = False
    if importQuery == 'generate':
        generateRows = int(input('How many rows? '))
        generateCols = int(input('How many columns? '))
        startRow = int(input('Starting row: '))
        startCol = int(input('Starting column '))
        maze = [['#'] * generateCols for i in range(generateRows)]
        generateMaze(maze, startRow, startCol)
        print(toString(maze))
        retry = False
retry = True
while retry:
    b = input('Animate? True/False: ').lower()
    if b == 'true':
        animate = True
        delay = float(input('Delay between moves (sec): '))
        row, col = solve(maze)
        solve2(row, col)
        solved(maze)
        retry = False
    if b == 'false':
        animate = False
        print(toString(maze))
        retry = False
