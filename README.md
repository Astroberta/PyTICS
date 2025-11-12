### Description of the methodology can be found at https://doi.org/10.1093/rasti/rzaf021

### PyTICS allows for easy intercalibration of photometric time-series data, applying a maximum likelihood ensemble photometry method. You can use the attached jupyter notebook ('PyTICS_Example_Use.ipynb') to run the algorithm for now, see below for the data you require. There is also an installable package available, see below instructions for usage. You can contact the author (rv40@st-andrews.ac.uk) if you'd like help with the intercalibration.

### The jupyter notebook shows example usage of the PyTICS algorithm for NGC 3783 taken with ten Las Cumbres Observatory (LCO) 1-m telescopes for the u band, as described in the linked publication. 

### 1. **Data Format**
#### You currently need a list of 6 arrays of data in this order:
##### i) Date (e.g. in MJD)
##### ii) Filter Name
##### iii) Unique Star identifier
##### iv) Instrumental magnitude
##### v) Instrumental magnitude error
##### vi) Unique telescope identifier

#### This should contain all your available comparisons stars as well as your Target.
#### If you encounter plotting errors, try setting the 'plot' argument in the functions to False, you will still get the final data tables - plotting bugs are still being fixed.

### 2. **PyTICS package installation (alternative to jupyter notebook)**
#### The python package is available to install via the usual git clone, but using the jupyter notebook is recommended while the package is being generalised. If you do use the package in this way, this is how to run it:

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

### 3. **Empirical colour-corrections**
#### As described in the linked publication, using 32 AGN fields we find consistent slopes of the residuals vs star-colours unique to each telescope, that can be used to derive the colour-dependent offsets in the LCO telescope data (the 'global solution'). The same colour-corrections can be derived with PyTICS for indivudal fields again using the attached jupyter notebook.
#### Given the u-g colour index C(u-g) of your target, the colour correction parameter can be computed as a*C(u-g) + b, where a and b are specific to each filter.

#### u band
| Telescope       | a | b |
|------------|:---:|:------------:|
| 1m001      |  0.0017263414071372986 ± 0.0005901625148146004 | -0.0032159407063751125 ± 0.0010161079369647597   |
| 1m003        |  -0.0065355305507921345 ± 0.0004991478377633185 | 0.009368118410877117 ± 0.0008511225966782469    |
| 1m004    |  0.0017020014195029487 ± 0.0008145923267436035 | -0.0016606518318294375 ± 0.0013708218147007601     |
| 1m005    |  -0.0006664675164166133 ± 0.00036645591842454303 | 0.0012770948905568098 ± 0.0006198747445340367     |
| 1m006    |  0.0014266992425666486 ± 0.000462702831935573 | -0.002868846228322815 ± 0.0007839345082349487     |
| 1m008    |  0.0012654450189588684 ± 0.0004504291270247489 | -0.0017610598500437098 ± 0.0007640127735934264     |
| 1m009    |  0.00298429430422531 ± 0.0003050136375345996 | -0.004650331996861675 ± 0.0005124902521514217     |
| 1m010    |  0.0017884887021757 ± 0.0005352035785321668 | -0.0030229795234532897 ± 0.0009008667692451755     |
| 1m011    |  -0.010912499177185859 ± 0.0005501797921170391 | 0.016485742319032076 ± 0.0009240916650843922     |
| 1m012    |  0.005664952047148578 ± 0.0004312673044256114 | -0.008346621166215144 ± 0.0007348664192273029     |
| 1m013    |  -0.0014274690905561683 ± 0.00043541683215359386 | 0.0022804782281842404 ± 0.0007281224844010012     |
| 1m014    |  0.003707327584200889 ± 0.00047516139873966627 | -0.005501661626963999 ± 0.0008018081738138129     |

