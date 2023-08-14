from customtkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from tkinter import Image
from PIL import Image
from send2trash import send2trash as trash
import os

# Setting up GUI

set_default_color_theme('dark-blue')
root = CTk()
root.title('Image Viewer')
root.iconbitmap(
    'C:\PythonProjectsWasiG\GUI Python\Image Viewer\ImageViewerIcon.ico')
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
# The Photo Preview Sidebar

image_preview_frame = CTkFrame(root)
image_preview_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)

image_preview_frame.columnconfigure(index=0, weight=1)

image_preview_frame.rowconfigure(index=0, weight=1)
image_preview_frame.rowconfigure(index=1, weight=1)
image_preview_frame.rowconfigure(index=2, weight=1)

##############################################

# The Tool Sidebar

tool_frame = CTkFrame(root)
tool_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

tool_frame.rowconfigure(index=0, weight=1)
tool_frame.rowconfigure(index=1, weight=1)
tool_frame.rowconfigure(index=2, weight=1)
tool_frame.rowconfigure(index=3, weight=1)
tool_frame.rowconfigure(index=4, weight=1)
tool_frame.rowconfigure(index=5, weight=1)

tool_frame.columnconfigure(index=0, weight=1)


# File Manager Button


# ---- Finding the best image size for button placement

# --------- Global variable to see if the image fits in the frame:


def optimal_image_size(image, rotate):
    if rotate:
        if image.width > 1000 and image.height > 700:
            return 800, 600
        elif image.width > 1000 and image.height < 700:
            return image.height, 600
        elif image.height > 700 and image.width < 1000:
            return 800, image.width
        else:
            return image.height, image.width
    else:
        if image.width > 1000 and image.height > 700:
            return 800, 600
        elif image.width > 1000 and image.height < 700:
            return 800, image.height
        elif image.height > 700 and image.width < 1000:
            return image.width, 600
        else:
            return image.width, image.height


# ----- Creating the Image

# ----------- Global variable to check if the image was created
is_image_normal = False
is_image_there = False

# ----------- Global variable to get the optimal_image_size

optimal_image_size_var = None
optimal_image_size_var_rotate = None


# noinspection PyGlobalUndefined
def file_button_func():
    global opening_image, photo_label, image_file, photo, i, is_image_normal, is_image_rotated, optimal_image_size_var, optimal_image_size_var_rotate, is_image_there, rotate_label, current_image, preview_photos, before_image, before_image_label, after_image, after_image_label, after_image_name, before_image_index, dark_before_image_open, dark_after_image_open
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
        rotate_label.destroy()
    except NameError:
        pass

    photo_label = CTkLabel(photo_frame, image=photo, text='')
    photo_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    photo_frame.grid_propagate(True)
    photo_frame.configure(border_width=5, border_color='#1c538b')

    # ---------- Preview Image Development

    directory_list = image_file.split('/')

    optimal_image_size_var = optimal_image_size(opening_image, False)
    optimal_image_size_var_rotate = optimal_image_size(opening_image, True)

    current_image_frame = CTkFrame(image_preview_frame, border_width=5, border_color='#1c538b')
    current_image_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)

    preview_photo = CTkImage(dark_image=opening_image, size=(200, 300))

    current_image = CTkLabel(current_image_frame, text='', image=preview_photo)
    current_image.pack(padx=5, pady=10)

    preview_photos = []
    directory_name = len(directory_list) - 1
    photo_directory = directory_list[:directory_name]
    photo_directory = '/'.join(photo_directory)
    for item in os.listdir(photo_directory):

        if item.endswith((".png", ".jpg")):
            complete_path = photo_directory + '/' + item
            preview_photos.append(complete_path)

    first_image_indicator = preview_photos.index(image_file)

    before_image_index = first_image_indicator - 1

    before_image_name = preview_photos[before_image_index]
    dark_before_image_open = Image.open(before_image_name)

    before_image_frame = CTkFrame(image_preview_frame, border_width=5, border_color='#3b3b3b')
    before_image_frame.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)

    before_image = CTkImage(dark_image=dark_before_image_open, size=(200, 300))

    before_image_label = CTkLabel(before_image_frame, text='', image=before_image)
    before_image_label.pack(padx=5, pady=10)

    after_image_index = first_image_indicator + 1

    try:
        after_image_name = preview_photos[after_image_index]
    except IndexError:
        after_image_name = preview_photos[0]

    after_image_frame = CTkFrame(image_preview_frame, border_width=5, border_color='#3b3b3b')
    after_image_frame.grid(row=2, column=0, sticky='NSEW', padx=5, pady=5)

    dark_after_image_open = Image.open(after_image_name)

    after_image = CTkImage(dark_image=dark_after_image_open, size=(200, 300))

    after_image_label = CTkLabel(after_image_frame, text='', image=after_image)
    after_image_label.pack(padx=5, pady=10)

    # ---------------------------------------

    is_image_normal = True
    is_image_there = True


# Arrow binding:

