import flet as ft
import os

def main(page: ft.Page):
    """
    Main function to create the Flet application UI and logic.
    """
    page.title = "Save Text File"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20

    # --- UI Controls ---

    # TextField for the user to enter the desired filename.
    file_name_input = ft.TextField(
        label="File Name",
        hint_text="e.g., my_notes.txt",
        width=300,
        border_radius=ft.border_radius.all(10),
    )

    # TextField for the user to enter the content to be saved.
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
        if e.path:
            # If the user selected a path (didn't cancel)
            try:
                with open(e.path, "w", encoding="utf-8") as f:
                    f.write(file_content_input.value)
                
                show_snackbar(f"Successfully saved to: {os.path.basename(e.path)}")
            except Exception as ex:
                show_snackbar(f"Error saving file: {ex}")
        else:
            # If the user cancelled the dialog
            show_snackbar("Operation cancelled by user.")

    # Instantiate the FilePicker and add it to the page's overlay.
    # The overlay is a layer that can display on top of other controls.
    file_picker = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(file_picker)

    # --- Actions ---

    def save_file_action(e):
        """
        This function is called when the 'Save File' button is clicked.
        It triggers the FilePicker's save_file dialog.
        """
        # Use the text from the input field as the default file name.
        # Fallback to a default name if the input is empty.
        file_name = file_name_input.value if file_name_input.value else "new_file.txt"
        
        # This opens the native Android file saver dialog.
        # The user chooses the folder and confirms the file name.
        # The actual file writing happens in the `save_file_result` callback.
        file_picker.save_file(
            dialog_title="Save Text File As...",
            file_name=file_name,
            allowed_extensions=["txt", "log", "md"] # Optional: filter for file types
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
                    "Enter a filename and content, then click 'Save File'.\nYou will be prompted to choose a folder to save the file in.",
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

# Entry point for the Flet application
if __name__ == "__main__":
    ft.app(target=main)
