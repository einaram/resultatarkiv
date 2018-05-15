import os
from xlrd import open_workbook
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import hashlib
import platform
from resark.processexcel import excelfile


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
    return render_template('template.html', my_string="Wheeeee!", 
        my_list=[0,1,2,3,4,5], title="Index", current_time=datetime.datetime.now())

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
  
    return render_template('upload.html', my_string="Foo", 
        my_list=[6,7,8,9,10,11], title="Upload excel file", current_time=datetime.datetime.now())

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
    return render_template('process.html', my_string= request.files['file'].filename, 
        title="Processing file", current_time=datetime.datetime.now(),okheader=importfile.validheader(),
        okdata=importfile.validdata(),valuewarnings=importfile.valuewarning,md5=importfile.md5)


@app.route("/about")
def about():
    return render_template('about.html', my_string="Bar", 
        my_list=[12,13,14,15,16,17], title="About", current_time=datetime.datetime.now())

@app.route("/contact")
def contact():
    return render_template('template.html', my_string="FooBar"
        , my_list=[18,19,20,21,22,23], title="Contact Us", current_time=datetime.datetime.now())


if __name__ == '__main__':
    app.run(debug=True)