def up_arrow_function(event=None):
    global preview_photos, current_image, before_image_index, dark_before_image_open, dark_after_image_open

    new_image = CTkImage(dark_image=dark_before_image_open, size=optimal_image_size(dark_before_image_open, False))

    new_image_preview = CTkImage(dark_image=dark_before_image_open, size=(200, 300))

    photo_label.configure(image=new_image)

    current_image.configure(image=new_image_preview)

    try:
        new_dark_before_image_open = Image.open(preview_photos[before_image_index - 1])
        before_image.configure(dark_image=new_dark_before_image_open)
    except IndexError:
        new_dark_before_image_open = Image.open(preview_photos[-1])
        before_image.configure(dark_image=new_dark_before_image_open)

    dark_before_image_open = new_dark_before_image_open

    new_dark_after_image_open = Image.open(preview_photos[before_image_index + 1])

    dark_after_image_open = new_dark_after_image_open

    after_image.configure(dark_image=new_dark_after_image_open)

    before_image_index = before_image_index - 1

    # ---------------------------------------


root.bind('<Up>', up_arrow_function)
root.update()

file_button = CTkButton(tool_frame, text='File Manager', command=file_button_func)
file_button.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

# ----- Rotate Image Button
i = 0
false_rotation_size = False
is_image_rotated = False
degree_image = None


def rotate_button_func():
    global i, rotate_label, rotated_image, photo_label, is_image_normal, is_image_rotated, false_rotation_size, is_image_there, degree_image

    if not is_image_there:
        ms.showerror('No Image to Rotate', 'No image was found to rotate, please open an image.')

    else:

        if not is_image_normal:
            photo_label.destroy()
            rotate_label.destroy()

        if i == 0:
            degree_image = opening_image.transpose(Image.ROTATE_90)
            rotated_image = CTkImage(opening_image.transpose(Image.ROTATE_90),
                                     size=optimal_image_size(opening_image, True))
            is_image_rotated = True
            i += 1

        elif i == 1:
            degree_image = opening_image.transpose(Image.ROTATE_180)
            rotated_image = CTkImage(opening_image.transpose(Image.ROTATE_180),
                                     size=optimal_image_size(opening_image, False))
            is_image_rotated = False
            false_rotation_size = True
            i += 1

        elif i == 2:
            degree_image = opening_image.transpose(Image.ROTATE_270)
            rotated_image = CTkImage(opening_image.transpose(Image.ROTATE_270),
                                     size=optimal_image_size(opening_image, True))
            is_image_rotated = True
            i += 1

        else:
            degree_image = opening_image
            rotated_image = CTkImage(opening_image, size=optimal_image_size(opening_image, False))
            is_image_rotated = False
            false_rotation_size = True
            i = 0

        rotate_label = CTkLabel(photo_frame, image=rotated_image, text='')
        photo_label.destroy()
        rotate_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        is_image_normal = False


rotate_button = CTkButton(tool_frame, text='Rotate Image', command=rotate_button_func)
rotate_button.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)


# ----- Delete Image Button


def delete_image_func():
    global is_image_there
    answer = ms.askyesno('Photo Deletion', 'Are you sure you want to delete this file?')
    if answer:
        if is_image_there:
            trash_path = image_file.replace("/", "\\")
            trash(trash_path)

            try:
                photo_label.destroy()
                rotate_label.destroy()
            except NameError:
                pass

            is_image_there = False

            ms.showinfo('File Deletion Success', 'Your file was deleted successfully')

        else:
            ms.showerror('No Image Found', "Your image was not found, please try again!")
    else:
        return


delete_image_button = CTkButton(tool_frame, text='Delete Image', command=delete_image_func)
delete_image_button.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)


# ------- Finding the optimal size for full screen images
def optimal_fullscreen_size(image):
    if image.width > 1910 and image.height > 1070:
        return 1300, 700
    elif image.width > 1910 and image.height < 1070:
        return 1300, image.height
    elif image.height > 1070 and image.width < 1910:
        return image.width, 700
    else:
        return 1200, image.height


in_full_screen = False


# ------- Enter Full Screen Button
def enter_full_screen_func():
    global is_image_normal, rotated_image, rotate_label, is_image_rotated, in_full_screen, false_rotation_size, degree_image
    if is_image_there:
        image_preview_frame.grid_forget()
        tool_frame.grid_forget()
        root.after(1, root.wm_attributes, '-fullscreen', True)

        if is_image_normal:
            new_fullscreen_image = CTkImage(opening_image, size=optimal_fullscreen_size(opening_image))
            photo_label.configure(image=new_fullscreen_image)

        else:
            new_fullscreen_image = CTkImage(degree_image, size=optimal_fullscreen_size(opening_image))
            rotate_label.configure(image=new_fullscreen_image)

    else:
        ms.showwarning('No Image', 'An image is needed to go into full screen, please choose an image!')

    in_full_screen = True


enter_fullscreen_button = CTkButton(tool_frame, text='Full Screen', command=enter_full_screen_func)
enter_fullscreen_button.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)


