# -*- coding: utf-8 -*-
"""Python objects which provide access to the experimental giant dipole resonance (GDR) fits with SLO or MLO of the Reference Input Parameter Library (RIPL). 

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

__all__ = ('slo_local_file_path', 'mlo_local_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Relative path to database file
slo_local_file_path = _os.path.join("gamma", "gdr-parameters-exp-SLO.dat")
mlo_local_file_path = _os.path.join("gamma", "gdr-parameters-exp-MLO.dat")

# ========================

#FILE_HEADER = "#   gdr-parameter-exp-SLO.dat\n#   Experimental values and errors of GDR parameters  within SLO approach\n#\n# Z   A El Reac  E1     CS1     W1    E2     CS2    W2  E_{min}-E_{max} Ref\n#               Err     Err    Err   Err     Err    Err\n#              [MeV]   [mb]   [MeV] [MeV]   [mb]  [MeV]     [MeV]\n#-----------------------------------------------------------------------\n"
SLO_FILE_HEADER  = "#     Experimental values and uncertainties of GDR parameters within Standard Lorentzian (SLO) method\n#  Second line for each isotope -  uncertainties of  corresponding  quantities in the nearest upper line\n#     FORTRAN format  of data reading for one entry is FORMAT(2I4,1X,A2,A3,2X,7F8.3,A22,/,16X,7F8.3)\n#\n#  Z  A  El Id     Er1     Wr1     Sr1     Er2    Wr2     Sr2        Sr  E_{min}-E_{max} Ref.\n#                 dEr1    dWr1    dSr1    dEr2   dWr2    dSr2       dSr\n#                [MeV]    [MeV]           [MeV]  [MeV]                         [MeV]\n#---------------------------------------------------------------------------------------------------\n"
MLO_FILE_HEADER  = "#     Experimental values and uncertainties of GDR parameters within Modified Lorentzian (MLO) method\n#  Second line for each isotope -  uncertainties of  corresponding  quantities in the nearest upper line\n#     FORTRAN format  of data reading for one entry is FORMAT(2I4,1X,A2,A3,2X,7F8.3,A22,/,16X,7F8.3)\n#\n#  Z  A  El Id     Er1     Wr1     Sr1     Er2    Wr2     Sr2        Sr  E_{min}-E_{max} Ref.\n#                 dEr1    dWr1    dSr1    dEr2   dWr2    dSr2       dSr\n#                [MeV]    [MeV]           [MeV]  [MeV]                         [MeV]\n#---------------------------------------------------------------------------------------------------\n"
LINE1_FORMAT = '(2I4,1X,A2,A3,2X,7F8.3,A22,/,16X,7F8.3)'
LINE2_FORMAT = '(2I4,1X,A2,A3,2X,7F8.3,A22,/,16X,7F8.3)'
#LINE2_FORMAT = '(15X,F5.2,2X,F5.1,2X,F5.2,2X,F5.2,2X,F5.1,3X,F5.2)'
line1_reader = _ff.FortranRecordReader(LINE1_FORMAT)
line2_reader = _ff.FortranRecordReader(LINE2_FORMAT)
line1_writer = _ff.FortranRecordWriter(LINE1_FORMAT)
line2_writer = _ff.FortranRecordWriter(LINE2_FORMAT)

# ========================

references_string = """
1960Fas  R.W.Fast, P.A.Flournoy, R.S.Tickle, W.D.Whitehead;
         Phys. Rev., 118(2), 535(1960).
1962Fu1  S. C. Fultz, R. L. Bramblett, J. T. Caldwell, N. E. Hansen,
         C. P. Jupiter; Phys. Rev., 128, 2345(1962).
1962Fu2  S. C. Fultz, R. L. Bramblett, J. T. Caldwell, N. A. Kerr;
         Phys. Rev., 127, 1273(1962).
1963Br1  R. L. Bramblett, J. T. Caldwell, G. F. Auchampaugh,
         S. C. Fultz; Phys. Rev., 129, 2723(1963).
