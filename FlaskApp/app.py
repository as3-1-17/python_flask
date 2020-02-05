from flask import Flask,render_template, request, json, redirect, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
#from flask.ext.session import Session

app = Flask(__name__)
app.secret_key = 'my_secret_key'
mysql = MySQL()
 

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Admin1234'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3307
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

@app.route('/cerrar',methods=['POST'])
def cerrar():
    session.clear()
    return redirect("/")
    

@app.route('/showLoged')
def showLoged():
    return 'OK'
@app.route('/loged')
def loged():
    return render_template('loged.html')


@app.route('/showLogIn')
def showLogIn():
    #if clear() in session:
     #   return render_template('login.html')
    if 'user_id' in session:
        user_id = session ['user_id']
        print (user_id)
        return redirect('loged')
    else:
        return render_template('login.html')

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    # create user code will be here !!
    #Desde el signup envia los datos del login en POST, queda comprobar si recoge los datos aqui
    #se han cambiado las variables _name,_email,_hashed_password
    #link: https://code.tutsplus.com/es/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
    # read the posted values from the UI
    
    p_name = request.form['inputName']
    p_email = request.form['inputEmail']
    _password = request.form['inputPassword']

    _hashed_password = generate_password_hash(_password)
    p_password = _hashed_password
    #print(p_name,p_email,p_password)

    cursor.callproc('crear_usuario',(p_name,p_email,p_password))

    # validate the received values
    '''if _name and _email and _password:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})'''
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])}) 

@app.route('/logIn',methods=['POST'])
def logIn():
    p_email = request.form['inputEmail']
    _password = request.form['inputPassword']
    print (p_email,_password)

   
    P_hash =  cursor.execute ("select user_password from tbl_user where user_username = '"+ p_email +"'")
    P_hash = cursor.fetchall()
    P_hash = str(P_hash)
    P_hash = P_hash[3:][:-5]
    print (P_hash)
    #print (P_hash[2:][:-4])
    
    # print(user.password, ' ', form.password.data, ' ', check_password_hash(user.password, form.password.data))
    if check_password_hash(P_hash,_password):
        session['user_id'] = p_email
        #session['username'] = user.name
        print("Logeado correctamente")
        return redirect('showLoged')
    else:
        return json.dump ({'error'})
    return redirect(url_for('showSignUp'))    

if __name__ == "__main__":
    app.run()
