# -*- coding: utf-8 -*-
"""Print the location on disk where the RIPL MS shell correction database resides

Usage:
    if __name__ == '__main__':
        # RIPLpy
        import riplpy.densities as dens

        # Print the full path of this particular RIPL database
        print(dens.shell_corr.db_ms_file_path)

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# OS
import os

# Unit testing
import unittest

# RIPLpy
import riplpy.densities as dens

# ========================

class TestRIPLShellCorrDatabase(unittest.TestCase):
    def test_shell_corr_db_ms_file_path(self):
        """Test the existence and validity of the RIPL MS shell correction database file path."""
        # Retrieve the database file path
        try:
            db_ms_file_path = dens.shell_corr.db_ms_file_path
        except Exception as e:
            self.fail(f"Failed to access shell correction database file path: {e}")
        
        # Assert that the file path is not None or empty
        self.assertIsNotNone(db_ms_file_path, "The shell correction database file path is None")
        self.assertTrue(len(db_ms_file_path) > 0, "The shell correction database file path is empty")
        
        # Assert that the file exists on disk
        self.assertTrue(os.path.exists(db_ms_file_path), f"The file does not exist at: {db_ms_file_path}")

if __name__ == '__main__':
    unittest.main()