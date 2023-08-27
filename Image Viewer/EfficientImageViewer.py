# Import Statements
from customtkinter import CTkFrame, CTkLabel, CTkImage, CTk, CTkButton, set_default_color_theme, set_appearance_mode
from tkinter import filedialog as fd, messagebox as ms
from PIL import Image
from send2trash import send2trash as trash
import os

'''
To Do:

- Work on Full Screen Class


'''

'''
Bugs:

- Make rotate function work with delete function / vice versa (it only rotates the first image you open)
- When you try to delete from three images to two images, the before image and the current image are the same (focus on the current_image???) 


Bugs I couldn't fix:

- When you delete the first image in the folder and try to go up using the up arrow, the preview images will go out of order. But if you click up again, the images will fix themselves. If you click the up arrow key a second time, the images will move  normally.

'''

######################################

# Set up default color theme.
set_default_color_theme('dark-blue')


######################################

# Finding the best image size
def optimal_image_size(image):
    max_width = 800
    max_height = 600

    target_width = max_width if image.width > max_width else image.width
    target_height = max_height if image.height > max_height else image.height

    return target_width, target_height


######################################

# Main Window Class
class RootWindow:
    def __init__(self, num_rows, num_columns):
        self.root = CTk()
        self.configure_rows_and_columns(num_rows, num_columns, self.root)

    @staticmethod
    def configure_rows_and_columns(num_rows, num_columns, widget):
        # Adjusting Rows
        for row_index in range(num_rows):
            widget.rowconfigure(index=row_index, weight=1)

        # Adjusting Columns
        for col_index in range(num_columns):
            widget.columnconfigure(index=col_index, weight=1)

    def window_title(self, title):
        try:
            self.root.title(title)
        except ValueError:
            print("Error: Title must be a string.")
        return self

    def window_icon(self, icon_path):
        try:
            self.root.iconbitmap(icon_path)
        except ValueError:
            print("Error: Invalid icon path.")
        return self

    def maximize_window(self):
        self.root.after(1, self.root.wm_state, 'zoomed')
        return self

    def modify_window_fullscreen(self, make_fullscreen):
        try:
            if make_fullscreen:
                self.root.after(1, self.root.wm_attributes, '-fullscreen', make_fullscreen)

            else:
                set_appearance_mode('light')
                self.root.attributes('-fullscreen', make_fullscreen)
                set_appearance_mode('dark')

        except ValueError:
            print('Error: Only True or False accepted.')
        return self

    def update_window(self):
        self.root.update()
        return self

    def schedule_window_updates(self, delay, function_to_delay):
        value = self.root.after(delay, function_to_delay)
        return value

    def stop_window_updates(self, function_to_stop):
        self.root.after_cancel(function_to_stop)
        return self

    def get_screen_measurements(self):
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        return width, height

    def create_window_binding(self, key, function):
        self.root.bind(key, function)
        return self

    def create_root_loop(self):
        self.root.mainloop()
        return self


# Main Window Instance
main_window_manager = RootWindow(num_rows=1, num_columns=3).window_title('Image Viewer').window_icon(
    'C:\PythonProjectsWasiG\GUI Python\Image Viewer\ImageViewerIcon.ico').maximize_window()


######################################

# Photo Frame Class
class PhotoFrame:
    def __init__(self, master, num_rows, num_columns):
        self.master = master
        self.photo_frame = None
        self.create_photo_frame()
        self.photo_frame_border(True)
        main_window_manager.configure_rows_and_columns(num_rows, num_columns, self.photo_frame)

    def create_photo_frame(self):
        self.photo_frame = CTkFrame(main_window_manager.root)
        self.photo_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        return self

    def modify_photo_frame_propagation(self, choice):
        try:
            self.photo_frame.grid_propagate(choice)
        except ValueError:
            print('Error: Only True or False accepted.')
        return self

    def photo_frame_border(self, create):
        try:
            if create:
                self.photo_frame.configure(border_width=5, border_color='#1c538b')
            else:
                self.photo_frame.configure(border_width=0)

        except ValueError:
            print('Error: Only True or False accepted.')
        return self


# Photo Frame Instance
photo_frame_manager = PhotoFrame(main_window_manager.root, 1, 1)


######################################

