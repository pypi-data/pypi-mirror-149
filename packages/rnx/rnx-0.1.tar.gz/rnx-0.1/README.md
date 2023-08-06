# rnx

A Python library to read in RINEX files.

This library is designed to read version 2.11 RINEX navigation ('N') and
observation ('O') files, specifically for GPS ('G') system data.

Reading Data
------------
First import the library::

```python
import rnx
```

To read a RINEX file, call the `read` function passing the name of the file::

```python
nav = rnx.read("ohdt0710.22n")
obs = rnx.read("ohdt0710.22o")
```

The type of file (navigation or observation) is determined automatically by the
first line of file, not the extension.  You can also read both a navigation file
and its corresponding observation file in one command::

```python
nav, obs = rnx.read("ohdt0710.22n", "ohdt0710.22o")
```

This has the added advantage of mapping the ephemeris data from the navigation
object to the corresponding moments in time and space vehicles of the
observation object.  It creates a new attribute in the observation object called
`ephs`.

Navigation Objects
------------------
The navigation (`nav`) object has three main attributes: the array of times of
clock `t_oc` in GPS week seconds, the array of PRN numbers for all GPS space
vehicles found in the navigation file, and the matrix of ephemerides `ephs`
corresponding to each pairing of time and PRN.  The relationship of these three
attributes can be visualized as follows::

```
        .--------------.
        |    |    |    | prns
        '--------------'
.----.  .--------------.
|    |  |    |    |    |
|----|  |----|----|----|
|    |  |    |    |    |
|----|  |----|----|----|
|    |  |    |    |    |
'----'  '--------------'
 t_oc                   ephs
```

Not all elements of the `ephs` matrix are populated.  In such cases, the value
of that element of the matrix is `None`.

Suppose we wish to get the ephemeris for the 3rd space vehicle at the first
moment in time.  Then we would do ::

```python
t = nav.t[0]
prn = nav.prns[2]
eph = nav.ephs[0, 2]
```

The attributes of eph are listed in the EphG class.  As an example, if we wanted
to get the square root of the orbit semi-major axis radius, we would do ::

```python
eph.sqrtA
```

The navigation object has an additional property which stores the date and time
stamp of the beginning of the GPS week corresponding to the first record in the
file: `ts_bow`.  So, if we wanted to get the timestamp of the kth moment in
time, we would do ::

```python
ts = nav.ts_bow + datetime.timedelta(seconds=nav.t_oc[k])
```

Observation Objects
-------------------
The observation (`obs`) objects are organized in a manner similar to navigation
objects.  The arrays of receiver times `t` in GPS week seconds and event flags
`events` have as many elements as there are rows in any of the observation
matrices and the arrays of space vehicle names `svs`, system letters `sys`, and
space vehicle numbers `prns` have as many elements as there are columns in the
observation matrices::

```
              .--------------.
              |    |    |    | sys
              :==============:
              |    |    |    | prns
              :==============:
              |    |    |    | svs
              '--------------'
.----..----.  .--------------.
|    ||    |  |    |    |    |
|----||----|  |----|----|----|
|    ||    |  |    |    |    |
|----||----|  |----|----|----|
|    ||    |  |    |    |    |
'----''----'  '--------------'
  t   events                   C1, L2, D5, etc.
```

As an example, GPS satellite 5 would have a `sys` value of 'G', a `prns` value
of 5, and a `svs` value of "G05".  You can find the column index of a space
vehicle by name with the `sv_ind` dictionary::

```python
j = obs.sv_ind["G05"]
```

A RINEX observation file does not necessarily hold every possible type of
observation.  The types are labeled with a letter and a frequency band number.
The possible band numbers are 1, 2, 5, 6, 7, and 8.  The possible letters are ::

Letter | Meaning           | Units
:----: | ----------------- | :----:
 'C'   | C/A pseudorange   | m
 'P'   | P(Y) pseudorange  | m
 'L'   | Carrier phase     | cycles
 'D'   | Doppler frequency | Hz
 'S'   | Signal strength   | dB-Hz

So, to access the C/A pseudorange from the L1 frequency of the jth space vehicle
at the kth moment in time, we would do ::

```python
rho = obs.C1[k, j]
```

Observation types which are no where defined within the RINEX file will still
exist as attributes of the observation object but will have a value of `None`.

To see if a space vehicle has any observation data at a given moment in time,
we can use the `is_vis` matrix::

```python
obs.is_vis[k, j]
```

This is a matrix of boolean values (`True` or `False`).  Very similar to this,
the `vis_prn` matrix is `NaN` wherever `is_vis` is `False` and is equal to the
PRN of the space vehicle wherever `is_vis` is `True`.  So, we could plot the
visibility of space vehicles by PRN with ::

```python
import matplotlib.pyplot as plt
plt.plot(obs.t, obs.vis_prn)
```

Like with the navigation object, we can get the timestamp of the kth moment in
time by ::

```python
ts = obs.ts_bow + datetime.timedelta(seconds=obs.t[k])
```

When a navigation file is read in the same command as an observation object, the
observation object will get an additional attribute called `ephs`.  So, to get
the `C1` pseudorange and corresponding ephemeris for space vehicle `j` at time
`k`, we would do ::

```python
C1 = obs.C1[k, j]
eph = obs.ephs[k, j]
```

Additional attributes are described in the Obs class.

Finding Data
------------
Some sites from which RINEX files can be downloaded for free are ::

-   https://geodesy.noaa.gov/UFCORS/
-   https://gssc.esa.int/portal/
