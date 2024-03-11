# Print the location on disk where the RIPL natural abundance database resides

if __name__ == '__main__':
    # RIPLpy
    import riplpy.masses as masses

    # Print the full path of this particular RIPL database
    print(masses.ab.db_file_path)
