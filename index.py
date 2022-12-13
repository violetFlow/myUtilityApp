from crypt import methods
from service.icsReader import icsReader
import os
from flask import Flask
from flask import render_template
from flask.globals import request
from flask.helpers import url_for
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import click

# const
UPLOAD_FOLDER = '/app/upload'
ALLOWED_EXTENSIONS = {'ics'}

# app configs
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@172.18.0.3:5432/postgres"
db = SQLAlchemy(app)

class Account(db.Model):
    accountid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(64))
    pw = db.Column(db.String(64))
    category = db.Column(db.String(64))
    etc = db.Column(db.String(120))

@app.before_first_request
def initdb():
    db.create_all()

# root
@app.route("/")
def init():
    return render_template('index.html')

# ics
@app.route('/ics/analysis-form')
def ics_analysis_form():
    return render_template('ics/analysis-form.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ics/upload', methods=['POST'])
def upload_file():
    '''
        Check if the post request has the file part
    '''
    if 'file' not in request.files:
        print('No file part')
        return redirect(request.url)

    '''
        If the user does not select a file, the browser submits an 
        empty file witout a filename.
    '''
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)

    '''
        Get total time working
        
    '''
    if file and allowed_file(file.filename):
        startDate = request.form['start-date']
        endDate = request.form['end-date']
        print(startDate)
        print(endDate)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        resultList = icsReader.get_total_time_working(filename, startDate, endDate)
        return  render_template('ics/result.html',
                                resultList=resultList[0], 
                                dateList=resultList[1], 
                                filename=file.filename,
                                startDate=startDate,
                                endDate=endDate
                                )

# account
@app.route('/account/list', methods=['GET'])
def account_list():
    try:
        # accountテーブルの並び順をcategory順で指定
        datas = Account.query.order_by(Account.category).all()
        print(0)
    except print(0):
        pass

    return render_template('account/list.html', lists=datas)

@app.route('/account/register-form', methods=['GET'])
def account_register_form():
    return render_template('account/register-form.html')

@app.route('/account/regist', methods=['POST'])
def register():
    # データバインド
    id = request.form['id']
    pw = request.form['pw']
    category = request.form['category']
    etc = request.form['etc']
    newAccount = Account(id=id, pw=pw, category=category, etc=etc)

    # db処理
    try:
        db.session.add(newAccount)
        db.session.commit()
        print(0)
    except print(0):
        pass
    return redirect('/')

@app.route('/account/edit-form/')
@app.route('/account/edit-form/<int:accountid>')
def account_edit_form(accountid):
    try:
        account = db.session.get(Account, accountid)
        print(0)
    except print(0):
        pass
    return render_template('account/edit-form.html', account=account)

@app.route('/account/delete/')
@app.route('/account/delete/<int:accountid>', methods=['GET'])
def account_delete(accountid):
    try:
        account = Account.query.filter_by(accountid=accountid).first()
        db.session.delete(account)
        db.session.commit()
        print(0)
    except print(0):
        pass
    return render_template('index.html') 

@app.route('/account/edit-form/edit', methods=['POST'])
def account_edit():
    account = Account.query.filter_by(accountid=request.form['accountid']).first()
    account.id = request.form['id']
    account.pw = request.form['pw']
    account.category = request.form['category']
    account.etc = request.form['etc']

    db.session.commit()

    return redirect('/')

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, debug=True)
