from flask import*
# initialize application
import pymysql 
import sms
# connect to DB
connection= pymysql.connect(host="localhost", user="root", password="", database="heroesokogardens")
# create a cursor 
cursor= connection.cursor()

app= Flask(__name__)
app.secret_key="@123wgsfdhgdgdsjg"
#home route
@app.route("/home")
def home():
  # select from DB 
  sql1="SELECT*FROM products where product_cartegory='electronics'"
  sql2="SELECT*FROM products where product_cartegory='furniture'"
  sql3="SELECT*FROM products where product_cartegory='clothes'"
  # execute sql 
  cursor1=connection.cursor()
  cursor1.execute(sql1)
  cursor2=connection.cursor()
  cursor2.execute(sql2)
  cursor3=connection.cursor()
  cursor3.execute(sql3)
  # fetch rows 
  electronics =cursor1.fetchall()
  furniture=cursor2.fetchall()
  clothes=cursor3.fetchall()
  return render_template('home.html', electronics=electronics, furniture=furniture, clothes=clothes)


# singleitem route
@app.route("/singleitem/<product_id>")  
def single(product_id):
  # select from DB
  sql="SELECT* FROM products where product_id=%s"
  # execute sql
  cursor1=connection.cursor()
  cursor1.execute(sql,(product_id))
  # fetch single product 
  product=cursor1.fetchone()
  return render_template("single.html", product=product)


# upload route
@app.route("/upload", methods=["POST", "GET"])
def upload():
  if request.method =="POST":
    # upload here 
    product_name=request.form["product_name"]
    product_desc=request.form["product_desc"]
    product_cost=request.form["product_cost"]
    product_cartegory=request.form["product_cartegory"]
    product_image_name=request.files["product_image_name"]
    product_image_name.save("..static/images/" + product_image_name.filename)
    # our data 
    data=(product_name, product_desc, product_cost, product_cartegory, product_image_name.filename)
    sql="insert into products(product_name, product_desc, product_cost, product_cartegory, product_image_name) values(%s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    connection.commit()
    return render_template('upload.html', msg="upload successful") 
  else:
    return render_template("upload.html")
  
#register
@app.route("/register", methods=["POST","GET"])
def register():
    if request.method=="GET":
      return render_template("register.html")
    else:
      username=request.form["username"]
      email=request.form["email"]
      phone=request.form["phone"]
      password1=request.form["password1"]
      password2=request.form["password2"]
    if len(password1)<8:
      return  render_template("register.html", error="password must be atleast 8 characters")
    elif password1!=password2:
      return  render_template("register.html", error="passwords don't match")
    else:
      sql= "insert into users(username, email, phone, password) values(%s, %s, %s, %s)"
      cursor.execute(sql,(username, email, phone, password1))
      connection.commit()
      sms.send_sms(phone,"thank you for registration")
      return render_template("register.html", success="Registration successful")


#login
@app.route("/login", methods=["POST", "GET"])    
def login():
  if request.method=="GET":
    return render_template("login.html")
  else:
    username=request.form["username"]
    password=request.form["password"]

    sql="SELECT * FROM users WHERE username= %s and password=%s"
    cursor.execute(sql,(username, password))
    
    # check if user exist 
    if cursor.rowcount ==0:
      return render_template("login.html", error="invalid login credentials")
    else:
      session['key']=username
      return redirect("/home")


#logout
@app.route("/logout")
def logout():
  session.clear()
  return redirect("/login")


# Below we only need to use a POST, as posted in our Single item
@app.route('/mpesa', methods = ['POST'])
def mpesa():
    # Receive the amount and phone from single item
    phone = request.form['phone']
    amount = request.form['amount']
    # import mpesa.py module
    import mpesa
    # Call the SIM Toolkit(stk) push function present in mpesa.py
    mpesa.stk_push(phone, amount)
    # SHow user below message.
    return '<h3>Please Complete Payment in   Phone and we will deliver in minutes</h3>' \
    '<a href="/home" class="btn btn-dark btn-sm">Back to Products</a>'


@app.route('/vendors', methods=['POST', 'GET'])
def vendors():
 if request.method =="POST":
     firstname=request.form['firstname']
    #  firstname=request.form["firstname"]
     lastname=request.form["lastname"]
     county=request.form["county"]
     password1=request.form["password1"]
     password2=request.form["password2"]
     email=request.form['email']
     if len(password1)<8:
          return  render_template("vendors.html", error="password must be atleast 8 characters")
     elif password1!=password2:
          return  render_template("vendors.html", error="passwords don't match")
     else:
      sql= "insert into vendors(firstname,lastname, county, password, email) values(%s, %s, %s, %s, %s)"
      cursor.execute(sql,(firstname,lastname, county, password1, email))
      connection.commit()
      # sms.send_sms(phone,"thank you for registration")
      return render_template("vendors.html", success="Registration successful")


 else:
    return render_template("vendors.html")
    







if __name__ =="__main__":
#run application
  app.run(debug=True)