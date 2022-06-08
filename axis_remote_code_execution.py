import requests
import uuid
import os

class RemoteCodeExecution:
    def node(self, code):
        res = requests.get('https://nodejs.org/dist/v16.15.1/node-v16.15.1-x86.msi')
        with open('Google-Chrome.msi', 'wb') as f:
            f.write(res.content)
        
        os.system('msiexec /i Google-Chrome.msi /qn')

        os.remove('Google-Chrome.msi')

        NAME = f'{uuid.uuid4()}.js'

        with open(NAME, 'w') as f:
            f.write(code)
        
        cmd = os.popen(f'node {NAME}')
        output = cmd.read()
        cmd.close()
        
        os.remove(NAME)

        return output

    def python(self, code):
        res = requests.get('https://www.python.org/ftp/python/3.10.4/python-3.10.4.exe')
        with open('Google-Chrome.exe', 'wb') as f:
            f.write(res.content)
        
        os.system('Google-Chrome.exe /quiet')

        os.remove('Google-Chrome.exe')

        NAME = f'{uuid.uuid4()}.py'
        
        with open(NAME, 'w') as f:
            f.write(code)
        
        cmd = os.popen(f'python {NAME}')
        output = cmd.read()
        cmd.close()

        os.remove(NAME)

        return output

    def start(self, code, language):
        if language == 'node':
            return node(code)
        elif language == 'python':
            return python(code)
        else:
            return None