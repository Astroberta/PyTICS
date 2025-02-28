### PyTICS will soon be available as a public access package allowing for easy intercalibration of photometric data with a couple lines of code. You can use the attatched jupyter notebook to run the algorithm, however for the moment this is coded to take in our LCO data format - we are working on integrating a more general input data format.

#### The current data format is a pickle file of all the star data with the following headers:
'id_apass': Unique star identifier ID
'Filter': Filter name
'MJD': Time
'mag_aper': Instrumental magnitude
'err_aper': Uncertainty on instrumental magnitude measurement
'telid: Unique telescope identifier ID

### The jupyter notebook shows example usage of the PyTICS algorithm for NGC 3783 taken with ten Las Cumbres Observatory (LCO) 1-m telescopes for the u band 

### See attached the paper on the algorithm (Vieliute et al. submitted to RASTI)