1963Bur  N. A. Burgov, G. V. Danilyan, B. S. Dolbilkin, L. E. Lazareva,
         F.A.Nikolaev; Zhur. Eksper. Teoret. Fiz. 45,(6),1694(1963).
1964Br1  R. L. Bramblett, J. T. Caldwell, R. R. Harvey, S. C. Fultz;
         Phys. Rev., 133, B869(1964).
1964Fu1  S. C. Fultz, R. L. Bramblett, J. T. Caldwell, R. R. Harvey;
         Phys. Rev., 133, B1149(1964).
1964Ha2  R. R. Harvey, J. T. Caldwell, R. L. Bramblett, S. C. Fultz;
         Phys. Rev., 136, B126(1964).
1965Be1  B.L. Berman, R.L. Bramblett, J.T. Caldwell, R.R. Harvey,
         S.C. Fultz; Phys. Rev.Lett.,15,727(1965).
1965Wyc  J. M. Wyckoff, B. Ziegler, H. W. Koch, R. Uhlig;
         Phys. Rev. B137, 576(1965).
1966Br1  R. L. Bramblett, J. T. Caldwell, B. L. Berman, R. R. Harvey,
         S. C. Fultz; Phys. Rev., 148, 1198(1966).
1966Fu1  S.C.Fultz, J.T.Caldwell, B.L.Berman, R.L.Bramblett, R.R.Harvey;
         Phys.Rev. 143, 790 (1966).
1967Be2  B. L. Berman, J. T. Caldwell, R. R. Harvey, M. A. Kelly,
         R. L. Bramblett, S. C. Fultz; Phys. Rev., 162, 1098(1967).
1967Cos  S. Costa, F. Ferrero, C. Manfredotti, L. Pasqualini,
         G. Piragino, H. Arenhovel; Nuovo Cimento B, 51, 199(1967),
1968Be5  R.Bergere, R. Beil, A. Veyssiere; Nucl. Phys. A121,
         463(1968).
1968Su1  R. E. Sund, M. P. Baker, L. A. Kull, R. B. Walton;
         Phys.Rev., 176, 1366(1968).
1969Be1  B. L. Berman, R. L. Bramblett, J. T. Caldwell, H. S. Davis,
         M. A. Kelly, S. C. Fultz; Phys. Rev., 177, 1745(1969).
1969Be6  R. Bergere, H. Beil, P. Carlos, A. Veyssiere; Nucl. Phys.,
         A133, 417(1969).
1969Be8  B. L. Berman, M. A. Kelly, R. L. Bramblett, J. T. Caldwell,
         H. S. Davis, S. C. Fultz; Phys. Rev., 185, 1576(1969).
1969Bez  N. Bezic, D. Brajnik, D. Jamnik, G. Kernel;
         Nucl. Phys. A128, 426(1969).
1969Dob  B.S.Dolbilkin, A.I.Isakov, V.I.Korin, L.E.Lazareva, N.V.Linkova,
         B.A.Tulupov; Yadern.Fiz. 9, 675 (1969).
1969Fu1  S. C. Fultz, B. L. Berman, J. T. Caldwell, R. L. Bramblett,
         M. A. Kelly; Phys. Rev., 186, 1255(1969).
1970Be8  B. L. Berman, S. C. Fultz, J. T. Caldwell, M. A. Kelly,
         S. S. Dietrich; Phys. Rev., C2, 2318(1970).
1970Gor  B.I.Goryachev, B.S.Ishkhanov, I.M.Kapitonov, I.M.Piskarev,
         V.G.Shevchenko, O.P.Shevchenko; Yad.Fiz. 11, 252 (1970).
1970Su1  R. E. Sund, V. V. Verbinski, H. Weber, L. A. Kull;
         Phys. Rev., C2, 1129(1970).
1970Ve1  A. Veyssiere, H. Beil, R. Bergere, P. Carlos, A. Lepretre;
         Nucl. Phys. A159, 561(1970).
