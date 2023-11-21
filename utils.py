from nicegui import ui, client
import os
import subprocess

class Code():

    def __init__(self, code: str, output: ui.log):
        self.code = code
        self.output = output

    async def get_code():
        return await ui.run_javascript('editor.getValue()')

    def run_code(self):
        result = subprocess.run(["./c_main"], stdout=subprocess.PIPE, text=True)
        self.push(result.stdout)
        self.push(f"returned {result.returncode}")

    async def compile_code(self):
        self.clear()
        ui.notify("Compiling code")
        with open('c_onlinecompile.cpp', 'w+') as file:
            code_result = await Code.get_code()
            file.write(code_result)
        result = subprocess.run(['g++', 'c_onlinecompile.cpp', '-o', 'c_main'], stdout=subprocess.PIPE, text=True)
        Code.run_code(self.output)

class FileStructure():
    def __init__(self, path: str):
        self.path = path

    def get_file_structure():
        pass

    def format_file_structure():
        pass

class Editor():

    def load_editor():
        codeeditor = open('codeeditor.html', 'r+').read()
        ui.add_body_html(codeeditor)