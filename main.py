from nicegui import ui, client
import os
import subprocess
from utils import *

ui.dark_mode(True)

Editor.load_editor()
code_output = ui.log(max_lines=10).classes('w-full h-40')

with ui.row():
    CPPVERSION = ui.radio({1:'C', 2:'C++'}, value=2).props('inline').set_enabled(False)
    runBtn = ui.button("Run", on_click=lambda e: Code.compile_code(code_output))

    
ui.run()