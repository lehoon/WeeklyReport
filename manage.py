from app import create_app, db
from app.models import Role, Department, Report
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Role=Role,
                Department=Department, Report=Report)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    db.create_all()
    Role.insert_roles()
    Department.insert_departments()

if __name__ == '__main__':
    manager.run()