# Photo Label Class
class PhotoLabel:
    def __init__(self, master):
        self.master = master
        self.photo_label = None

    def create_photo_label(self, photo_on_screen):
        self.photo_label = CTkLabel(photo_frame_manager.photo_frame, image=photo_on_screen, text='')
        self.photo_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    def change_photo_label_photo(self, new_image):
        self.photo_label.configure(image=new_image)

    def pack_photo_label(self):
        self.photo_label.pack(fill='both', expand=True)

    def grid_photo_label(self):
        self.photo_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)


# Photo Label Instance
photo_label_manager = PhotoLabel(master=photo_frame_manager.photo_frame)


######################################

# Photo Preview Sidebar Class
class PhotoPreviewSidebar:
    def __init__(self, master):
        self.master = master
        self.image_preview_frame = None

    def create_image_preview_frame(self, num_rows, num_columns):
        self.image_preview_frame = CTkFrame(self.master)
        self.image_preview_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)
        main_window_manager.configure_rows_and_columns(num_rows, num_columns, self.image_preview_frame)
        return self

    def forget_image_preview_frame(self):
        self.image_preview_frame.grid_forget()
        return self

    def destroy_image_preview_frame(self):
        self.image_preview_frame.destroy()
        return self


# Photo Preview Sidebar Instance
photo_preview_bar_manager = PhotoPreviewSidebar(main_window_manager.root)


######################################

# Tool Sidebar Class
class ToolSidebar:
    def __init__(self, master, num_rows, num_columns):
        self.master = master
        self.tool_frame = None
        self.create_tool_sidebar()
        main_window_manager.configure_rows_and_columns(num_rows, num_columns, self.tool_frame)

    def create_tool_sidebar(self):
        self.tool_frame = CTkFrame(self.master)
        self.tool_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        return self

    def grid_tool_sidebar(self):
        self.tool_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        return self

    def forget_tool_sidebar(self):
        self.tool_frame.grid_forget()
        return self


# Tool Sidebar Instance
tool_sidebar_manager = ToolSidebar(main_window_manager.root, num_rows=6, num_columns=1)


######################################

# File Handler Class
class FileHandler:
    def __init__(self):
        self.image_open = None
        self.image_file_name = None
        self.optimal_image_size_var = None
        self.photo = 0

    def opening_image_file(self):
        try:
            filetypes = (
                ('All Files', '*'),
                ('JPG', '*.jpg'),
                ('PNG', '*.png'),
            )

            self.image_file_name = fd.askopenfilename(title='Please open an image', initialdir='/',
                                                      filetypes=filetypes)

            self.image_open = Image.open(self.image_file_name)

            self.optimal_image_size_var = optimal_image_size(self.image_open)

            self.photo = CTkImage(self.image_open, size=optimal_image_size(self.image_open))

            return self

        except AttributeError:
            print('No file selected')


# File Handler Instance
file_handler_manager = FileHandler()


######################################

# Image Placer Class

class ImagePlacer:
    def __init__(self, master):
        self.master = master

        self.has_image_ever_been_rotated = False
        self.is_image_there = False

        self.rotation_state = 0

        self.preview_photos = None
        self.selected_preview_image_index = None
        self.num_of_photos = None

    @staticmethod
    def photo_placement(photo_to_use):
        photo_label_manager.create_photo_label(photo_to_use)

    def preview_bar_initialization(self):

        directory_list = file_handler_manager.image_file_name.split('/')

        photo_preview_bar_manager.create_image_preview_frame(num_rows=3, num_columns=1)

        preview_photo = CTkImage(dark_image=file_handler_manager.image_open, size=(200, 300))

        current_image_manager.create_current_image(master=photo_preview_bar_manager.image_preview_frame,
                                                   preview_photo=preview_photo)

        self.preview_photos = []
        self.num_of_photos = 0
        directory_name = len(directory_list) - 1
        photo_directory = directory_list[:directory_name]
        photo_directory = '/'.join(photo_directory)
        for item in os.listdir(photo_directory):
            if item.endswith((".png", ".jpg")):
                complete_path = photo_directory + '/' + item
                self.preview_photos.append(complete_path)
                self.num_of_photos += 1

        self.selected_preview_image_index = self.preview_photos.index(file_handler_manager.image_file_name)

        if self.num_of_photos >= 3:
            before_image_manager.create_before_image_requirements(self.selected_preview_image_index,
                                                                  self.preview_photos,
                                                                  photo_preview_bar_manager.image_preview_frame)
            after_image_manager.create_after_image_requirements(self.selected_preview_image_index, self.preview_photos,
                                                                photo_preview_bar_manager.image_preview_frame)

        elif self.num_of_photos == 2:
            after_image_manager.destroy_after_image_frame()
            before_image_manager.create_before_image_requirements(self.selected_preview_image_index,
                                                                  self.preview_photos,
                                                                  photo_preview_bar_manager.image_preview_frame)
        else:
            after_image_manager.destroy_after_image_frame()
            before_image_manager.destroy_before_image()
            current_image_manager.current_image_frame.pack()
            print('Only One Image Found')

    def file_handler_button_function(self):

        try:
            if photo_label_manager.photo_label is not None:
                photo_label_manager.photo_label.destroy()

            if rotate_image_manager.rotate_label is not None:
                rotate_image_manager.rotate_label.destroy()

        except NameError:
            pass

        file_handler_manager.opening_image_file()
        self.photo_placement(file_handler_manager.photo)
        self.preview_bar_initialization()

        self.has_image_ever_been_rotated = True
        self.is_image_there = True


