# =======================================================

from tkinter import *
from winsound import *
import random
import json
import sys
import os

# =======================================================

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    See more on topic here:
        https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/7675014#7675014
    """
    
    return os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), relative_path)

# =======================================================

options = {
    "mode": {
        "fast": {
            "bombs": 15,
            "height": 7,
            "width": 8
        },
        "normal": {
            "bombs": 35,
            "height": 10,
            "width": 20
        },
        "slow": {
            "bombs": 99,
            "height": 16,
            "width": 30
        }
    },
    "color": ['blue', 'green', 'orange', 'pink', 'purple', 'red', 'yellow'],
    "font": ['Comic Sans MS', 'Courier', 'Tahoma', 'Times New Roman']
}

# =======================================================

def sounds(select):
    if data['sound'][0] == 'off':
        return
    
    if select == 'bomb':
        PlaySound(resource_path(r'data\sounds\find_bomb.wav'), SND_FILENAME | SND_ASYNC)
    elif select == 'miss':
        PlaySound(resource_path(r'data\sounds\miss.wav'), SND_FILENAME | SND_ASYNC)
    elif select == 'end':
        PlaySound(resource_path(r'data\sounds\end.wav'), SND_FILENAME | SND_ASYNC)
    elif select == 'click':
        PlaySound(resource_path(r'data\sounds\click.wav'), SND_FILENAME | SND_ASYNC)
    elif select == 'click2':
        PlaySound(resource_path(r'data\sounds\click2.wav'), SND_FILENAME | SND_ASYNC)
    elif select == 'start':
        PlaySound(resource_path(r'data\sounds\start.wav'), SND_FILENAME | SND_ASYNC)
    elif select == 'exit':
        PlaySound(resource_path(r'data\sounds\exit.wav'), SND_FILENAME | SND_ASYNC)        

# =======================================================

def menu():
    global bombs_num, height, width, pl1_color, pl2_color, small_font, big_font, data
    
    with open(resource_path('data\data.json')) as file:
        data = json.load(file)
    
    bombs_num = options['mode'][data['mode']]['bombs']
    height = options['mode'][data['mode']]['height']
    width = options['mode'][data['mode']]['width']
    pl1_color = data['player1']
    pl2_color = data['player2']
    small_font = (data['font'], "14")
    big_font = (data['font'], "18")
    
    root = Tk()
    root.title("Minesweeper")
    root.resizable(0, 0)
    root.iconbitmap(resource_path(r"data\icon\bomb.ico"))
    root.configure(bg='#172a3a')
    
    photo_start = PhotoImage(file = resource_path(r"data\img\start.png")).subsample(2, 2)
    photo_setting = PhotoImage(file = resource_path(r"data\img\setting.png")).subsample(2, 2)
    photo_exit = PhotoImage(file = resource_path(r"data\img\exit.png")).subsample(2, 2)
    
    def action(task):
        root.destroy()
        
        if task == 'start':
            sounds('start')
            start()
        elif task == 'setting':
            sounds('click2')
            setting()
        elif task == 'exit':
            sounds('exit')
    
    Button(root, text=' Start', image=photo_start, compound='left', font=big_font, bg='grey', command=lambda: action('start')).grid(row=0, column=0, ipadx=100, padx=30, pady=30, sticky=W+E)
    Button(root, text=' Setting', image=photo_setting, compound='left', font=big_font, bg='grey', command=lambda: action('setting')).grid(row=1, column=0, padx=30, sticky=W+E)
    Button(root, text=' Exit', image=photo_exit, compound='left', font=big_font, bg='grey', command=lambda: action('exit')).grid(row=2, column=0, padx=30, pady=30, sticky=W+E)
    
    root.mainloop()

# =======================================================

def setting():
    sett = Tk()
    sett.title('Minesweeper -> Setting')
    sett.iconbitmap(resource_path(r".\data\icon\setting.ico"))
    sett.resizable(0, 0)
    sett.configure(bg='#172a3a')
    
    mode_frame = LabelFrame(sett, text='MODE', font=small_font, bg='#172a3a', fg='grey')
    
    mode_var = StringVar()
    mode_var.set(data['mode'])
    
    for item in options['mode']:
        Radiobutton(mode_frame, text=item.title(), fg='white', bg='#172a3a', selectcolor='black', activebackground='#172a3a', font=big_font, variable=mode_var, value=item, command=lambda: sounds('click')).pack(ipadx=15, anchor=W)
    
    mode_frame.grid(row=0, column=0, padx=20, pady=15, sticky=S+N, rowspan=2)
    
    pl1_frame = LabelFrame(sett, text='PLAYER 1', font=small_font, bg=data['player1'], fg='black')
    
    pl1_color_var = StringVar()
    pl1_color_var.set(pl1_color)

    def change1():
        nonlocal pl1_frame
        
        sounds('click')
        pl1_frame['bg'] = pl1_color_var.get()

    col = 0
    for item in options['color']:
        Radiobutton(pl1_frame, text=item.title(), fg=item, bg='#172a3a', selectcolor='black', activebackground='#172a3a', font=big_font, variable=pl1_color_var, value=item, command=change1).grid(row=0, column=col, ipadx=15)
        col += 1

    pl1_frame.grid(row=0, column=1, padx=20, pady=15, sticky=E+W, columnspan=3)
    
    pl2_frame = LabelFrame(sett, text='PLAYER 2', font=small_font, bg=data['player2'], fg='black')
    
    pl2_color_var = StringVar()
    pl2_color_var.set(data['player2'])
    
    def change2():
        nonlocal pl2_frame
        
        sounds('click')
        pl2_frame['bg'] = pl2_color_var.get()
    
    col = 0
    for item in options['color']:
        Radiobutton(pl2_frame, text=item.title(), fg=item, bg='#172a3a', selectcolor='black', activebackground='#172a3a', font=big_font, variable=pl2_color_var, value=item, command=change2).grid(row=0, column=col, ipadx=15)
        col += 1
    
    pl2_frame.grid(row=1, column=1, padx=20, pady=15, sticky=E+W, columnspan=3)
    
    font_frame = LabelFrame(sett, text='FONT', font=small_font, bg='#172a3a', fg='grey')

    font_var = StringVar()
    font_var.set(data['font'])
    
    col = 0
    for item in options['font']:
        Radiobutton(font_frame, text=item, fg='white', bg='#172a3a', selectcolor='black', activebackground='#172a3a', font=(item, '18'), variable=font_var, value=item, command=lambda: sounds('click')).grid(row=0, column=col, ipadx=5)
        col += 1
    
    font_frame.grid(row=2, column=0, padx=20, pady=15, sticky=E+W, columnspan=2)
    
    sounds_frame = LabelFrame(sett, text='SOUNDS', font=small_font, bg='#172a3a', fg='grey')
    
    def toggle(task):
        if task == 'off':
            PlaySound(resource_path(r'data\sounds\on.wav'), SND_FILENAME | SND_ASYNC)
            data['sound'][0] = 'on'
            data['sound'][1] = on_off['bg'] = 'green'
            on_off['text'] = 'ON '
            on_off['command'] = lambda: toggle('on')
        else:
            PlaySound(resource_path(r'data\sounds\off.wav'), SND_FILENAME | SND_ASYNC)
            data['sound'][0] = 'off'
            data['sound'][1] = on_off['bg'] = 'red'
            on_off['text'] = 'OFF'
            on_off['command'] = lambda: toggle('off')
    
    on_off = Button(sounds_frame, width=6, text=data['sound'][0].upper(), bg=data['sound'][1], fg='white', font=small_font, command=lambda: toggle(data['sound'][0]))
    on_off.pack(pady=5)
    
    sounds_frame.grid(row=2, column=2, padx=20, pady=15, sticky=E+W)
    
    def save():
        global data
        nonlocal mode_var, font_var, pl1_color_var, pl2_color_var
        
        sounds('click2')
        data['mode'] = mode_var.get()
        data['font'] = font_var.get()
        if pl1_color_var.get() != pl2_color_var.get():
            data['player1'] = pl1_color_var.get()
            data['player2'] = pl2_color_var.get()
        
        with open(resource_path('data\data.json'), 'w') as file:
            json.dump(data, file, indent=4)
        
        sett.destroy()
        menu()
    
    Button(sett, text='MENU', bg='grey', fg='#172a3a', font=big_font, command=save).grid(row=2, column=3, padx=20, pady=15, sticky=E+W+N+S)

# =======================================================

def setUp():
    global bombs, field
    
    bombs = []
    
    while len(bombs) != bombs_num:
        x = random.randint(0, height - 1)
        y = random.randint(0, width - 1)
        if (x, y) not in bombs:
            bombs.append((x, y))
    
    field = {}
    
    for i in range(height):
        for j in range(width):
            
            if (i, j) in bombs:
                field[(i, j)] = -1
                continue
            
            near_bombs = 0
            
            if i > 0 and (i-1, j) in bombs:
                near_bombs += 1
            if i < height-1 and (i+1, j) in bombs:
                near_bombs += 1
            if j > 0 and (i, j-1) in bombs:
                near_bombs += 1
            if j < width-1 and (i, j+1) in bombs:
                near_bombs += 1
            if i > 0 and j > 0 and (i-1, j-1) in bombs:
                near_bombs += 1
            if i > 0 and j < width-1 and (i-1, j+1) in bombs:
                near_bombs += 1
            if i < height-1 and j > 0 and (i+1, j-1) in bombs:
                near_bombs += 1
            if i < height-1 and j < width-1 and (i+1, j+1) in bombs:
                near_bombs += 1
            
            field[(i, j)] = near_bombs

def start():
    setUp()
    
    flag = True
    main = Tk()
    main.title("Minesweeper")
    main.resizable(0, 0)
    main.iconbitmap(resource_path(r"data\icon\bomb.ico"))
    
    photo_bomb = PhotoImage(file = resource_path(r"data\img\bomb.png")).subsample(2, 2)
    photo_reset = PhotoImage(file = resource_path(r"data\img\reset.png")).subsample(2, 2)
    
    for i in range(height):
        for j in range(width):
            Button(main, bg='#172a3a', command=lambda i=i, j=j: play(i, j), padx=20, font=small_font).grid(row=i, column=j)
    
    pl1 = pl2 = 0
    
    def back():
        main.destroy()
        sounds('click2')
        menu()
    
    pl1_label = Label(main, text=pl1, bg=pl1_color, font=big_font)
    pl1_label.grid(row=height, column=0, columnspan=width//2, sticky=E+W)
    pl2_label = Label(main, text=pl2, bg=pl2_color, font=big_font)
    pl2_label.grid(row=height, column=width//2, columnspan=width//2, sticky=E+W)
    switch_label = Label(main, text='Find  {}  Bombs  to  Win!'.format(bombs_num//2+1), bg=pl1_color, font=big_font)
    switch_label.grid(row=height+1, column=0, columnspan=width, sticky=E+W)
    menu_button = Button(main, text='M    E    N    U', bg='#172a3a', fg='grey', font=small_font, command=back)
    menu_button.grid(row=height+2, column=0, columnspan=width, sticky=E+W+N+S)
    
    checked = []
    used = []
    
    def end():
        sounds('end')
        menu_button['fg'] = '#172a3a'
        menu_button['bg'] = 'white'
        
        def reset():
            main.destroy()
            sounds('start')
            start()
        
        Button(main, image=photo_reset, bg='white', fg='black', command=reset).grid(row=height+2, column=width-1, sticky=E+W+N+S)
        
        for item in field.keys():
            if item not in used:
                if field[item] == -1:
                    Button(main, bg='white', image=photo_bomb, state=DISABLED, font=small_font).grid(row=item[0], column=item[1], sticky=E+W+S+N)
                elif field[item]:
                    Button(main, text=field[item], bg='white', state=DISABLED, font=small_font).grid(row=item[0], column=item[1], sticky=E+W)
                else:
                    Button(main, bg='white', state=DISABLED, font=small_font).grid(row=item[0], column=item[1], sticky=E+W)
    
    def findzero(i, j):
        if field[(i, j)]:
            used.append((i, j))
            checked.append((i, j))
            
            Button(main, text=field[(i, j)], bg='#09bc8a', state=DISABLED, font=small_font).grid(row=i, column=j, sticky=E+W)
            return
        elif (i, j) in checked:
            return
        
        used.append((i, j))
        checked.append((i, j))
        Button(main, bg='#D0CDD7', state=DISABLED, font=small_font).grid(row=i, column=j, sticky=E+W)
        
        if i > 0:
            findzero(i-1, j)
        if i < height-1:
            findzero(i+1, j)
        if j > 0:
            findzero(i, j-1)
        if j < width-1:
            findzero(i, j+1)
        if i > 0 and j > 0:
            findzero(i-1, j-1)
        if i > 0 and j < width-1:
            findzero(i-1, j+1)
        if i < height-1 and j > 0:
            findzero(i+1, j-1)
        if i < height-1 and j < width-1:
            findzero(i+1, j+1)
    
    def play(row, col):
        nonlocal flag, pl1, pl2
        
        if field[(row, col)] == -1:
            used.append((row, col))
            
            Button(main, bg=pl1_color if flag else pl2_color, image=photo_bomb, state=DISABLED, padx=20, font=small_font).grid(row=row, column=col, sticky=E+W+S+N)
            
            if flag:
                pl1 += 1
            else:
                pl2 += 1
            
            if pl1 != bombs_num//2 + 1 and pl2 != bombs_num//2 + 1:
                sounds('bomb')
        elif field[(row, col)]:
            flag = not flag
            used.append((row, col))
            sounds('miss')
            
            Button(main, text=field[(row, col)], bg='#09bc8a', state=DISABLED, font=small_font).grid(row=row, column=col, sticky=E+W)
        else:
            flag = not flag
            
            sounds('miss')
            checked.clear()
            findzero(row, col)
        
        if flag:
            pl1_label['text'] = pl1
            switch_label['bg'] = pl1_color
        else:
            pl2_label['text'] = pl2
            switch_label['bg'] = pl2_color
        
        if pl1 == bombs_num//2 + 1 or pl2 == bombs_num//2 + 1:
            end()
            switch_label['text'] = '{}  Won!'.format(pl1_color.title() if flag else pl2_color.title())
            return main.mainloop()

# =======================================================

menu()