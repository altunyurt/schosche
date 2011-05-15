#coding:utf-8
from constraint import *
import psyco 
psyco.full()
def solve_magic_square(size = 5):
    "Get the magic square solution for any numbered square."
    magic = Problem()#create a blank problem
    rows = range(size)#Rows indices eg[0, 1, 2]
    cols = range(size)#cols indices eg [0, 1, 2]
    board_line_sum = sum(range(1, size*size+1))/size # What does each row, col and diag sum up to? Eg 15, for size 3
    board = [(row, col) for row in rows for col in cols] # Cartesan of rows and col, eg [(0, 0), (0, 1), (1, 0), (1, 1)] for size = 2
    row_set = [zip([el]*len(cols), cols) for el in rows]#A list of all the rows, eg [[(0, 0), (0, 1)], [(1, 0), (1, 1)]]
    col_set = [zip(rows, [el]*len(rows)) for el in cols]#A list of all the columns, eg [[(0, 0), (1, 0)], [(0, 1), (1, 1)]]
    diag1 = zip(rows, cols)#One of the diagonals, eg [(0,0), (0,1)]
    diag2 = zip(rows, cols[::-1])#Other diagonal, eg [(0,1), (1,0)]

    magic.addVariables(board, range(1, size*size+1))#add Each block of square as a variable. There range is between [1..n*n+1]
    magic.addConstraint(ExactSumConstraint(board_line_sum), diag1)#Add diagonals as a constraint, they must sum to board_line_sum
    magic.addConstraint(ExactSumConstraint(board_line_sum), diag2)#Add other diagonal as constraint.
    for row in row_set:
        magic.addConstraint(ExactSumConstraint(board_line_sum), row)#Add each row as constraint, they must sum to board_line_sum
    for col in col_set:
        magic.addConstraint(ExactSumConstraint(board_line_sum), col)#Similarly add each column as constraint.
    magic.addConstraint(AllDifferentConstraint(), board)#Every block has a different number.
    return magic.getSolution() #Retutn the solution.

if __name__ == '__main__':
    print solve_magic_square()
