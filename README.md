# RIPLpy

Reference Input Parameter Library

## Description

This is the Python interface for Reference Input Parameter Library (RIPL). This code base is intended for use in supplying, accessing, and general interface with RIPL for use in nuclear physics applications. RIPL is built around "sections" which house  data and parameters for specific nuclear physics properties.

## Installation

To install RIPLpy please perform the following actions:
1. Ensure your local environment is connected to the internet.
2. Download the code from the Git repository.
3. If necessary, unzip the compressed file and switch to the top level directory (which should include this read me file).
4. Perform the appropriate pip installation based off how you want RIPL to behave in your given environment.

```bash
pip3 install -e .
```

* The above command will install the package locally to your machine. Note that the install with the "-e" option allows the package to be updated in real time, so modifications to the source code will be live as soon as you make them. This is ideal for development / research environments and is the most common way to install and use RIPLpy.

```bash
pip3 install
```

* If you want the source to stay exactly as it was on the repository, use the above command instead. Note the lack of the "-e" option. This installation method is intended for production environments. 

* To operate RIPLpy in an environment that does not provide active "outside" internet access, such as on high-performance computing (HPC) clusters or on secure networks, first download the tarball of the required packages and then upload these files along with this directory to the appropriate area. The installation may then proceed via pip in the normal fashion.

## Requirements

The list of Python3 package dependencies is actively kept up in the requirements.txt file. These requirements are automatically satisfied when installing via the above two methods.

## Authors

* Matthew Mumpower {[mumpower@lanl.gov](mailto:mumpower@lanl.gov)}

## License

Distributed under the OSS License. See LICENSE.txt for more information.

## Usage

RIPLpy provides nearly complete access to the databases that comprise RIPL. The code is intended to be well documented. This means you should be able to find how to use the majority of the Application Protocol Interface (API) in the source files themselves. Simple but useful examples are provided below for convenience. 

### Core RIPLpy Usage

* Example: Import the RIPLpy interface in Python:

```python
import riplpy
```

* Example: Load available databases in RIPLpy (warning this could take a long time if all databases are installed):

```python
import riplpy

riplpy.load()
```

* Example: Check if nucleus is in one of the RIPL databases (prints True): 

```python
import riplpy

riplpy.load()
n = Nucleus(Z=50, N=82)
print(riplpy.in_ripl(n)) # Prints True
```

* Example: Check if an element is in one of the RIPL databases (prints True): 

```python
import riplpy

riplpy.load()
e = Element('tin')
print(riplpy.in_ripl(e)) # Prints True
```

* Example: Print the sections a particular nucleus resides in: 

```python
import riplpy

riplpy.load()
n = Nucleus(Z=50, N=82)
print(riplpy.in_sections(n)) # Prints ['densities', 'gamma', 'levels', 'masses']
```

* Example: Print the databases a particular nucleus resides in: 

```python
import riplpy

riplpy.load()
n = Nuclide(Z=50, A=132)
print(riplpy.in_dbs(n)) # Prints [('densities', 'shellcorr_ms'), ('gamma', 'theory_gdr'), ('levels', 'discrete_levels'), ('levels', 'constant_temperature'), ('masses', 'frdm1995'), ('masses', 'hfb14')]

### RIPLpy: Fission Section Usage

* Example: Access the HFB barrier database in the fission section of RIPL:

```python
import riplpy

riplpy.fission.hfb.load()      # Load the database
print(riplpy.fission.hfb.data) # Print all entries the database
```

* Example: Access the empirical barrier database in the fission section of RIPL:

```python
import riplpy

riplpy.fission.empirical.load()      # Load the database
print(riplpy.fission.empirical.data) # Print all entries the database
```

