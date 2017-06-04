import unittest
import tempfile
from tal.api.app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_file, self.db_path = tempfile.mkstemp()

        app.config['DATABASE'] = self.db_path
        app.config['TESTING'] = True

        self.app = app.test_client(use_cookies=False)

        app.init_db()

    def tearDown(self):
        os.close(self.db_file)
        os.unlink(self.db_path)

    def test_empty_db(self):
        r = self.app.get('/posts/')
        assert r.data == {'posts': []}

if __name__ == '__main__':
    unittest.main()