# ------ Exiting full screen
def exit_full_screen_mode(event=None):
    global in_full_screen, is_image_normal, degree_image
    if in_full_screen:
        set_appearance_mode("light")
        root.attributes('-fullscreen', False)
        set_appearance_mode("dark")

        if is_image_normal:

            try:
                rotate_label.destroy()
            except NameError:
                pass

            photo.configure(size=optimal_image_size(opening_image, False))
            photo_label.configure(image=photo, width=500)

        else:
            photo_label.destroy()
            if false_rotation_size:
                new_fullscreen_image = CTkImage(degree_image, size=optimal_image_size(degree_image, False))
            else:
                new_fullscreen_image = CTkImage(degree_image, size=optimal_image_size(degree_image, True))
            rotate_label.configure(image=new_fullscreen_image, width=500)

        tool_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        image_preview_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)

    else:
        pass


root.bind('<KeyPress-Escape>', exit_full_screen_mode)


# ---------- Zoom in Button


def zoom_in():
    global is_image_normal, is_image_rotated, optimal_image_size_var, optimal_image_size_var_rotate, is_image_there
    if is_image_there:
        photo_frame.grid_propagate(False)
        try:
            if is_image_rotated:
                optimal_image_size_var_rotate = tuple(val + 40 for val in optimal_image_size_var_rotate)
                rotated_image.configure(size=optimal_image_size_var_rotate)

            else:
                optimal_image_size_var = tuple(val + 40 for val in optimal_image_size_var)
                if is_image_normal:
                    photo.configure(size=optimal_image_size_var)
                rotated_image.configure(size=optimal_image_size_var)
        except NameError:
            pass
    else:
        ms.showerror('No Image Found', 'No image was found, please try again.')


zoom_in_button = CTkButton(tool_frame, text='Zoom In', command=zoom_in)
zoom_in_button.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)

repeat_zoom = None


def start_zoom_in(_):
    global is_image_there, repeat_zoom
    if is_image_there:
        repeat_zoom = root.after(100, repeat_zoom_in)
    else:
        pass


def repeat_zoom_in():
    zoom_in()
    global repeat_zoom
    repeat_zoom = root.after(100, repeat_zoom_in)


def stop_zoom_in(_):
    global repeat_zoom
    if repeat_zoom is not None:
        root.after_cancel(repeat_zoom)
        repeat_zoom = None


zoom_in_button.bind("<Button-1>", start_zoom_in)
zoom_in_button.bind("<ButtonRelease-1>", stop_zoom_in)


# ------------- Zoom Out Button


def zoom_out():
    global is_image_normal, is_image_rotated, optimal_image_size_var, optimal_image_size_var_rotate, is_image_there
    if is_image_there:
        photo_frame.grid_propagate(False)
        try:
            if is_image_rotated:
                optimal_image_size_var_rotate = tuple(val - 40 for val in optimal_image_size_var_rotate)
                rotated_image.configure(size=optimal_image_size_var_rotate)

            else:
                optimal_image_size_var = tuple(val - 40 for val in optimal_image_size_var)
                if is_image_normal:
                    photo.configure(size=optimal_image_size_var)
                rotated_image.configure(size=optimal_image_size_var)
        except NameError:
            pass
    else:
        ms.showerror('No Image Found', 'No image was found, please try again.')


second_repeat_zoom = None


def start_zoom_out(_):
    global second_repeat_zoom, is_image_there
    if is_image_there:
        second_repeat_zoom = root.after(100, repeat_zoom_out)
    else:
        pass


def repeat_zoom_out():
    zoom_out()
    global second_repeat_zoom
    second_repeat_zoom = root.after(100, repeat_zoom_out)


def stop_zoom_out(_):
    global second_repeat_zoom
    if second_repeat_zoom is not None:
        root.after_cancel(second_repeat_zoom)
        second_repeat_zoom = None


zoom_out_button = CTkButton(tool_frame, text='Zoom Out', command=zoom_out)
zoom_out_button.grid(row=5, column=0, sticky='nsew', padx=5, pady=5)

zoom_out_button.bind("<Button-1>", start_zoom_out)
zoom_out_button.bind("<ButtonRelease-1>", stop_zoom_out)

#########################################################################

# Bugs:
# - After you zoom in and zoom out, the full screen image isn't the correct size and if when you come out of full screen you cannot zoom back in or zoom out.
# - Zoom in and Zoom out dont work when you use the arrow bindings!

# To Do:
# - Bind the up and down arrow keys to go through the images
# - - Maybe also have arrow icons on the screen (top and bottom of the photo frame, if rotated to the side of the image, top and bottom) that users can click on to go through the images.
# - - The arrows appear for a second when users click on the arrow keys or when they hover over them with their mouse, they disappear a moment later.

# - Glamify everything (add icons etc)

# - Calculate the perfect sizes for any computer screen size?
# - Optimize everything, try to get the number of code you have down.

root.mainloop()
