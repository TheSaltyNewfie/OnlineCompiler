from nicegui import ui, client
import os
import subprocess

async def get_code():
    return await ui.run_javascript('editor.getValue()')

async def example_code(lang: str):
    with open("exampleCode/example.cpp") as file:
        await ui.run_javascript(f'editor.setValue("{file.read()}")')

async def get_height():
    return await ui.run_javascript('window.innerHeight;')

async def compile_code(output: ui.log):
    output.clear()
    ui.notify("Compiling code")
    with open('c_onlinecompile.cpp', 'w+') as file:
        code_result = await get_code()
        file.write(code_result)
    result = subprocess.run(['g++', 'c_onlinecompile.cpp', '-o', 'c_main'], stdout=subprocess.PIPE, text=True)
    #ui.notify(result)
    #output.push(f"Return code: {result.returncode}")
    run_code(output)


def run_code(output: ui.log):
    result = subprocess.run(["./c_main"], stdout=subprocess.PIPE, text=True)
    output.push(result.stdout)
    output.push(f"returned {result.returncode}")

def loadEditor():
    codeeditor = open('codeeditor.html', 'r+').read()
    ui.add_body_html(codeeditor)