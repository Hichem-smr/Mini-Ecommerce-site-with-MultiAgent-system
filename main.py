from flask import Flask, render_template, url_for, request
import time
from spade import agent, quit_spade,web
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template
from pprint import pprint
import json
import time

from flask import Flask, flash, redirect, render_template, \
     request, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        data=[{'name':'red'}, {'name':'green'}, {'name':'blue'}])

@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    print((select))
    return(str(select))

if __name__=='__main__':
    app.run(debug=True)

