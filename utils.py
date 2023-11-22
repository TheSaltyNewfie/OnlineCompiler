from nicegui import ui, client
import os
import subprocess

class Code:

    def __init__(self, output: ui.log):
        self.output = output

    async def get_code():
        return await ui.run_javascript('editor.getValue()')

    def run_code(self):
        result = subprocess.run(["./workdir/c_main"], stdout=subprocess.PIPE, text=True)
        self.push(result.stdout)
        self.push(f"returned {result.returncode}")

    async def compile_code(self, lang):
        self.clear()
        self.push("Compiling....")
        
        match lang:
            # C++ Needs to be compiled, so we compile then run
            case "c_cpp":
                with open('workdir/c_onlinecompile.cpp', "w+") as file:
                    code_result = await Code.get_code()
                    file.write(code_result)
                result = subprocess.run(['g++', 'workdir/c_onlinecompile.cpp', '-o', 'workdir/c_main'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
                self.push(f"{result.stderr} || {result.stdout}")
                Code.run_code(self)

            # Python only needs to be interpreted, so we wont compile this time.
            case "python":
                with open('workdir/python_onlinecompile.ppy', "w+") as file:
                    code_result = await Code.get_code()
                    file.write(code_result)
                result = subprocess.run(['python3', 'workdir/python_onlinecompile.ppy'],stdout=subprocess.PIPE, text=True)
                self.push(result.stdout)

    '''
    async def compile_code(self):
        self.clear()
        ui.notify("Compiling code")
        with open('c_onlinecompile.cpp', 'w+') as file:
            code_result = await Code.get_code()
            file.write(code_result)
        result = subprocess.run(['g++', 'c_onlinecompile.cpp', '-o', 'c_main'], stdout=subprocess.PIPE, text=True)
        Code.run_code(self.output)
    '''

class FileStructure:
    def __init__(self, path: str):
        self.path = path

    def get_file_structure():
        pass

    def format_file_structure():
        pass

class Editor:

    def __init__(self, lang):
        self.lang = lang

    def load_editor(self):
        codeeditor = open('codeeditor.html', 'r+').read()
        ui.add_body_html(codeeditor)

    async def set_lang_editor(self, new_lang):
        await ui.run_javascript(f'editor.session.setMode("ace/mode/{new_lang}")')
