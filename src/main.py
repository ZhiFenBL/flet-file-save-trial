# test_filesave.py
import flet as ft
import logging

logging.basicConfig(level=logging.INFO)

def main(page: ft.Page):
    page.title = "Minimal Save Test"

    def save_file_result(e: ft.FilePickerResultEvent):
        if e.error:
            logging.error(f"FilePicker Error: {e.error}")
        else:
            logging.info("Save dialog was handled by OS.")

    file_picker = ft.FilePicker(on_result=save_file_result)
    page.overlay.append(file_picker)

    def trigger_save(e):
        logging.info("Button clicked. Preparing to save hardcoded data.")
        # Hardcoded data to remove any issues from TextField
        test_bytes = "This is a test.".encode("utf-8")
        
        logging.info(f"Calling save_file with {len(test_bytes)} bytes.")
        file_picker.save_file(
            dialog_title="Save Test File",
            file_name="test.txt",
            file_data=test_bytes
        )
        logging.info("save_file call finished.")

    page.add(ft.ElevatedButton("Save Test File", on_click=trigger_save))

ft.app(target=main)
