# -*- coding: utf-8 -*-
"""Python objects which provide access to the experimental giant dipole resonance (GDR) fits with SLO of the Reference Input Parameter Library (RIPL). 

Python 3.10+ is expected to run this code properly.

Examples:
    (1) @TODO: Finish
        $

Todo:
    * Provide more examples of use cases.
    * Test in production.
    
Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# OS
import os as _os

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.collections as _c
import riplpy.db as _db
from . import core as _core

# ========================

__all__ = ('db_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))
# Database location
db_file_path = _os.path.join(__loc__, "data", "ripl3-gdr-parameters&errors-exp-SLO.dat")

# ========================

FILE_HEADER = "#   gdr-parameters&errors-exp-SLO.dat\n#   Experimental values and errors of GDR parameters  within SLO approach\n#\n# Z   A El Reac  E1     CS1     W1    E2     CS2    W2  E_{min}-E_{max} Ref\n#               Err     Err    Err   Err     Err    Err\n#              [MeV]   [mb]   [MeV] [MeV]   [mb]  [MeV]     [MeV]\n#-----------------------------------------------------------------------\n"
LINE1_FORMAT = '(2X,I2,1X,I3,1X,A2,1X,I2,1X,F5.2,2X,F5.1,2X,F5.2,2X,F5.2,2X,F5.1,3X,F5.2,1X,F4.1,3X,F4.1,2X,A5)'
LINE2_FORMAT = '(15X,F5.2,2X,F5.1,2X,F5.2,2X,F5.2,2X,F5.1,3X,F5.2)'
line1_reader = _ff.FortranRecordReader(LINE1_FORMAT)
line2_reader = _ff.FortranRecordReader(LINE2_FORMAT)
line1_writer = _ff.FortranRecordWriter(LINE1_FORMAT)
line2_writer = _ff.FortranRecordWriter(LINE2_FORMAT)

# ========================

references = {}
references['62Fu1'] = "S. C. Fultz, R. L. Bramblett, J. T. Caldwell, N. E. Hansen, C. P. Jupiter; Phys. Rev., 128, 2345(1962)."
references['62Fu2'] = "S. C. Fultz, R. L. Bramblett, J. T. Caldwell, N. A. Kerr; Phys. Rev., 127, 1273(1962)."
references['63Br1'] = "R. L. Bramblett, J. T. Caldwell, G. F. Auchampaugh, S. C. Fultz; Phys. Rev., 129, 2723(1963)."
references['63Bur'] = "N. A. Burgov, G. V. Danilyan, B. S. Dolbilkin, L. E. Lazareva, F.A.Nikolaev; Zhur. Eksper. Teoret. Fiz. 45,(6),1694(1963)."
references['64Bo3'] = "C. D. Bowman, G. F. Auchampaugh, S. C. Fultz; Phys. Rev., 133, B676(1964)."
references['64Br1'] = "R. L. Bramblett, J. T. Caldwell, R. R. Harvey, S. C. Fultz; Phys. Rev., 133, B869(1964)."
references['64Fu1'] = "S. C. Fultz, R. L. Bramblett, J. T. Caldwell, R. R. Harvey; Phys. Rev., 133, B1149(1964)."
references['64Ha2'] = "R. R. Harvey, J. T. Caldwell, R. L. Bramblett, S. C. Fultz; Phys. Rev., 136, B126(1964)."
references['65Wyc'] = "J. M. Wyckoff, B. Ziegler, H. W. Koch, R. Uhlig; Phys. Rev. B137, 576(1965)."
references['66Ax1'] = "P. Axel, J. Miller, C. Schuhl, G. Tamas, C. Tzara; J. Physique, 27,262(1966)."
references['66Br1'] = "R. L. Bramblett, J. T. Caldwell, B. L. Berman, R. R. Harvey, S. C. Fultz; Phys. Rev., 148, 1198(1966)."
references['67Be2'] = "B. L. Berman, J. T. Caldwell, R. R. Harvey, M. A. Kelly, R. L. Bramblett, S. C. Fultz; Phys. Rev., 162, 1098(1967)."
references['68Be5'] = "R.Bergere, R. Beil, A. Veyssiere; Nucl. Phys. A121, 463(1968)."
references['68Su1'] = "R. E. Sund, M. P. Baker, L. A. Kull, R. B. Walton; Phys. Rev., 176, 1366(1968)."
references['69Be1'] = "B. L. Berman, R. L. Bramblett, J. T. Caldwell, H. S. Davis, M. A. Kelly, S. C. Fultz; Phys. Rev., 177, 1745(1969)."
references['69Be6'] = "R. Bergere, H. Beil, P. Carlos, A. Veyssiere; Nucl. Phys., A133, 417(1969)."
references['69Be8'] = "B. L. Berman, M. A. Kelly, R. L. Bramblett, J. T. Caldwell, H. S. Davis, S. C. Fultz; Phys. Rev., 185, 1576(1969)."
references['69Fu1'] = "S. C. Fultz, B. L. Berman, J. T. Caldwell, R. L. Bramblett, M. A. Kelly; Phys. Rev., 186, 1255(1969)."
references['69Bez'] = "N. Bezic, D. Brajnik, D. Jamnik, G. Kernel; Nucl. Phys. A128, 426(1969)."
references['70Be8'] = "B. L. Berman, S. C. Fultz, J. T. Caldwell, M. A. Kelly, S. S. Dietrich; Phys. Rev., C2, 2318(1970)."
references['70Su1'] = "R. E. Sund, V. V. Verbinski, H. Weber, L. A. Kull; Phys. Rev., C2, 1129(1970)."
references['70Ve1'] = "A. Veyssiere, H. Beil, R. Bergere, P. Carlos, A. Lepretre; Nucl. Phys. A159, 561(1970)."
references['71Be4'] = "H. Beil, R. Bergere, P. Carlos, A. Lepretre, A. Veyssiere, A. Parlag; Nucl. Phys. A172, 426(1971)."
references['71Ca1'] = "P. Carlos, H. Beil, R. Bergere, A. Lepretre, A. Veyssiere; Nucl. Phys. A172, 437(1971)."
references['71Le1'] = "A. Lepretre, H. Beil, R. Bergere, P. Carlos, A. Veyssiere, M. Sugawara; Nucl. Phys. A175, 609(1971)."
references['72Yo']  = "L. M. Young, Ph.D. Thesis, University of Illinois(1972), unpublished."
references['73Ve1'] = "A. Veyssiere, H. Reil, R. Bergere, P. Carlos, A. Lepretre, K. Kernbach; Nucl. Phys. A199, 45(1973)."
references['74Be3'] = "H. Beil, R. Bergere, P. Carlos, A. Lepretre, A. De Miniac, A. Veyssiere; Nucl. Phys. A227, 427(1974)."
references['74Ca5'] = "P. Carlos, H. Beil, R. Bergere, A. Lepretre, A. De Miniac, A. Veyssiere; Nucl. Phys. A225, 171(1974)."
references['74Fu3'] = "S. C. Fultz, R. A. Alvarez, B. L. Berman, P. Meyer; Phys. Rev., C10, 608(1974)."
references['74Le1'] = "A. Lepretre, H. Beil, R. Bergere, P. Carlos, A. De Miniac, A. Veyssiere, K. Kernbach; Nucl. Phys. A219, 39(1974)."
references['74Ve1'] = "A. Veyssiere, H. Beil, R. Bergere, P. Carlos, A. Lepretre, A. De Miniac; Nucl. Phys. A227, 513(1974)."
references['75Ve5'] = "A. Veyssiere, H. Beil, R. Bergere, P. Carlos, A. Lepretre, A. De Miniac; J. Physique 36, L-267(1975)."
references['75Ahr'] = "J. Ahrens, H. Borchert, K. H. Czock, H. B. Eppler, H. Gimm, H. Gundrum,M. Kroning, P. Riehn, G. Sita Ram, A. Zieger, B. Ziegler; Nucl. Phys. A251, 479(1975)."
references['76Ca1'] = "P. Carlos, H. Beil, R. Bergere, J. Fagot, A. Lepretre, A. Veyssiere, G. V. Solodukhov; Nucl. Phys. A258, 365(1976)."
references['76Le2'] = "A. Lepretre, H. Beil, R. Bergere, P. Carlos, J. Fagot, A. De Miniac, A. Veyssiere, H. Miyase; Nucl. Phys. A258, 350(1976)."
references['76Gur'] = "G. M. Gurevich, L. E. Lazareva, V. M. Mazur, G. V. Solodukhov, B. A. Tulupov; Nucl. Phys. A273, 326(1976)."
references['77Wei'] = "J.Weise, M.N.Thompson, K.Shoda, H.Tsubata; Austr. J. Phys., 30, 401(1977) (see also IAEA-TECDOC-1178, IAEA, October 2000.)"
references['78Gur'] = "G. M. Gurevich, L. E. Lazareva, V. M. Mazur, G. V. Solodukhov; Prob. Yad. Fiz. Kosm. Luch. 8, 106(1978)."
references['78Nor'] = "J. W. Norbury, M. N. Thompson, K. Shoda, H. Tsubota; Australian Jour. of Phys. 31, 471(1978)."
references['79Al2'] = "R. A. Alavarez, B. L. Berman, D. D. Faul, F. H. Lewis, Jr., P. Meyer; Phys. Rev., C20, 128(1979)."
references['79Be4'] = "B. L. Berman, D. D. Faul, R. A. Alvarez, P. Meyer, D. L. Olson; Phys. Rev., C19, 1205(1979)."
references['80Ca1'] = "J. T. Caldwell, E. J. Dowdy, B. L. Berman, R. A. Avarez, P. Meyer; Phys. Rev., C21, 1215(1980)."
references['81Ram'] = "S.Raman, O.Shahal, G.G. Slauther; Phys.Rev. C23, 2794(1981)."
references['81Gur'] = "G. M. Gurevich, L. E. Lazareva, V. M. Mazur, S. Yu. Merkulov, G. V. Solodukhov, V. A. Tyutin; Nucl. Phys. A351, 257(1981)."
references['86Be1'] = "B. L. Berman, R. E. Pywell, M. N. Thompson, K. G. Mcneill, J. W. Jury, J. G. Woodworth; Bull. Am. Phys. Soc. 31, 855(1986)."
references['86Be2'] = "B. L. Berman, J. T. Caldwell, E. J. Dowdy, S. S. Dietrich, P. Meyer, R. A. Alvarez; Phys. Rev., C34, 2201(1986)."
references['89Bat'] = "A. D. Bates, R. P. Rassool, E. A. Milne, M. N. Thompson, K. G. Mcneil; Phys. Rev. C40, 506(1989)."
references['92Kop'] = "J.Kopecky, M.Uhl, R.E.Chrien; Preprint ECN-RX--92-011, April 1992."
references['95Li1'] = "Liu Jianfen and Su Zongdi; J. Chinese Nucl. Phys., 16, 560(1995)."
references['02Ish'] = "B. S. Ishkhanov, I. M. Kapitonov, E. I. Lileeva, E. V. Shirokov, V. A. Erokhova, M. A. Elkin, A. V. Izotova; Moscow State Univ.Inst.of Nucl.Phys. Reports, No.2002, 27/711(2002)."
references['03Er']  = "V. A. Erokhova, M. A. Elkin, A. V. Izotova, B. S. Ishkhanov, I. M. Kapitonov, E. I. Lilieva, E. V. Shirokov; Izv. Ros. Akad. Nauk, Ser.Fiz. 67, 1479(2003)."
references['03Var'] = "V. V. Varlamov, M. E. Stepanov, V. V. Chesnokov; Izv. Ros. Akad. Nauk, Ser.Fiz. 67, 656(2003)."
references['08Var'] = "V. V. Varlamov (private communication, 2008)."

# ========================

def line1_as_tuple(entry: object, ) -> tuple:
    """Return line1 in the ASCII file as a tuple. """
    return (entry.n.Z, entry.n.A, entry.n.symbol, entry.reac, entry.E1, entry.CS1, entry.W1, entry.E2, entry.CS2, entry.W2, entry.Emin, entry.Emax, entry.reference)


def line2_as_tuple(entry: object, ) -> tuple:
    """Return line2 in the ASCII file as a tuple. """
    return (entry.E1_error, entry.CS1_error, entry.W1_error, entry.E2_error, entry.CS2_error, entry.W2_error)


def read_ascii_file(fpath: str) -> dict:
    """Read data from an ASCII file and return a dictionary. """
    # Data placeholder
    d = {}

    # Counter for number of header lines
    header_lines = 0

    # Read file
    with open(fpath, 'r') as fp:
        # Skip the header
        flag = False
        for i,line in enumerate(fp.readlines()):
            if "#" in line[0]:
                header_lines += 1
                continue
            # Define even / odd structure of data
            j = i - header_lines
            #print(line, i, j)
            if j % 2 == 0:
                data = line1_reader.read(line)
                Z    = int(data[0])
                A    = int(data[1])
                n    = _c.Nuclide(Z=Z, A=A)
                reac = int(data[3])
                E1   = float(data[4])
                CS1  = float(data[5])
                W1   = float(data[6])
                try:
                    E2  = float(data[7])
                    CS2 = float(data[8])
                    W2  = float(data[9])
                except:
                    E2  = None
                    CS2 = None
                    W2  = None
                Emin = float(data[10])
                Emax = float(data[11])
                ref  = data[12]
                flag = False
            else:
                data = line2_reader.read(line)
                E1_error  = float(data[0])
                CS1_error = float(data[1])
                W1_error  = float(data[2])
                try:
                    E2_error  = float(data[3])
                    CS2_error = float(data[4])
                    W2_error  = float(data[5])
                except:
                    E2_error  = None
                    CS2_error = None
                    W2_error  = None
                flag = True
            if flag:
                packet = {'n': n, 'reac': reac, 'E1': E1, 'E2': E2, 'W1': W1, 'W2': W2, 'CS1': CS1, 'CS2': CS2,
                          'E1_error': E1_error, 'E2_error': E2_error, 'W1_error': W1_error, 'W2_error': W2_error,
                          'CS1_error': CS1_error, 'CS2_error': CS2_error, 'Emin': Emin, 'Emax': Emax, 
                          'reference': ref,
                         }
                d[n] = packet
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line1 = line1_as_tuple(data[n])
            line2 = line2_as_tuple(data[n])
            fp.write(line1_writer.write(line1)+"\n")
            fp.write(line2_writer.write(line2)+"\n")


class Entry(_core.Experimental_GDR_Parameter, _db.NuclideDatabaseEntry):
    """An object which represents an entry in the experimental GDR SLO parameter database. """
    pass


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load() -> Database:
    """Load and return the experimental GDR SLO parameter database. """
    return _db.load(Database, db_file_path)
