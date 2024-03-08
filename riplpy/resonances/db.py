"""
The average resonance parameters recommended for RIPL-2 were updated for RIPL-3 
on the basis of the new resonance data compiled by Mughabghab [06M]. This 
compilation includes the most recent experimental data on the individual resonance 
parameters as well as the systematic evaluations of the average resonance spacings, 
the neutron strength functions and the total radiative widths. The independent 
analysis of new experimental data has been carried out also by the Obninsk group 
during the RIPL-3 CRP [04I, 05I]. Differences between the Mughabghab’s and Obninsk 
recommendations were carefully analysed on the last stage of the RIPL-3 report 
preparation. The main attention was paid to an estimation of uncertainties for the 
recommended parameters, based on experienced guesswork of systematic errors beside 
statistical uncertainties. It was noted that the recent Mughabghab’s uncertainties 
of the resonance spacing look too small for nuclides, the individual resonance 
parameters of which were not revised relatively the previous compilations [81M, 84M]. 
For such cases it was decided to prefer the larger uncertainties from the RIPL-2 
owing to the conservative approaches developed under the previous RIPL CRP stages. 
The contradictive data for remaining nuclides were analysed additionally by means 
of the standard approaches [07I] and their results were adopted for the present 
RIPL-3 recommendations. Details of this analysis are given in the final RIPL-3 
report.
The recommended parameters are given separately for s- and p-wave resonances in 
files resonances0.dat and resonances1.dat respectively. The file for s-wave 
resonances contents 300 nuclides and the file for p-wave resonances includes 119 
nuclides.
"""


# ========================

# RIPLpy
import riplpy.db as _db
import riplpy.resonances as _resonances

# ========================

class SwaveDatabase(_db.NuclideDatabase):

    reader: object = _resonances.res.read_ascii_file
    entry : object = _resonances.res.Entry
    writer: object = _resonances.res.write_swave_ascii_file


class PwaveDatabase(_db.NuclideDatabase):

    reader: object = _resonances.res.read_ascii_file
    entry : object = _resonances.res.Entry
    writer: object = _resonances.res.write_pwave_ascii_file
