# Load all of the densities section databases from ASCII files into memory and access the egsm database

if __name__ == '__main__':
    # RIPLpy
    import riplpy.densities as dens

    # At this point dens.db is not defined!

    # Load all of the databases
    dens.load()

    # Print the ESGM database
    print(dens.db.egsm.data)
