# Import Statements

from customtkinter import CTkFrame, CTkLabel, CTkImage, CTk, CTkButton, set_default_color_theme, set_appearance_mode
from tkinter import filedialog as fd, messagebox as ms, TclError
from PIL import Image
from send2trash import send2trash as trash
import os

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
class RootWindowHandler:
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
                photo_frame_manager.photo_frame_border(True)
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


# Main Window Manager
main_window_manager = RootWindowHandler(num_rows=1, num_columns=3).window_title('Image Viewer').window_icon(
    'C:\PythonProjectsWasiG\GUI Python\Image Viewer\Image_Viewer_Icon.ico').maximize_window()


######################################

# Photo Frame Class
class PhotoFrameHandler:
    def __init__(self, master, num_rows, num_columns):
        self.master = master
        self.photo_frame = None
        self.create_photo_frame()
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


# Photo Frame Manager
photo_frame_manager = PhotoFrameHandler(main_window_manager.root, 1, 1)


######################################

# Photo Label Class
class PhotoLabelHandler:
    def __init__(self, master):
        self.master = master
        self.photo_label = None

    def create_photo_label(self, photo_on_screen):
        try:

            self.photo_label = CTkLabel(photo_frame_manager.photo_frame, image=photo_on_screen, text='')
            self.photo_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        except TclError:
            print('No File Selected')

    def change_photo_label_photo(self, new_image):
        self.photo_label.configure(image=new_image)

    def pack_photo_label(self):
        self.photo_label.pack(fill='both', expand=True)

    def grid_photo_label(self):
        self.photo_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)


# Photo Label Manager
photo_label_manager = PhotoLabelHandler(master=photo_frame_manager.photo_frame)


######################################

# Photo Preview Sidebar Class
class PhotoPreviewSidebarHandler:
    def __init__(self, master):
        self.master = master
        self.photo_preview_bar_frame = None

    def create_image_preview_frame(self, num_rows, num_columns):
        self.photo_preview_bar_frame = CTkFrame(self.master)
        self.photo_preview_bar_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)
        main_window_manager.configure_rows_and_columns(num_rows, num_columns, self.photo_preview_bar_frame)
        return self

    def forget_image_preview_frame(self):
        self.photo_preview_bar_frame.grid_forget()
        return self

    def destroy_image_preview_frame(self):
        self.photo_preview_bar_frame.destroy()
        return self


# Photo Preview Sidebar Manager
photo_preview_bar_manager = PhotoPreviewSidebarHandler(main_window_manager.root)


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


# Tool Sidebar Manager
tool_sidebar_manager = ToolSidebar(main_window_manager.root, num_rows=6, num_columns=1)


######################################

# File Handler Class
class FileHandler:
    def __init__(self):
        self.image_open = None
        self.image_file_name = None
        self.optimal_image_size_var = None
        self.original_image_size = None
        self.photo = None

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

            photo_frame_manager.photo_frame_border(True)

            self.optimal_image_size_var = optimal_image_size(self.image_open)

            self.original_image_size = optimal_image_size(self.image_open)

            self.photo = CTkImage(self.image_open, size=optimal_image_size(self.image_open))

            rotate_image_manager.is_image_rotated = False
            rotate_image_manager.false_rotation = False
            image_placer_manager.rotation_state = 0

            return self

        except AttributeError:
            print('No file selected')


# File Handler Manager
file_handler_manager = FileHandler()


######################################

# Image Placer Class

