from flask import render_template
from . import auth


@auth.route('/login')
def login():
    # By storing the blueprint templates in their own subdirectory, there is no
    # risk of naming collisions with the main blueprint or any other blueprints
    # that will be added in the future.
    return render_template('auth/login.html')
