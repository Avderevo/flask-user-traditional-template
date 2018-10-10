from flask import (
    Blueprint,
    request,
    flash,
    redirect,
    url_for,
    render_template,
    jsonify
)
from app import bcrypt
from flask_login import logout_user, current_user, login_required, login_user
from .form import RegisterForm, LoginForm, UserEditForm
from sqlalchemy.exc import IntegrityError
from .models.user import User
from functools import wraps


module = Blueprint('user', __name__)


def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') != current_user.id:
            flash("Not Authorized")
            return redirect(url_for('user.signup'))
        return fn(*args, **kwargs)
    return wrapper


@module.route('/')
def index():
    return render_template('user/index.html', user=User.query.first())


@module.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        try:
            new_user = User(form.username.data, form.password.data, form.email.data)
            User.save_to_db(new_user)
            flash('Thanks for registering')
        except IntegrityError as e:

            flash("Username already taken.")
            return render_template('user/signup_form.html', form=form)
        flash("User created! Welcome.")
        return redirect(url_for('user.show', id=new_user.id))
    return render_template('user/signup_form.html', form=form)


@module.route('/login/', methods=['GET', 'POST'])
def login_handler():
    form = LoginForm(request.form)
    user = User.query.filter_by(username = form.username.data).first()
    if user and User.check_password(user, form.password.data):
        flash('You have successfully logged in!')
        login_user(user)
        return redirect(url_for('.show', id = user.id))
    flash("Invalid credentials.")

    return render_template('user/login_form.html', form=form)


@module.route('/logout')
@login_required
def logout_handler():
    logout_user()
    flash('You have been signed out.')
    return redirect(url_for('user.login_handler'))


@module.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(id):
    form = UserEditForm()
    return render_template('user/edit.html', user=User.query.get(id), form=form)


@module.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@ensure_correct_user
def show(id):
    found_user = User.query.get(id)
    if request.method == "POST":
        form = UserEditForm(request.form)
        if form.validate():
            found_user.username = form.username.data
            if User.check_password(found_user, form.old_password.data):
                if form.new_password.data == form.confirm.data:
                    found_user.password = bcrypt.generate_password_hash(form.new_password.data)
                    User.save_to_db(found_user)
                    flash('User edited!')
                return redirect(url_for('user.show', id=found_user.id))
        flash('User not edited! Double check passwords.')
        return render_template('user/edit.html', user=found_user, form=form)
    return render_template('user/show.html', user=found_user)


@module.route('/<int:id>/delete', methods=['POST'])
@login_required
@ensure_correct_user
def delete_handler(id):
    found_user = User.query.get(id)
    if request.method == 'POST':
        User.delete_from_db(found_user)
        logout_user()
        return redirect(url_for('user.index'))


@module.route('/api/<int:id>', methods=['GET'])
@login_required
def get_user_api(id):

    find_user = User.query.get(id)
    users = {'name': find_user.username, 'email':find_user.email}
    return jsonify({'user': users})