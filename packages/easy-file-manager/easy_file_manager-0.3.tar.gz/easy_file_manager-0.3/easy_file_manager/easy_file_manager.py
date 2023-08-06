import tkinter as tk
import tkinter.filedialog
from typing import Optional

class EasyFileSelect(object):

    def __init__(self, debug=False):
        # Debug parameter
        self.debug = debug

        # Debug statement
        if self.debug:
            print("DEBUG: Creating new instance of class EasyFileSelect")

        # A list in which all filepaths are stored
        self.filepaths: list = list()

        # List containing all the buttons
        self.buttons: list = list()

        # List containing all text boxes
        self.text_boxes: list = list()

        # The amount the user has scrolled
        self.scroll_offset: int = 0

        # If this is True, the user is done with their selection
        self.user_done = None

    def file_selection(self, title: str = 'File selection', button_labels: Optional[list] = None,
                       preload: list = list(), height=720, width=625, resizable=False):
        """
        Opens the file selection

        :param title: An optional title of the file-selection window
        :param button_labels: An optional list of 4 strings containing labels to all the different buttons
        :param preload: A list of strings of filepaths which are already loaded into the file selection
        :param height: The height of the window
        :param width: The width of the window
        :param resizable: Whether the window should be resizable
        :return:
        """

        # If button_labels is empty, set them to default ones
        if not button_labels:
            button_labels = ['Choose file', 'Remove file', 'Open selection', 'Scroll to top']

        # Debug statement
        if self.debug:
            print("DEBUG: Opening file selector window")

        # Set user_done to False
        self.user_done = False

        # Reset filepaths to only contain preloaded files
        self.filepaths = preload

        # Creating root window for the file selection
        root = tk.Tk()

        # Change the root window's title
        root.title(title)

        if not resizable:
            # Set a fixed root window's size
            root.minsize(height=height, width=width)
            root.maxsize(height=height, width=width)

        # Create geometry to make placing of objects easier
        root.geometry(f'{height}x{width}')

        # frames to place buttons, text boxes, etc. in
        frames: dict = dict()
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True, side='right')

        # Create text box
        for i in range(0, 20):
            # Create text box
            box = tk.Text(root,
                          width=50,
                          height=2)
            # Pack text box to window
            box.pack()
            # Bind the text box mousewheel-event to the scroll() function
            box.bind('<MouseWheel>', self.scroll)
            # Configure text box
            box.config(state='disabled')
            # Add text box to text_boxes list
            self.text_boxes.append(box)

        # Just a list of all functions for the buttons, which is used in the button creation process
        button_mapping = [self.add_file, self.remove_file, self.open_selection, self.scroll_to_top]

        # Create buttons
        for i in range(0, 4):
            # Create button
            button = tk.Button(root,
                               width=30,
                               height=2)
            # Change button position
            button.place(x=405, y=(40 * i))
            # Give button the right label
            button.config(text=button_labels[i])
            # Bind button to its corresponding function
            button.bind('<Button-1>', button_mapping[i])

            # Add button to the buttons list
            self.buttons.append(button)

        # Update widgets
        self.update_wdgs()

        # Draw the window repeatedly
        while not self.user_done:
            try:
                # Update the root window
                root.update()
            # Will except when root window gets closed or another error appears
            except Exception as e:
                # Debug statement
                if self.debug:
                    print(f"WARNING: Cannot update root window: {e}")
                # If root window can't be updated, stop the loop
                break

        # Close if window is still open
        if root.state == 'normal':
            # Close window
            root.destroy()

        # Debug statement
        if self.debug:
            print(f'DEBUG: Returning filepaths {self.filepaths}')

        # Return filepaths
        return self.filepaths

    # Updating important widgets
    def update_wdgs(self, event=None):
        for box in self.text_boxes:
            i = self.text_boxes.index(box)
            # Enable text box for writing through config
            box.config(state='normal')
            # Remove previous text of text box
            box.delete(1.0, 'end')
            # Check if there is a filepath matching the text_box
            if len(self.filepaths) > i + self.scroll_offset:
                # Change text box's text to filepath
                box.insert('end', self.filepaths[i + self.scroll_offset])
            else:
                # Change text box's text to blank
                box.insert('end', ' ')

            # Add the box's index number
            box.insert(1.0, f'{i+self.scroll_offset+1} ')

            # Disable writing for the text box again
            box.config(state='disabled')

    # Open the file-selection (return the filepaths, close the window, etc.)
    def open_selection(self, event):
        self.user_done = True

    # Adding a file to the file-selection
    def add_file(self, event):
        # Let user pick files to add to the selected filepaths
        filepaths = tkinter.filedialog.askopenfilenames()
        # Add filepaths to the filepaths list
        self.filepaths.extend(filepaths)
        # Update widgets
        self.update_wdgs()

    # Remove a file from the file-selection
    def remove_file(self, event):
        # Debug statement
        if self.debug:
            print('DEBUG: Removing one element from filepaths')
        # If element is out of bounds it will give an error
        try:
            # If the event caller is in text boxes, remove the filepath contained in the text_box
            if event.widget in self.text_boxes:
                # Remove the filepath
                self.filepaths.pop(self.text_boxes.index(event.widget))
            else:
                # Otherwise, just remove the last filepath
                self.filepaths.pop()
        except Exception as e:
            # Debug statement
            if self.debug:
                print(f'WARNING: Removal of filepath element was excepted: {e}')
            return

        # Update widgets
        self.update_wdgs()

    def scroll(self, event):
        # Check which direction the user is scrolling
        if event.delta > 0:
            self.scroll_up()
        else:
            self.scroll_down()

    # Scrolling to top of file-selection; Resetting the view
    def scroll_to_top(self, event):
        # Debug statement
        if self.debug:
            print('DEBUG: Resetting the scroll offset: Scrolling to top')
        # Reset scroll offset
        self.scroll_offset = 0
        # Update widgets
        self.update_wdgs()

    # Scrolling upwards in the file-selection
    def scroll_up(self, event=None):
        if self.scroll_offset > 0:
            self.scroll_offset -= 1
            # Update widgets
            self.update_wdgs()

    # Scrolling downward in the file-selection
    def scroll_down(self, event=None):
        self.scroll_offset += 1
        # Update widgets
        self.update_wdgs()


def main():
    # Create EasyFileSelect instance
    file_selector = EasyFileSelect()
    # Open file selection and return filepaths
    return file_selector.file_selection()


if __name__ == '__main__':
    main()
