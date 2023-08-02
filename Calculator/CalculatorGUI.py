from customtkinter import *
from PIL import Image

# set_appearance_mode('dark')
set_default_color_theme('calculator_custom_theme.json')

# Window setup

root = CTk()
root.title('Calculator App')
root.iconbitmap('C:\PythonProjectsWasiG\GUI Python\Calculator\Calculator Icon.ico')
root.geometry('360x500')

# Custom Font

my_font = CTkFont(size=25)

# Input Field

Placeholder = CTkEntry(root, width=35, font=my_font, justify='right')
Placeholder.grid(row=0, column=0, columnspan=4, padx=3, pady=3, sticky='nsew')
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


# Night Mode Switch
mode_frame = CTkFrame(root, width=30, height=20, fg_color='#343638')
mode_frame.place(x=10, y=8, anchor='nw')

mode_var = IntVar()


def night_mode_func():
    if mode_var.get() == 1:
        set_appearance_mode('light')
        mode_frame.configure(fg_color='#F9F9FA')
    else:
        set_appearance_mode('dark')
        mode_frame.configure(fg_color='#343638')


mode_switch = CTkSwitch(mode_frame, variable=mode_var, command=night_mode_func, text='', width=30, switch_width=40,
                        onvalue=1, offvalue=0)
mode_switch.pack()

print(mode_var.get())


# Clear Button:

def clear_button_func():
    Placeholder.delete(0, END)


clr_button = CTkButton(root, text='CLR', width=32, height=20, command=clear_button_func, font=my_font)
clr_button.grid(row=1, column=0, sticky='nsew', padx=3, pady=3)


# Positive/Negative Button:

def posneg_button_func():
    global fpsng_num
    if float(Placeholder.get()) >= 0:
        Placeholder.insert(0, '-')
    else:
        Placeholder.delete(0, 1)


posneg_button = CTkButton(root, text='+/-', width=34, height=20, command=posneg_button_func, font=my_font)
posneg_button.grid(row=1, column=1, sticky='nsew', padx=3, pady=3)


# Power Button:

def power_button_func():
    first_num = Placeholder.get()
    global fp_num
    fp_num = first_num
    Placeholder.delete(0, END)


power_button = CTkButton(root, text='xʸ', width=40, height=20, font=my_font, command=power_button_func)
power_button.grid(row=1, column=2, sticky='nsew', padx=3, pady=3)


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
            num_button = CTkButton(root, text=str(i), command=le_lambda_func(i), font=my_font, width=40, height=20)
            num_button.grid(row=row, column=column, sticky='nsew', padx=3, pady=3)

        else:
            num_button = CTkButton(root, text='0', command=le_lambda_func(0), font=my_font, width=88, height=20)
            num_button.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=3, pady=3)

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


div_button = CTkButton(root, text='÷', command=div_button_func, font=my_font, width=41, height=20)
div_button.grid(row=1, column=3, sticky='nsew', padx=3, pady=3)


# Multiply Button:

def mult_button_func():
    first_num = Placeholder.get()
    global fm_num
    fm_num = first_num
    Placeholder.delete(0, END)


mult_button = CTkButton(root, text='X', width=41, height=20, command=mult_button_func, font=my_font)
mult_button.grid(row=2, column=3, sticky='nsew', padx=3, pady=3)


# Subtract Button:

def subtract_button_func():
    first_num = Placeholder.get()
    global fs_num
    fs_num = first_num
    Placeholder.delete(0, END)


sub_button = CTkButton(root, text='-', command=subtract_button_func, font=my_font, width=41, height=20)
sub_button.grid(row=3, column=3, sticky='nsew', padx=3, pady=3)


# Add Button:

def add_button_func():
    first_num = Placeholder.get()
    global f_num
    f_num = first_num
    Placeholder.delete(0, END)


add_button = CTkButton(root, text='+', command=add_button_func, font=my_font, width=39, height=20)
add_button.grid(row=4, column=3, sticky='nsew', padx=3, pady=3)


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


equal_button = CTkButton(root, text='=', command=equal_button_function, font=my_font, width=41, height=20)
equal_button.grid(row=5, column=3, columnspan=3, sticky='nsew', padx=3, pady=3)

# Decimal Button:

decimal_dot_img = CTkImage(light_image=Image.open('Decimal_icon.png'), dark_image=Image.open('Decimal_icon_white.png'))


def dot_button_func():
    Placeholder.insert(Placeholder.get(), '.')


dot_button = CTkButton(root, command=dot_button_func, width=41, height=20, image=decimal_dot_img, text='')
dot_button.grid(row=5, column=2, sticky='nsew', padx=3, pady=3)

# Making window dynamically resizeable

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
