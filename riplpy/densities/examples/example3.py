# Print the location on disk where the RIPL MS shell correction database resides

if __name__ == '__main__':
    # RIPLpy
    import riplpy.densities as dens

    # Print the full path of this particular RIPL database
    print(dens.shell_corr.db_ms_file_path)
