from flask import Flask, render_template,json,request
from flaskext.mysql import MySQL


app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'

mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()
# mysql.get_db().cursor()

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    # create user code will be here !!
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    cursor.callproc('sp_createUser',(_name,_email,_password))
    data = cursor.fetchall()
    # validate the received values
    # if _name and _email and _password:
    #     return json.dumps({'html':'<span>All fields good !!</span>'})
    # else:
    #     return json.dumps({'html':'<span>Enter the required fields</span>'})
    if len(data) == 0:
    	conn.commit()
    	return json.dumps({'message':'User created successfully !'})
    else:
    	return json.dumps({'error':str(data[0])})

if __name__ == "__main__":
    app.run()