# Image Placer Instance
image_placer_manager = ImagePlacer(main_window_manager.root)


######################################

# Before Image Class

class BeforeImageOrganization:
    def __init__(self):
        self.dark_before_image_open = None
        self.before_image_exists = False

        self.before_image_frame = None
        self.before_image_label = None
        self.before_image = None
        self.before_image_name = None
        self.before_image_index = None

    def create_before_image_requirements(self, current_image_index, list_of_photos, frame_root):
        self.before_image_index = current_image_index - 1

        self.before_image_name = list_of_photos[self.before_image_index]
        self.dark_before_image_open = Image.open(self.before_image_name)

        self.before_image_frame = CTkFrame(frame_root, border_width=5, border_color='#3b3b3b')
        self.before_image_frame.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)

        self.before_image = CTkImage(dark_image=self.dark_before_image_open, size=(200, 300))

        self.before_image_label = CTkLabel(self.before_image_frame, text='', image=self.before_image)
        self.before_image_label.pack(padx=5, pady=10)

        self.before_image_exists = True

        return self

    def destroy_before_image(self):
        if self.before_image_label:
            self.before_image_label.destroy()
            self.before_image_exists = False

            return self


# Before Image Instance
before_image_manager = BeforeImageOrganization()


######################################

# After Image Class
class AfterImageOrganization:
    def __init__(self):

        self.dark_after_image_open = None
        self.after_image_exists = None

        self.after_image_frame = None
        self.after_image_label = None
        self.after_image = None
        self.after_image_name = None
        self.after_image_index = None

    def create_after_image_requirements(self, current_image_index, list_of_photos, frame_root):

        self.after_image_index = current_image_index + 1

        try:
            self.after_image_name = list_of_photos[self.after_image_index]
        except IndexError:
            self.after_image_name = list_of_photos[0]

        self.after_image_frame = CTkFrame(frame_root, border_width=5, border_color='#3b3b3b')
        self.after_image_frame.grid(row=2, column=0, sticky='NSEW', padx=5, pady=5)

        self.dark_after_image_open = Image.open(self.after_image_name)

        self.after_image = CTkImage(dark_image=self.dark_after_image_open, size=(200, 300))

        self.after_image_label = CTkLabel(self.after_image_frame, text='', image=self.after_image)
        self.after_image_label.pack(padx=5, pady=10)

        self.after_image_exists = True

        return self

    def destroy_after_image_frame(self):
        if self.after_image_label:
            self.after_image_frame.destroy()
            self.after_image_exists = False

            return self


# After Image Instance
after_image_manager = AfterImageOrganization()


######################################

# Current Image Class
class CurrentImageOrganization:
    def __init__(self):
        self.current_image_frame = None
        self.current_image = None

    def create_current_image(self, preview_photo, master):
        self.current_image_frame = CTkFrame(master, border_width=5,
                                            border_color='#1c538b')
        self.current_image_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)

        self.current_image = CTkLabel(self.current_image_frame, text='', image=preview_photo)
        self.current_image.pack(padx=5, pady=10)

        return self

    def destroy_current_image_frame(self):
        if self.current_image:
            self.current_image_frame.destroy()

            return self


# Current Image Instance
current_image_manager = CurrentImageOrganization()

######################################

# File Button Initialization

