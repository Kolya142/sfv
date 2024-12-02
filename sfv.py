import os
from pathlib import Path
from flask import Flask, request

app = Flask(__name__)

files_path = './files/'

def html_path(path: str) -> str:
    html = open("folder.html").read()
    html = html.replace("%path%", path).replace("%url%", request.host)
    urls = ""
    files = os.listdir(files_path + path)
    for p in files:
        urls += f'<a href="{Path(path) / p}">{p}</a><br>'
    html = html.replace("%urls%", urls)
    return html

@app.route('/<path>')
def root_path(path):
    if os.path.isfile(files_path + path):
        return open(files_path + path).read()
    return html_path(path)

@app.route('/')
def main():
    return html_path("/")

if __name__ == '__main__':
    app.run("0.0.0.0", 9569, ssl_context=('/server/cert.crt', '/server/cert.key'))