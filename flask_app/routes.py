# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for
from flask import jsonify, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from .utils.blockchain.blockchain import Block, Blockchain
from pprint import pprint
import json
import random
import functools
from . import socketio
from .utils.database.generateNFT import generateRandomJPG
import os
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def nft_login_required(func):
	@functools.wraps(func)
	def nft_secure_function(*args, **kwargs):
		if "nft_email" not in session:
			return redirect(url_for("nft_login", next=request.url))
		return func(*args, **kwargs)
	return nft_secure_function

def getUser():	
	return db.reversibleEncrypt('decrypt',session['email']) if 'email' in session else None

def nft_getUser():	
	return db.reversibleEncrypt('decrypt',session['nft_email']) if 'nft_email' in session else None

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/nft_login')
def nft_login():
	return render_template('nft_login.html')

@app.route('/nft_signup', methods = ["POST","GET"])
def nft_signup():
	if request.method == "POST":
		form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
		result = db.nft_createUser(form_fields['email'], form_fields['password'])
		return json.dumps(result)
	elif request.method == "GET":
		return render_template('nft_signup.html')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
	result = db.authenticate(email=form_fields['email'],password=form_fields['password'])
	if result['success'] == 1:
		session['email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 
	return json.dumps(result)

@app.route('/process_nft_login', methods = ["POST","GET"])
def process_nft_login():
	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
	result = db.nft_authenticate(email=form_fields['email'],password=form_fields['password'])
	if result['success'] == 1:
		session['nft_email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 
	return json.dumps(result)
#######################################################################################
# CHATROOM RELATED
#######################################################################################
def isOwner(user):
	return True if user == 'owner@email.com' else False
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
	user = getUser()
	join_room('main')
	if isOwner(user):
		emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
	else:
		emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:gray;text-align: left'}, room='main')


@socketio.on('send',namespace='/chat')
def send(message):
	if isOwner(getUser()):
		emit('status', {'msg': message['msg'], 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
	else:
		emit('status', {'msg': message['msg'], 'style': 'width: 100%;color:gray;text-align: left'}, room='main')

@socketio.on('leave',namespace='/chat')
def leave(message):
	leave_room('main')
	if isOwner(getUser()):
		emit('status', {'msg': getUser() +' has left the room.','style': 'width: 100%;color:blue;text-align: right'}, room='main')
	else:
		emit('status', {'msg': getUser() +' has left the room.','style': 'width: 100%;color:gray;text-align: left'}, room='main')

#######################################################################################
# OTHER
#######################################################################################

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x     = random.choice(['I started university when I was a wee lad of 15 years.','I have a pet sparrow.','I write poetry.'])
	return render_template('home.html', fun_fact = x, user = getUser())

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)

@app.route('/projects')
def project():
	return render_template('projects.html')

@app.route('/piano')
def piano():
	return render_template('piano.html')

@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
	feedback = request.form
	values = (feedback.get('name'),feedback.get('email'),feedback.get('feedback'))
	db.insertRows(parameters=values)
	#return render_template('processfeedback.html', feedback_data = db.query("SELECT * FROM feedback"))
@app.route('/processfeedback', methods = ['GET'])
def getFeedbackPage():
	return render_template('processfeedback.html', feedback_data = db.query("SELECT * FROM feedback"))


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

#######################################
# nft
######################################
@nft_login_required
@app.route('/nftSell')
def nftSell():
	nftlist = db.getUserAllNFTs(nft_getUser())
	
	for nft in nftlist:
		pprint(nft)
		nft['path']=nft['path'].replace('flask_app','..')
	pprint(nftlist)
	return render_template('nft_sell.html',user=nft_getUser(),nftlist=nftlist)
@nft_login_required
@app.route('/nftBuy')
def nftBuy():
	nftlist = db.getOtherAllNFTs(nft_getUser())

	for nft in nftlist:
		pprint(nft)
		nft['path']=nft['path'].replace('flask_app','..')
	return render_template('nft_buy.html',user=nft_getUser(),nftlist=nftlist)
@nft_login_required
@app.route('/createNFT',methods = ['POST'])
def createNFT():
	db.createNFT(nft_getUser(),request.form.get('description'),request.form.get('token'))
	return ''

	
@nft_login_required
@app.route('/uploadNFT',methods = ['POST'])
def uploadNFT():
	data = request.form
	while True:
		filename = f"flask_app/static/nft/images/{random.randint(1, 1000000)}.jpg"
		if not os.path.exists(filename):
			break
	request.files['image'].save(filename)
	db.uploadNFT(nft_getUser(),data.get('description'),data.get('token'),filename)
	return ''
	
@nft_login_required
@app.route('/updateNFT',methods = ['POST'])
def updateNFT():
	data = request.form
	db.updateNFT(data.get('id'),data.get('description'),data.get('token'))

@nft_login_required
@app.route('/buyNFT',methods = ['POST'])
def buyNFT():
    data = request.form
    return json.dumps(db.buyNFT(nft_getUser(),data.get('nft_id')))

@nft_login_required
@app.route('/nft_owner')
def nft_owner():
    return render_template('nft_owner.html',user=nft_getUser(),recordlst=db.getAllRecords())
####################################
# for test
####################################
@app.route('/getAllUsers')
def getAllUsers():
    return db.nft_getAllUsers()

@app.route('/generateNFT')
def generateNFT():
    path = generateRandomJPG()
    return path

@app.route('/getAllNFTs')
def getAllNFTs():
    return db.nft_getAllNFTs()
