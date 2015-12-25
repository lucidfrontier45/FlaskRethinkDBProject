from flask_script import Manager

from webapp import create_app

app = create_app("../conf/config.py")
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