class ImagePlacerHandler:
    def __init__(self, master):
        self.master = master

        self.has_image_ever_been_rotated = False
        self.is_image_there = False

        self.rotation_state = 0

        self.list_of_preview_photos = None
        self.preview_photo = None
        self.selected_preview_image_index = None
        self.num_of_photos = None
        self.first_photo_in_directory = False

    def photo_placement(self, photo_to_use):
        photo_label_manager.create_photo_label(photo_to_use)
        return self

    def preview_bar_initialization(self):
        if file_handler_manager.image_file_name:
            directory_list = file_handler_manager.image_file_name.split('/')

            if not full_screen_manager.went_into_full_screen_once:
                photo_preview_bar_manager.create_image_preview_frame(num_rows=3, num_columns=1)

            self.preview_photo = CTkImage(dark_image=file_handler_manager.image_open, size=(200, 300))

            current_image_manager.create_current_image(master=photo_preview_bar_manager.photo_preview_bar_frame,
                                                       preview_photo=self.preview_photo)

            self.list_of_preview_photos = []
            self.num_of_photos = 0
            directory_name = len(directory_list) - 1
            photo_directory = directory_list[:directory_name]
            photo_directory = '/'.join(photo_directory)
            for item in os.listdir(photo_directory):
                if item.endswith((".png", ".jpg")):
                    complete_path = photo_directory + '/' + item
                    self.list_of_preview_photos.append(complete_path)
                    self.num_of_photos += 1

            self.selected_preview_image_index = self.list_of_preview_photos.index(file_handler_manager.image_file_name)

            if self.selected_preview_image_index == 0:
                self.first_photo_in_directory = True

            if self.num_of_photos >= 3:
                before_image_manager.create_before_image_requirements(self.selected_preview_image_index,
                                                                      self.list_of_preview_photos,
                                                                      photo_preview_bar_manager.photo_preview_bar_frame)
                after_image_manager.create_after_image_requirements(self.selected_preview_image_index,
                                                                    self.list_of_preview_photos,
                                                                    photo_preview_bar_manager.photo_preview_bar_frame)

            elif self.num_of_photos == 2:
                after_image_manager.destroy_after_image_frame()
                before_image_manager.create_before_image_requirements(self.selected_preview_image_index,
                                                                      self.list_of_preview_photos,
                                                                      photo_preview_bar_manager.photo_preview_bar_frame)
            else:
                after_image_manager.destroy_after_image_frame()
                before_image_manager.destroy_before_image()
                current_image_manager.current_image_frame.pack()
                print('Only One Image Found')
        else:
            print('No file selected.')

    def file_button_function(self):

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


# Image Placer Manager
image_placer_manager = ImagePlacerHandler(main_window_manager.root)


######################################

# Before Image Class

class BeforeImageHandler:
    def __init__(self):
        self.dark_before_image_open = None
        self.before_image_exists = False

        self.before_image_frame = None
        self.before_image_label = None
        self.before_image = None
        self.before_image_name = None
        self.before_image_index = None

    def create_before_image_requirements(self, current_image_index, list_of_photos, frame_root):
        self.create_before_image_frame(frame_root)
        self.create_before_image(current_image_index, list_of_photos)
        self.create_before_image_label()

        self.before_image_exists = True

        return self

    def destroy_before_image(self):
        if self.before_image_label:
            self.before_image_label.destroy()
            self.before_image_exists = False

            return self

    def create_before_image(self, current_image_index, list_of_photos):
        self.before_image_index = current_image_index - 1

        self.before_image_name = list_of_photos[self.before_image_index]
        self.dark_before_image_open = Image.open(self.before_image_name)

        self.before_image = CTkImage(dark_image=self.dark_before_image_open, size=(200, 300))

        return self

    def create_before_image_frame(self, frame_root):
        self.before_image_frame = CTkFrame(frame_root, border_width=5, border_color='#3b3b3b')
        self.before_image_frame.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)
        return self

    def create_before_image_label(self):
        self.before_image_label = CTkLabel(self.before_image_frame, text='', image=self.before_image)
        self.before_image_label.pack(padx=5, pady=10)

        return self


# Before Image Manager
before_image_manager = BeforeImageHandler()


######################################

