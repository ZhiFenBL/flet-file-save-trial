import flet as ft
import os
import shutil
import logging
import tempfile # Import the tempfile library

# It's good practice to set up logging for better debugging.
logging.basicConfig(level=logging.INFO)

def main(page: ft.Page):
    """
    Main function using a robust two-step save-then-move process.
    This version uses the correct method to get a temporary directory.
    """
    page.title = "Save Text File"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20

    logging.info("App starting with robust save-move method.")

    # --- UI Controls ---
    file_name_input = ft.TextField(
        label="File Name",
        hint_text="e.g., my_notes.txt",
        width=300,
        border_radius=ft.border_radius.all(10),
    )

    file_content_input = ft.TextField(
        label="Content",
        hint_text="Enter the text you want to save...",
        multiline=True,
        min_lines=5,
        max_lines=10,
        width=300,
        border_radius=ft.border_radius.all(10),
    )
    
    # This will hold the path of the file saved internally
    internal_file_path = ft.Text()

    # --- File Picker Logic ---

    def move_file_to_selected_directory(e: ft.FilePickerResultEvent):
        """
        Callback for when the user picks a destination directory.
        """
        destination_directory = e.path
        logging.info(f"Directory picker result: {destination_directory}")

        if not destination_directory:
            show_snackbar("Operation cancelled: No folder was selected.")
            logging.warning("User cancelled the directory picker.")
            return

        source_path = internal_file_path.value
        if not source_path or not os.path.exists(source_path):
            show_snackbar("Error: Source file not found. Please try saving again.")
            logging.error(f"Source file not found at path: {source_path}")
            return
            
        try:
            file_name = os.path.basename(source_path)
            destination_path = os.path.join(destination_directory, file_name)
            
            logging.info(f"Moving file from {source_path} to {destination_path}")
            shutil.move(source_path, destination_path)
            
            show_snackbar(f"File moved successfully to {file_name}")
            logging.info("File move successful.")

        except Exception as ex:
            error_message = f"Error moving file: {ex}"
            show_snackbar(error_message)
            logging.error(error_message)
        finally:
            page.update()


    # Instantiate the FilePicker for getting a directory path
    directory_picker = ft.FilePicker(on_result=move_file_to_selected_directory)
    page.overlay.append(directory_picker)

    # --- Actions ---

    def save_file_internally_and_prompt_for_move(e):
        """
        STEP 1: Saves the file to the app's private temporary directory.
        STEP 2: Opens the directory picker for the user to choose a destination.
        """
        file_name = file_name_input.value
        content = file_content_input.value

        if not file_name or not content:
            show_snackbar("File name and content cannot be empty.")
            return
            
        try:
            # CORRECTED: Use tempfile.gettempdir() to get the app's private cache directory.
            # This is a reliable, writable location on Android.
            temp_dir = tempfile.gettempdir()
            
            # This is the temporary location where we save the file first
            temp_path = os.path.join(temp_dir, file_name)
            internal_file_path.value = temp_path # Store for the move operation
            
            logging.info(f"Step 1: Saving file internally to {temp_path}")
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            logging.info("Internal save successful. Now prompting for destination.")
            
            # Now that the file is safely saved, ask the user where to move it.
            directory_picker.get_directory_path(
                dialog_title="Choose a Folder to Move the File To"
            )

        except Exception as ex:
            error_message = f"Error during internal save: {ex}"
            show_snackbar(error_message)
            logging.error(error_message)
        
        page.update()


    def show_snackbar(message: str):
        """Helper function to display a message."""
        page.snack_bar = ft.SnackBar(ft.Text(message), duration=4000)
        page.snack_bar.open = True
        page.update()

    # --- Page Layout ---
    page.add(
        ft.Column(
            controls=[
                ft.Text("Flet File Saver", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Saves a file and then asks you where to move it.",
                    size=12,
                    color=ft.Colors.GREY_600,
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(),
                file_name_input,
                file_content_input,
                ft.FilledButton(
                    text="Save and Choose Location",
                    icon=ft.Icons.MOVE_DOWN,
                    on_click=save_file_internally_and_prompt_for_move,
                    width=300,
                    height=50
                ),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()
    logging.info("Page layout created and updated.")


if __name__ == "__main__":
    ft.app(target=main)
