import unittest
def get_suite():
    "Return a unittest.TestSuite."
    import basketball_db.tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(basketball_db.tests)
    return suite