# After Image Class
class AfterImageHandler:
    def __init__(self):

        self.dark_after_image_open = None
        self.after_image_exists = None

        self.after_image_frame = None
        self.after_image_label = None
        self.after_image = None
        self.after_image_name = None
        self.after_image_index = None

    def create_after_image_requirements(self, current_image_index, list_of_photos, frame_root):

        self.create_after_image_frame(frame_root)
        self.create_after_image(current_image_index, list_of_photos)
        self.create_after_image_label()

        self.after_image_exists = True

        return self

    def create_after_image(self, current_image_index, list_of_photos):
        self.after_image_index = current_image_index + 1

        try:
            self.after_image_name = list_of_photos[self.after_image_index]
        except IndexError:
            self.after_image_name = list_of_photos[0]

        self.dark_after_image_open = Image.open(self.after_image_name)

        self.after_image = CTkImage(dark_image=self.dark_after_image_open, size=(200, 300))

        return self

    def create_after_image_label(self):

        self.after_image_label = CTkLabel(self.after_image_frame, text='', image=self.after_image)
        self.after_image_label.pack(padx=5, pady=10)

        return self

    def create_after_image_frame(self, frame_root):

        self.after_image_frame = CTkFrame(frame_root, border_width=5, border_color='#3b3b3b')
        self.after_image_frame.grid(row=2, column=0, sticky='NSEW', padx=5, pady=5)

        return self

    def destroy_after_image_frame(self):
        if self.after_image_label:
            self.after_image_frame.destroy()
            self.after_image_exists = False

            return self


# After Image Manager
after_image_manager = AfterImageHandler()


######################################

# Current Image Class
class CurrentImageHandler:
    def __init__(self):
        self.current_image_frame = None
        self.current_image_label = None

    def create_current_image(self, preview_photo, master):
        self.current_image_frame = CTkFrame(master, border_width=5,
                                            border_color='#1c538b')
        self.current_image_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)

        self.current_image_label = CTkLabel(self.current_image_frame, text='', image=preview_photo)
        self.current_image_label.pack(padx=5, pady=10)

        return self

    def destroy_current_image_frame(self):
        if self.current_image_label:
            self.current_image_frame.destroy()

            return self


# Current Image Manager
current_image_manager = CurrentImageHandler()

######################################

# File Button Button

file_button_icon_open = Image.open('C:\PythonProjectsWasiG\GUI Python\Image Viewer\File_Explorer_Icon.ico')
file_button_icon_image = CTkImage(dark_image=file_button_icon_open, size=(64, 64))
file_button = CTkButton(tool_sidebar_manager.tool_frame, text='',
                        command=image_placer_manager.file_button_function, image=file_button_icon_image)
file_button.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)


######################################

# Up Arrow Class

class UpArrowHandler:
    def __init__(self):
        self.up_arrow_use_indicator = False
        self.new_up_label_image = None

    def up_arrow_button_func(self, event=None):
        if image_placer_manager.num_of_photos > 1 and not full_screen_manager.in_full_screen:

            self.up_arrow_use_indicator = True
            image_placer_manager.rotation_state = 0
            file_handler_manager.optimal_image_size_var = file_handler_manager.original_image_size

            self.change_after_image()

            self.change_current_image()

            image_placer_manager.selected_preview_image_index -= 1
            if image_placer_manager.selected_preview_image_index < 0:
                image_placer_manager.selected_preview_image_index = len(image_placer_manager.list_of_preview_photos) - 1

            self.change_before_image()

            down_arrow_manager.down_arrow_use_indicator = False

        else:
            print('Cannot use arrow function.')
            return self

    def change_before_image(self):
        if image_placer_manager.num_of_photos > 1:
            before_image_manager.before_image_name = image_placer_manager.list_of_preview_photos[
                image_placer_manager.selected_preview_image_index - 1]
            before_image_manager.dark_before_image_open = Image.open(before_image_manager.before_image_name)
            before_image_manager.before_image.configure(dark_image=before_image_manager.dark_before_image_open)
            before_image_manager.before_image_label.configure(image=before_image_manager.before_image)

        return self

    def change_current_image(self):
        if image_placer_manager.num_of_photos > 1:
            old_before_image = CTkImage(dark_image=before_image_manager.dark_before_image_open, size=(200, 300))

            if down_arrow_manager.down_arrow_use_indicator:
                before_image_manager.before_image_name = image_placer_manager.list_of_preview_photos[
                    image_placer_manager.selected_preview_image_index - 1]
                before_image_manager.dark_before_image_open = Image.open(before_image_manager.before_image_name)
                old_before_image = CTkImage(dark_image=before_image_manager.dark_before_image_open, size=(200, 300))

            file_handler_manager.image_open = before_image_manager.dark_before_image_open
            current_image_manager.current_image_label.configure(image=old_before_image)

            self.new_up_label_image = CTkImage(dark_image=before_image_manager.dark_before_image_open,
                                               size=optimal_image_size(before_image_manager.dark_before_image_open))

            if rotate_image_manager.is_image_rotated or rotate_image_manager.false_rotation:
                rotate_image_manager.rotate_label.configure(image=self.new_up_label_image)
            else:
                photo_label_manager.photo_label.configure(image=self.new_up_label_image)

        return self

    def change_after_image(self):

        if image_placer_manager.num_of_photos > 2:
            file_handler_manager.image_open = Image.open(image_placer_manager.list_of_preview_photos[
                                                             image_placer_manager.selected_preview_image_index])
            old_current_image = CTkImage(dark_image=file_handler_manager.image_open, size=(200, 300))
            after_image_manager.after_image_label.configure(image=old_current_image)

        return self