1971Be4  H. Beil, R. Bergere, P. Carlos, A. Lepretre, A. Veyssiere,
         A. Parlag; Nucl. Phys. A172, 426(1971).
1971Ca1  P. Carlos, H. Beil, R. Bergere, A. Lepretre, A. Veyssiere;
         Nucl. Phys. A172, 437(1971).
1971Fu2  S.C.Fultz, R.A.Alvarez, B.L.Berman, M.A.Kelly, D.R.Lasher,
         T.W.Phillips, J.McElhinney; Phys.Rev. C4, 149 (1971).
1971Le1  A. Lepretre, H. Beil, R. Bergere, P. Carlos, A. Veyssiere,
         M. Sugawara; Nucl. Phys. A175, 609(1971).
1972Ahr  J.Ahrens,H.Borchert,H.B.Eppler,H.Gimm,H.Gundrum; C,72SENDAI,213,1972.
1972De1  T.K.Deague, R.J.J.Stewart; Nucl.Phys. A191, 305 (1972).
1972Yo   L. M. Young, Ph.D. Thesis, University of Illinois(1972),unpublished.
1973Ve1  A. Veyssiere, H. Reil, R. Bergere, P. Carlos, A. Lepretre,
         K. kernbach; Nucl. Phys. A199, 45(1973).
1974Be3  H. Beil, R. Bergere, P. Carlos, A. Lepretre, A. De Miniac,
         A. Veyssiere; Nucl. Phys. A227, 427(1974).
1974Ca5  P. Carlos, H. Beil, R. Bergere, A. Lepretre, A. De Miniac,
         A. Veyssiere; Nucl. Phys. A225, 171(1974).
1974Fu3  S. C. Fultz, R. A. Alvarez, B. L. Berman, P. Meyer;
         Phys. Rev., C10, 608(1974).
1974Le1  A. Lepretre, H. Beil, R. Bergere, P. Carlos, A. De Miniac,
         A. Veyssiere, K. Kernbach; Nucl. Phys. A219, 39(1974).
1974Ve1  A. Veyssiere, H. Beil, R. Bergere, P. Carlos, A. Lepretre,
         A. De Miniac; Nucl. Phys. A227, 513(1974).
1975Ahr  J. Ahrens, H. Borchert, K. H. Czock, H. B. Eppler, H. Gimm,
         H. Gundrum,M. Kroning, P. Riehn, G. Sita Ram, A. Zieger,
         B. Ziegler; Nucl. Phys. A251, 479(1975).
1975Mcc  J.J.McCarthy, R.C.Morrison, H.J.Vander-Molen;
         Phys.Rev.C11,772(1975).
1976Ca1  P. Carlos, H. Beil, R. Bergere, J. Fagot, A. Lepretre,
         A. Veyssiere, G. V. Solodukhov; Nucl. Phys. A258, 365(1976).
1976Gor  B.I.Goryachev, Y.V.Kuznetsov, V.N.Orlin, N.A.Pozhidaeva,
         V.G.Shevchenko; Yad.Fiz. 23, 1145 (1976).
1976Le2  A. Lepretre, H. Beil, R. Bergere, P. Carlos, J. Fagot,
         A.De Miniac, A. Veyssiere, H. Miyase; Nucl. Phys. A258, 350(1976).
1977Gor  A.M.Goryachev, G.N.Zalesnyi; Yad.Fiz. 26, 465 (1977).
1976Gur  G. M. Gurevich, L. E. Lazareva, V. M. Mazur, G. V. Solodukhov,
         B. A. Tulupov; Nucl. Phys. A273, 326(1976).
1978Gur  G. M. Gurevich, L. E. Lazareva, V. M. Mazur, G. V. Solodukhov;
         Prob. Yad. Fiz. Kosm. Luch. 8, 106(1978).
1978Nor  J. W. Norbury, M. N. Thompson, K. Shoda, H. Tsubota;
         Australian Jour. of Phys. 31, 471(1978).
