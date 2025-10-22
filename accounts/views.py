import os

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from accounts.models import User
from db_extensions import db
from utils import allowed_file, save_uploaded_image

accounts = Blueprint('accounts', __name__, )


@accounts.route('/accounts/login', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        account = User.query.filter_by(email=email).first()

        if account and check_password_hash(account.password, password):
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            session['role'] = account.role
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('accounts/login.html', msg=msg)


@accounts.route('/accounts/register', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        conf_password = request.form.get('conf_password')
        image_file = request.files.get('profile_image')

        # Check password match
        if password != conf_password:
            msg = 'Passwords do not match!'
            return render_template('accounts/register.html', msg=msg)

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            msg = 'Email already taken!'
            return render_template('accounts/register.html', msg=msg)

        try:
            image_path = save_uploaded_image(image_file)
        except ValueError as e:
            msg = str(e)
            print(f"Error while trying to save image profile")
            return render_template('accounts/register.html', msg=msg)

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create and add the new user
        new_user = User(username=username, email=email, password=hashed_password, image_path=image_path)
        db.session.add(new_user)
        db.session.commit()

        msg = 'Registration successful!'
        flash('Registration successful!', 'success')

        return redirect(url_for('accounts.login'))

    return render_template('accounts/register.html', msg=msg)


@accounts.route('/accounts/profile', methods=['GET', 'PATCH'])
def profile():
    msg = ''

    if 'loggedin' in session:
        print("session", session)
        account = User.query.filter_by(id=session['id']).first()
        print(f"acount info: {account}")
        return render_template('accounts/profile.html', account=account)

    # User is not logged
    msg = 'You must logged before'
    return render_template('accounts/login.html', msg=msg)


@accounts.route('/accounts/profile/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id=None):
    if 'loggedin' not in session:
        return redirect(url_for('accounts.login'))

    logged_user = User.query.get(session['id'])
    user_to_edit = User.query.get(user_id)

    if logged_user and user_to_edit and (logged_user.role == 'admin' or logged_user.id == user_to_edit.id):

        msg = ''

        if request.method == 'POST':
            new_username = request.form.get('username')
            new_email = request.form.get('email')
            new_password = request.form.get('password')
            conf_password = request.form.get('conf_password')
            new_image = request.files.get('profile_image')

            # Check password match
            if new_password != conf_password:
                msg = 'Passwords do not match!'
                return render_template('accounts/edit_profile.html', account=user_to_edit, msg=msg)

            # update fields
            user_to_edit.username = new_username
            user_to_edit.email = new_email

            if new_password:  # only update if a new password is entered
                from werkzeug.security import generate_password_hash
                user_to_edit.password = generate_password_hash(new_password)

            try:
                user_to_edit.image_path = save_uploaded_image(new_image, old_image_path=user_to_edit.image_path)
            except ValueError as e:
                msg = str(e)
                return render_template('accounts/edit_profile.html', account=user_to_edit, msg=msg)

            db.session.commit()
            msg = 'Profile updated successfully!'
            return redirect(url_for('accounts.profile'))

    return render_template('accounts/edit_profile.html', account=user_to_edit, msg=msg)


@accounts.route('/accounts/logout')
def logout():
    # Clear all session data
    session.clear()

    # Optionally, flash a message
    flash('You have been logged out.', 'info')

    # Redirect to login page
    return redirect(url_for('accounts.login'))


@accounts.route('/users')
def users():
    if 'loggedin' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('accounts.login'))

    user = User.query.get(session['id'])

    # Only admin can access
    if user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('accounts.profile'))

    # Get all users
    all_users = User.query.all()
    return render_template('accounts/users.html', users=all_users)


@accounts.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'loggedin' not in session:
        return redirect(url_for('accounts.login'))

    current_user = User.query.get(session['id'])
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('accounts.profile'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        password = request.form.get('password')
        conf_password = request.form.get('conf_password')

        if password:
            if password != conf_password:
                flash('Passwords do not match!', 'danger')
                return render_template('accounts/edit_profile.html', account=user)

        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('accounts.users'))

    print(f"user to edit : {user}")
    return render_template('accounts/edit_profile.html', account=user)


@accounts.route('/users/delete/<int:user_id>', methods=['GET','DELETE'])
def delete_user(user_id):
    if 'loggedin' not in session:
        return redirect(url_for('accounts.login'))

    current_user = User.query.get(session['id'])
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('accounts.profile'))




    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    # remove image_path
    if user.image_path:
        image_abs = os.path.join(current_app.root_path, user.image_path)
        if os.path.exists(image_abs):
            os.remove(image_abs)
            print(f"remove image associate with this account : {image_abs}")


    flash('User deleted successfully', 'success')
    return redirect(url_for('accounts.users'))
