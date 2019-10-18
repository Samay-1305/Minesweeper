from tkinter import *
from random import randint as rnd
import time

size = (9,9)
num = 10
window = Tk()
window.title("Minesweeper")
window.configure(bg="white")
btn_cmd = "= Button(fm, font = font, width = 8, height = 4, bd = 2)"
lbl_cmd = "= Label(fm, text = txt, font = font, width = 8, height = 4, bd = 2, bg = b_clr, fg = 'black')"
bnd_cmd_r = ".bind(r_click, r_cmd)"
bnd_cmd_l = ".bind(l_click, l_cmd)"
grd_cmd = ".grid(column=i, row=j)"
r_click = "<Button-1>"
l_click = "<Button-3>"
font = ("Times",10,"bold")

def refresh():
    global lost, rem_grid, rem_mines, running, window, status_map
    font = ("Times",30,"bold")
    fn = ("Helvetia", 25, "bold", "italic")
    rem_grid = 0
    for i in status_map:
        for j in i:
            if j == "_":
                rem_grid += 1
    clr = "black"
    s_txt = ""
    if lost:
        s_txt = "You Lose :( "
        clr = "red"
        running = False
    elif rem_grid == 0:
        s_txt = "You Win :) "
        clr = "green"
        running = False
    r_txt = "Remaining: " + str(rem_mines)
    s_lbl = Label(window, text = s_txt,  font = font, width = 11, height = 2, bd = 2, bg = "white", fg = clr)
    s_lbl.grid(column = 1, row = 6)
    r_lbl = Label(window, text = r_txt,  font = fn, width = 12, height = 2, bd = 2, bg = "white", fg = clr)
    r_lbl.grid(column = 1, row = 2)
    window.update()
    if not(running):
        finish(lost)

def new_game():
    font = ("Times",30,"bold")
    t_lbl = Label(window, text = "     ",  font = font, width = 11, height = 2, bd = 2, bg = "white")
    t_lbl.grid(column = 1, row = 0)
    fm.destroy()
    main()
    
def finish(lost = False):
    global start_time, mines_list
    if lost:
        b_clr = "red"
        for each in mines_list:
            i = each%size[0]
            j = each//size[1]
            var = chr(65+i) + str(j)
            txt = "X"
            exec(var + lbl_cmd)
            exec(var + grd_cmd)
    font = ("Times",30,"bold")
    end_time = int(time.time())
    dt = end_time - start_time
    t_txt = " Time: " + str(dt)
    t_lbl = Label(window, text = t_txt,  font = font, width = 11, height = 2, bd = 2, bg = "white")
    t_lbl.grid(column = 1, row = 0)
    window.update()

def left_click(event, var):
    global status_map, ref_map, size, lost, rem_mines, rem_grid, clicks, start_time
    if clicks == 0:
        start_time = int(time.time())
    clicks += 1
    cell_row = int(var[1:])
    cell_col = int(ord(var[0])) - 65
    if status_map[cell_row][cell_col] == "_":
        val = str(ref_map[cell_row][cell_col])
        status_map[cell_row][cell_col] = val
        i, j = cell_col, cell_row
        if ref_map[cell_row][cell_col] == "M":
            lost = True
            b_clr = "red"
            txt = "X"
        else:      
            b_clr = "white"
            txt = val
            if txt == " ":
                sur_check(var)
        exec(var + lbl_cmd)
        exec(var + grd_cmd)
        refresh()
        
def right_click(event, var, var_exe = None):
    global status_map, ref_map, size, lost, rem_mines, rem_grid, clicks, start_time
    if clicks == 0:
        start_time = int(time.time())
    clicks += 1
    clrs = ["SystemButtonFace","light grey"]
    cell_row = int(var[1:])
    cell_col = int(ord(var[0])) - 65
    val = str(status_map[cell_row][cell_col])
    if val == "D":
        rem_mines += 1
        status_map[cell_row][cell_col] = "_"
        clr = clrs[0]
    elif val == "_":
        rem_mines -= 1
        status_map[cell_row][cell_col] = "D"
        clr = clrs[1]
    i, j = cell_col, cell_row
    var_exe.configure(bg=clr)
    window.update()
    refresh()

def sur_check(var):
    global status_map, ref_map, size, lost
    update_list = []
    cell_row = int(var[1:])
    cell_col = int(ord(var[0])) - 65
    cond = "(i >= 0 and i < size[0]) and (j >= 0 and j < size[1])"
    for w in [(1,1), (-1,1), (1,-1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1)]:
        i = cell_row
        j = cell_col
        while eval(cond):
            val = ref_map[i][j]
            col = chr(65 + j)
            vr = col + str(i)
            update_list.append(vr)
            if val != " ":
                break
            i += w[0]
            j += w[1]
    for each in update_list:
        left_click(None, each)   

def create_grid(size, num):
    grid = []
    for j in range(size[1]):
        row = []
        for i in range(size[0]):
            row.append("_")
        grid.append(row)
    return grid

def reference_grid(grid, size, num):
    mines = []
    while len(mines) < num:
        val = rnd(0, (size[0]*size[1]-1))
        if val not in mines:
            mines.append(val)
    for each in mines:
        col = each%size[0]
        row = each//size[1]
        grid[row][col] = "M"
    for j in range(size[1]):
        for i in range(size[0]):
            num = 0
            cur = grid[j][i]
            check = [(j,i-1), (j,i+1), (j-1,i), (j+1,i), (j-1,i-1), (j-1,i+1), (j+1,i-1), (j+1,i+1)]
            if cur != "M":
                for each in check:
                    x, y = each
                    if (x >= 0 and x < size[1]) and (y >= 0 and y < size[0]):
                        if grid[x][y] == "M":
                            num += 1
                txt = " "
                if num != 0:
                    txt = str(num)
                grid[j][i] = txt
    return (grid, mines)

def main():
    global clicks, rem_mines, fm, status_map, ref_map, window, lost, running, mines_list
    running = True
    rem_mines  = num
    clicks = 0
    rem_grid = size[0]*size[1] - 10
    fm = Frame(window)
    fm.grid(row=0, column=0, rowspan = 9)
    status_map = create_grid(size, num)
    ref_map = create_grid(size, num)
    ref_map, mines_list = reference_grid(ref_map, size, num)
    lost = False
    for j in range(size[1]):
        for i in range(size[0]):
            col = chr(65+i)
            row = str(j)
            var_name = col+row
            exec(var_name + btn_cmd)
            r_cmd = lambda event, var=var_name: left_click(event, var)
            l_cmd = lambda event, var=var_name, var_exe=eval(var_name): right_click(event, var, var_exe)
            exec(var_name + bnd_cmd_l)
            exec(var_name + bnd_cmd_r)
            exec(var_name + grd_cmd)
    l1 = Label(window, width = 40, bg = "white")
    l1.grid(column = 1, row = 0)
    fn = ("Helvetia", 25, "bold", "italic")
    refresh()
    r_txt = "Remaining: " + str(rem_mines)
    n_btn = Button(window, font = fn, text= "New Game", width = 11, height = 2, bd = 3, bg = "#8BABFA", command = new_game)
    n_btn.grid(row = 8, column = 1)
    window.mainloop()

if __name__ == '__main__':
    main()
        
