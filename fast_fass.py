from os import makedirs, rmdir
from shutil import rmtree
from uuid import uuid4
from flask import Flask, render_template, request, redirect, url_for
from subprocess import Popen as exec, run


app = Flask(__name__)
apps_list = 'apps.txt'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    app_name = request.form['app_name']
    code = request.form['code']
    modules = request.form.getlist('module')
    args = request.form.getlist('argument')
    arg1 = args[0] if len(args) else "DUMMY"

    with open(apps_list, 'a') as f:
        f.write(app_name + '\n')

    makedirs(f'{app_name}')

    with open(f'{app_name}/app.py', 'w') as f:
        f.write(code)

    with open(f'{app_name}/arg.txt', 'w') as f:
        f.write(arg1)

    with open(f'{app_name}/requirements.txt', 'w') as f:
        for module in modules:
            f.write(module + '\n')

    exec([f'./gen_depl_logic.sh {app_name} {arg1}'], shell=True)

    return redirect(url_for('index'))


@app.route('/apps')
def list_apps():
    with open(apps_list, 'r') as f:
        app_names = f.read().splitlines()
    return render_template('apps.html', app_names=app_names)


@app.route('/deploy/<app_name>')
def deploy(app_name):
    def is_port_available(port: int) -> bool:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) != 0
        
    for port in range(5001, 2**16):
        if is_port_available(port):
            PORTNO = port
            break

    exec([f'./deploy_app.sh {app_name} {PORTNO}'], shell=True)
    return render_template('deployed.html', app_name=app_name, addr=f'http://127.0.0.1:{PORTNO}')


@app.route('/delete/<app_name>', methods=['POST'])
def delete_app(app_name):
    rmtree(f'./{app_name}')

    # Remove app name from the file
    with open(apps_list, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if line.strip() != app_name:
                f.write(line)
        f.truncate()

    exec([f'eval $(minikube docker-env) && docker rmi {app_name}-img'], shell=True)
    return redirect(url_for('list_apps'))


if __name__ == '__main__':
    app.run()
