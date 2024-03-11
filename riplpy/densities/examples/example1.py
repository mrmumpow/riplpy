# Load the BSFG level density database from ASCII file and print data

if __name__ == '__main__':
    # RIPLpy
    import riplpy.densities as dens

    # Load the database
    bsfg = dens.bsfg.load() # The BSFG level density database
    # Print the entire database
    print(bsfg.data)
