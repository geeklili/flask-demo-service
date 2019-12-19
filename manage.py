import os
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade
from app.models import User, Role, Permission
from app import create_app, db

# 如果本地有.env文件，就是用本地的.env文件，把.env下面的环境变量加载到系统环境变量里面
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrqate database to latest revision
    upgrade()
    # create or update user roles
    Role.insert_roles()