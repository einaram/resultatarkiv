import os
from xlrd import open_workbook
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import hashlib
import platform
from resark.processexcel import excelfile
from resark.staticdata import metadatalist


if platform.system()=='Windows':
	UPLOAD_FOLDER = 'c:/windows/temp/'
else:
	UPLOAD_FOLDER = '/tmp'
	
ALLOWED_EXTENSIONS = set(['xls','xlsx'])

import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter

@app.route("/")
def template_test():
    return render_template('template.html', my_string=request.environ.get('REMOTE_USER'), 
        my_list=[], title="Resultatarkiv", current_time=datetime.datetime.now())

@app.route("/home")
def home():
    return render_template('template.html', my_string="Foo", 
        my_list=[6,7,8,9,10,11], title="Home", current_time=datetime.datetime.now())

@app.route("/upload", methods=['GET', 'POST'])
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
def importdata():
    filepath=request.form['filepath']
    importfile=excelfile(filepath)
    importfile.importdata()
    return render_template('importdata.html', title="Importerer data",filepath=filepath,md5=importfile.md5)

@app.route("/metadata", methods=['POST','GET'])
def metadata():
    searchbuttontext="Søk"
    savebuttontext="Lagre"
    # TODO: Cleaner implementation!
    id=""
    name=""
    shortname=""
    description=""
    set=None
    error=""
    if request.method == 'POST':
        mtdt=metadatalist(req=request.form)
        if searchbuttontext ==  request.form['button']:    
            set=mtdt.search()
        elif savebuttontext == request.form['button']:
            md=metadatalist(name=request.form["name"])
            n=len(md.search(partial=False))
            md=metadatalist(shortname=request.form["shortname"])
            print(n)
            n=n+len(md.search(partial=False))
            print(n)
            if n>0:
                error="eksisterende"
                print(error)
            else:
                mtdt.save()
                set=mtdt.search()
        else:
            print("Unknown button")
        id=request.form["id"]
        name=request.form["name"]
        shortname=request.form["shortname"]
        description=request.form["description"]
        print(request.form)
        print(description)
    return render_template('metadata.html',sebt=searchbuttontext,sabt=savebuttontext,dataset=set,idval=id,nameval=name,shortname=shortname, description=description,error=error)
    
@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/contact")
def contact():
    return render_template('template.html', my_string="FooBar"
        , my_list=[18,19,20,21,22,23], title="Contact Us", current_time=datetime.datetime.now())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('htmlerror.html'), 404
        

if __name__ == '__main__':
    app.run(debug=True)
