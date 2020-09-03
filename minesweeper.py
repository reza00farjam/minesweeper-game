# import modules =================================================

from tkinter import *
import random

# game's logic ===================================================

bombs = []

while len(bombs) != 35:
    x = random.randint(0, 9)
    y = random.randint(0, 19)
    if (x, y) not in bombs:
        bombs.append((x, y))

field = {}

for i in range(10):
    for j in range(20):
        
        if (i, j) in bombs:
            field[(i, j)] = -1
            continue
        
        near_bombs = 0
        
        if i > 0 and (i-1, j) in bombs:
            near_bombs += 1
        if i < 9 and (i+1, j) in bombs:
            near_bombs += 1
        if j > 0 and (i, j-1) in bombs:
            near_bombs += 1
        if j < 19 and (i, j+1) in bombs:
            near_bombs += 1
        if i > 0 and j > 0 and (i-1, j-1) in bombs:
            near_bombs += 1
        if i > 0 and j < 19 and (i-1, j+1) in bombs:
            near_bombs += 1
        if i < 9 and j > 0 and (i+1, j-1) in bombs:
            near_bombs += 1
        if i < 9 and j < 19 and (i+1, j+1) in bombs:
            near_bombs += 1
        
        field[(i, j)] = near_bombs

# gui part & functionality ========================================

flag = True
myFont = ("Bahnschrift", "14")

main = Tk()
main.title("Minesweeper")
main.resizable(0, 0)
main.iconbitmap(r".\data\icon.ico")

for i in range(10):
    for j in range(20):
        Button(main, bg='#172a3a', command=lambda i=i, j=j: play(i, j), padx=20, font=myFont).grid(row=i, column=j)

pl1 = pl2 = 0

Label(main, text=pl1, bg='red', font=("Bahnschrift", "18")).grid(row=10, column=0, columnspan=10, sticky=E+W)
Label(main, text=pl2, bg='blue', font=("Bahnschrift", "18")).grid(row=10, column=10, columnspan=10, sticky=E+W)
Label(main, bg='red', font=("Bahnschrift", "18")).grid(row=11, column=0, columnspan=20, sticky=E+W)

checked = []
used = []

def end():
    for item in field.keys():
        if item not in used:
            if field[item] == -1:
                Button(main, bg='black', state=DISABLED, font=myFont).grid(row=item[0], column=item[1], sticky=E+W)
            elif field[item]:
                Button(main, text=field[item], bg='yellow', state=DISABLED, font=myFont).grid(row=item[0], column=item[1], sticky=E+W)
            else:
                Button(main, bg='yellow', state=DISABLED, font=myFont).grid(row=item[0], column=item[1], sticky=E+W)

def findzero(i, j):
    if field[(i, j)]:
        used.append((i, j))
        checked.append((i, j))
        
        Button(main, text=field[(i, j)], bg='#09bc8a', state=DISABLED, font=myFont).grid(row=i, column=j, sticky=E+W)
        return
    elif (i, j) in checked:
        return
    
    used.append((i, j))
    checked.append((i, j))
    Button(main, bg='#D0CDD7', state=DISABLED, font=myFont).grid(row=i, column=j, sticky=E+W)
    
    if i > 0:
        findzero(i-1, j)
    if i < 9:
        findzero(i+1, j)
    if j > 0:
        findzero(i, j-1)
    if j < 19:
        findzero(i, j+1)
    if i > 0 and j > 0:
        findzero(i-1, j-1)
    if i > 0 and j < 19:
        findzero(i-1, j+1)
    if i < 9 and j > 0:
        findzero(i+1, j-1)
    if i < 9 and j < 19:
        findzero(i+1, j+1)

def play(row, col):
    global flag, pl1, pl2
    
    if field[(row, col)] == -1:
        used.append((row, col))
        
        Button(main, bg='red' if flag else 'blue', state=DISABLED, padx=20, font=myFont).grid(row=row, column=col)
        
        if flag:
            pl1 += 1
        else:
            pl2 += 1        
    elif field[(row, col)]:
        flag = not flag
        used.append((row, col))
        Button(main, text=field[(row, col)], bg='#09bc8a', state=DISABLED, font=myFont).grid(row=row, column=col, sticky=E+W)
    else:
        flag = not flag
        
        checked.clear()
        findzero(row, col)
    
    if flag:
        Label(main, text=pl1, bg='red', font=("Bahnschrift", "18")).grid(row=10, column=0, columnspan=10, sticky=E+W)
        Label(main, bg='red', font=("Bahnschrift", "18")).grid(row=11, column=0, columnspan=20, sticky=E+W)
    else:
        Label(main, text=pl2, bg='blue', font=("Bahnschrift", "18")).grid(row=10, column=10, columnspan=10, sticky=E+W)
        Label(main, bg='blue', font=("Bahnschrift", "18")).grid(row=11, column=0, columnspan=20, sticky=E+W)
    
    if pl1 == 18:
        end()
        Label(main, text='Red Won!', bg='red', font=("Bahnschrift", "18")).grid(row=11, column=0, columnspan=20, sticky=E+W)
        return main.mainloop()
    elif pl2 == 18:
        end()
        Label(main, text='Blue Won!', bg='blue', font=("Bahnschrift", "18")).grid(row=11, column=0, columnspan=20, sticky=E+W)
        return main.mainloop()