# Up Arrow Manager

up_arrow_manager = UpArrowHandler()

######################################

# Up Arrow Binding

main_window_manager.create_window_binding('<Up>', up_arrow_manager.up_arrow_button_func).update_window()


######################################

# Down Arrow Class


class DownArrowHandler:
    def __init__(self):
        self.down_arrow_use_indicator = False
        self.new_down_label_image = None

    def down_arrow_button_func(self, event=None):
        if image_placer_manager.num_of_photos > 1 and not full_screen_manager.in_full_screen:

            self.down_arrow_use_indicator = True
            image_placer_manager.rotation_state = 0
            file_handler_manager.optimal_image_size_var = file_handler_manager.original_image_size
            final_index_of_image_list = len(image_placer_manager.list_of_preview_photos) - 1

            self.change_before_image()

            old_current_image_index = image_placer_manager.selected_preview_image_index

            self.change_current_image()

            image_placer_manager.selected_preview_image_index += 1
            if image_placer_manager.selected_preview_image_index >= final_index_of_image_list:
                image_placer_manager.selected_preview_image_index = -1

            new_current_image_index = image_placer_manager.selected_preview_image_index

            if old_current_image_index == final_index_of_image_list and new_current_image_index == -1:
                image_placer_manager.selected_preview_image_index = 0

            new_current_image_index = image_placer_manager.selected_preview_image_index

            self.change_after_image()

            up_arrow_manager.up_arrow_use_indicator = False

        else:
            print('Cannot use arrow function.')
            return self

    def change_before_image(self):
        if image_placer_manager.num_of_photos > 1:
            file_handler_manager.image_open = Image.open(image_placer_manager.list_of_preview_photos[
                                                             image_placer_manager.selected_preview_image_index])
            old_current_image = CTkImage(dark_image=file_handler_manager.image_open, size=(200, 300))
            before_image_manager.before_image_label.configure(image=old_current_image)

        return self

    def change_current_image(self):
        if image_placer_manager.num_of_photos > 1:
            old_after_image = CTkImage(dark_image=after_image_manager.dark_after_image_open, size=(200, 300))

            if up_arrow_manager.up_arrow_use_indicator:

                if image_placer_manager.selected_preview_image_index == len(
                        image_placer_manager.list_of_preview_photos) - 1:
                    image_placer_manager.selected_preview_image_index = -1

                after_image_manager.after_image_name = image_placer_manager.list_of_preview_photos[
                    image_placer_manager.selected_preview_image_index + 1]
                after_image_manager.dark_after_image_open = Image.open(after_image_manager.after_image_name)
                old_after_image = CTkImage(dark_image=after_image_manager.dark_after_image_open, size=(200, 300))

            file_handler_manager.image_open = after_image_manager.dark_after_image_open
            current_image_manager.current_image_label.configure(image=old_after_image)

            self.new_down_label_image = CTkImage(dark_image=after_image_manager.dark_after_image_open,
                                                 size=optimal_image_size(after_image_manager.dark_after_image_open))

            if rotate_image_manager.is_image_rotated or rotate_image_manager.false_rotation:
                rotate_image_manager.rotate_label.configure(image=self.new_down_label_image)
            else:
                photo_label_manager.photo_label.configure(image=self.new_down_label_image)

        return self

    def change_after_image(self):

        if image_placer_manager.num_of_photos > 2:
            after_image_manager.after_image_name = image_placer_manager.list_of_preview_photos[
                image_placer_manager.selected_preview_image_index + 1]
            after_image_manager.dark_after_image_open = Image.open(after_image_manager.after_image_name)
            after_image_manager.after_image.configure(dark_image=after_image_manager.dark_after_image_open)
            after_image_manager.after_image_label.configure(image=after_image_manager.after_image)

        return self


