from customtkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from tkinter import Image
from PIL import Image
import os
from send2trash import send2trash as trash

# Setting up GUI

set_default_color_theme('dark-blue')
root = CTk()
root.title('Image Viewer')
root.iconbitmap(
    'C:\PythonProjectsWasiG\GUI Python\ImageViewerEditor\ImageViewerIcon.ico')
root.after(1, root.wm_state, 'zoomed')

# Making window dynamically resizeable

root.rowconfigure(index=0, weight=1)

root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)

##############################################

# Photo Frame Creation

photo_frame = CTkFrame(root)
photo_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

photo_frame.rowconfigure(index=0, weight=1)

photo_frame.columnconfigure(index=0, weight=1)

#############################################

# The Tool Sidebar

tool_frame = CTkFrame(root)
tool_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

tool_frame.rowconfigure(index=0, weight=1)
tool_frame.rowconfigure(index=1, weight=1)
tool_frame.rowconfigure(index=2, weight=1)
tool_frame.rowconfigure(index=3, weight=1)
tool_frame.rowconfigure(index=4, weight=1)

tool_frame.columnconfigure(index=0, weight=1)


# File Manager Button


# ---- Finding the best image size for button placement
def optimal_image_size(image, rotate):
    if image.width > 1000 and image.height > 700:
        if rotate:
            image = (500, 600)
        else:
            image = (800, 500)
        return image
    if image.width > 1000 and image.height < 700:
        if rotate:
            image = (image.height, 600)
        else:
            image = (800, image.height)
        return image
    if image.height > 700 and image.width < 1000:
        if rotate:
            image = (500, image.width)
        else:
            image = (image.width, 500)
        return image
    if image.width <= 1000 and image.height <= 700:
        if rotate:
            image = (image.height, image.width)
        else:
            image = (image.width, image.height)
        return image


# ----- Creating the Image

# ----------- Global variable to check if the image was created
is_image_created = False
is_image_rotated = False

# ----------- Global variable to get the optimal_image_size

optimal_image_size_var = None
optimal_image_size_var_rotate = None


# noinspection PyGlobalUndefined
def file_button_func():
    global opening_image, photo_label, image_file, photo, i, is_image_created, is_image_rotated, optimal_image_size_var, optimal_image_size_var_rotate
    i = 0
    filetypes = (
        ('All Files', '*'),
        ('JPG', '*.jpg'),
        ('PNG', '*.png'),
    )
    image_file = fd.askopenfilename(title='Please open an image', initialdir='/',
                                    filetypes=filetypes)

    # ------- Photo placement

    opening_image = Image.open(image_file)
    photo = CTkImage(dark_image=opening_image, size=optimal_image_size(opening_image, False))

    try:
        photo_label.destroy()
    except NameError:
        pass

    optimal_image_size_var = optimal_image_size(opening_image, False)
    optimal_image_size_var_rotate = optimal_image_size(opening_image, True)

    photo_label = CTkLabel(photo_frame, image=photo, text='')
    photo_label.grid(row=0, column=0, sticky='nsew')

    is_image_created = True
    is_image_rotated = False


file_button = CTkButton(tool_frame, text='File Manager', command=file_button_func)
file_button.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

# ----- Rotate Image Button
i = 0
rotate_label = None
false_rotation_size = None


# noinspection PyGlobalUndefined
def rotate_button_func():
    global i, rotate_label, rotated_image, photo_label, is_image_created, is_image_rotated, false_rotation_size

    if not is_image_created:
        ms.showerror('No Image to Rotate', 'No image was found to rotate, please open an image.')

    if rotate_label is not None:
        photo_label.destroy()
        rotate_label.destroy()

    if i == 0:
        rotated_image = CTkImage(opening_image.transpose(Image.ROTATE_90),
                                 size=optimal_image_size(opening_image, True))
        i += 1
    elif i == 1:
        rotated_image = CTkImage(opening_image.transpose(Image.ROTATE_180),
                                 size=optimal_image_size(opening_image, False))
        false_rotation_size = True
        i += 1
    elif i == 2:
        rotated_image = CTkImage(opening_image.transpose(Image.ROTATE_270),
                                 size=optimal_image_size(opening_image, True))
        i += 1
    else:
        rotated_image = CTkImage(opening_image, size=optimal_image_size(opening_image, False))
        false_rotation_size = True
        i = 0

    rotate_label = CTkLabel(photo_frame, image=rotated_image, text='')
    photo_label.destroy()
    rotate_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    is_image_rotated = True


