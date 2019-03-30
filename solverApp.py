import sys
if sys.version_info[0] >= 3:
    import tkinter as tk
    from tkinter import *
    from tkinter import ttk
    import tkinter.font
else:
    import Tkinter as tk
    from tkinter import *
    import ttk
    import tkFont
import array
import math
import numpy as np
from copy import copy, deepcopy

def main():
    print("I SOLVE SUDOKU PUZZLES")

    root = tk.Tk()
    frame = tk.Frame(master = root)
    frame.pack(fill=tk.BOTH, expand=1)
    solveButton = tk.Button(master = frame, height = 1, width = 14)
    solveButton.grid(row = 10, column = 0, columnspan = 9)
    solveButton.config(text = "Solve", font = ('COURIER', 20))
    resetButton = tk.Button(master = frame, height = 2, width = 8)
    resetButton.grid(row = 11, column = 0, columnspan = 9, pady = 1)
    resetButton.config(text = "Reset", font = ('COURIER', 8))

    reset_pressed = False
    w, h = 9, 9;
    sudoku = []
    entry_list = []

    def set_grid():
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(master = frame, width = 2)
                entry.grid(row = row, column = col, padx = 1, pady = 1)
                if row < 3 or row > 5:
                    if col > 2 and col < 6:
                        entry.configure({'background': 'grey90'})
                else:
                    if col < 3 or col > 5:
                        entry.configure({'background': 'grey90'})
                entry_list.append(entry)
    set_grid()
    def reset_grid(event):
        reset_pressed = True
        for x in range(9):
            for y in range(9):
                    entry_list[x*9 + y].delete(0,'end')

    def solve_puzzle(event):
        print('Solving...')
        print('boop.')
        print('beep.')
        print('bop.')
        can_solve = True
        saved_sudoku = [] #this will be used to iterate through and save sudoku puzzles
        solved_sudoku = [[0 for x in range(w)] for y in range(h)]
        check_for_progress = [[], [], solved_sudoku]
        entry_list_postition = 0
        sudoku = []

        for x in range(9):
            sudoku.append([])
            for y in range(9):
                val = entry_list[entry_list_postition].get()
                if val in '123456789' and val != '':
                    sudoku[x].append([int(val)])

                elif val == '':
                    sudoku[x].append([1, 2, 3, 4, 5, 6, 7, 8, 9])
                else:
                    print('I will treat values not in range 1-9 as empty')
                    sudoku[x].append([1, 2, 3, 4, 5, 6, 7, 8, 9])
                entry_list_postition += 1

        sudoku_new = np.array(sudoku)
        for x in range(9):
            for y in range(9):
                block = find_block(sudoku_new, x, y)
                if is_multiple_rowcol(sudoku_new, x, y) \
                or is_multiple_block(block):
                    can_solve = False

        if can_solve:
            saved_sudoku.append(sudoku_new)
            if solve(saved_sudoku, solved_sudoku, check_for_progress):
                print('Solved!')
                for x in range(9):
                    for y in range(9):
                        entry_list[x*9 + y].delete(0,'end')
                        entry_list[x*9 + y].insert(END, solved_sudoku[x][y])
        else:
            print("This is not a valid puzzle")
            print('Try a valid puzzle')

    def find_block(puzzle, row, col):
        block = [[0 for x in range(3)] for y in range(3)]
        if row < 3:
            if col < 3:
                block = puzzle[0:3, 0:3]
            elif col < 6:
                block = puzzle[0:3, 3:6]
            else:
                block = puzzle[0:3, 6:9]
        elif row < 6:
            if col < 3:
                block = puzzle[3:6, 0:3]
            elif col < 6:
                block = puzzle[3:6, 3:6]
            else:
                block = puzzle[3:6, 6:9]
        else:
            if col < 3:
                block = puzzle[6:9, 0:3]
            elif col < 6:
                block = puzzle[6:9, 3:6]
            else:
                block = puzzle[6:9, 6:9]
        return block

    def guess_num(grid, len_saved, saved_sudoku):
        removed_one = False
        copy_sudoku = deepcopy(grid)
        copy_grid = deepcopy(grid)
        for x in range(9):
            for y in range(9):
                if removed_one == False:
                    if 1 < len(grid[x][y]) < 3:
                        #this finds if there are 2 options in a cell
                        #then it replaces the "tree root" with one guess
                        #and keeps going forward with the other guess
                        copy_sudoku[x][y].remove(copy_sudoku[x][y][0])
                        copy_grid[x][y].remove(copy_grid[x][y][1])
                        del saved_sudoku[-1]
                        saved_sudoku.append(copy_sudoku)
                        saved_sudoku.append(copy_grid)
                        removed_one = True

    def is_multiple_rowcol(grid, row, col):
        end = False
        double_value_in_row = []
        double_value_in_col = []
        for x in range(9):
            row_cell = grid[row][x]
            col_cell = grid[x][col]
            if len(row_cell) == 1:
                double_value_in_row.append(row_cell[0])
                check_row_number_repeat = double_value_in_row.count(row_cell[0])
                if check_row_number_repeat > 1:
                    end = True
            if len(col_cell) == 1:
                double_value_in_col.append(col_cell[0])
                check_col_number_repeat = double_value_in_col.count(col_cell[0])
                if check_col_number_repeat > 1:
                    end = True
        if end:
            return True
        else:
            return False

    def is_multiple_block(block):
        end = False
        block_values = []
        for x in range(3):
            for y in range(3):
                cell = block[x][y]
                if len(cell) == 1 and end == False:
                    block_values.append(cell[0])
                    block_values_repeat = block_values.count(cell[0])
                    if block_values_repeat > 1:
                        end = True
        if end == True:
            return True
        else:
            return False

    def solve(saved_sudoku, solved_sudoku, check_for_progress):
        is_done = False
        count_row, count_col = 0,0
        value_int = 0
        count = 0
        doubles_occur = False

        while is_done == False:
            if count > 5000:
                print('this puzzle is not solvable, try a real puzzle')
                return False
                break
            if doubles_occur:
                del saved_sudoku[-1]
            doubles_occur = False
            puzzle = saved_sudoku[len(saved_sudoku)-1]
            if check_for_progress[0] == check_for_progress[2]:
                guess_num(puzzle, len(saved_sudoku)-1, saved_sudoku)
            while count_row < 9:
                while count_col < 9:
                    length = len(puzzle[count_row][count_col])
                    if length == 1:
                        value = puzzle[count_row][count_col]
                        value_int = value[0]
                        block = find_block(puzzle, count_row,count_col)
                        if is_multiple_block(block) == False \
                        and is_multiple_rowcol(puzzle, count_row, count_col) == False:
                            solved_sudoku[count_row][count_col] = value_int
                        else:
                            doubles_occur = True
                        for x in range(3):
                            for y in range(3):
                                cell = block[x][y]
                                length_cell = len(block[x][y])
                                if length_cell > 1:
                                    if value_int in cell:
                                        cell.remove(value_int)
                        for x in range(9):
                            if len(puzzle[count_row][x]) > 1:
                                if value_int in puzzle[count_row][x]:
                                    puzzle[count_row][x].remove(value_int)
                            if len(puzzle[x][count_col]) > 1:
                                if value_int in puzzle[x][count_col]:
                                    puzzle[x][count_col].remove(value_int)
                    count_col += 1
                check_for_progress.append(solved_sudoku)
                if len(check_for_progress) != 3:
                    check_for_progress.remove(check_for_progress[0])
                count_row += 1
                count_col = 0
            count_row = 0
            count_col = 0
            count += 1
            is_zero = 1
            for x in range(9):
                for y in range(9):
                    is_zero *= solved_sudoku[x][y]
            if is_zero != 0:
                is_done = True
                return True

    solveButton.bind("<ButtonPress-1>", solve_puzzle)
    resetButton.bind("<ButtonPress-1>", reset_grid)
    root.title("Sudoku Solver")
    root.mainloop()
if __name__ == '__main__':
    main()
