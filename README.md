### PyTICS will soon be available as a public access package allowing for easy intercalibration of photometric data, applying a maximum likelihood ensemble photometry method. You can use the attatched jupyter notebook to run the algorithm, however for the moment this takes in our LCO data format which you would need to follow (see below) - we are working on integrating a more general input data format. Alternatively, you can contact the author (rv40@st-andrews.ac.uk) if you'd like help with the intercalibration while the package is still being developed.

#### The current data format is a pickle file of all the star data with the following headers:
#### 'id_apass': Unique star identifier ID
#### 'Filter': Filter name
#### 'MJD': Time
#### 'mag_aper': Instrumental magnitude
#### 'err_aper': Uncertainty on instrumental magnitude measurement
#### 'telid: Unique telescope identifier ID

### The jupyter notebook shows example usage of the PyTICS algorithm for NGC 3783 taken with ten Las Cumbres Observatory (LCO) 1-m telescopes for the u band 

### See attached the paper on the algorithm (Vieliute et al. submitted to RASTI)

### Making additional colour corrections as described in the paper will also be available soon

