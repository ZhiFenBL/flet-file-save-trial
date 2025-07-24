import flet as ft
import os
import logging

# It's good practice to set up logging for better debugging.
logging.basicConfig(level=logging.INFO)

def main(page: ft.Page):
    """
    Main function to create the Flet application UI and logic.
    This uses the direct FilePicker.save_file() method.
    """
    page.title = "Save Text File Directly"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20

    logging.info("App starting with direct save method.")

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

    # --- File Picker Logic ---

    def save_file_result(e: ft.FilePickerResultEvent):
        """
        Callback function that is triggered after the user selects a path
        in the FilePicker dialog.
        """
        logging.info(f"FilePicker result: path={e.path}, error={e.error}")

        if e.path:
            # If the user selected a path (didn't cancel)
            try:
                logging.info(f"Attempting to write to: {e.path}")
                # Ensure the value is not None before writing
                with open(e.path, "w", encoding="utf-8") as f:
                    f.write(file_content_input.value or "")
                
                show_snackbar(f"Successfully saved: {os.path.basename(e.path)}")
                logging.info("File saved successfully.")
            except Exception as ex:
                error_message = f"Error saving file: {ex}"
                show_snackbar(error_message)
                logging.error(error_message)
        elif e.error:
            error_message = f"FilePicker Error: {e.error}"
            show_snackbar(error_message)
            logging.error(error_message)
        else:
            show_snackbar("Operation cancelled by user.")
            logging.info("File save operation cancelled.")
        
        page.update()

    # Instantiate the FilePicker and add it to the page's overlay.
    file_picker = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(file_picker)
    page.update()
    logging.info("FilePicker added to overlay.")

    # --- Actions ---

    def save_file_action(e):
        """
        This function is called when the 'Save File' button is clicked.
        It triggers the FilePicker's save_file dialog.
        """
        logging.info("Save button clicked.")
        
        file_name = file_name_input.value if file_name_input.value else "new_file.txt"
        logging.info(f"Calling file_picker.save_file with filename: {file_name}")
        
        # This is the single, correct call to save the file.
        file_picker.save_file(
            dialog_title="Save File As...",
            file_name=file_name,
            allowed_extensions=["txt", "log", "md"]
        )

    def show_snackbar(message: str):
        """Helper function to display a message at the bottom of the screen."""
        page.snack_bar = ft.SnackBar(ft.Text(message), duration=4000)
        page.snack_bar.open = True
        page.update()

    # --- Page Layout ---
    page.add(
        ft.Column(
            controls=[
                ft.Text("Flet File Saver", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Enter a filename and content, then click 'Save File'.",
                    size=12,
                    color=ft.Colors.GREY_600,
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(),
                file_name_input,
                file_content_input,
                ft.FilledButton(
                    text="Save File",
                    icon=ft.Icons.SAVE,
                    on_click=save_file_action,
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
