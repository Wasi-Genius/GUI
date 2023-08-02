# My Old Calculator using original tkinter!

from tkinter import *

root = Tk()
root.title('Calculator App')
root.iconbitmap('C:\PythonProjectsWasiG\GUI Python\Calculator\Calculator Icon.ico')

# Input Field

Placeholder = Entry(root, width=35, borderwidth=5, font=20)
Placeholder.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
f_num = ''
fs_num = ''
fm_num = ''
fd_num = ''
fpsng_num = ''
fp_num = ''


def button_on_screen(num):
    current = Placeholder.get()
    Placeholder.delete(0, END)
    Placeholder.insert(0, str(current) + str(num))


# Clear Button:

def clear_button_func():
    Placeholder.delete(0, END)


clr_button = Button(root, text='CLR', padx=32, pady=20, command=clear_button_func, font=20)
clr_button.grid(row=1, column=0, sticky='nsew')


# Positive/Negative Button:

def posneg_button_func():
    global fpsng_num
    if float(Placeholder.get()) >= 0:
        Placeholder.insert(0, '-')
    else:
        Placeholder.delete(0, 1)


posneg_button = Button(root, text='+/-', padx=34, pady=20, command=posneg_button_func, font=20)
posneg_button.grid(row=1, column=1, sticky='nsew')


# Power Button:

def power_button_func():
    first_num = Placeholder.get()
    global fp_num
    fp_num = first_num
    Placeholder.delete(0, END)


power_button = Button(root, text='xʸ', padx=38, pady=20, command=power_button_func, font=20)
power_button.grid(row=1, column=2, sticky='nsew')


# Number Buttons

def buttons_with_num(num_of_buttons):
    i = 0
    row = 4
    column = 0

    def le_lambda_func(n):
        return lambda: button_on_screen(n)

    while i <= num_of_buttons:
        i += 1
        if i != 10:
            num_button = Button(root, text=i, padx=40, pady=20, command=le_lambda_func(i), font=20)
            num_button.grid(row=row, column=column, sticky='nsew')

        else:
            num_button = Button(root, text='0', padx=88, pady=20, command=le_lambda_func(0), font=20)
            num_button.grid(row=5, column=0, columnspan=2, sticky='nsew')

        column += 1
        if column >= 3:
            row -= 1
            column = 0


buttons_with_num(9)


# Division Button:

def div_button_func():
    first_num = Placeholder.get()
    global fd_num
    fd_num = first_num
    Placeholder.delete(0, END)


div_button = Button(root, text='÷', padx=41, pady=20, command=div_button_func, font=20)
div_button.grid(row=1, column=3, sticky='nsew')


# Multiply Button:

def mult_button_func():
    first_num = Placeholder.get()
    global fm_num
    fm_num = first_num
    Placeholder.delete(0, END)


mult_button = Button(root, text='X', padx=41, pady=20, command=mult_button_func, font=20)
mult_button.grid(row=2, column=3, sticky='nsew')


# Subtract Button:

def subtract_button_func():
    first_num = Placeholder.get()
    global fs_num
    fs_num = first_num
    Placeholder.delete(0, END)


sub_button = Button(root, text='-', padx=41, pady=20, command=subtract_button_func, font=20)
sub_button.grid(row=3, column=3, sticky='nsew')


# Add Button:

def add_button_func():
    first_num = Placeholder.get()
    global f_num
    f_num = first_num
    Placeholder.delete(0, END)


add_button = Button(root, text='+', padx=39, pady=20, command=add_button_func, font=20)
add_button.grid(row=4, column=3, sticky='nsew')


# Equal Button:

def equal_button_function():
    s_num = Placeholder.get()

    global f_num, fm_num, fs_num, fd_num, fp_num

    if len(f_num) != 0:
        result = float(s_num) + float(f_num)
    elif len(fs_num) != 0:
        result = float(fs_num) - float(s_num)
    elif len(fm_num) != 0:
        result = float(s_num) * float(fm_num)
    elif len(fd_num) != 0:
        result = float(fd_num) / float(s_num)
    elif len(fp_num) != 0:
        result = float(fp_num) ** float(s_num)

    f_num, fm_num, fs_num, fd_num, fp_num = '', '', '', '', ''
    Placeholder.delete(0, END)
    if result.is_integer():
        result = int(result)
    Placeholder.insert(0, str(result))


equal_button = Button(root, text='=', padx=41, pady=20, command=equal_button_function, font=20)
equal_button.grid(row=5, column=3, columnspan=3, sticky='nsew')


# Decimal Button:

def dot_button_func():
    Placeholder.insert(Placeholder.get(), '.')


dot_button = Button(root, text='.', padx=41, pady=20, command=dot_button_func, font=20)
dot_button.grid(row=5, column=2, sticky='nsew')

# Making window automatically resizeable

root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)
root.rowconfigure(index=3, weight=1)
root.rowconfigure(index=4, weight=1)
root.rowconfigure(index=5, weight=1)

root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.columnconfigure(index=3, weight=1)

root.mainloop()
