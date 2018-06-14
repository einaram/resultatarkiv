import os
from xlrd import open_workbook
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, Response,send_from_directory
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user ,current_user

from werkzeug import secure_filename
import hashlib
import platform
from resark.processexcel import excelfile
from resark.staticdata import metadatalist
from resark.searchdata import searchdata
from resark.user import User
from resark.dbconnector import dbconnector
from inspect import currentframe, getframeinfo

frameinfo = getframeinfo(currentframe())


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

@login_manager.user_loader
def load_user(user_id):
  #  g.user = current_user.username
    return User.get(user_id)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
  
         
           
@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter
 
    
@app.route("/None")
@app.route("/")
def home():
    return render_template('template.html',title="Resultatarkiv")

@app.route("/user", methods=["GET", "POST"])
@login_required
def setnewpassword():
    text=""
    if request.method == 'POST':
        oldpass=request.form['oldpass']
        password=request.form['pass1']
        minpass=5
        if len(password) < minpass:
            text="For kort passord - det må være minst {} tegn".format(minpass)
        elif password == request.form['pass2']:
            if current_user.update_password(oldpass,password):
                text="Nytt passord - OK" 
            else:
                text="Kunne ikke oppdatere passord - er gammelt passord riktig?"
        else:
            text="Nytt passord stemmer ikke med gjentakelse"
    return render_template('user.html',title="Brukerinnstillinger",text=text)
    
    
# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db=dbconnector()
        user = User(username)
        if user.check_password(password):
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
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
    searchbuttontext="Søk"
    savebuttontext="Lagre"
    downloadbuttontext="Last ned"
    set=None
    req={}
    error=""
    table=""
    search=searchdata()
    types=search.listnames('sampletypelist')
    
    overviewfields=search.overviewfields()
    overviewfields.insert(0,"Bruk")
    selected=None
    nfound=None
    if request.method == 'GET':
        if searchbuttontext ==  request.args.get('button'):    
            selected=request.args['sampletype']
            nfound=search.countsamples(request.args)
        elif downloadbuttontext ==  request.args.get('button'):
            search.download(request.args,UPLOAD_FOLDER)
            return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=search.filename,as_attachment=True)
        else:
            print("Unknown button")
        pass
    
    fields=None
    return render_template('search.html',ovf=overviewfields,path=request.path,dlbt=downloadbuttontext,sebt=searchbuttontext,dataset=set,error=error,table=table,fields=fields,req=request.form,title="Datasøk",types=types,selected=selected,nfound=nfound)
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
@login_required
def sampletype():
    return staticdata("sampletypelist")
    
@app.route("/species", methods=['POST','GET'])
@login_required
def species():
    return staticdata("specieslist")
    
@app.route("/newuser", methods=['POST','GET'])
@login_required
def newuser():
    return staticdata("users")

def staticdata(table):
    print(request.path)
    print(table)
    searchbuttontext="Søk"
    savebuttontext="Lagre"
    set=None
    error=""
    if request.method == 'POST':
        if table=="users":
            mtdt=User(request.form["username"])
        else:
            mtdt=metadatalist(table,req=request.form)
            # mtdt.getcolumns()    
        if searchbuttontext ==  request.form['button']:    
            set=mtdt.search()
        elif savebuttontext == request.form['button']:
            n=mtdt.checkexists(request.form)
            if table=="users":
                mtdt.reqset(request.form)
            if n>0:
                error="eksisterende"
            else:
# TODO: Flytt konrollen av om det eksisterer over i mtdt.save
                mtdt.save()
                set=mtdt.search()
        else:
            print("Unknown button")
    else:
        mtdt=metadatalist(table)
    print( frameinfo.filename, frameinfo.lineno)
    fields=mtdt.fields()
    print( frameinfo.filename, frameinfo.lineno)
    return render_template('metadata.html',path=request.path,sebt=searchbuttontext,sabt=savebuttontext,dataset=set,error=error,table=table,fields=fields,req=request.form,title=table.title())

   
@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.errorhandler(404)
def page_not_found2(e):
    return Response('<p>Denne siden finnes ikke...</p><p><a href="/">Tilbake</a>')
    #return render_template('htmlerror.html')
        

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Ugyldig bruker</p><p><a href="/">Tilbake</a>')
    
if __name__ == '__main__':
        
    app.secret_key = os.urandom(12)
    app.run(debug=True)
