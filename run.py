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

        
@app.route("/search")
def search():
    searchbuttontext="Søk"
    return render_template('search.html',sebt=searchbuttontext)
        
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

@app.route("/project", methods=['POST','GET']) 
def project():
    return staticdata("projects")

 
@app.route("/habitat", methods=['POST','GET']) 
def habitat():
    return staticdata("habitatlist")

@app.route("/samplecat", methods=['POST','GET']) 
def samplecat():
    return staticdata("samplecatlist")

@app.route("/topic", methods=['POST','GET']) 
def topic():
    return staticdata("topiclist")
    
@app.route("/quantity", methods=['POST','GET']) 
def quantity():
    return staticdata("quantitylist")
    
@app.route("/metadata", methods=['POST','GET'])
def metadata():
    return staticdata("metadatalist")

@app.route("/nuclide", methods=['POST','GET'])
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

@app.route("/contact")
def contact():
    return render_template('template.html', my_string="FooBar"
        , my_list=[18,19,20,21,22,23], title="Contact Us", current_time=datetime.datetime.now())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('htmlerror.html'), 404
        

if __name__ == '__main__':
    app.run(debug=True)
