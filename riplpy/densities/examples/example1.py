# -*- coding: utf-8 -*-
"""Load the BSFG level density database from ASCII file and print data.

Usage:
    if __name__ == '__main__':
        # RIPLpy
        import riplpy.densities as dens

        # Load the database
        bsfg = dens.bsfg.load() # The BSFG level density database
        # Print the entire database
        print(bsfg.data)

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# Unit testing
import unittest

# RIPLpy
import riplpy.densities as dens

# ========================

class TestRIPLpyBSFGDatabase(unittest.TestCase):
    """A simple Unit Test object. """

    def test_load_bsfg_database(self) -> None:
        """Test loading the BSFG level density database."""
        # Attempt to load the BSFG level density database
        try:
            bsfg = dens.bsfg.load()  # Load the database
        except Exception as e:
            self.fail(f"Failed to load BSFG database: {e}")
        
        # Check that the 'data' attribute is not None or empty
        self.assertIsNotNone(bsfg.data, "BSFG database 'data' attribute is None")
        self.assertTrue(len(bsfg.data) > 0, "BSFG database 'data' attribute is empty")

        # Optionally, add more specific checks for the structure of `bsfg.data` if known
        # For example, check if it's a dictionary, list, or contains expected keys
        self.assertTrue(isinstance(bsfg.data, dict), "BSFG database 'data' attribute is not a dictionary")


if __name__ == '__main__':
    unittest.main()
