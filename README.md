### Description of the methodology can be found at https://arxiv.org/abs/2505.23328

### PyTICS will soon be available as a public access package allowing for easy intercalibration of photometric data, applying a maximum likelihood ensemble photometry method. You can use the attached jupyter notebook ('PyTICS_Example_Use.ipynb') to run the algorithm for now, see below for the data you require. You can contact the author (rv40@st-andrews.ac.uk) if you'd like help with the intercalibration while the package is still being developed.

#### You currently need a list of 6 arrays of data in this order:
#### Date (e.g. in MJD)
#### Filter Name
#### Unique Star identifier
#### Instrumental magnitude
#### Instrumental magnitude error
#### Unique telescope identifier

### This should contain all your available comparisons stars as well as your Target.

### The jupyter notebook shows example usage of the PyTICS algorithm for NGC 3783 taken with ten Las Cumbres Observatory (LCO) 1-m telescopes for the u band 

### If you encounter plotting errors, try setting the 'plot' argument in the functions to False, you will still get the final data tables - plotting bugs are still being fixed.
