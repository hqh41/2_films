# coding=utf-8

from __future__ import unicode_literals, print_function

from datetime import datetime
from flask import Flask, render_template, session, flash, request, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import random
from db import Player
import game
import Correct



def main_func(x):
	return game.main(x)


def egal(str1, str2):
	return str1.strip() == str2.strip()

def bonus():
	session["score"] += 1
	flash("And it's a combo! +1")




app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['DEBUG'] = False  # 手动启动

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@app.route('/about/', methods=['GET'])
def about():
	return render_template('about.html')


@app.route('/the_best_scores/', methods=['GET'])
def the_best_scores():
	players_F = Player.objects(diff='F').order_by('-score').limit(10)
	top_10_F = [[x.nickname, x.score] for x in players_F]
	players_M = Player.objects(diff='M').order_by('-score').limit(10)
	top_10_M = [[x.nickname, x.score] for x in players_M]
	players_D = Player.objects(diff='D').order_by('-score').limit(10)
	top_10_D = [[x.nickname, x.score] for x in players_D]
	return render_template('the_best_scores.html', top_10_F=top_10_F, top_10_M=top_10_M, top_10_D=top_10_D)


def get_player(_id):
	try:
		player = Player.objects.get(id=_id)
		return player
	except Player.DoesNotExist:
		return None


@app.route('/create/', methods=['GET', 'POST'])
def create():
	diff_dict = {
		'F': 25,
		'M': 50,
		'D': 100
	}
	player_id = session.get('player')
	if player_id:
		player = get_player(player_id)
		if player:
			return redirect(url_for('mode'))
		else:
			session.pop('player', None)

	form = request.form
	if not form.get('name'):
		return render_template('create.html')
	else:
		nickname = form.get('name')
		diff = form.get('options')
		player = Player(nickname=nickname, diff=diff)
		player.created = datetime.now()
		player.save()
		#save之后自动生成player.id
		flash('Welcome, {}'.format(player.nickname))
		session['player'] = unicode(player.id)
		session['diff'] = diff_dict[diff]
		if session["diff"] == 25:
			session["difficulte"] = "Easy"
		elif session["diff"] == 50:
			session["difficulte"] = "Normal"
		else:
			session["difficulte"] = "Hard"
		session['count'], session['score'] = 1, 0
		session['bonus'] = 0
		#session['malus'] = 0
		return redirect(url_for('mode'))


@app.route('/mode/', methods=['GET', 'POST'])
def mode():
	player_id = session.get('player', None)
	if player_id is None:
		return redirect(url_for('create'))
	else:
		player = get_player(player_id)
		if player is None:
			session.pop('player', None)
			return redirect(url_for('create'))
	#post执行的部分
	#redirect默认是get方法
	if request.method == 'POST':
		m = request.form.get('optionsMode')
		if m == "Square":
			session['mode'] = "carre"
			return redirect(url_for('carre'))
		elif m == "50:50":
			session['mode'] = "duo"
			return redirect(url_for('duo'))
		else:
			session['mode'] = "cache"
			return redirect(url_for('cache'))

   # session['count'] = 1
   # session['score'] = 1
   #get方法的执行部分
	if session['count'] == 11:
		score = session['score']
		session.pop('count')
		session.pop('score')
		session.pop('player')
		players = Player.objects(diff=player.diff).order_by('-score').limit(10)
		top_10 = [[x.nickname, x.score] for x in players]
		return render_template('end.html', score=score, top_10=top_10)

	film1, film2, option_list, session['name'] = main_func(session['diff'])
	#print(session['name'])
	cover1 = game.get_cover(film1)
	cover2 = game.get_cover(film2)

	session['film_1'] = film1['title']
	session['film_2'] = film2['title']
	session['option_a'] = option_list[0]
	session['option_b'] = option_list[1]
	session['option_c'] = option_list[2]
	session['option_d'] = option_list[3]
	session['cover1'] = cover1
	session['cover2'] = cover2
	return render_template('select_mode.html')


@app.route('/carre/', methods=['GET', 'POST'])
def carre():
	player_id = session.get('player', None)
	if player_id is None:
		return redirect(url_for('create'))
	else:
		player = get_player(player_id)
		if player is None:
			session.pop('player', None)
			return redirect(url_for('create'))

	if request.method == 'POST':
		session['count'] += 1
		answer = request.form.get('optionsRadios')
		s = session['name']
		a = answer.encode('ascii', 'ignore')
		if egal(s, a):
			session['score'] += 3
			#选该模式，只要连续答对三次，就再加一分
			session['bonus'] += 1
			session['malus'] = 0
			if session['bonus']>=3:
				bonus()
			else:
				flash("Correct! 3 points for the champ")
			player.score = session['score']
			player.save()
		else:
			session['bonus'] = 0
			session['malus'] += 1
			if session['malus']>=3:
				flash ("May the force be with you!")
			else:
				flash("Wrong! Try 50:50 next time")
		return redirect(url_for('mode'))
	return render_template('carre.html')


@app.route('/duo/', methods=['GET', 'POST'])
def duo():
	player_id = session.get('player', None)
	if player_id is None:
		return redirect(url_for('create'))
	else:
		player = get_player(player_id)
		if player is None:
			session.pop('player', None)
			return redirect(url_for('create'))

	option_list = [session['option_a'], session['option_b'], session['option_c'],
				   session['option_d']]
	option_a = random.choice(option_list)
	while option_a == session['name']:
		option_a = random.choice(option_list)
	options_duo = [option_a, session['name']]
	random.shuffle(options_duo)
	option_a = options_duo[0]
	option_b = options_duo[1]

	if request.method == 'POST':
		session['count'] += 1
		answer = request.form.get('optionsRadios')
		s = session['name']
		a = answer.encode('ascii', 'ignore')

		if egal(s, a):
			session['score'] += 1
			session['bonus'] += 1
			session['malus'] = 0
			if session['bonus']>=3:
				bonus()
			else:
				flash("Correct! Don't be happy it was not that hard")
			player.score = session['score']
			player.save()

		else:
			session['bonus'] = 0
			session['malus'] += 1
			if session['malus']>=3:
				flash ("May the force be with you!")
			else:
				flash("Wrong! Shame on you..")
		return redirect(url_for('mode'))
	return render_template('duo.html', option_a=option_a, option_b=option_b)


@app.route('/cache/', methods=['GET', 'POST'])
def cache():
	player_id = session.get('player', None)
	if player_id is None:
		return redirect(url_for('create'))
	else:
		player = get_player(player_id)
		if player is None:
			session.pop('player', None)
			return redirect(url_for('create'))

	if request.method == 'POST':
		session['count'] += 1
		answer = request.form.get('reponseCache')
		print(Correct.similar(answer, session['name']))
		if Correct.similar(answer, session['name']) >= 0.78:
			session['score'] += 5
			session['bonus'] += 1
			session['malus'] = 0
			if session['bonus']>=3:
				bonus()
			else:
				flash("Correct! Did you cheat?")
			player.score = session['score']
			player.save()
			
		else:
			session['bonus'] = 0
			session['malus'] += 1
			if session['malus']>=3:
				flash ("May the force be with you!")
			else:
				flash("Wrong! Not even close") 
		return redirect(url_for('mode'))
	return render_template('cache.html')

@app.route('/quit', methods=['GET'])
def quit():

	player_id = session.get('player', None)
	if player_id:
		player = get_player(player_id)
		session.pop('player', None)
		player.delete()
		   

	session.pop('count')
	session.pop('score')
	return redirect('/')


if __name__ == '__main__':
	manager.run()