# Down Arrow Manager

down_arrow_manager = DownArrowHandler()

######################################

# ---- Down Arrow Binding

main_window_manager.create_window_binding('<Down>', down_arrow_manager.down_arrow_button_func).update_window()


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
            file_handler_manager.optimal_image_size_var = file_handler_manager.original_image_size
            self.destroy_previous_image()
            self.create_rotated_image(photo_frame_manager.photo_frame, self.rotate_image())

        return self

    def destroy_previous_image(self):

        if not image_placer_manager.has_image_ever_been_rotated:
            photo_label_manager.photo_label.destroy()
            self.rotate_label.destroy()

        return self

    def rotate_image(self):

        file_handler_manager.image_open = Image.open(
            image_placer_manager.list_of_preview_photos[image_placer_manager.selected_preview_image_index])

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


# Rotate Image Manager

rotate_image_manager = RotationHandler()

######################################

# Rotate Button Button

rotate_icon_open = Image.open(r'C:\PythonProjectsWasiG\GUI Python\Image Viewer\rotate_icon.ico')
rotate_icon_image = CTkImage(dark_image=rotate_icon_open, size=(64, 64))
rotate_button = CTkButton(tool_sidebar_manager.tool_frame, text='', image=rotate_icon_image,
                          command=rotate_image_manager.rotation_button_func)
rotate_button.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)


######################################

# Delete Image Class

