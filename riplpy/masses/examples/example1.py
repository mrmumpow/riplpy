# Load the HFB-14 ground state masses database from ASCII file and print data

if __name__ == '__main__':
    # RIPLpy
    import riplpy.masses as masses

    # Load the database
    hfb14 = masses.hfb.load() # The HFB-14 ground state masses database

    # Print the entire database
    print(hfb14.data)
