from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import smtplib
import ssl
from email.message import EmailMessage

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL; SSLServerCertificateDigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=UYF54754;PWD=chjkrtfuykjhDHDRJG;", "", "")
#url_for('static', filename='style.css')


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

email_sender = 'sparkspurple7@gmail.com'
email_password = 'aospfzlnxtndjtox'




@app.route("/",methods=['GET'])
def home():
    if 'phone' not in session:
      return redirect(url_for('index'))
    return render_template('home.html',name='Home')
@app.route("/index")
def index():
  return render_template('index.html')
 
@app.route("/register",methods=['GET','POST'])
def register():
  if request.method == 'POST':
    subject = 'Welcome to Purple Sparks'
    username = request.form['username']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']

    if not username or not phone or not email or not password:
      return render_template('register.html',error='Please fill all fields')
    #hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    query = "SELECT * FROM user WHERE phone=? OR email=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,phone)
    ibm_db.bind_param(stmt,2,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    if not isUser:
      insert_sql = "INSERT INTO USER VALUES ('"+username+"','"+phone+"','"+email+"','"+password+"')"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.execute(prep_stmt)
      email_receiver = request.form['email']
      body = "Hello "+username+", You have been registered successfully. Welcome to Purple Sparks Community."
      e_m = EmailMessage()
      e_m['From'] = email_sender
      e_m['To'] = email_receiver
      e_m['subject'] = subject
      e_m.set_content(body)
      context = ssl.create_default_context()
      with smtplib . SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, e_m.as_string())
      return render_template('register.html',success="You can login")
    else:
      return render_template('register.html',error='Invalid Credentials')

  return render_template('register.html',name='Home')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
      phone = request.form['phone']
      password = request.form['password']

      if not phone or not password:
        return render_template('login.html',error='Please fill all fields')
        
      query = "select COUNT(*) from user where phone='"+phone+"' and password='"+password+"'"
      stmt = ibm_db.exec_immediate(conn,query)
      isUser = ibm_db.fetch_tuple(stmt)
      print(isUser,password)

      if not isUser:
        return render_template('login.html',error='Invalid Credentials')
      
      #isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

      #if not isPasswordMatch:
        #return render_template('login.html',error='Invalid Credentials')

      #session['phone'] = isUser['PHONE']
      return redirect(url_for('userhome'))
      
    return render_template('login.html')

@app.route("/admin",methods=['GET','POST'])
def adregister():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if not username or not email or not password:
      return render_template('adminregister.html',error='Please fill all fields')
    #hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    query = "SELECT * FROM admin WHERE username=? OR email=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,username)
    ibm_db.bind_param(stmt,2,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    if not isUser:
      insert_sql = "INSERT INTO ADMIN VALUES ('"+username+"','"+email+"','"+password+"')"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.execute(prep_stmt)
      return render_template('adminregister.html',success="You can login")
    else:
      return render_template('adminregister.html',error='Invalid Credentials')

  return render_template('adminregister.html',name='Home')

@app.route("/adminlogin",methods=['GET','POST'])
def adlogin():
    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']

      query = "select COUNT(*) from ADMIN where username='"+username+"' and password='"+password+"'"
      stmt = ibm_db.exec_immediate(conn,query)
      isUser = ibm_db.fetch_tuple(stmt)
      print(isUser,password)

      #isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

      #if not isPasswordMatch:
        #return render_template('login.html',error='Invalid Credentials')

      #session['phone'] = isUser['PHONE']

      if not username or not password:
        return render_template('adminlogin.html',error='Please fill all fields')

      if not isUser:
        return render_template('adminlogin.html',error='Invalid Credentials')
      
      #isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

      #if not isPasswordMatch:
        #return render_template('adminlogin.html',error='Invalid Credentials')

      #session['email'] = isUser['EMAIL']
      return redirect(url_for('addproducts'))

    return render_template('adminlogin.html',name='Home')
    
@app.route("/userhome")
def userhome():
    return render_template('home11-grid.html')    
    
@app.route("/women")
def women():
    return render_template('home2-default.html')
    
@app.route("/men")
def men():
    return render_template('home2-default.html')
    
@app.route("/kids")
def kids():
    return render_template('home2-default.html')
    
@app.route("/bags")
def bags():
    return render_template('home14-bags.html')

@app.route("/shoes")
def shoes():
    return render_template('home7-shoes.html')

@app.route("/jewellery")
def jewellery():
    return render_template('home8-jewellery.html')

@app.route("/cosmetics")
def cosmetics():
    return render_template('home5-cosmetic.html')    
    
@app.route("/contact")
def contact():
    return render_template('home2-default.html')
    
@app.route("/addproducts")
def addproducts():
    return render_template('add_food_items.html')
    
@app.route("/cart")
def cart():
    return render_template('cart-variant1.html')
    
@app.route("/checkout")
def out():
    return render_template('checkout.html')
    
@app.route("/product")
def product():
    return render_template('product-layout-1.html')
    
@app.route('/logouta')
def logouta():
    session.pop('email', None)
    return redirect(url_for('adlogin'))
    
@app.route('/logoutu')
def logoutu():
    session.pop('phone', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)