file_button = CTkButton(tool_sidebar_manager.tool_frame, text='File Manager',
                        command=image_placer_manager.file_handler_button_function)
file_button.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)


######################################

class UpArrow:
    def __init__(self):
        self.arrow_use_indicator = False
        self.up_arrow_use_indicator = False
        self.pre_image_file_deletion = False

    def up_arrow_button_func(self):
        if before_image_manager.before_image_exists:

            self.arrow_use_indicator = True
            self.up_arrow_use_indicator = True
            image_placer_manager.rotation_state = 0

            pass

        else:
            print('Only One Image Detected.')
            return self


######################################

# Rotate Image Class

class RotationHandler:
    def __init__(self):

        self.false_rotation = False
        self.is_image_rotated = False
        self.degree_image = None
        self.rotate_label = None
        self.rotated_image = None

    def rotation_button_func(self):
        if not image_placer_manager.is_image_there:
            ms.showerror('No Image to Rotate', 'No image to rotate. Please open an image.')

        else:
            self.destroy_previous_image()
            self.create_rotated_image(photo_frame_manager.photo_frame, self.rotate_image())

        return self

    def destroy_previous_image(self):

        if not image_placer_manager.has_image_ever_been_rotated:
            photo_label_manager.photo_label.destroy()
            self.rotate_label.destroy()

        return self

    def rotate_image(self):

        if image_placer_manager.rotation_state == 0:

            self.degree_image = file_handler_manager.image_open.transpose(Image.ROTATE_90)

            # if arrow_use_indicator:
            #     self.degree_image = selected_preview_image_open.transpose(Image.ROTATE_90)

            self.is_image_rotated = True
            image_placer_manager.rotation_state += 1

        elif image_placer_manager.rotation_state == 1:
            self.degree_image = file_handler_manager.image_open.transpose(Image.ROTATE_180)

            # if arrow_use_indicator:
            #     self.degree_image = selected_preview_image_open.transpose(Image.ROTATE_180)

            self.is_image_rotated = False
            self.false_rotation = True
            image_placer_manager.rotation_state += 1

        elif image_placer_manager.rotation_state == 2:
            self.degree_image = file_handler_manager.image_open.transpose(Image.ROTATE_270)

            # if arrow_use_indicator:
            #     self.degree_image = selected_preview_image_open.transpose(Image.ROTATE_270)

            self.is_image_rotated = True
            image_placer_manager.rotation_state += 1

        else:
            self.degree_image = file_handler_manager.image_open

            # if arrow_use_indicator:
            #     self.degree_image = selected_preview_image_open

            self.is_image_rotated = False
            self.false_rotation = True
            image_placer_manager.rotation_state = 0

        self.rotated_image = CTkImage(self.degree_image, size=optimal_image_size(file_handler_manager.image_open))

        return self.rotated_image

    def create_rotated_image(self, master, image):

        photo_label_manager.photo_label.destroy()
        self.rotate_label = CTkLabel(master, image=image, text='')
        self.rotate_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        image_placer_manager.has_image_ever_been_rotated = False

        return self


# Rotate Image Instance

rotate_image_manager = RotationHandler()

######################################


# Rotate Button Initialization

rotate_button = CTkButton(tool_sidebar_manager.tool_frame, text='Rotate Image',
                          command=rotate_image_manager.rotation_button_func)
rotate_button.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

######################################

# Arrow binding:

pre_image_file_deletion = False

# ----- Arrow button rotation indicators
arrow_use_indicator = False
up_arrow_use_indicator = False
down_arrow_use_indicator = False


