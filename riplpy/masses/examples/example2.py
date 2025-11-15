# Load all of the masses section databases from ASCII files into memory and access the FRDM1995 database
# This example assumes: 
#     (1) The RIPL database has been downloaded to the user's local machine.
#     (2) The RIPL_LOCATION environmental variable has been set to the above location.

if __name__ == '__main__':
    # RIPLpy
    from riplpy.config import RIPL_PATH
    import riplpy.masses as masses

    # At this point masses.db is not defined!

    # Load all of the databases
    masses.load(RIPL_PATH) # This may take some time!

    # Print the FRDM1995 database
    print(masses.db.frdm1995.data)