1979Al2  R. A. Alavarez, B. L. Berman, D. D. Faul, F. H. Lewis, Jr.,
         P. Meyer; Phys. Rev., C20, 128(1979).
1979Be4  B. L. Berman, D. D. Faul, R. A. Alvarez, P. Meyer, D. L. Olson;
         Phys. Rev., C19, 1205(1979).
1980Ca1  J. T. Caldwell, E. J. Dowdy, B. L. Berman, R. A. Avarez,
         P. Meyer; Phys. Rev., C21, 1215(1980).
1981Gur  G. M. Gurevich, L. E. Lazareva, V. M. Mazur, S. Yu. Merkulov,
         G. V. Solodukhov, V. A. Tyutin; Nucl. Phys. A351, 257(1981).
1981Ish  B.S.Ishkhanov, I.M.Kapitonov, V.I.Shvedunov, A.I.Gutii,
         A.M.Parlag; Yad.Fiz. 33, 581 (1981).
1985Ahr  J.Ahrens; Nucl.Phys. A446, 229c (1985).
1986Ass  Y I.Assafiri, M.N.Thompson;
         Nucl. Phys. A460 455 (1986).
1986Be1  B. L. Berman, R. E. Pywell, M. N. Thompson, K. G. Mcneill,
         J. W. Jury, J. G. Woodworth; Bull. Am. Phys. Soc. 31, 855(1986).
1986Be2  B. L. Berman, J. T. Caldwell, E. J. Dowdy, S. S. Dietrich,
         P. Meyer, R. A. Alvarez; Phys. Rev., C34, 2201(1986).
1986Var  V.V.Varlamov, P.N.Zaikin, I.M.Kapitonov, M.V.Ufimtsev;
         A.P.Chernyaev; Izv.Akad.Nauk SSSR, Ser.Fiz. 50, 192 (1986).
1987Ahs  M.H.Ahsan, S.A.Siddiqui, H.H.Thies; Nucl.Phys. A469, 381 (1987).
1987O'k  G.J. O'Keefe,M.N. Thompson,Y.I. Assafiri,R.E. Pywel;
         Nucl. Phys. A469 239(1987).
1989Bat  A. D. Bates, R. P. Rassool, E. A. Milne, M. N. Thompson, K.G. Mcneil;
         Phys. Rev. C40, 506(1989).
1989Ras  R.P.Rassool, M.N.Thompson; Phys.Rev. C39, 1631 (1989).
         Phys. Rev. C40, 506(1989).
1995Li1  Liu Jianfen and Su Zongdi; J.Chinese Nucl.Phys.,16,560(1995).
2002Ish  B. S. Ishkhanov, I. M. Kapitonov, E. I. Lileeva, E. V. Shirokov,
         V. A. Erokhova, M. A. Elkin, A. V. Izotova;
         Moscow State Univ.Inst.of Nucl.Phys. Reports, No.2002, 27/711(2002).
2003Er   V. A. Erokhova, M. A. Elkin, A. V. Izotova, B. S. Ishkhanov,
         I. M. Kapitonov, E. I. Lilieva, E. V. Shirokov;
         Izv. Ros. Akad. Nauk, Ser.Fiz. 67, 1479(2003).
2003Rod  T.E.Rodrigues,J.D.T.Arruda-Neto,Z.Carvalheiro,J.Mesa;Phys.Rev.C68(2003).
2003Var  V. V. Varlamov, M. E. Stepanov, V. V. Chesnokov;
         Izv. Ros. Akad. Nauk, Ser.Fiz. 67, 656(2003).