# ---- Up Arrow Binding
def up_arrow_function(event=None):
    global preview_photos, before_image_index, after_image_index, dark_before_image_open, dark_after_image_open, before_image_name, pre_image_file_name, pre_image_file_deletion, selected_preview_image_index, is_image_there, arrow_use_indicator, i, selected_preview_image_open, is_image_normal, up_arrow_use_indicator, new_up_image, rotated_image, num_of_photos, before_image_exists, degree_image, optimal_image_size_var

    if before_image_exists:
        is_image_there = True
        arrow_use_indicator = True
        up_arrow_use_indicator = True
        optimal_image_size_var = optimal_image_size(opening_image)

        i = 0

        selected_preview_image_index -= 1
        selected_preview_image_open = dark_before_image_open
        degree_image = dark_before_image_open
        rotated_image = CTkImage(selected_preview_image_open,
                                 size=optimal_image_size(selected_preview_image_open))

        if selected_preview_image_index < 0:
            selected_preview_image_index = len(preview_photos) - 1

        pre_image_file_name = preview_photos[selected_preview_image_index]

        new_up_image = CTkImage(dark_image=dark_before_image_open,
                                size=optimal_image_size(dark_before_image_open))

        new_image_preview = CTkImage(dark_image=dark_before_image_open, size=(200, 300))

        if is_image_normal:
            photo_label.configure(image=new_up_image)
        else:
            rotate_label.configure(image=new_up_image)

        current_image.configure(image=new_image_preview)

        pre_image_file_deletion = True

        if num_of_photos >= 3:

            before_image_index = selected_preview_image_index - 1
            after_image_index = selected_preview_image_index + 1

            if before_image_index < 0:
                before_image_index = len(preview_photos) - 1

            if after_image_index >= len(preview_photos):
                after_image_index = 0

            new_dark_before_image_open = Image.open(preview_photos[before_image_index])
            dark_before_image_open = new_dark_before_image_open
            before_image.configure(dark_image=new_dark_before_image_open)

            new_dark_after_image_open = Image.open(preview_photos[after_image_index])
            dark_after_image_open = new_dark_after_image_open
            after_image.configure(dark_image=new_dark_after_image_open)

            print("Selected Preview Image Index after update:", selected_preview_image_index)
            print("Before Image Index after update:", before_image_index)
            print("After Image Index after update:", after_image_index)

        else:
            before_image_index = selected_preview_image_index - 1

            if before_image_index < 0:
                before_image_index = len(preview_photos) - 1

            new_dark_before_image_open = Image.open(preview_photos[before_image_index])
            dark_before_image_open = new_dark_before_image_open
            before_image.configure(dark_image=new_dark_before_image_open)

    else:
        print('Only one image detected')


main_window_manager.create_window_binding('<Up>', up_arrow_function).update_window()


# ---- Down Arrow Binding
def down_arrow_function(event=None):
    global preview_photos, before_image_index, after_image_index, dark_before_image_open, dark_after_image_open, after_image_name, pre_image_file_name, pre_image_file_deletion, selected_preview_image_index, is_image_there, arrow_use_indicator, i, selected_preview_image_open, is_image_normal, down_arrow_use_indicator, new_down_image, rotated_image, num_of_photos, degree_image, optimal_image_size_var

    if num_of_photos >= 3:
        is_image_there = True
        arrow_use_indicator = True
        down_arrow_use_indicator = True
        optimal_image_size_var = optimal_image_size(opening_image)

        i = 0

        if selected_preview_image_index == len(preview_photos) - 1:
            after_image_index = 0

        selected_preview_image_index = after_image_index
        selected_preview_image_open = dark_after_image_open
        degree_image = dark_after_image_open

        rotated_image = CTkImage(selected_preview_image_open,
                                 size=optimal_image_size(selected_preview_image_open))

        try:
            pre_image_file_name = preview_photos[after_image_index]
        except IndexError:
            pass

        new_down_image = CTkImage(dark_image=dark_after_image_open,
                                  size=optimal_image_size(dark_after_image_open))

        new_image_preview = CTkImage(dark_image=dark_after_image_open, size=(200, 300))

        if is_image_normal:
            photo_label.configure(image=new_down_image)
        else:
            rotate_label.configure(image=new_down_image)

        current_image.configure(image=new_image_preview)

        pre_image_file_deletion = True

        before_image_index += 1
        after_image_index += 1

        if before_image_index >= len(preview_photos):
            before_image_index = 0

        if after_image_index >= len(preview_photos):
            after_image_index = 0

        new_dark_before_image_open = Image.open(preview_photos[before_image_index])
        dark_before_image_open = new_dark_before_image_open
        before_image.configure(dark_image=new_dark_before_image_open)

        new_dark_after_image_open = Image.open(preview_photos[after_image_index])
        dark_after_image_open = new_dark_after_image_open
        after_image.configure(dark_image=new_dark_after_image_open)

        print("Selected Preview Image Index after update:", selected_preview_image_index)
        print("Before Image Index after update:", before_image_index)
        print("After Image Index after update:", after_image_index)

    else:
        print('Down arrow not needed.')


main_window_manager.create_window_binding('<Down>', down_arrow_function).update_window()


