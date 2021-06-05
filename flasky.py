import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

# Integration with Python Shell
# Load all the required variables automatically
@app.shell_context_processor                                                    # Add wrapped function to the shell context
def make_shell_context():
    return dict(db=db, User=User, Role=Role)                                    # Shell will import these items automatically into shell, 
                                                                                # in addition to app, which is imprted by default

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    
