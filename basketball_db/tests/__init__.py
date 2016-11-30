import unittest
def get_suite():
    import basketball_db.tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(basketball_db.tests)
    return suite
