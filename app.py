from flask import Flask, request, jsonify, render_template, redirect, flash, session
from models import db, connect_db, User, Feedback
from forms import RegisterForm,LoginForm, FeedbackForm
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

app=Flask(__name__)
bcrypt = Bcrypt()


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = 'hihi'

connect_db(app)
db.create_all()

@app.route('/')
def homepage(): 
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def show_registration():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, first_name, last_name, email)

        # db.session.add(new_user)
        db.session.commit()
        session['username'] = user.username
        flash('new user added')


        return redirect(f'/users/{user.username}')
    else:
        return render_template("/users/register.html",form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    """Show a form that when submitted will login a user."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user  = User.authenticate(username,password)

        if user:
            flash (f'welcome back, {user.username}')
            session["username"] = user.username #keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ['Invalid username/password']
    
    return render_template("users/login.html",form=form)


@app.route('/users/<username>')
def show_user(username):
    if "username" not in session:
        flash("Please log in")
        return redirect('/')

    form = FeedbackForm()
    user = User.query.get(username)
    all_feedback = Feedback.query.all()
    # process the login form first
    return render_template("users/show.html", user=user, form=form, all_feedback=all_feedback)

@app.route("/logout")
def logout():
    """log user out!"""
    session.pop("username")
    flash("good bye")
    return redirect("/")

# -------------------------------------------------------------------------
# FEEDBACK

@app.route("/users/<username>/feedback/add", methods=['GET','POST'])
def add_feedback(username):
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content,username=session['username'])
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f"/users/{session['username']}")


    return render_template('feedback/add.html',form=form)

@app.route('/feedback/<int:feedback_id>/delete',methods=['POST'])
def delete_feedback(feedback_id):
    """delete feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session:
        flash('log in first')
        return redirect('/login')

    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        return redirect('/users/<username>')
    flash("you do not have the permission to do that.")
    return redirect('/users/<username>')

@app.route('/feedback/<int:feedback_id>/update',methods=['GET','POST'])
def update_feedback(feedback_id):
    form = FeedbackForm()
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session:
        flash('log in first')
        return redirect('/login')

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{session['username']}")
    else:
        return render_template('feedback/update.html',form=form, feedback=feedback)

