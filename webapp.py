from flask import Flask
from model import *

app = Flask(__name__)

engine = create_engine('sqlite:///fizzbuzz.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine, qutoflush=False)
session = DBsession()

@app.route('/')
def hello_world():
	return 'Hello World'

if __name__== '__main__':
	app.run()
