# stringunitconverter

## Goal
Get the multiplication factor
required to convert from one unit to another,
with the units being given as strings.


## Main concepts
- Use strings to specify units
  (e.g. 'kN').
- Allow quasi all mathematical combinations of units
  (e.g. 'N/m^2').
  Math execution order rules should be respected.
- Keep code short (~100 LOC) and unit-independent
  and put all unit-related data in a data file (JSON).
  It should be easy to add units.
- Focus lies on engineering applications.
  Currency conversion etc. is not supported.
- Working concept:
  1. Keep a data file with a multiplier for each individual unit
     to its SI brother without prefix.
     For example: kg (to g): 1e-3, mmHg (to Pa): 0.00750.
  2. Use this datafile to get the multiplier for each given side to base SI.
     This is done by substituting each prefix and unit in the string
     with the appropriate numerical value.
     The equation, containing only mathematical operations and numbers,
     is then evaluated, returning the multiplier.
  3. Multiplier for the conversion follows from dividing the two derived multipliers.

## Limits and notes
- Dimensional correctness is not checked.
- Conversions are always multiplicative.
  Therefore, conversions between coordinate systems with a different origin
  are not (yet) supported.
  For example, between °C and K.
  (For this reason, °C and °F are deliberately unsupported; use K.)
  Conversions between Hz and s are therefore also not possible,
  as this would require inverting the value.
- SI style conventions are followed. Some notes:
  - A multiplication are defined using a space ` ` or
    a multiplication dot `·`.
    The asterisk `*` (Python multiplication symbol) is also supported
  - Units not separated by a space or multiplication dot (e.g. 'Nm' for 'N·m')
    are not in line with SI style conventions
    and are not supported by this parser.

## Supported prefixes and units
Prefixes: y to Y.  
Units:
- SI: g, N, s, Pa, bar, A, K, mol, Hz, J, W, C, V, Ohm, S, F, L, rad
- Imperial: oz, psi, mi, ft, in, mil, mph
- Nautical: (NM, nmi), (kn, kt)
- other: mmHg, gf, (°, deg, degree)
- also supported: %


Functionality to easily add prefixes will be added in the future.


## Examples
```python3
>>> import stringunitconverter as suc
>>>
>>> suc.multiplier('N/m^2', 'kN/cm^2')
10.0
>>> suc.multiplier('1/kPa', '1/(N/m^2)')
0.001
```


## Contribution and development
### Testing
Tests are in the directory `tests`
in the root directory.
To run the tests, navigate to the root directory
and run
`python tests/test.py`.

This requires a local copy of the repo.
Note that the tests will be run on
the `stringunitconverter` Python package.
This package may or may not point to
the code in the local copy of the repo,
depending on how the package was installed.

Perhaps a testing framework such as `pytest` will be used in the future,
however, currently the tests are very simple
and the codebase to be tested is also very small.
So, it appears that in this particular case
those testing frameworks mostly create overhead.


### To get this repo locally
1. Clone the repo.
The directory with the project will be located in the current working directory of the terminal.
    ```
    $ git clone git@gitlab.com:abaeyens/stringunitconverter.git
    ```
1. Navigate to the created directory.
    ```
    $ cd stringunitconverter
    ```


### Create a local install
A local install allows to try out the library locally.
This can be useful during development.
First, ensure that the project root directory is named `stringunitconverter`.
Second, run in the project root directory:
```
$ python -m pip install -e .
```
This installs the package such that it is accessible
like all other Python packages, e.g. using `import stringunitconverter`.
The `-e` option denotes that it uses a symbolic link:
code changes in the project directory (including branch switching)
take effect at the first following `import`.
No re-installation is required.

Note: `python` should refer to Python 3.
One may have to write `python3` to avoid using Python 2. 

Note: there appear to be problems with this method on some Windows machines.

Note: if it is desired to install several versions of the same package on a single system,
for example a stable version from PyPi
and a development version from a local install,
it may be useful to use
[Python virtual environments](https://docs.python.org/3/tutorial/venv.html).


## Contact
Have a question, suggestion, ... ? Send an email to
[2arne.baeyens@gmail.com](mailto:2arne.baeyens@gmail.com).

It is also possible to use the [GitLab issues webpage](https://gitlab.com/abaeyens/stringunitconverter/-/issues).
