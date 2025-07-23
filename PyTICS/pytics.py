from .filter import Filter
import pandas as pd
import pickle

class PyTICS:
    """
    def __init__(self, datafile, names_list,verbose=True, objname = 'MyAGN',AGN_ID = None):
        # Initialize a list of NestedObject instances with different names
        #self.filters = [FilterObject(name, default_value) for name in names_list]
        if verbose: print(f" [PyTICS] Calibrating {objname} field")
        self.verbose = verbose
        self.objname = objname
        self.filters = {name: Filter(name,verbose = self.verbose) for name in names_list}
        self.AGN_ID = AGN_ID
        self.catalogue = 'apass_updated.csv'
        if verbose: print(" [PyTICS] Loading Data...")
        self.lco = pd.read_pickle(datafile)
        self.TEL = list(pd.unique(self.lco['telid']))

        self.Corrs = {} # initialise Corr output dict.
        # Optional parameters
        self.max_loops = 200
        self.frac = 0.5
        self.safe = 0.6
        self.bad_IDs = []
        self.star_lim = 100 
        self.Plot = False  # Plot all lightcurves
        self.unit = 'mag'
        self.err_th = 0.05
        self.Rem_out = True
        
        if verbose: print(' [PyTICS] Telescopes Detected:\n        ', self.TEL)
        print(" [PyTICS] Cleaning....")
        self.lco2 = self.Clean(self.lco)
    
    """
    def __init__(self, data_arrays, TEL, names_list,verbose=True, objname = 'MyAGN',AGN_ID = None):
        # Initialize a list of NestedObject instances with different names
        #self.filters = [FilterObject(name, default_value) for name in names_list]
        if verbose: print(f" [PyTICS] Calibrating {objname} field")
        self.data_arrays = data_arrays
        self.verbose = verbose
        self.objname = objname
        self.filters = {name: Filter(name,verbose = self.verbose) for name in names_list}
        self.AGN_ID = AGN_ID
        self.TEL = TEL
        
        self.Corrs = {} # initialise Corr output dict.
        # Optional parameters
        self.max_loops = 200
        self.frac = 0.5
        self.safe = 0.6
        self.bad_IDs = []
        self.star_lim = 100 
        self.Plot = False  # Plot all lightcurves
        self.unit = 'mag'
        self.err_th = 0.05
        self.Rem_out = True

    
    
    def __repr__(self):
        return f"PyTICS(nested_objects={self.filters})"

    def LoadStarFile(self,flnname=None):
        if flnname == None: 
            flnname = self.objname+'_Calibrated_Stars.pkl'
        star_data = pd.read_pickle(flnname)
        for name, filt in self.filters.items():
            if self.verbose: print(f" [PyTICS] Loading Filter: {name}")
            ss = (star_data.Filter == name)
            filt.DF = star_data[ss]
            if self.verbose:
                print('      Latest image Processed: {}'.format(filt.DF.MJD.max()))
            
    def Calibrate(self):
        """ Do all the filters at once"""
        self.DF = {}
        self.TR = {}
        self.All_DF = pd.DataFrame()
        for name, filt in self.filters.items():
            if self.verbose: print(f" [PyTICS] Processing Filter: {name}")
            # Example operation: append '-processed' to the value of each object
            #filt.name += "-processed"
            
            filt.Corr(self.lco2, name, MAX_LOOPS = self.max_loops, bad_IDs = self.bad_IDs,
                                        safe = self.safe, frac = self.frac, TEL = self.TEL, 
                                        AGN_ID = self.AGN_ID, Star_Lim = self.star_lim)

            filt.Phot_Cal( name ,catalogue=self.catalogue)
            if self.All_DF.empty:
                self.All_DF = filt.DF
            else:
                self.All_DF = pd.concat([self.All_DF,filt.DF],ignore_index=True,)
        self.All_DF.to_pickle(self.objname +'_Calibrated_Stars'+'.pkl')
        if self.verbose: 
            print(' [PyTICS] Saved Field Stars in: '+ self.objname +'_Calibrated_Stars.csv')

    def CalibrateUpdate(self):
        """ Do all the filters at once"""
        self.All_DF = pd.DataFrame()
        for name, filt in self.filters.items():
            if self.verbose: print(f" [PyTICS] Processing Filter: {name}")
            # Example operation: append '-processed' to the value of each object
            #filt.name += "-processed"
            if self.verbose:
                print('      Latest image taken: {}'.format(self.lco2.MJD.max()))
            filt.CorrUpdate(self.lco2, name, MAX_LOOPS = self.max_loops, bad_IDs = self.bad_IDs,
                                        safe = self.safe, frac = self.frac, TEL = self.TEL, 
                                        AGN_ID = self.AGN_ID, Star_Lim = self.star_lim)

            filt.Phot_Cal( name ,catalogue=self.catalogue)
            if self.All_DF.empty:
                self.All_DF = filt.DF
            else:
                self.All_DF = pd.concat([self.All_DF,filt.DF],ignore_index=True,)
        self.All_DF.to_csv(self.objname +'_Calibrated_Stars'+'.csv')
        if self.verbose: 
            print(' [PyTICS] Saved Field Stars in: '+ self.objname +'_Calibrated_Stars.csv')
    
    def CalibrateUpdate_New(self):
        """ Do all the filters at once"""
        self.All_DF = pd.DataFrame()
        for name, filt in self.filters.items():
            if self.verbose: print(f" [PyTICS] Processing Filter: {name}")
            # Example operation: append '-processed' to the value of each object
            #filt.name += "-processed"
            #if self.verbose:
            #    print('      Latest image taken: {}'.format(self.lco2.MJD.max()))
            
            filt.CorrUpdate_New(self.data_arrays, self.TEL, name, MAX_LOOPS = self.max_loops, bad_IDs = self.bad_IDs,
                                        safe = self.safe, frac = self.frac, TEL = self.TEL, 
                                        AGN_ID = self.AGN_ID, Star_Lim = self.star_lim)

            filt.Phot_Cal( name ,catalogue=self.catalogue)
            if self.All_DF.empty:
                self.All_DF = filt.DF
            else:
                self.All_DF = pd.concat([self.All_DF,filt.DF],ignore_index=True,)
                
        self.All_DF.to_csv(self.objname +'_Calibrated_Stars'+'.csv')
        if self.verbose: 
            print(' [PyTICS] Saved Field Stars in: '+ self.objname +'_Calibrated_Stars.csv')
    
    def AGNCalibrate(self):
        # AGN = pd.concat([AGN_DF_up, AGN_DF_B, AGN_DF_gp, 
        #       AGN_DF_V, AGN_DF_rp, AGN_DF_ip, AGN_DF_zs], ignore_index=True)
        if self.lco2 is None:
            self.lco2 = pd.read_pickle(self.objname +'_Calibrated_Stars.pkl')
        self.AGN = pd.DataFrame()
        for name, filt in self.filters.items():
            if self.verbose: print(f"Processing {name}: {filt}")
            if self.AGN.empty:
                self.AGN = filt.AGN_LC( unit = self.unit, 
                                err_th = self.err_th, Plot = self.Plot,
                                Rem_out = self.Rem_out, TEL = self.TEL, 
                                AGN_ID = self.AGN_ID, zp = None)
            else:
                # Append to the combined DataFrame
                self.AGN = pd.concat([self.AGN,
                                      filt.AGN_LC( unit = self.unit,err_th = self.err_th, 
                                                  Plot = self.Plot, Rem_out = self.Rem_out , 
                                                  TEL = self.TEL, AGN_ID = self.AGN_ID, zp = None)],
                                     ignore_index=True)
 
        self.AGN.to_pickle(self.objname +'_Calibrated_AGN'+'.pkl')
        self.AGN.to_csv(self.objname +'_Calibrated_AGN'+'.csv')
        if self.verbose: print(' [PyTICS] Saved AGN LC in:'+ self.objname +'_Calibrated_AGN.csv')
            



                       
    def Clean(self,Star_File,bad_err_size = 20):
        """ Drop duplicate values, existing zp and zp_err columns, and strange errors (= 99.0).
        
        Input:
        Star_File - Original data file (pd dataframe).
        
        Output:
        File2 - Cleaned up data file (pd dataframe).
        """
        
        File2 = Star_File.drop(columns = ["zp", "zp_err"])
        File2 = File2.drop_duplicates(subset=['id_apass', 'Filter', 'MJD', 
                                              'corr_aper', 'telid', 'airmass', 'seeing'], 
                                      keep='first', inplace=False, ignore_index=False)
        File2 = File2.drop(File2[(File2['err_aper'] > bad_err_size)].index)
        return(File2)
        
