# Installation

## Prerequisites
This manual presumes that you have access to the following: 
* A running linux distribution with python3 installed
* Administrator privileges (sudo rights)
* A working internet connection

## Downloading the software
The latest release of the software can be obtained from https://gitlab.com/truttink/smap/-/releases. If you are familiar with Git, we make sure the latest release matches the contents of the master branch (https://gitlab.com/truttink/smap). However, sometimes one would like to use the latest and greatest developments. These development versions are available in the 'dev' branch (https://gitlab.com/truttink/smap/tree/dev). Thus, the software can be downloaded using three ways:

* Downloading the release: using the browser, or using `wget`.
* Downloading the master branch using the command line (git): `git clone https://gitlab.com/truttink/smap.git`
* Getting the latest developments: `git clone https://gitlab.com/truttink/smap.git; git checkout dev`

## Installing dependencies
The scripts included in this software depend on a couple of python packages, together with the bedtools software. Installing bedtools requires administrator privileges, while installing the python packages can be done in virtual environments. 

### bedtools
This software ships [BEDtools](https://github.com/arq5x/bedtools2), which is covered by an MIT license.

### Python packages.
As noted above, the package dependencies from python can be installed in virtual environments, allowing these dependencies to be installed without administrator privileges and for a single user only. According to the [python docs](https://docs.python.org/3/tutorial/venv.html), a virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages. Creating a virtual environment for python3 is pretty straightforward:

```{bash}
python3 -m venv $environment folder name$ 
```
The above commands will create a folder `$environment folder name$` which contains the new virtual environment. This local environment has the same structure as the global python environment. For example, a python executable can be found in `$environment folder name$/bin/`. However, it is not necessary to adjust scripts to point to the python executable in this folder. Instead, python virtual environments can be activated to perform this adjustment automatically.


A virtual environment can be activated using 
```{bash}
source $environment folder name$/bin/activate
```
When activated, the `$environment folder name$/bin/` folder will be added to the linux PATH. As a consequence, for every python-related operation that the user performs, the activated virtual environment is used. This includes installing and removing software, running python, etc. Environments can also be activated from scripts, making it possible to install software into virtual environments and remove that virtual environment when the script finishes.

For installing python software, `pip` is used. By default pip will install packages from the Python Package Index, https://pypi.org. If packages are installed into a virtual environment, no sudo rights are required. For your convenience, all the python dependencies have been listed in a requirements file. This list of requirements can be passed to `pip`, which will automatically install the dependencies.
By default, virtual environments can ship outdated pip versions. It is necessary to update pip before you continue, otherwise you might get an error that cython is not installed.
``` {bash}
pip install --upgrade pip
pip install smap/
```

After you have finished your analysis in the virtual environment, you leave from the virtual environment by
```{bash}
deactivate
```

## Example installation
```{bash} 
git clone https://gitlab.com/truttink/smap.git
cd smap
git checkout Dev
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```

# Removing smap
Uninstalling smap is a matter of removing the virtual environment and uninstalling `bedtools`. For example:
```{bash}
rm -r .venv
```
