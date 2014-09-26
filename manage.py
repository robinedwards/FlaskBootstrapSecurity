#!/usr/bin/env python
from flask_application import app
from flask.ext.script import Manager, Server, Command

from flask.ext.security.script import CreateUserCommand, AddRoleCommand,\
    RemoveRoleCommand, ActivateUserCommand, DeactivateUserCommand

manager = Manager(app)


class CreateDB(Command):
    def run(self, *args):
        app.db.create_all()


manager.add_command("runserver", Server())
manager.add_command('create_db', CreateDB())
manager.add_command('create_user', CreateUserCommand())
manager.add_command('add_role', AddRoleCommand())
manager.add_command('remove_role', RemoveRoleCommand())
manager.add_command('deactivate_user', DeactivateUserCommand())
manager.add_command('activate_user', ActivateUserCommand())


if __name__ == "__main__":
    manager.run()
