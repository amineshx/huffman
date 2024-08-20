from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fb72f65e10a78ba35f0d3a2d'

from bigtp import routes