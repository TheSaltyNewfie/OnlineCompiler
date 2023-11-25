from nicegui import ui, client
import os
import subprocess
from utils.utils import *

#code_output = ui.log(max_lines=10).style("width:50%; height:50%")

ui.dark_mode(True)

editor = Editor(lang="python")

ui.query('.nicegui-content').classes('h-screen no-wrap')

with ui.row(wrap=False).classes("w-full h-screen"):
    with ui.column().classes("w-full h-full"):
        editor.load_editor()

    with ui.column().classes("w-1/4 h-full"):
        code_output = ui.log(max_lines=10).style("width:100%; height:50%")
        with ui.row().classes("items-center"):
            ui.label("Language")
            LANGUAGE = ui.select(["python", "cpp", "assembly_x86"], value="cpp", on_change=lambda e: editor.set_lang_editor(LANGUAGE.value))
        runBtn = ui.button("Run", on_click=lambda e: Code.compile_code(code_output, LANGUAGE.value))

'''
with ui.row():
    LANGUAGE = ui.select(["python", "c_cpp", "assembly_x86"], value="c_cpp")
    lang_button = ui.button("Set Language (temp)", on_click=lambda e: editor.set_lang_editor(LANGUAGE.value))
    runBtn = ui.button("Run", on_click=lambda e: Code.compile_code(code_output, LANGUAGE.value))

with ui.row():
    exampleBtn = ui.button("Load Language Example", on_click=lambda e: editor.set_lang_editor_example(LANGUAGE.value))
'''

ui.run()