from flask import Blueprint


"""
The constructor to instantiating an object of class Blueprint take 2 required
arguments - The blueprint name and the module or package where the blueprint
is located.
"""
main = Blueprint('main', __name__)

"""
The routes of the application are stored in the views.py & error handlers are in
errors.py, which are all in the same directory. Importing these moduels causes 
the routes and error handlers to be associated with the blueprint.
"""

"""
!! It is important to note that the modules are imported at the bottom of the 
script to avoid errors due to circular dependencies. In our example, the problem
is that views.py & errors.py in turn are going to import the `main` blueprint 
object, so the imports are going to fail unless the circular reference occurs
after `main` is defined.
"""

from .import views, errors