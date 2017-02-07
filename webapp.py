from flask import Flask , request , render_template
from Database import *

app = Flask(__name__)

engine = create_engine('sqlite:///fizzbuzz.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine, autoflush=False)
session = DBsession()

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')





if __name__== '__main__':
	app.run(debug=True)
