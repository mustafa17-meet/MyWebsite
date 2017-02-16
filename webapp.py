from flask import Flask , request , render_template , redirect, url_for, flash
from flask import session as sign_in_session
from Database import *

app = Flask(__name__)
app.secret_key = "yyuditsyidsrysrxeazedxe"
engine = create_engine('sqlite:///Database.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine, autoflush=False)
session = DBsession()

def verify_password(email,password):
	user= session.query(User).filter_by(email=email).first()
	if not user or not user.verify_password(password):
		return False
	else:
		return True


@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
	if request.method == 'GET':
		return render_template('sign_in.html')
	elif request.method=='POST':
	   email=request.form['username']
	   password=request.form['password']
	   if email is None or password is None:
	   		flash("Missing arguments")
	   		return redirect(url_for(sign_in))
	   if verify_password(email, password):
	   		user=session.query(User).filter_by(email=email).one()
	   		flash('Login Successful, weclome, %s' % user.name)
	   		sign_in_session['name']=user.name
	   		sign_in_session['email']=user.email
	   		sign_in_session['id']=user.id
	   		return redirect(url_for('home'))
	   else:
	   		flash('Incorrect username/password combination')
	   		return redirect(url_for('sign_in'))
#		name = request.form['username']
#		password = request.form['password']
#		user = session.query(User).filter_by(name=name).first()
#		session.commit()
#		if :
#			pass
#		if user.password_hash == password:
#			return redirect(url_for('home_page'))
#		else:
#			return render_template(url_for('sign_in.html'))


@app.route('/make_a_game', methods = ['GET','POST'])
def make_a_game():
    if request.method == 'POST':
        when = request.form['when']
        where = request.form['where']
        age_below = request.form['age_below']
        phone_number = request.form['phone_number']
        if when == "" or where == "" or phone_number == "" :
            flash("Your form is missing arguments")
            return redirect(url_for('make_a_game'))
            return redirect(url_for('make_a_game'))
        newGame = Match(time = when, location = where,game_complete = False, age_below=age_below, phone_number = phone_number)
        session.add(newGame)
        session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('make_a_game.html')

@app.route('/about_us')
def about_us():
	return render_template('about_us.html')


@app.route('/sign_up', methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        date_of_birth = request.form['date_of_birth']
        if name == "" or email == "" or password == "" or date_of_birth == "" :
            flash("Your form is missing arguments")
            return redirect(url_for('sign_up'))
        if session.query(User).filter_by(email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('sign_up'))
        user = User(name = name, email=email, date_of_birth = date_of_birth)
        user.hash_password(password)
        session.add(user)
        session.commit()
        flash("User Created Successfully!")
        return redirect(url_for('sign_in'))
    else:
        return render_template('sign_up.html')



@app.route('/make_a_team', methods=['GET','POST'])
def make_a_team():
	if request.method == 'GET':
		return render_template('make_a_team')

@app.route("/")
def home():
	allGames = session.query(Match).all()
	return render_template('home.html', allGames = allGames)


if __name__== '__main__':
	app.run(debug=True)
