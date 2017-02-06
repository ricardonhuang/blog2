#coding=utf-8
'''
Created on 2016年12月27日

@author: huangning
'''
# import Flask Script object
import os
from flask_script import Manager, Server
from flask_migrate import Migrate,MigrateCommand
from head import create_app
from config import config
import models

# Init manager object via app object
app = create_app(config[os.getenv('FLASK_CONFIG') or 'default'])
manager = Manager(app)

migrate = Migrate(app, models.db)

# Create a new commands: server
# This command will be run the Flask development_env server
manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    """Create a python CLI.
    return: Default import object
    type: `Dict`
    """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(app=app,db=models.db,User=models.User,Post=models.Post,
                Comment=models.Comment,Tag=models.Tag)

if __name__ == '__main__':
    manager.run()