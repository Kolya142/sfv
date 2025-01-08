import os
from pathlib import Path
import stat
from flask import Flask, request

app = Flask(__name__)

files_path = './files/'

def get_permision(i: int) -> str:
    v = ''
    if i & 4 != 0:
        v += 'r'
    else:
        v += '-'
    if i & 2 != 0:
        v += 'w'
    else:
        v += '-'
    if i & 1 != 0:
        v += 'x'
    else:
        v += '-'
    return v

def get_ft(b: str) -> str:
    if os.path.isdir(b):
        return 'd'
    if os.path.islink(b):
        return 'l'
    if os.path.isjunction(b):
        return 'l'
    if stat.S_ISFIFO(os.stat(b).st_mode):
        return 'p'
    return '-'

def html_path(path: str) -> str:
    html = open("folder.html").read()
    html = html.replace("%path%", path).replace("%url%", request.host)
    urls = ""
    files = os.listdir(files_path + path)
    for p in files:
        if p.lower() == 'pyindex.py':
            b = files_path + path + '/' + p
            glb = {}
            lcl = {}
            exec(open(b).read(), glb, lcl)
            if "main" in glb:
                return glb["main"]()
            if "main" in lcl:
                return lcl["main"]()
    for p in files:
        access = ""
        b = files_path + p
        access += get_ft(b)
        perm = os.stat(b).st_mode
        perm = oct(perm)[-3:]
        access += get_permision(int(perm[0]))
        access += get_permision(int(perm[1]))
        access += get_permision(int(perm[2]))
        urls += f'<a href="{Path(path) / p}">{access} {p}</a><br>'
    html = html.replace("%urls%", urls)
    return html

@app.route('/<path>')
def root_path(path):
    if get_ft(files_path + path) != 'd':
        return open(files_path + path).read()
    return html_path(path)

@app.route('/')
def main():
    return html_path("/")

if __name__ == '__main__':
    app.run("0.0.0.0", 9569, ssl_context=('/server/cert.crt', '/server/cert.key'))
