from flask import Flask, render_template
from subprocess import Popen as exec, run
from uuid import uuid4
from sys import argv

app = Flask(__name__)
APPNAME = argv[1]
PORTNO = int(argv[2])


@app.route('/')
def run_function():
    depl_id = uuid4().hex
    p = run([f'./run_job.sh {APPNAME} {depl_id}'], shell=True, capture_output=True)
    return p.stdout

if __name__ == '__main__':
    app.run(port=PORTNO)
