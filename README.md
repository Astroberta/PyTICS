### Description of the methodology can be found at https://doi.org/10.1093/rasti/rzaf021

### PyTICS allows for easy intercalibration of photometric time-series data, applying a maximum likelihood ensemble photometry method. You can use the attached jupyter notebook ('PyTICS_Example_Use.ipynb') to run the algorithm for now, see below for the data you require. You can contact the author (rv40@st-andrews.ac.uk) if you'd like help with the intercalibration.

### The jupyter notebook shows example usage of the PyTICS algorithm for NGC 3783 taken with ten Las Cumbres Observatory (LCO) 1-m telescopes for the u band 

### 1. <u>Data Format</u>
#### You currently need a list of 6 arrays of data in this order:
#### Date (e.g. in MJD)
#### Filter Name
#### Unique Star identifier
#### Instrumental magnitude
#### Instrumental magnitude error
#### Unique telescope identifier

### This should contain all your available comparisons stars as well as your Target.
### If you encounter plotting errors, try setting the 'plot' argument in the functions to False, you will still get the final data tables - plotting bugs are still being fixed.

### 2. PyTICS package installation (alternative to jupyter notebook)
### The python package is available to install via the usual git clone, but using the jupyter notebook is recommended while the package is being generalised. If you do use the package in this way, this is how to run it:

```python
import PyTICS

#e.g for our LCO AGN data the filters and unique targed identifier:
filters = ['up', 'B', 'V']
AGN_ID = 2387
#e.g for our LCO data, I get the lists from a pickle file:
lco2 = pd.read_pickle('lco_latest_stan.pkl')

Date = lco2.MJD.values
Filter = lco2.Filter.values
Star_IDs = lco2.id_apass.values
Inst_Mag = lco2.mag_aper.values
Inst_Mag_Err = lco2.err_aper.values
Tel_ID = lco2.telid.values

#Data format:
DATA = [Date, Filter, Star_IDs, Inst_Mag, Inst_Mag_Err, Tel_ID]
#Define your list of telescopes, even if its just one:
TEL = pd.unique(lco2.telid.values)

#Run the calibration, which saves star calibration file as .csv
myagn = PyTICS.PyTICS(DATA, TEL, filters, verbose=True,
                     objname='NGC3783', AGN_ID=AGN_ID)
myagn.max_loops = 100
myagn.CalibrateUpdate_New()

#Calibrate your target for specified filter
Calibrated_AGN = myagn.filters['up'].AGN_LC()

```
#### A note on the .csv file with calibrated star data: The dataframe has a lot of columns that are of no use to the general user and are mainly there to track the convergence etc. The file is needed for the final calibration of your target, as shown in the last line of the code above. If desired, the useful columns in the dataframe are the following:

##### mag_aper: calibrated (instrumental) star magnitude

##### err_tot: total noise model derived for the comparison stars. This is the square sum of the nominal uncertainty err_aper, the star-specific noise term rms_star, the telescope-specific noise term rms_sc, and the time-specific noise term rms_t. For the science target, only err_aper, rms_sc, and rms_t are summed in the noise model.

##### DMAGT: time-specific correction parameter applied to the uncalibrated data.

##### DMAGS: teleScope specific correction parameter applied to the uncalibrated data.