rotate_button = CTkButton(tool_frame, text='Rotate Image', command=rotate_button_func)
rotate_button.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)


# ----- Delete Image Button


# noinspection PyGlobalUndefined
def delete_image_func():
    answer = ms.askyesno('Photo Deletion', 'Are you sure you want to delete this file?')
    if answer:
        if os.path.exists(image_file):
            trash_path = image_file.replace("/", "\\")
            trash(trash_path)

            photo_label.destroy()
            # noinspection PyUnresolvedReferences
            rotate_label.destroy()

            ms.showinfo('File Deletion Success', 'Your file was deleted successfully')

        else:
            ms.showerror('No Image Found', "Your image was not found, please try again!")
    else:
        return


delete_image_button = CTkButton(tool_frame, text='Delete Image', command=delete_image_func)
delete_image_button.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)


# ------- Finding the optimal size for full screen images
def optimal_fullscreen_size(image, rotate):
    if image.width > 1910 and image.height > 1070:
        if rotate:
            image = (1100, 700)
        else:
            image = (1300, 700)
        return image
    if image.width > 1910 and image.height < 1070:
        if rotate:
            image = (image.height, 700)
        else:
            image = (1300, image.height)
        return image
    if image.height > 1070 and image.width < 1910:
        if rotate:
            image = (1100, 700)
        else:
            image = (image.width, 700)
        return image
    if image.width <= 1910 and image.height <= 1070:
        if rotate:
            image = (1100, 700)
        else:
            image = (1200, image.height)
        return image


# ------- Enter Full Screen Button
# noinspection PyGlobalUndefined,PyUnresolvedReferences
def enter_full_screen_func():
    try:
        if photo_frame.winfo_children():
            global rotated_image, rotate_label

            image_preview_frame.grid_forget()
            tool_frame.grid_forget()

            root.after(1, root.wm_attributes, '-fullscreen', True)

            new_photo = CTkImage(opening_image, size=optimal_fullscreen_size(opening_image, False))
            photo_label.configure(image=new_photo, width=1920, height=1080)

            try:
                if rotate_label.winfo_children():
                    photo_label.grid_forget()
                    rotated_image.configure(size=optimal_fullscreen_size(opening_image, True))
                    rotate_label.configure(image=rotated_image)
            except AttributeError:
                pass

        else:
            ms.showwarning('No Image', 'An image is needed to go into full screen, please choose an image!')
    except _tkinter.TclError:
        pass


enter_fullscreen_button = CTkButton(tool_frame, text='Full Screen', command=enter_full_screen_func)
enter_fullscreen_button.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)


# ------ Exiting full screen
# noinspection PyGlobalUndefined,PyUnresolvedReferences,PyUnusedLocal
def exit_full_screen_mode(event=None):
    set_appearance_mode("light")
    root.attributes('-fullscreen', False)
    root.update()
    set_appearance_mode("dark")
    root.update()

    if photo_frame.winfo_children() and rotate_label.winfo_children() == 0:
        try:
            rotate_label.destroy()
        except AttributeError:
            pass

        photo.configure(size=optimal_image_size(opening_image, False))

        photo_label.configure(image=photo, width=600)

        root.update()

    try:
        if rotate_label.winfo_children():
            try:
                photo_label.destroy()
            except AttributeError:
                pass

            rotated_image.configure(size=optimal_image_size(opening_image, True))
            rotate_label.configure(image=rotated_image, width=600)
    except AttributeError:
        pass

    tool_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
    image_preview_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)


root.bind('<KeyPress-Escape>', exit_full_screen_mode)


# noinspection PyGlobalUndefined,PyUnresolvedReferences
def zoom_in():
    global opening_image, zoomed_in_size, is_image_created, is_image_rotated, optimal_image_size_var, optimal_image_size_var_rotate

    if is_image_created or false_rotation_size:
        optimal_image_size_var = tuple(val + 10 for val in optimal_image_size_var)
        photo.configure(size=optimal_image_size_var)
        print(optimal_image_size_var)

    if is_image_rotated and not false_rotation_size:
        optimal_image_size_var_rotate = tuple(val + 10 for val in optimal_image_size_var_rotate)
        rotated_image.configure(size=optimal_image_size_var_rotate)


root.update()

zoom_in_button = CTkButton(tool_frame, text='Zoom In', command=zoom_in)
zoom_in_button.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)

# ------------- Zoom Out Button

#############################################

# The Photo Preview Sidebar

image_preview_frame = CTkFrame(root)
image_preview_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)

##############################################


root.mainloop()
