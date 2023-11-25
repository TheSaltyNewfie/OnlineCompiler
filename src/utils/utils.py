from nicegui import ui, client
import os
import subprocess

class Code:

    def __init__(self, output: ui.log):
        self.output = output

    async def get_code():
        return await ui.run_javascript('window.editor.getValue()')

    def run_code(self, lang):
        match lang:
            case "cpp":
                result = subprocess.run(["./src/workdir/c_main"], stdout=subprocess.PIPE, text=True)
                self.push(result.stdout)
                self.push(f"returned {result.returncode}")
            case "assembly_x86":
                result = subprocess.run(["./src/workdir/asm_main"], stdout=subprocess.PIPE, text=True)
                self.push(result.stdout)

    async def compile_code(self, lang):
        self.clear()
        self.push("Compiling....")
        
        match lang:
            # C++ Needs to be compiled, so we compile then run
            case "cpp":
                with open('src/workdir/c_onlinecompile.cpp', "w+") as file:
                    code_result = await Code.get_code()
                    file.write(code_result)
                result = subprocess.run(['g++', 'src/workdir/c_onlinecompile.cpp', '-o', 'src/workdir/c_main'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
                self.push(f"\n{result.stderr}\n")
                Code.run_code(self, "cpp")

            # Python only needs to be interpreted, so we wont compile this time.
            case "python":
                with open('src/workdir/python_onlinecompile.ppy', "w+") as file:
                    code_result = await Code.get_code()
                    file.write(code_result)
                result = subprocess.run(['python3', 'src/workdir/python_onlinecompile.ppy'], stdout=subprocess.PIPE, text=True)
                self.push(result.stdout)

            # ASM
            case "assembly_x86":
                with open('src/workdir/asm_onlinecompile.asm', 'w') as file:
                    code_result = await Code.get_code()
                    file.write(code_result)
                building = subprocess.run(['nasm', '-f', 'elf32', 'src/workdir/asm_onlinecompile.asm', '-o', 'src/workdir/asm.o'], stdout=subprocess.PIPE, text=True)
                linking = subprocess.run(['ld', '-m', 'elf_i386', 'src/workdir/asm.o', '-o', 'src/workdir/asm_main'], stdout=subprocess.PIPE, text=True)
                self.push(f"\n{building.stderr}\n")
                Code.run_code(self, lang)

class Files:
    def __init__(self, path: str):
        self.path = path

    def cache_file(self, code:str, lang:str):
        match lang:
            case "cpp":
                with open('src/workdir/cache/c_cache.cache') as file:
                    file.write(code)
                    ui.notfiy("Wrote to cache for C++ code")
            case "python":
                with open('src/workdir/cache/python_cache.cache') as file:
                    file.write(code)
                    ui.notify("Wrote to cache for Python code")
        

class Editor:

    def __init__(self, lang):
        self.lang = lang

    main_div = '''
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <!-- Include Monaco Editor from a CDN -->
    </head>
    <body>
      <div id="editor-container"></div>
    </body>
    </html>
    '''
    
    body_script = '''
    <script>
        require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.30.1/min/vs' }});
        require(['vs/editor/editor.main'], function() {
          window.editor = monaco.editor.create(document.getElementById('editor-container'), {
            language: 'cpp', // Set the programming language
            theme: 'vs-dark' // Set the editor theme (optional)
          });
        });
      </script>
    '''
    
    head_script = '''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.30.1/min/vs/loader.js"></script>
    '''

    def load_editor(self):
        #codeeditor = open('src/codeeditor.html', 'r+').read()
        #ui.add_body_html(codeeditor)
        with ui.card().style("height: 100%; width:100%;").classes(""):
            ui.html(Editor.main_div)
            style = ui.html("<style>#editor-container {position:absolute; top:1vh; left:2vh; right:2vh; bottom:1vh;}</style>")
            ui.add_body_html(Editor.head_script)
            ui.add_body_html(Editor.body_script)


    async def set_lang_editor(self, new_lang):
        try:
            await ui.run_javascript(f'monaco.editor.setModelLanguage(window.editor.getModel(), "{new_lang}");')
        except TimeoutError:
            print(f"Language changed to {new_lang}")

    async def set_lang_editor_example(self, lang):
        match lang:
            case "cpp":
                await ui.run_javascript('editor.setValue("#include <iostream>\\n'
                                        'int main() {\\n'
                                        '    std::cout << \\"Hello, world!\\" << std::endl;\\n'
                                        '    return 0;\\n'
                                        '}")')
            case "python":
                await ui.run_javascript('editor.setValue("print(\\"Hello, world!\\")")')
            case "assembly_x86":
                await ui.run_javascript('editor.setValue("section .data\\n'
                                        'hello db \\"Hello, world!\\",0xa  ; Hello, world! string followed by a newline character\\n'
                                        'len equ $ - hello            ; Length of the Hello, world! string\\n\\n'
                                        'section .text\\n'
                                        'global _start\\n\\n'
                                        '_start:\\n'
                                        '    ; Write Hello, world! to stdout\\n'
                                        '    mov eax, 4            ; The system call for sys_write (4)\\n'
                                        '    mov ebx, 1            ; File descriptor 1 - stdout\\n'
                                        '    mov ecx, hello        ; Pointer to the message\\n'
                                        '    mov edx, len          ; Message length\\n'
                                        '    int 0x80              ; Call kernel\\n\\n'
                                        '    ; Exit the program\\n'
                                        '    mov eax, 1            ; The system call for sys_exit (1)\\n'
                                        '    xor ebx, ebx          ; Return a code of 0\\n'
                                        '    int 0x80              ; Call kernel")')


if __name__ == "__main__":
    print("This is not a executable :)")