class DeleteImageHandler:

    def delete_button_func(self):
        if self.ask_for_deletion():
            if image_placer_manager.is_image_there:

                file_handler_manager.optimal_image_size_var = file_handler_manager.original_image_size

                if image_placer_manager.num_of_photos >= 3:
                    self.deletion_of_three_or_more_images()

                elif image_placer_manager.num_of_photos == 2:
                    self.deletion_of_two_images()

                else:
                    self.deletion_of_one_image()

                image_placer_manager.rotation_state = 0

                ms.showinfo('File Deletion Success', 'Your file was deleted successfully')

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
        self.file_deletion()
        self.destroy_labels()
        self.create_new_photo_label()
        self.create_new_before_image()
        image_placer_manager.is_image_there = True
        image_placer_manager.has_image_ever_been_rotated = True

        return self

    def deletion_of_two_images(self):
        self.change_current_image()
        self.file_deletion()
        self.destroy_labels()
        self.create_new_photo_label()
        image_placer_manager.is_image_there = True
        image_placer_manager.has_image_ever_been_rotated = True

        return self

    def deletion_of_one_image(self):

        self.file_deletion()

        photo_preview_bar_manager.destroy_image_preview_frame()

        self.destroy_labels()

        image_placer_manager.is_image_there = False
        image_placer_manager.has_image_ever_been_rotated = False

        return self

    def file_deletion(self):
        # if pre_image_file_deletion:
        #     trash_path = pre_image_file_name.replace("/", "\\")
        #     trash(trash_path)
        # else:
        #     trash_path = image_file.replace("/", "\\")
        #     trash(trash_path)

        file_path = image_placer_manager.list_of_preview_photos.pop(image_placer_manager.selected_preview_image_index)

        trash_path = file_path.replace("/", "\\")
        trash(trash_path)
        image_placer_manager.num_of_photos -= 1

        image_placer_manager.selected_preview_image_index = before_image_manager.before_image_index

        if image_placer_manager.first_photo_in_directory:
            image_placer_manager.selected_preview_image_index = len(image_placer_manager.list_of_preview_photos) - 1
            image_placer_manager.first_photo_in_directory = False

        try:
            file_handler_manager.image_open = Image.open(image_placer_manager.list_of_preview_photos[
                                                             before_image_manager.before_image_index])
            file_handler_manager.image_open.close()

            before_image_manager.before_image_index = image_placer_manager.selected_preview_image_index - 1
            after_image_manager.after_image_index = image_placer_manager.selected_preview_image_index + 1

        except (TypeError, IndexError):
            print('Only one or two images detected')

        return self

    def destroy_labels(self):
        try:
            if rotate_image_manager.rotate_label is not None or rotate_image_manager.degree_image is not None:
                rotate_image_manager.rotate_label.destroy()
            else:
                photo_label_manager.photo_label.destroy()
        except NameError:
            print("Label destroy failed.")

        return self

    def change_current_image(self):
        if image_placer_manager.num_of_photos > 3:
            current_image_manager.current_image_label.configure(image=before_image_manager.before_image)

        elif image_placer_manager.num_of_photos == 3:
            current_image_manager.current_image_label.configure(image=before_image_manager.before_image)
            after_image_manager.destroy_after_image_frame()

        elif image_placer_manager.num_of_photos == 2:
            current_image_manager.destroy_current_image_frame()
            before_image_manager.before_image_frame.pack()

        return self

    def create_new_photo_label(self):
        file_handler_manager.photo = CTkImage(dark_image=before_image_manager.dark_before_image_open,
                                              size=optimal_image_size(before_image_manager.dark_before_image_open))

        photo_label_manager.create_photo_label(file_handler_manager.photo)

        return self

    def create_new_before_image(self):

        new_before_image_file_name = image_placer_manager.list_of_preview_photos[
            image_placer_manager.selected_preview_image_index - 1]

        before_image_manager.dark_before_image_open = Image.open(new_before_image_file_name)

        # selected_preview_image_open = dark_before_image_open

        before_image_manager.before_image = CTkImage(dark_image=before_image_manager.dark_before_image_open,
                                                     size=(200, 300))
        before_image_manager.before_image_label.configure(image=before_image_manager.before_image)

        return self


# Delete Image Manager

delete_image_manager = DeleteImageHandler()

######################################

# Delete Image Button

delete_image_icon_open = Image.open(r'C:\PythonProjectsWasiG\GUI Python\Image Viewer\trashcan_icon.ico')
delete_image_icon_image = CTkImage(dark_image=delete_image_icon_open, size=(64, 64))
delete_image_button = CTkButton(tool_sidebar_manager.tool_frame, text='', image=delete_image_icon_image,
                                command=delete_image_manager.delete_button_func)
delete_image_button.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)


######################################

# Full Screen Class

class FullScreenHandler:
    def __init__(self):
        self.in_full_screen = False
        self.went_into_full_screen_once = False

    def full_screen_button_func(self):

        if image_placer_manager.is_image_there:

            self.set_up_full_screen()

            main_window_manager.modify_window_fullscreen(True)

            if rotate_image_manager.is_image_rotated or rotate_image_manager.false_rotation:

                self.make_rotate_image_full_screen()

            else:

                self.make_normal_image_full_screen()

            self.in_full_screen = True
            self.went_into_full_screen_once = True

        else:
            ms.showerror('No Image', 'An image is needed to go into full screen, please choose an image!')

        return self

    def set_up_full_screen(self):

        tool_sidebar_manager.forget_tool_sidebar()
        photo_preview_bar_manager.forget_image_preview_frame()

        return self

    def make_rotate_image_full_screen(self):

        new_fullscreen_image = CTkImage(rotate_image_manager.degree_image,
                                        size=main_window_manager.get_screen_measurements())

        rotate_image_manager.rotate_label.configure(image=new_fullscreen_image)
        rotate_image_manager.rotate_label.pack(fill="both", expand=True)

        return self

    def make_normal_image_full_screen(self):

        file_handler_manager.image_open = Image.open(image_placer_manager.list_of_preview_photos[
                                                         image_placer_manager.selected_preview_image_index])
        new_fullscreen_image = CTkImage(file_handler_manager.image_open,
                                        size=main_window_manager.get_screen_measurements())

        photo_label_manager.photo_label.configure(image=new_fullscreen_image)
        photo_label_manager.photo_label.pack(fill="both", expand=True)

        return self


