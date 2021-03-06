from convert import convert

from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload', methods=["GET", "POST"])
def upload_file():
    if request.method == 'GET':
        return render_template("home.html")
    elif request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part!')
            return render_template("home.html")
        if not request.form.get("lang"):
            flash('No selected language!')
            return render_template("home.html")
        
        file = request.files['file']
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file!')
            return render_template("home.html")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            converted_file = convert(file, request.form.get("lang"))
            flash('Successfully processed!')
            return render_template("home.html",
                                    converted_file=converted_file,
                                    img_src=UPLOAD_FOLDER+filename)
