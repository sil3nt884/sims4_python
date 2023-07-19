__all__ = ['TestResult', 'TestCase', 'TestSuite', 'TextTestRunner', 'TestLoader', 'FunctionTestCase', 'main', 'defaultTestLoader', 'SkipTest', 'skip', 'skipIf', 'skipUnless', 'expectedFailure', 'TextTestResult', 'installHandler', 'registerResult', 'removeResult', 'removeHandler']
def load_tests(loader, tests, pattern):
    import os.path
    this_dir = os.path.dirname(__file__)
    return loader.discover(start_dir=this_dir, pattern=pattern)