# Full Screen Manager

full_screen_manager = FullScreenHandler()

######################################

# Enter Full Screen Button

enter_fullscreen_icon_open = Image.open(r'C:\PythonProjectsWasiG\GUI Python\Image Viewer\fullscreen_icon.ico')
enter_fullscreen_icon_image = CTkImage(dark_image=enter_fullscreen_icon_open, size=(64, 64))
enter_fullscreen_button = CTkButton(tool_sidebar_manager.tool_frame, text='', image=enter_fullscreen_icon_image,
                                    command=full_screen_manager.full_screen_button_func)
enter_fullscreen_button.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)


######################################

# Exit Full Screen Class

class ExitFullScreenHandler:
    def __init__(self):
        self.exit_image = None

    def exit_full_screen_button_func(self, event=None):
        if full_screen_manager.in_full_screen:

            main_window_manager.modify_window_fullscreen(False)
            photo_frame_manager.photo_frame_border(True)
            photo_frame_manager.modify_photo_frame_propagation(True)

            if rotate_image_manager.is_image_rotated or rotate_image_manager.false_rotation:
                self.exit_rotated_image()
            else:
                self.exit_normal_image()

            tool_sidebar_manager.grid_tool_sidebar()
            photo_preview_bar_manager.photo_preview_bar_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)

            full_screen_manager.in_full_screen = False

        return self

    def exit_rotated_image(self):
        photo_label_manager.photo_label.destroy()

        self.exit_image = CTkImage(rotate_image_manager.degree_image,
                                   size=optimal_image_size(rotate_image_manager.degree_image))
        rotate_image_manager.rotate_label.configure(image=self.exit_image, width=500)

        return self

    def exit_normal_image(self):
        if rotate_image_manager.rotate_label:
            rotate_image_manager.rotate_label.destroy()

        file_handler_manager.image_open = Image.open(image_placer_manager.list_of_preview_photos[
                                                         image_placer_manager.selected_preview_image_index])

        self.exit_image = CTkImage(file_handler_manager.image_open,
                                   size=optimal_image_size(file_handler_manager.image_open))

        photo_label_manager.photo_label.configure(image=self.exit_image)

        return self


# Exit Full Screen Manager

exit_full_screen_manager = ExitFullScreenHandler()

######################################

# Exit Full Screen Button

main_window_manager.create_window_binding('<KeyPress-Escape>', exit_full_screen_manager.exit_full_screen_button_func)


######################################

# Zoom In Class

class ZoomInHandler:
    def __init__(self):
        self.zoom_in_value = None

    def zoom_in_button_func(self):
        if image_placer_manager.is_image_there:
            photo_frame_manager.modify_photo_frame_propagation(False)
            file_handler_manager.optimal_image_size_var = tuple(
                val + 40 for val in file_handler_manager.optimal_image_size_var)

            if rotate_image_manager.is_image_rotated or rotate_image_manager.false_rotation:
                print('Rotation Zoom')
                rotate_image_manager.rotated_image.configure(size=file_handler_manager.optimal_image_size_var)

            else:

                if up_arrow_manager.up_arrow_use_indicator:
                    print('Up Arrow Zoom')
                    up_arrow_manager.new_up_label_image.configure(size=file_handler_manager.optimal_image_size_var)
                elif down_arrow_manager.down_arrow_use_indicator:
                    print('Down Arrow Zoom')
                    down_arrow_manager.new_down_label_image.configure(size=file_handler_manager.optimal_image_size_var)
                else:
                    print('Normal Image Zoom')
                    file_handler_manager.photo.configure(size=file_handler_manager.optimal_image_size_var)

        else:
            ms.showerror('No Image Found', 'No image found, please try again.')

        return self

    def start_zoom_in(self, _):
        if image_placer_manager.is_image_there:
            self.zoom_in_value = main_window_manager.schedule_window_updates(110, self.repeat_zoom_in)

        return self

    def repeat_zoom_in(self):
        self.zoom_in_button_func()
        self.zoom_in_value = main_window_manager.schedule_window_updates(110, self.repeat_zoom_in)

        return self

    def stop_zoom_in(self, _):
        if self.zoom_in_value is not None:
            main_window_manager.stop_window_updates(self.zoom_in_value)
            self.zoom_in_value = None

        return self


