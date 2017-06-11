# project/server/tests/base.py


from flask_testing import TestCase

from app import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        #app.config.from_object('config.appConfig')
        return app

    def setUp(self):
        #db.create_all()
        #db.session.commit()
        pass

    def tearDown(self):
        #db.session.remove()
        #db.drop_all()
        pass
