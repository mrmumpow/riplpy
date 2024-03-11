# Load ground state masses database from ASCII file, update, and save a new file

if __name__ == '__main__':
    # RIPLpy
    from riplpy.collections import Nuclide
    import riplpy.masses as masses

    # Load the database
    frdm1995 = masses.frdm.load() # The FRDM1995 ground state masses database

    # Copy the database
    new_data = frdm1995.data
    # Update an entry with a random number
    entry = Nuclide(z=50, a=132)
    new_data[entry].Mth = -76.112
    # Update another entry
    entry = Nuclide(z=80, a=190)
    new_data[entry].Mth = -80.32

    # Save the new database to file
    new_db = masses.frdm.Database(new_data)
    new_db.save("example4.dat")
