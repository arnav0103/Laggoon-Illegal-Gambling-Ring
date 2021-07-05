from Tool import app, db
from Tool.models import User, TeamA, TeamB
from Tool.forms import RegistrationForm, LoginForm , TeamsAddForm
from flask import render_template,request, url_for, redirect, flash ,abort, jsonify, make_response
from flask_login import current_user, login_required, login_user , logout_user
from sqlalchemy import desc, asc
import os
from datetime import datetime

@app.route('/' , methods = ['GET' , 'POST'])
def index():
    return render_template("index.htm")

@app.route('/register' , methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.htm', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/login' , methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.check_password(form.password.data) :

            login_user(user)
            print(current_user.username)
            flash('Log in Success!')

            next = request.args.get('next')
            if next == None or not next[0] =='/':
                next = url_for('select')
            return redirect(next)
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'

    return render_template('login.htm', form=form, error = error)


@app.route('/teamsadd' , methods = ['GET' , 'POST'])
def teamadd():
    form = TeamsAddForm()
    if current_user.username != 'Admin1' and current_user.username != 'Admin2':
        print(current_user.username)
        abort(403)
    else:
        if form.validate_on_submit():
            teama = TeamA(name = form.teama.data)
            teamb = TeamB(name = form.teamb.data)
            db.session.add(teama)
            db.session.add(teamb)
            db.session.commit()
            teama.a_date=form.date.data
            db.session.commit()
            return redirect(url_for('teamadd'))
    return render_template('teamsadd.htm' , form=form)

@app.route('/teama/<ids>' , methods = ['GET' , 'POST'])
@login_required
def teama(ids):
    teama = TeamA.query.get(ids)
    teamb = TeamB.query.get(ids)
    now = datetime.now()
    if teama.a_date.strftime('%d-%m-%Y') <= now.strftime('%d-%m-%Y'):
        abort(403)
    if teama in current_user.teama:
        current_user.teama.remove(teama)
        print(current_user.teama)
        db.session.commit()
        print(current_user.teama)
        print(teama)
    elif teamb in current_user.teamb:
        current_user.teamb.remove(teamb)
        current_user.teama.append(teama)
        db.session.commit()
    else:
        current_user.teama.append(teama)
        db.session.commit()
    return redirect(url_for('select'))

@app.route('/teamb/<ids>' , methods = ['GET' , 'POST'])
@login_required
def teamb(ids):
    teama = TeamA.query.get(ids)
    teamb = TeamB.query.get(ids)
    now = datetime.now()
    if teama.a_date.strftime('%d-%m-%Y') <= now.strftime('%d-%m-%Y'):
        abort(403)
    if teamb in current_user.teamb:
        current_user.teamb.remove(teamb)
        db.session.commit()
    elif teama in current_user.teama:
        current_user.teama.remove(teama)
        current_user.teamb.append(teamb)
        db.session.commit()
    else:
        current_user.teamb.append(teamb)
        db.session.commit()
    return redirect(url_for('select'))

@app.route('/select' , methods = ['GET' , 'POST'])
@login_required
def select():
    teama = TeamA.query.order_by(TeamA.id.asc())
    teamb = TeamB.query.order_by(TeamB.id.asc())
    now = datetime.now()
    teama_name = []
    teamb_name = []
    teama_player = []
    teamb_player = []
    teamasupporter = []
    playera_id = []
    playerb_id = []
    if teama:
        for i in teama:
            teama_player.append(i.id)
        for i in teama:
            teama_name.append(i.name)
        for i in teamb:
            teamb_name.append(i.name)
        for i in current_user.teama:
            playera_id.append(i.id)
        for i in current_user.teamb:
            playerb_id.append(i.id)
        for i in teama:
            teamasupporter.append(i)
    else:
        pass
    return render_template('select.htm' , teama = teama, teamb = teamb , teama_player = teama_player , teamb_player = teamb_player , now = now,
                            teama_name = teama_name , teamb_name = teamb_name , playera_id = playera_id , playerb_id = playerb_id , teamasupporter = teamasupporter)

@app.route('/show/results', methods = ['GET', 'POST'])
@login_required
def show_score():
    teama = TeamA.query.order_by(TeamA.id.asc())
    teamb = TeamB.query.order_by(TeamB.id.asc())
    teama_name = []
    teamb_name = []
    teama_player = []
    teamasupporter = []
    teambsupporter = []
    teamalength = []
    teamblength = []
    if current_user.username != 'Admin1' and current_user.username != 'Admin2':
        print(current_user.username)
        abort(403)
    else:
        for i in teama:
            teama_name.append(i.name)
        for i in teamb:
            teamb_name.append(i.name)
        for i in teama:
            teama_player.append(i.id)
        for i in teama:
            teamasupporter.append(i)
        for i in teamb:
            teambsupporter.append(i)
        for i in teama:
            a = []
            for j in i.supporter:
                a.append(j)
            teamalength.append(len(a))
        for i in teamb:
            a = []
            for j in i.supporter:
                a.append(j)
            teamblength.append(len(a))

    return render_template('result.htm', teama = teama, teamb = teamb , teama_name = teama_name, teamb_name = teamb_name, teama_player = teama_player,
                        teamasupporter = teamasupporter , teambsupporter = teambsupporter , teamalength = teamalength , teamblength = teamblength)
if __name__ == '__main__':
    app.run(debug=True)
