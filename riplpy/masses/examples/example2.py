# Load all of the masses section databases from ASCII files into memory and access the FRDM1995 database

if __name__ == '__main__':
    # RIPLpy
    import riplpy.masses as masses

    # At this point masses.db is not defined!

    # Load all of the databases
    masses.load()

    # Print the FRDM1995 database
    print(masses.db.frdm1995.data)
