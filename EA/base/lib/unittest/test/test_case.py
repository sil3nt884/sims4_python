import contextlib
class Test(object):

    class Foo(unittest.TestCase):

        def runTest(self):
            pass

        def test1(self):
            pass

    class Bar(Foo):

        def test2(self):
            pass

    class LoggingTestCase(unittest.TestCase):

        def __init__(self, events):
            super(Test.LoggingTestCase, self).__init__('test')
            self.events = events

        def setUp(self):
            self.events.append('setUp')

        def test(self):
            self.events.append('test')

        def tearDown(self):
            self.events.append('tearDown')