# Zoom In Manager

zoom_in_manager = ZoomInHandler()

######################################

# Zoom In Buttons and Binding

zoom_in_image_open = Image.open(r'C:\PythonProjectsWasiG\GUI Python\Image Viewer\zoom_in_icon.ico')
zoom_in_image = CTkImage(dark_image=zoom_in_image_open, size=(64, 64))
zoom_in_button = CTkButton(tool_sidebar_manager.tool_frame, text='', image=zoom_in_image,
                           command=zoom_in_manager.zoom_in_button_func)
zoom_in_button.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)

zoom_in_button.bind("<Button-1>", zoom_in_manager.start_zoom_in)
zoom_in_button.bind("<ButtonRelease-1>", zoom_in_manager.stop_zoom_in)


######################################

# Zoom Out Class

class ZoomOutHandler:
    def __init__(self):
        self.zoom_out_value = None

    def zoom_out_button_func(self):

        if image_placer_manager.is_image_there:
            photo_frame_manager.modify_photo_frame_propagation(False)
            file_handler_manager.optimal_image_size_var = tuple(
                val - 40 for val in file_handler_manager.optimal_image_size_var)

            if rotate_image_manager.is_image_rotated or rotate_image_manager.false_rotation:
                rotate_image_manager.rotated_image.configure(size=file_handler_manager.optimal_image_size_var)

            else:

                if up_arrow_manager.up_arrow_use_indicator:
                    up_arrow_manager.new_up_label_image.configure(size=file_handler_manager.optimal_image_size_var)
                elif down_arrow_manager.down_arrow_use_indicator:
                    down_arrow_manager.new_down_label_image.configure(size=file_handler_manager.optimal_image_size_var)
                else:
                    file_handler_manager.photo.configure(size=file_handler_manager.optimal_image_size_var)

        else:
            ms.showerror('No Image Found', 'No image found, please try again.')

        return self

    def start_zoom_out(self, _):
        if image_placer_manager.is_image_there:
            self.zoom_out_value = main_window_manager.schedule_window_updates(110, self.repeat_zoom_out)

        return self

    def repeat_zoom_out(self):
        self.zoom_out_button_func()
        self.zoom_out_value = main_window_manager.schedule_window_updates(110, self.repeat_zoom_out)

        return self

    def stop_zoom_out(self, _):
        if self.zoom_out_value is not None:
            main_window_manager.stop_window_updates(self.zoom_out_value)
            self.zoom_out_value = None


# Zoom Out Manager

zoom_out_manager = ZoomOutHandler()

######################################

# Zoom out button and binding


zoom_out_image_open = Image.open(r'C:\PythonProjectsWasiG\GUI Python\Image Viewer\zoom_out_icon.ico')
zoom_out_image = CTkImage(dark_image=zoom_out_image_open, size=(64, 64))
zoom_out_button = CTkButton(tool_sidebar_manager.tool_frame, text='', image=zoom_out_image,
                            command=zoom_out_manager.zoom_out_button_func)
zoom_out_button.grid(row=5, column=0, sticky='nsew', padx=5, pady=5)

zoom_out_button.bind("<Button-1>", zoom_out_manager.start_zoom_out)
zoom_out_button.bind("<ButtonRelease-1>", zoom_out_manager.stop_zoom_out)

######################################

# Create the window loop

main_window_manager.create_root_loop()