######################################

# Delete Image Class

class DeleteImageHandler:
    def __init__(self):
        pass

    def delete_button_func(self):
        if self.ask_for_deletion():
            if image_placer_manager.is_image_there:
                if image_placer_manager.num_of_photos >= 3:
                    self.deletion_of_three_or_more_images()

                elif image_placer_manager.num_of_photos == 2:
                    self.deletion_of_two_images()

                else:
                    self.deletion_of_one_image()

                image_placer_manager.rotation_state = 0

            else:
                ms.showerror('No Image Found', "Your image was not found, please try again!")

        else:
            print("Deletion cancelled.")

        return self

    @staticmethod
    def ask_for_deletion():
        answer = ms.askyesno('Photo Deletion', 'Are you sure you want to delete this file?')

        return answer

    def deletion_of_three_or_more_images(self):
        self.change_current_image()
        self.file_deletion(file_handler_manager.image_file_name)
        self.destroy_labels()
        self.create_new_photo_label()
        self.create_new_before_image()
        image_placer_manager.is_image_there = True
        image_placer_manager.has_image_ever_been_rotated = True

        return self

    def deletion_of_two_images(self):
        self.change_current_image()
        self.file_deletion(file_handler_manager.image_file_name)
        self.destroy_labels()
        self.create_new_photo_label()
        image_placer_manager.is_image_there = True
        image_placer_manager.has_image_ever_been_rotated = True

        return self

    def deletion_of_one_image(self):

        self.file_deletion(file_handler_manager.image_file_name)

        photo_preview_bar_manager.destroy_image_preview_frame()

        if rotate_image_manager.degree_image is not None:
            rotate_label.destroy()
        else:
            photo_label_manager.photo_label.destroy()

        image_placer_manager.is_image_there = False
        image_placer_manager.has_image_ever_been_rotated = False

        return self

    def file_deletion(self, file_path):
        # if pre_image_file_deletion:
        #     trash_path = pre_image_file_name.replace("/", "\\")
        #     trash(trash_path)
        # else:
        #     trash_path = image_file.replace("/", "\\")
        #     trash(trash_path)

        trash_path = file_path.replace("/", "\\")
        trash(trash_path)
        image_placer_manager.num_of_photos -= 1

        image_placer_manager.preview_photos.pop(image_placer_manager.selected_preview_image_index)
        image_placer_manager.selected_preview_image_index = before_image_manager.before_image_index

        file_handler_manager.image_open = Image.open(image_placer_manager.preview_photos[
                                                         before_image_manager.before_image_index])

        try:
            before_image_manager.before_image_index = image_placer_manager.selected_preview_image_index - 1
            after_image_manager.after_image_index = image_placer_manager.selected_preview_image_index + 1

            before_image_manager.before_image_name = image_placer_manager.preview_photos[
                before_image_manager.before_image_index]

            file_handler_manager.image_file_name = image_placer_manager.preview_photos[image_placer_manager.selected_preview_image_index]

        except (TypeError, IndexError):
            print('Only one or two images detected')

        return self

    def destroy_labels(self):
        try:
            photo_label_manager.photo_label.destroy()
            if rotate_image_manager.rotate_label is not None:
                rotate_image_manager.rotate_label.destroy()
            # if image_placer_manager.num_of_photos == 2:
            #     after_image_frame.destroy()
        except NameError:
            print("Label destroy failed.")

        return self

    def change_current_image(self):
        if image_placer_manager.num_of_photos > 3:
            print('I got greater than 3!')
            current_image_manager.current_image.configure(image=before_image_manager.before_image)

        elif image_placer_manager.num_of_photos == 3:
            print('I got equal to 3!')
            # current_image_manager.current_image.configure(image=current_image_manager.current_image)
            after_image_manager.destroy_after_image_frame()

        elif image_placer_manager.num_of_photos == 2:
            print('I got equal to 2!')
            current_image_manager.destroy_current_image_frame()
            before_image_manager.before_image_frame.pack()

        return self

    def create_new_photo_label(self):
        new_photo_label_image = CTkImage(dark_image=before_image_manager.dark_before_image_open,
                                         size=optimal_image_size(before_image_manager.dark_before_image_open))

        photo_label_manager.create_photo_label(new_photo_label_image)

        return self

    def create_new_before_image(self):

        new_before_image_file_name = image_placer_manager.preview_photos[
            image_placer_manager.selected_preview_image_index - 1]

        before_image_manager.dark_before_image_open = Image.open(new_before_image_file_name)

        # selected_preview_image_open = dark_before_image_open

        before_image_manager.before_image = CTkImage(dark_image=before_image_manager.dark_before_image_open,
                                                     size=(200, 300))
        before_image_manager.before_image_label.configure(image=before_image_manager.before_image)

        return self


