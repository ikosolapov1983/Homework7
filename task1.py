import requests
import json
import unittest


class TestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.title = 'Преступление и наказание'
        cls.author = 'Федор Достоевский'
        cls.name = 'Родион'
        cls.type = 'Студент'
        cls.level = 40
        cls.books_url = 'http://pulse-rest-testing.herokuapp.com/books/'
        cls.roles_url = 'http://pulse-rest-testing.herokuapp.com/roles/'
        cls.headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    @classmethod
    def tearDownClass(cls):
        books_url = 'http://pulse-rest-testing.herokuapp.com/books/'
        roles_url = 'http://pulse-rest-testing.herokuapp.com/roles/'
        resp = requests.get(books_url).json()
        for i in resp:
            if i['author'] == 'Федор Достоевский' or i['author'] == 'Дюма':
                requests.delete(books_url + str(i['id']))
        resp = requests.get(roles_url).json()
        for j in resp:
            if j['type'] == 'Студент' or j['type'] == 'моряк':
                requests.delete(roles_url + str(j['id']))

    def setUp(self):
        book = json.dumps({'title': self.title, 'author': self.author})
        resp = requests.post(self.books_url, book, headers=self.headers)
        self.book = resp.json()
        self.url_book = self.books_url + str(self.book['id'])
        role = json.dumps({'name': self.name, 'type': self.type, 'level': self.level, 'book': self.url_book})
        resp = requests.post(self.roles_url, role, headers=self.headers)
        self.role = resp.json()
        self.url_role = self.roles_url + str(self.role['id'])

    def test_add_book(self):
        book = json.dumps({'title': self.title, 'author': self.author})
        resp = requests.post(self.books_url, book, headers=self.headers)
        resp_book = resp.json()
        resp_book['id'] = self.book['id']
        self.assertEqual(201, resp.status_code)
        self.assertEqual(resp_book, self.book)

    def test_check_url_book(self):
        resp = requests.get(self.books_url + str(self.book['id']))
        self.assertEqual(200, resp.status_code)

    def test_edit_book(self):
        book = json.dumps({'title': 'Граф Монте-Кри́сто', 'author': 'Дюма'})
        resp = requests.put(self.books_url + str(self.book["id"]), book, headers=self.headers)
        self.assertEqual(200, resp.status_code)
        edit_book = resp.json()
        resp = requests.get(self.books_url + str(self.book['id']))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json(), edit_book)

    def test_check_data_book(self):
        all_data = requests.get(self.books_url)
        all_data = all_data.json()
        if self.book in all_data:
            a = True
            self.assertTrue(a)

    def test_del_book(self):
        resp = requests.delete(self.books_url + str(self.book["id"]))
        self.assertEqual(resp.status_code, 204)
        resp = requests.get(self.books_url + str(self.book['id']))
        self.assertEqual(resp.status_code, 404)
        all_data = requests.get(self.books_url)
        all_data = all_data.json()
        if self.book not in all_data:
            a = True
            self.assertTrue(a)

    def test_add_role(self):
        role = json.dumps({'name': self.name, 'type': self.type, 'level': self.level, 'book': self.url_book})
        resp = requests.post(self.roles_url, role, headers=self.headers)
        resp_role = resp.json()
        resp_role['id'] = self.role['id']
        self.assertEqual(201, resp.status_code)
        self.assertEqual(resp_role, self.role)

    def test_check_url_role(self):
        resp = requests.get(self.roles_url + str(self.role['id']))
        self.assertEqual(200, resp.status_code)

    def test_edit_role(self):
        role = json.dumps({'name': 'Эдмонт', 'type': 'моряк', 'level': 18, 'book': self.url_book})
        resp = requests.put(self.roles_url + str(self.role["id"]), role, headers=self.headers)
        self.assertEqual(200, resp.status_code)
        edit_role = resp.json()
        resp = requests.get(self.roles_url + str(self.role['id']))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json(), edit_role)

    def test_check_data_role(self):
        all_data = requests.get(self.roles_url)
        all_data = all_data.json()
        if self.role in all_data:
            a = True
            self.assertTrue(a)

    def test_del_role(self):
        resp = requests.delete(self.roles_url + str(self.role["id"]))
        self.assertEqual(resp.status_code, 204)
        resp = requests.get(self.roles_url + str(self.role['id']))
        self.assertEqual(resp.status_code, 404)
        all_data = requests.get(self.roles_url)
        all_data = all_data.json()
        if self.role not in all_data:
            a = True
            self.assertTrue(a)

    def test_bad_book_data(self):
        book = json.dumps({'title': self.title, 'author': self.author})
        resp = requests.post(self.books_url, book)
        self.assertNotEqual(201, resp.status_code, f' Неверный формат заголовка, ошибка {resp.status_code}!')

    def test_empty_book(self):
        book = json.dumps({'title': '', 'author': ''})
        resp = requests.post(self.books_url, book, headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {'author': ['This field may not be blank.'],
                                       'title': ['This field may not be blank.']})


myTestSuit = unittest.TestLoader().loadTestsFromTestCase(TestClass)

if __name__ == '__main()':
    from HtmlTestRunner import HTMLTestRunner

    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output=r".\\"))
