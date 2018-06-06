import os
from xlrd import open_workbook
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 

from werkzeug import secure_filename
import hashlib
import platform
from resark.processexcel import excelfile
from resark.staticdata import metadatalist

class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# For testing ... create some users with ids 1 to 20       
users = [User(id) for id in range(1, 21)]


if platform.system()=='Windows':
	UPLOAD_FOLDER = 'c:/windows/temp/'
else:
	UPLOAD_FOLDER = '/tmp'
	
ALLOWED_EXTENSIONS = set(['xls','xlsx'])

import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(
    SECRET_KEY = os.urandom(12)
)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



           
           
           
@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
    
@app.route("/None")
@app.route("/")
def home():
    return render_template('template.html',title="Resultatarkiv")

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    elif False:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')
    else:
        return render_template("login.html")


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Ugyldig bruker</p><p><a href="/">Tilbake</a>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)
            
@app.route("/search", methods=['GET', 'POST'])
def search():
    print(request.path)
    searchbuttontext="Søk"
    savebuttontext="Lagre"
    set=None
    req={}
    error=""
    table=""
    if request.method == 'POST':
        if searchbuttontext ==  request.form['button']:    
            True
        else:
            print("Unknown button")
        print(request.form)
    else:
        True
    fields=None
    return render_template('search.html',path=request.path,sebt=searchbuttontext,dataset=set,error=error,table=table,fields=fields,req=request.form,title="Datasøk")
#    return render_template('search.html',sebt=searchbuttontext)

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

    return render_template('upload.html',  
        title="Upload excel file")

@app.route("/process", methods=['GET', 'POST'] )
@login_required
def process():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath =os.path.join(app.config['UPLOAD_FOLDER'], filename) 
            file.save(filepath)
            importfile=excelfile(filepath)
            importfile.check()
    return render_template('process.html', my_string=request.files['file'].filename, filepath=filepath,
        title="Processing file", current_time=datetime.datetime.now(),
        valuewarnings=importfile.valuewarning,valueerrors=importfile.valueerror,md5=importfile.md5)
        
@app.route("/importdata", methods=['POST'] )
@login_required
def importdata():
    filepath=request.form['filepath']
    importfile=excelfile(filepath)
    importfile.importdata()
    return render_template('importdata.html', title="Importerer data",filepath=filepath,md5=importfile.md5)

@app.route("/project", methods=['POST','GET']) 
@login_required
def project():
    return staticdata("projects")

 
@app.route("/habitat", methods=['POST','GET']) 
@login_required
def habitat():
    return staticdata("habitatlist")

@app.route("/samplecat", methods=['POST','GET']) 
@login_required
def samplecat():
    return staticdata("samplecatlist")

@app.route("/topic", methods=['POST','GET']) 
@login_required
def topic():
    return staticdata("topiclist")
    
@app.route("/quantity", methods=['POST','GET']) 
@login_required
def quantity():
    return staticdata("quantitylist")
    
@app.route("/metadata", methods=['POST','GET'])
@login_required
def metadata():
    return staticdata("metadatalist")

@app.route("/nuclide", methods=['POST','GET'])
@login_required
def nuclide():
    return staticdata("nuclidelist")

@app.route("/sampletype", methods=['POST','GET'])
def sampletype():
    return staticdata("sampletypelist")
    
@app.route("/species", methods=['POST','GET'])
def species():
    return staticdata("specieslist")
    
def staticdata(table):  
    print(request.path)
    print(table)
    searchbuttontext="Søk"
    savebuttontext="Lagre"
    set=None
    error=""
    if request.method == 'POST':
        mtdt=metadatalist(table,req=request.form)
        if searchbuttontext ==  request.form['button']:    
            set=mtdt.search()
        elif savebuttontext == request.form['button']:
            md=metadatalist(table,name=request.form["name"])
            n=len(md.search(partial=False))
            try:
                md=metadatalist(table,shortname=request.form["shortname"])
                print(n)
                n=n+len(md.search(partial=False))
            except AttributeError:
                True # Just ignore it
            print(n)
            if n>0:
                error="eksisterende"
            else:
                mtdt.save()
                set=mtdt.search()
        else:
            print("Unknown button")
        print(request.form)
    else:
        mtdt=metadatalist(table)
    fields=mtdt.fields()
    return render_template('metadata.html',path=request.path,sebt=searchbuttontext,sabt=savebuttontext,dataset=set,error=error,table=table,fields=fields,req=request.form,title=table.title())

   
@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('htmlerror.html'), 404
        

if __name__ == '__main__':
        
    app.secret_key = os.urandom(12)
    app.run(debug=True)