# Delete Image Instance

delete_image_manager = DeleteImageHandler()

######################################

# Delete Image Button

delete_image_button = CTkButton(tool_sidebar_manager.tool_frame, text='Delete Image',
                                command=delete_image_manager.delete_button_func)
delete_image_button.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)

######################################

# ------- Enter Full Screen Button
in_full_screen = False


def enter_full_screen_func():
    global is_image_normal, rotated_image, rotate_label, is_image_rotated, in_full_screen, false_rotation_size, degree_image, selected_preview_image_open, arrow_use_indicator
    if is_image_there:

        photo_preview_bar_manager.forget_image_preview_frame()
        tool_sidebar_manager.forget_tool_sidebar()
        photo_frame_manager.photo_frame_border(False)
        main_window_manager.modify_window_fullscreen(True)

        if is_image_normal:

            if arrow_use_indicator:
                new_fullscreen_image = CTkImage(selected_preview_image_open,
                                                size=main_window_manager.get_screen_measurements())
            else:
                new_fullscreen_image = CTkImage(opening_image, size=main_window_manager.get_screen_measurements())

            photo_label.configure(image=new_fullscreen_image)
            photo_label.pack(fill="both", expand=True)

        else:
            new_fullscreen_image = CTkImage(degree_image, size=main_window_manager.get_screen_measurements())
            rotate_label.configure(image=new_fullscreen_image)
            rotate_label.pack(fill="both", expand=True)

    else:
        print("No image found, cannot enter full screen.")
        ms.showerror('No Image', 'An image is needed to go into full screen, please choose an image!')

    in_full_screen = True


enter_fullscreen_button = CTkButton(tool_sidebar_manager.tool_frame, text='Full Screen', command=enter_full_screen_func)
enter_fullscreen_button.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)


# ------ Exiting full screen
def exit_full_screen_mode(event=None):
    global in_full_screen, is_image_normal, degree_image, selected_preview_image_open, arrow_use_indicator, optimal_image_size_var

    photo_frame_manager.modify_photo_frame_propagation(True)
    optimal_image_size_var = optimal_image_size(opening_image)

    if in_full_screen:

        photo_frame_manager.photo_frame_border(True)
        main_window_manager.modify_window_fullscreen(False)

        if is_image_normal:

            try:
                rotate_label.destroy()
            except NameError:
                pass

            if arrow_use_indicator:
                new_fullscreen_image = CTkImage(selected_preview_image_open,
                                                size=optimal_image_size(
                                                    selected_preview_image_open))
            else:
                new_fullscreen_image = CTkImage(opening_image,
                                                size=optimal_image_size(opening_image))

            photo_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
            photo_label.configure(image=new_fullscreen_image)

        else:
            photo_label.destroy()
            if false_rotation_size:
                new_fullscreen_image = CTkImage(degree_image,
                                                size=optimal_image_size(degree_image))
            else:
                new_fullscreen_image = CTkImage(degree_image,
                                                size=optimal_image_size(degree_image))

            rotate_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
            rotate_label.configure(image=new_fullscreen_image, width=500)

        tool_sidebar_manager.grid_tool_sidebar()
        photo_preview_bar_manager.image_preview_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)

    else:
        pass


main_window_manager.create_window_binding('<KeyPress-Escape>', exit_full_screen_mode)


# ---------- Zoom in Button


