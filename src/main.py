import flet as ft
import os
import logging

logging.basicConfig(level=logging.INFO)

def main(page: ft.Page):
    page.title = "Save Text File (Latest Flet)"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20

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

    def show_snackbar(message: str):
        page.snack_bar = ft.SnackBar(ft.Text(message), duration=4000)
        page.snack_bar.open = True
        page.update()

    # --- File Picker Logic (Corrected) ---
    def save_file_result(e: ft.FilePickerResultEvent):
        """
        This callback now handles the file writing.
        """
        if e.path:
            try:
                # Get content and encode it to bytes
                content_to_save = file_content_input.value or ""
                file_data_bytes = content_to_save.encode("utf-8")
                
                # Write the bytes to the file path provided by the picker
                with open(e.path, "wb") as f:
                    f.write(file_data_bytes)
                
                show_snackbar(f"Successfully saved: {os.path.basename(e.path)}")
                logging.info(f"File saved successfully to {e.path}")
            except Exception as ex:
                show_snackbar(f"Error saving file: {ex}")
                logging.error(f"Error saving file: {ex}")
        elif e.error:
            show_snackbar(f"FilePicker Error: {e.error}")
            logging.error(f"FilePicker Error: {e.error}")
        else:
            show_snackbar("Operation cancelled by user.")
            logging.info("File save operation cancelled.")
        
        page.update()

    file_picker = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(file_picker)

    # --- Actions (Corrected) ---
    def save_file_action(e):
        """
        This function now ONLY triggers the dialog.
        The file_data argument is removed.
        """
        file_name = file_name_input.value if file_name_input.value else "new_file.txt"
        
        file_picker.save_file(
            dialog_title="Save File As...",
            file_name=file_name,
            allowed_extensions=["txt", "log", "md"]
        )

    # --- Page Layout ---
    page.add(
        ft.Column(
            controls=[
                ft.Text("Flet File Saver", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Enter a filename and content, then click 'Save File'.",
                    size=12, color=ft.Colors.GREY_600
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

if __name__ == "__main__":
    ft.app(target=main)
