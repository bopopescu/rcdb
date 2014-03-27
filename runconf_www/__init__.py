from runconf_db.model import RunConfiguration

__author__ = 'romanov'
from flask import Flask, render_template, g, request, url_for

import runconf_db
#from runconf_db import Board

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
#app.config.from_object('config')
app.config.from_object(__name__)

@app.before_request
def before_request():

    g.tdb = runconf_db.ConfigurationProvider()
    g.tdb.connect()

@app.teardown_request
def teardown_request(exception):
    #tdb = getattr(g, 'db', None)
    pass


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

@app.route('/sample')
def sample():
    return render_template('index.html')

@app.route('/')
def index():
    runs = g.tdb.session.query(RunConfiguration).order_by(RunConfiguration.number.desc()).all()
    return render_template("index.html", runs=runs)

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page

#from  import mod as boardsModule
from boards.views import mod as boards_module
from runs.views import mod as runs_module
from logs.views import mod as logs_module
from files.views import mod as files_module
from crates.views import mod as crates_module
from statistics.views import mod as statistics_module

app.register_blueprint(boards_module)
app.register_blueprint(runs_module)
app.register_blueprint(logs_module)
app.register_blueprint(files_module)
app.register_blueprint(crates_module)
app.register_blueprint(statistics_module)


if __name__ == '__main__':
    app.run()