def zoom_in():
    global is_image_normal, is_image_rotated, is_image_there, selected_preview_image_open, up_arrow_use_indicator, down_arrow_use_indicator, new_up_image, new_down_image, optimal_image_size_var
    print("Zooming in...")
    if is_image_there:
        photo_frame_manager.modify_photo_frame_propagation(False)
        try:
            optimal_image_size_var = tuple(val + 40 for val in optimal_image_size_var)

            if is_image_rotated:
                print("Zooming in on rotated image...")
                rotated_image.configure(size=optimal_image_size_var)
                rotate_label.configure(image=rotated_image)

            else:

                print("Zooming in on normal image...")

                if is_image_normal:

                    if up_arrow_use_indicator:
                        new_up_image.configure(size=optimal_image_size_var)
                        photo_label.configure(image=new_up_image)
                        print("Zooming in on up image...")

                    elif down_arrow_use_indicator:
                        new_down_image.configure(size=optimal_image_size_var)
                        photo_label.configure(image=new_down_image)
                        print("Zooming in on down image...")

                    else:
                        print("Zooming in on le normal image...")
                        photo.configure(size=optimal_image_size_var)
                        photo_label.configure(image=photo)
                else:
                    print("Zooming in on the rotate image...")
                    rotated_image.configure(size=optimal_image_size_var)
                    rotate_label.configure(image=rotated_image)
        except NameError:
            pass
    else:
        print("No image found, cannot zoom in.")
        ms.showerror('No Image Found', 'No image was found, please try again.')


zoom_in_button = CTkButton(tool_sidebar_manager.tool_frame, text='Zoom In', command=zoom_in)
zoom_in_button.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)

repeat_zoom = None


def start_zoom_in(_):
    global is_image_there, repeat_zoom
    if is_image_there:
        repeat_zoom = main_window_manager.schedule_window_updates(110, repeat_zoom_in)
    else:
        pass


def repeat_zoom_in():
    zoom_in()
    global repeat_zoom
    repeat_zoom = main_window_manager.schedule_window_updates(110, repeat_zoom_in)


def stop_zoom_in(_):
    global repeat_zoom
    if repeat_zoom is not None:
        main_window_manager.stop_window_updates(repeat_zoom)
        repeat_zoom = None


zoom_in_button.bind("<Button-1>", start_zoom_in)
zoom_in_button.bind("<ButtonRelease-1>", stop_zoom_in)


# ------------- Zoom Out Button


def zoom_out():
    global is_image_normal, is_image_rotated, optimal_image_size_var, is_image_there, up_arrow_use_indicator, down_arrow_use_indicator, new_up_image, new_down_image
    print("Zooming out...")
    if is_image_there:
        photo_frame_manager.modify_photo_frame_propagation(False)
        try:
            optimal_image_size_var = tuple(val - 40 for val in optimal_image_size_var)

            if is_image_rotated:
                print("Zooming out on rotated image...")
                rotated_image.configure(size=optimal_image_size_var)
                rotate_label.configure(image=rotated_image)
            else:
                print("Zooming out on normal image...")

                if is_image_normal:

                    if up_arrow_use_indicator:
                        new_up_image.configure(size=optimal_image_size_var)
                        photo_label.configure(image=new_up_image)
                        print("Zooming in on up image...")

                    elif down_arrow_use_indicator:
                        new_down_image.configure(size=optimal_image_size_var)
                        photo_label.configure(image=new_down_image)
                        print("Zooming in on down image...")

                    else:
                        print("Zooming in on le normal image...")
                        photo.configure(size=optimal_image_size_var)
                        photo_label.configure(image=photo)

                print("Zooming out on the rotate image...")
                rotated_image.configure(size=optimal_image_size_var)
                rotate_label.configure(image=rotated_image)

        except NameError:
            pass
    else:
        print("No image found, cannot zoom out.")
        ms.showerror('No Image Found', 'No image Found')


second_repeat_zoom = None


def start_zoom_out(_):
    global second_repeat_zoom, is_image_there
    if is_image_there:
        second_repeat_zoom = main_window_manager.schedule_window_updates(110, repeat_zoom_out)
    else:
        pass


def repeat_zoom_out():
    zoom_out()
    global second_repeat_zoom
    second_repeat_zoom = main_window_manager.schedule_window_updates(110, repeat_zoom_out)


def stop_zoom_out(_):
    global second_repeat_zoom
    if second_repeat_zoom is not None:
        main_window_manager.stop_window_updates(second_repeat_zoom)
        second_repeat_zoom = None


zoom_out_button = CTkButton(tool_sidebar_manager.tool_frame, text='Zoom Out', command=zoom_out)
zoom_out_button.grid(row=5, column=0, sticky='nsew', padx=5, pady=5)

zoom_out_button.bind("<Button-1>", start_zoom_out)
zoom_out_button.bind("<ButtonRelease-1>", stop_zoom_out)

#########################################################################

main_window_manager.create_root_loop()
