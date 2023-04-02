from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key='sample'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'login'

# connecting to MySQL database
import pymysql as pms 
db = pms.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

cur = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

# home page after logging in
@app.route('/home')
def home():
    return render_template('home.html',username=session['username'])

# function to authenticate credentials
@app.route('/login',methods=['GET','POST'])
def login():
    msg=''

    if request.method=='POST':
        print("login inside")
        username = request.form['username']
        password = request.form['password']
        cur.execute('select * from user where username=%s and password=%s',(username,password))
        record = cur.fetchone()
        
        if record: # if record exists create a logged in session
            print("login exists")
            session['loggedin']=True
            session['username']=record[0]
            return redirect(url_for('home'))
        else: # incorrect login credentials
            print("login doesn't exist")
            msg = 'Incorrect username/password. Try again!'

    return render_template('index.html',msg=msg)

# retrieve classification model built using DecisionTrees
import pickle
model = pickle.load(open('model.pkl','rb'))

# predict function to deploy the model retrieved
@app.route("/predict",methods=['post'])
def pred():
    result=''
    features = [int(i) for i in (request.form.values())]
    pred = model.predict([features])
    if pred == [0]:
        result = "The customer 'has' purchased the product."
    else:
        result = "The customer 'has not' purchased the product."
    return render_template("success.html",data=result)

# main function
if __name__ == '__main__':
    app.run(host="localhost",port=5000,debug=True) # debug true automatically reloads changes
