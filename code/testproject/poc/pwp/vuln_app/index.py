import os, hashlib, random
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)
app.config.from_object('__init__')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    filename = ''
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	else:
	    return 'not allowed\n', 403

    if filename == '':
	filename = '../'

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    /uploads/%s 
    ''' % (filename)

from flask import send_file

## vulnerability is in this function, one can give a filename=../index.py to read our source code
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    if allowed_file(filename) and os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],filename)):
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'],filename),  as_attachment=True)
    else:
        return 'not allowed\n', 403

if __name__ == "__main__":
    app.run(host='0.0.0.0')