#### B band
| Telescope       | a | b |
|------------|:---:|:------------:|
| 1m001      |  0.004175815110471496 ± 0.0004777203330014147 | -0.00535782195111683 ± 0.0008191444765644996 |
| 1m003        |  -0.01523830092171476 ± 0.0006262809442429832 | 0.023317868660900992 ± 0.0010605268372192705 |
| 1m004    |  -0.02921181968947498 ± 0.0008051187432256742 | 0.045301973375972 ± 0.0013649788519055628|
| 1m005    |  0.020704312702169533 ± 0.0005597542488654725 | -0.03219742849361546 ± 0.0009406218426790819 |
| 1m006    |  -0.00549491354851794 ± 0.000430556278899436 | 0.008494504665349595 ± 0.0007278284958083668 |
| 1m008    |  -0.004806567502356087 ± 0.0005357969091102969 | 0.004958028331129685 ± 0.0009109923592714405 |
| 1m009    |  -0.006077323406509686 ± 0.0005955721309926824 | 0.009585095765108841 ± 0.0009968683432225855 |
| 1m010    |  0.018544688760144756 ± 0.0007615644433857684 | -0.028942225367428853 ± 0.0012861441918137467 |
| 1m011    |  -0.02163759083534493 ± 0.0006589488227508183 | 0.03391315931691288 ± 0.0011226776997971012 |
| 1m012    |  0.003405474780052887 ± 0.0004857704361980028 | -0.005416418614304406 ± 0.0008117183544171544 |
| 1m013    |  0.01655989928593596 ± 0.0005293215334977591 | -0.025643578008209184 ± 0.0008986845787380647 |
| 1m014    | 0.009909376779915005 ± 0.0005592940716768443 |  -0.013001063787418957 ± 0.0009479233795874628 |


#### g band
| Telescope       | a | b  |
|------------|:---:|:------------:|
| 1m001      |  ** | **    |
| 1m003        |  ** | **    |
| 1m004    |  ** | **     |
| 1m005    |  ** | **     |
| 1m006    |  ** | **     |
| 1m008    |  ** | **     |
| 1m009    |  ** | **     |
| 1m010    |  ** | **     |
| 1m011    |  ** | **     |
| 1m012    |  ** | **     |
| 1m013    |  ** | **     |

#### V band
| Telescope       | a | b  |
|------------|:---:|:------------:|
| 1m001      |  ** | **    |
| 1m003        |  ** | **    |
| 1m004    |  ** | **     |
| 1m005    |  ** | **     |
| 1m006    |  ** | **     |
| 1m008    |  ** | **     |
| 1m009    |  ** | **     |
| 1m010    |  ** | **     |
| 1m011    |  ** | **     |
| 1m012    |  ** | **     |
| 1m013    |  ** | **     |

#### r band
| Telescope       | a | b  |
|------------|:---:|:------------:|
| 1m001      |  ** | **    |
| 1m003        |  ** | **    |
| 1m004    |  ** | **     |
| 1m005    |  ** | **     |
| 1m006    |  ** | **     |
| 1m008    |  ** | **     |
| 1m009    |  ** | **     |
| 1m010    |  ** | **     |
| 1m011    |  ** | **     |
| 1m012    |  ** | **     |
| 1m013    |  ** | **     |

#### i band
| Telescope       | a | b  |
|------------|:---:|:------------:|
| 1m001      |  ** | **    |
| 1m003        |  ** | **    |
| 1m004    |  ** | **     |
| 1m005    |  ** | **     |
| 1m006    |  ** | **     |
| 1m008    |  ** | **     |
| 1m009    |  ** | **     |
| 1m010    |  ** | **     |
| 1m011    |  ** | **     |
| 1m012    |  ** | **     |
| 1m013    |  ** | **     |

#### z band
| Telescope       | a | b  |
|------------|:---:|:------------:|
| 1m001      |  ** | **    |
| 1m003        |  ** | **    |
| 1m004    |  ** | **     |
| 1m005    |  ** | **     |
| 1m006    |  ** | **     |
| 1m008    |  ** | **     |
| 1m009    |  ** | **     |
| 1m010    |  ** | **     |
| 1m011    |  ** | **     |
| 1m012    |  ** | **     |
| 1m013    |  ** | **     |




