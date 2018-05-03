from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, make_response
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from request import REQUEST
from functools import wraps

app = Flask(__name__)

#CONFIG MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#Index Page
@app.route('/')
def index():
	return render_template('index.html')

#About Page
@app.route('/about')
def about():
	return render_template('about.html')

#Articles Page to get all articles from navigation bar
@app.route('/articles')
def articles():
	#Create cursor
	cur = mysql.connection.cursor()

	#Execute Query
	result = cur.execute('SELECT * from articles')

	#Get all articles
	articles = cur.fetchall()

	#Close Connection
	cur.close()

	if result > 0:
		return render_template('articles.html', articles = articles)
	else:
		msg = 'No Article Found'
		return render_template('articles.html', msg = msg)

	return render_template('dashboard.html')

#Get specific article information when clicked
@app.route('/article/<string:id>/')
def article(id):
	#Create cursor
	cur = mysql.connection.cursor()

	#Get article by id
	result = cur.execute('SELECT * from articles WHERE id = %s', [id])

	article = cur.fetchone()

	#Close connection
	cur.close()

	return render_template('article.html', article = article)

#Registration Form  class to validate the all fields
class RegisterForm(Form):
	name = StringField('Name', [validators.length(min=1, max=50)])
	username = StringField('Username', [validators.length(min=4, max=25)])
	email = StringField('Email', [validators.length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password')

#Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
	#Get Registration Form
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
			#Get Register form fields
			name = form.name.data
			email = form.email.data
			username = form.username.data
			password = sha256_crypt.encrypt(str(form.password.data))

			#Create Cursor
			cur = mysql.connection.cursor()

			#Execute Query
			cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

			#Commit to DB
			mysql.connection.commit()

			#Close Connection
			cur.close()

			flash('You are now registered, can log in', 'success')

			return redirect(url_for('index'))

	return render_template('register.html', form = form)

#Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		#Get Form Fields
		username = request.form['username']
		password_candidate = request.form['password']

		#Create Cursor
		cur = mysql.connection.cursor()

		#Execute Query
		result = cur.execute('SELECT * from users WHERE username = %s', [username])

		if result > 0:
			#Get stored hash
			data = cur.fetchone()
			password = data['password']

			#Compare passwords
			if sha256_crypt.verify(password_candidate, password):
				#Passed
				session['logged_in'] = True
				session['username'] = username

				flash('You are now logged in', 'success')

				return redirect(url_for('dashboard'))
			else:
				error = 'Invalid Login'
				return render_template('login.html', error = error)
		else:
			error = 'Username Not Found'
			return render_template('login.html', error = error)

		#Close connection
		cur.close()

	return render_template('login.html')

#Python Decorators
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap

#Logout Route
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You are successfully logged out', 'success')
	return redirect(url_for('login'))

#Dashboard Route
@app.route('/dashboard')
@is_logged_in
def dashboard():
	#Create cursor
	cur = mysql.connection.cursor()

	#Execute Query
	result = cur.execute('SELECT * from articles')

	#Get all articles
	articles = cur.fetchall()

	#Close Connection
	cur.close()

	if result > 0:
		return render_template('dashboard.html', articles = articles)
	else:
		msg = 'No Article Found'
		return render_template('dashboard.html', msg = msg)

	return render_template('dashboard.html')

#Article Form class to validate all the fields of add article
class ArticleForm(Form):
	title = StringField('Title', [validators.length(min = 1, max = 200)])
	body = TextAreaField('Body', [validators.length(min = 30)])

#Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
	form = ArticleForm(request.form)
	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']

		#Create Cursor
		cur = mysql.connection.cursor()

		#Execute Query
		cur.execute("INSERT INTO articles(title, author, body) VALUES (%s, %s, %s)", (title, session['username'], body))

		#Commit DB
		mysql.connection.commit()

		#Close connection
		cur.close()

		flash('Article Created', 'success')

		return redirect(url_for('dashboard'))

	return render_template('add_article.html', form = form)

#Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
#Here get method is used to fetch the page from the server and when submit button is clicked post request is send to submit the details.
@is_logged_in
def edit_article(id):
	#Get Form
	form = ArticleForm(request.form)

	#Create cursor
	cur = mysql.connection.cursor()

	#Get article by id
	result = cur.execute('SELECT * from articles WHERE id = %s', [id])

	article = cur.fetchone()

	#Populate article form fields for article got from stored articles from database
	form.title.data = article['title']
	form.body.data = article['body']

	if request.method == 'POST' and form.validate():
		title = request.form['title']
		body = request.form['body']

		#Create cursor
		cur = mysql.connection.cursor()

		#Update article in database
		cur.execute('UPDATE articles SET title=%s, body=%s WHERE id = %s', (title, body, id))

		#commit DB
		mysql.connection.commit()

		#Close connection
		cur.close()

		flash('Article Updated', 'success')

		return redirect(url_for('dashboard'))

	return render_template('edit_article.html', form = form)

#Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
#Delete Article
def delete_article(id):
	#Create Cursor
	cur = mysql.connection.cursor()

	#Execute Query
	cur.execute("DELETE FROM articles where id = %s", [id])

	#Query to reset ID of articles table 
	cur.execute('SET @num := 0')
	cur.execute('UPDATE articles SET id = @num := (@num + 1)')
	cur.execute('ALTER TABLE articles AUTO_INCREMENT = 1')
	#Commit DB
	mysql.connection.commit()

	#Close connection
	cur.close()

	flash('Article Deleted', 'success')

	return redirect(url_for('dashboard'))

if __name__ == '__main__':
	app.secret_key = 'secret123'
	app.run(debug=True)
