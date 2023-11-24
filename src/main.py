from nicegui import ui, client
import os
import subprocess
from utils.utils import *

ui.dark_mode(True)

editor = Editor(lang="python")
editor.load_editor()

code_output = ui.log(max_lines=10).classes('w-full h-40')

with ui.row():
    LANGUAGE = ui.select(["python", "c_cpp", "assembly_x86"], value="c_cpp")
    lang_button = ui.button("Set Language (temp)", on_click=lambda e: editor.set_lang_editor(LANGUAGE.value))
    runBtn = ui.button("Run", on_click=lambda e: Code.compile_code(code_output, LANGUAGE.value))

with ui.row():
    exampleBtn = ui.button("Load Language Example", on_click=lambda e: editor.set_lang_editor_example(LANGUAGE.value))

ui.run()