"""

def set_references(references_string: str) -> dict:
    """Parse the references string into a dictionary. """

    # Dictionary to store the parsed references
    references = {}

    # Split the references into individual entries
    lines = references_string.strip().split("\n")

    # Temporary variables
    key   = ""
    value = ""

    for line in lines:
        # Check if the line starts with a key
        if line[:7].strip().isalnum():
            if key:  # If there's already a key, store the previous key-value pair
                references[key] = value.strip()
            # Start a new key-value pair
            key = line[:7].strip()
            value = line[7:].strip()
        else:
            # Append the line to the current value
            value += " " + line.strip()

    # Add the last key-value pair to the dictionary
    if key:
        references[key] = value.strip()
    
    return references

references = set_references(references_string)

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
            if j % 2 == 0:
                data = line1_reader.read(line)
                Z    = int(data[0])
                A    = int(data[1])
                n    = _c.Nuclide(Z=Z, A=A)
                #  Z  A  El Id     Er1     Wr1     Sr1     Er2    Wr2     Sr2        Sr  E_{min}-E_{max} Ref.
                Id   = str(data[3])
                Er1  = float(data[4])
                Wr1  = float(data[5])
                Sr1  = float(data[6])
                Er2  = float(data[7])
                Wr2  = float(data[8])
                Sr2  = float(data[9])
                Sr   = float(data[10])
                temp = data[11].split()
                Emin = float(temp[0])
                Emax = float(temp[2])
                ref  = str(temp[3])
                flag = False
            else:
                #                 dEr1    dWr1    dSr1    dEr2   dWr2    dSr2       dSr
                data = line2_reader.read(line)
                try:
                    dEr1 = float(data[0])
                    dWr1 = float(data[1])
                    dSr1 = float(data[2])
                    dEr2 = float(data[3])
                    dWr2 = float(data[4])
                    dSr2 = float(data[5])
                    dSr  = float(data[6])
                except:
                    dEr1 = None
                    dWr1 = None
                    dSr1 = None
                    dEr2 = None
                    dWr2 = None
                    dSr2 = None
                    dSr  = None
                flag = True
            if flag:
                packet = {'n': n, 'Id': Id, 'Er1': Er1, 'Er2': Er2, 'Wr1': Wr1, 'Wr2': Wr2, 'Sr1': Sr1, 'Sr2': Sr2, 'Sr': Sr,
                          'dEr1': dEr1, 'dEr2': dEr2, 'dWr1': dWr1, 'dWr2': dWr2,
                          'dSr1': dSr1, 'dSr2': dSr2, 'dSr': dSr, 'Emin': Emin, 'Emax': Emax, 
                          'reference': ref,
                         }
                d[n] = packet
    return d


def write_slo_ascii_file(fpath: str, data: dict) -> None:
    """Write ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(SLO_FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line1 = line1_as_tuple(data[n])
            line2 = line2_as_tuple(data[n])
            fp.write(line1_writer.write(line1)+"\n")
            fp.write(line2_writer.write(line2)+"\n")


def write_mlo_ascii_file(fpath: str, data: dict) -> None:
    """Write ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(MLO_FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line1 = line1_as_tuple(data[n])
            line2 = line2_as_tuple(data[n])
            fp.write(line1_writer.write(line1)+"\n")
            fp.write(line2_writer.write(line2)+"\n")


class Entry(_core.Experimental_GDR_Parameter, _db.NuclideDatabaseEntry):
    """An object which represents an entry in the experimental GDR SLO parameter database. """
    pass



class SLO_Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_slo_ascii_file


class MLO_Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_mlo_ascii_file


def load_slo(directory: str = None, file_path: str = None) -> SLO_Database:
    """Load the database into memory and return it. """
    if file_path is not None:
        return _db.load(SLO_Database, file_path)
    elif directory is not None:
        file_path = _os.path.join(directory, slo_local_file_path)
        return _db.load(SLO_Database, file_path)


def load_mlo(directory: str = None, file_path: str = None) -> MLO_Database:
    """Load the database into memory and return it. """
    if file_path is not None:
        return _db.load(MLO_Database, file_path)
    elif directory is not None:
        file_path = _os.path.join(directory, mlo_local_file_path)
        return _db.load(MLO_Database, file_path)
