from lib.gsc_explorer.classes.GSCF.GSCFFile import GscfFile


class GSCEV:

    # number of bytes that usually reads the program
    bytes2Read = 4

    # *** vars that need to be reseted when loading a new gsc file ***
    # GSC file class
    gsc_file = GscfFile()
