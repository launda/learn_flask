from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = # add your Heroku Postgres database URL here
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/learningflask'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/learningflask'
# sqlalchemy.exc.ProgrammingError: (mysql.connector.errors.ProgrammingError) 1045 (28000): 
# Access denied for user 'root'@'localhost' (using password: NO) 
# This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.

# also if try connect as another db users loma 'mysql+mysqlconnector://loma@localhost
# Access denied for user 'loma'@'%' to database 'learningflask'  <-- this user no access to this database
# fix - supply password with username e.g bou:bou and only authorised users who can access db and erad/write to it
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://bou:bou@localhost/learningflask'

# ModuleNotFoundError: No module named 'MySQLdb' if don't specify mysql+mysqlconnector
#connection_string = 'mysql+mysqlconnector://' + database_user + ':' + database_password + '@' + database_host + ':' + database_port + '/' + database_name

db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data,\
                     form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('home'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if 'email' in session:
    return redirect(url_for('home'))

  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("login.html", form=form)
    else:
      email = form.email.data 
      password = form.password.data 

      user = User.query.filter_by(email=email).first()
      if user is not None and user.check_password(password):
        session['email'] = form.email.data 
        return redirect(url_for('home'))
      else:
        return redirect(url_for('login'))

  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
  if 'email' not in session:
    return redirect(url_for('login'))

  form = AddressForm()

  places = []
  my_coordinates = (-27.570278, 153.008056)

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('home.html', form=form)
    else:
      # get the address
      address = form.address.data 

      # query for places around it
      p = Place()
      my_coordinates = p.address_to_latlng(address)
      places = p.query(address)

      # return those results
      return render_template('home.html', form=form, \
        my_coordinates=my_coordinates, places=places)

  elif request.method == 'GET':
    return render_template("home.html", form=form, \
      my_coordinates=my_coordinates, places=places)

if __name__ == "__main__":
  app.run(debug=True)