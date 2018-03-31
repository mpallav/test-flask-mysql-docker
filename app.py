from flask import Flask, render_template, request, flash
from flaskext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mypassword'
app.config['MYSQL_DATABASE_DB'] = 'userinfo'
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.secret_key = "super secret key"


mysql.init_app(app)
conn=mysql.connect()
cursor = conn.cursor()

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/update')
def update():
    return render_template('update.html')
@app.route('/add_data', methods=['POST'])
def add_data():
    name=request.form['name']
    address=request.form['address']
    phone=request.form['phone']
    cursor.execute("INSERT INTO user(name, address, phone) VALUES(%s,%s,%s)",(name,address,phone))
    #commit to DB
    conn.commit()
    flash ('Update Success')
    return render_template('update.html')

@app.route('/findyourdata', methods=['GET','POST'])
def findyourdata():
    return render_template('findyourdata.html')
@app.route('/results', methods=['GET','POST'])
def results():
    name=request.form['name']
    cursor.execute("SELECT * from user where name like %s",("%" + name + "%",))
    results = cursor.fetchall()
    return render_template('results.html', results=results)
@app.route('/dumpall', methods=['GET'])
def dumpall():
    cursor.execute("SELECT * from user") 
    results = cursor.fetchall()
    return render_template('results.html', results=results)
 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
