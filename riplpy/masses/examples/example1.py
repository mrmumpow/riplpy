# Load the HFB-14 ground state masses database from ASCII file and print data
# This example assumes: 
#     (1) The RIPL database has been downloaded to the user's local machine.
#     (2) The RIPL_LOCATION environmental variable has been set to the above location.

if __name__ == '__main__':
    # RIPLpy
    import riplpy.masses as masses

    # Load the database
    hfb14 = masses.hfb14.load() # The HFB-14 ground state masses database

    # Print the entire database
    print(hfb14.data)
