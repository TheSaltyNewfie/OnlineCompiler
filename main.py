from nicegui import ui, client
import os
import subprocess

ui.dark_mode(True)

async def compile_code():
    ui.notify("Compiling code")
    with open('c_onlinecompile.cpp', 'w') as file:
        code_result = await get_code()
        file.write(code_result)

    result = subprocess.run(['g++', 'c_onlinecompile.cpp', '-o', 'c_main'], stdout=subprocess.PIPE, text=True)
    ui.notify(result)
def run_code():
    result = subprocess.run(["./c_main"], stdout=subprocess.PIPE, text=True)
    #ui.notify(result.stdout)
    code_output.value = result.stdout

async def get_code():
    return await ui.run_javascript('editor.getValue()')

codeeditor = open('codeeditor.html', 'r+').read()

ui.add_body_html(codeeditor)

code_output = ui.textarea(label="", placeholder="This is where your code output will be!").style('width: 500px;')

with ui.row():
    CPPVERSION = ui.radio({1:'C', 2:'C++'}, value=2).props('inline').set_enabled(False)
    compileBtn = ui.button("Compile", on_click=compile_code)
    runBtn = ui.button("Run", on_click=run_code)
    
ui.run()