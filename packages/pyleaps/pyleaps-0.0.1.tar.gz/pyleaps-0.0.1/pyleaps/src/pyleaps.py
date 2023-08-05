from itertools import combinations
import numpy as np
import statsmodels.api as sm
import pandas as pd


class regsubsets:
    """
    An approximate translation of R's leaps::regsubsets. Not optimized yet. In the future, automatic handling
    of categorical covariates needs to be added
    INPUTS:
        - df : a Pandas DataFrame which includes response variable (endog_name) and covariates (exog_names)
        - endog_name : the column name for the response variable
        - exog_names : the column names for the covariates (must be a list)
        - method: "full", "forward", "backward" for best set/forward/backward selection
        - maxlen : maximum number of covariates to include (only for best set/forward selection. Neglected otherwise)

    OUTPUTS:
        - summary: returns a data frame containing all the relevant parameters for selection (R2/Adjusted R2/BIC/AIC)
    """
    
    def __init__(self,df,endog_name,exog_names, intercept=True, method="full", maxlen=8):
        """
        Class Constructor
        """
             
        #check for NAs
        assert not df.isna().any().any(), "No NAs allowed in the data set!"
        
        #check how many output variables are selected
        assert type(endog_name) == str, "Only one output variable is accepted!"
        
        #check that the inputs columns are in a list
        assert type(exog_names) == list, "Input covariates names must be included in a list!"
        
        #store data frame inside the class
        self.df = df.copy(deep=True)
        
        #remove all non-numeric columns. This will need to be modified in the future
        non_numeric = []
        for col in exog_names:
            if not pd.api.types.is_numeric_dtype(self.df[col]):
                non_numeric.append(col)
        
        #remove the endog names from the exog and remove also all non-numeric columns
        exog_names = list(set(exog_names)-set([endog_name])-set(non_numeric))
        
        #store the columns into the class
        self.exog_names = exog_names
        self.endog_name = endog_name
        
        #adds the intercept if the user asks so
        self.intercept = intercept
        if self.intercept:
            #add the intercept
            self.df["intercept"] = 1
            self.interceptYesNo = ["intercept"]
        else:
            self.interceptYesNo = []
        
        #set maximum length. If not 
        self.maxlen = min(len(self.exog_names),maxlen)
        
        #perform selection
        if method == "full" :
            self.__searchFull__(maxlen = self.maxlen)
        elif method == "forward":
            self.__searchForward__(maxlen = self.maxlen)
        elif method == "backward":
            self.__searchBackward__()
        
    
    
    def __searchFull__(self,maxlen=None):
        """
        Best Set selection routine. Not to be accessed by the user.
        """
        
        if (maxlen is not None):
            self.maxlen = min(maxlen,self.maxlen)
            
        combinations_dic = {}
        
        for i in range(1,self.maxlen+1):
            rsquared_track = -np.Inf
            rsquared_adj_track = 0
            bic_track = 0
            aic_track = 0
            ssr_track = 0
            
            
            #generate list of combinations to search for given number of parameters
            searchSpace = combinations(self.exog_names,i)
            for it in searchSpace:
                lm_fit = sm.OLS(self.df[self.endog_name],self.df[self.interceptYesNo+list(it)]).fit()
                if lm_fit.rsquared > rsquared_track:
                    best_pars = self.interceptYesNo+list(it)
                    rsquared_track = lm_fit.rsquared
                    rsquared_adj_track = lm_fit.rsquared_adj
                    bic_track = lm_fit.bic
                    aic_track = lm_fit.aic
                    ssr_track = lm_fit.ssr
            
            #store found information into a dictionary, for given number of parameters
            combinations_dic[i] = { "r2"    : rsquared_track     ,
                                    "r2_adj": rsquared_adj_track ,
                                    "bic"   : bic_track          ,  
                                    "aic"   : aic_track          ,
                                    "ssr"   : ssr_track          ,
                                    "vars"  : best_pars          }
            
        self.summary = pd.DataFrame(combinations_dic).T
    
    def __searchForward__(self,maxlen = None):
        """
        Forward selection routine. Not to be accessed by the user.
        """
        
        if (maxlen is not None):
            self.maxlen = min(maxlen,self.maxlen)
        
        combinations_dic = {}
        
        searchList = self.exog_names[:]
        outList = self.interceptYesNo[:]
        
        while (len(searchList)!=0) & (len(list(set(outList)-set(["intercept"]))) < self.maxlen):
            
            rsquared_track = -np.Inf
            rsquared_adj_track = 0
            bic_track = 0
            aic_track = 0
            ssr_track = 0
            
            for col in searchList:
                lm_fit = sm.OLS(self.df[self.endog_name],self.df[outList+[col]]).fit()
                if lm_fit.rsquared > rsquared_track:
                    best_pars = outList+[col]
                    rsquared_track = lm_fit.rsquared
                    rsquared_adj_track = lm_fit.rsquared_adj
                    bic_track = lm_fit.bic
                    aic_track = lm_fit.aic
                    ssr_track = lm_fit.ssr
                
            idx = len(outList+[col])-1 if self.intercept else len(outList+[col])
            combinations_dic[idx] = {"r2"       : rsquared_track      ,
                                     "r2_adj"   : rsquared_adj_track  ,
                                     "bic"      : bic_track           ,
                                     "aic"      : aic_track           ,
                                     "ssr"      : ssr_track           ,
                                     "vars"     : best_pars           }
            
            outList = best_pars
            searchList.remove(outList[-1])
            
        
        self.summary = pd.DataFrame(combinations_dic).T
    
    def __searchBackward__(self):
        """
        Backward selection routine. Not to be accessed by the user.
        """
        
        combinations_dic = {}
        
        searchList = self.exog_names[:]
        outList = self.interceptYesNo[:] + searchList
             
        
        #first, we get the complete fit
        lm_fit = sm.OLS(self.df[self.endog_name],self.df[outList]).fit()
        idx = len(outList)-1 if self.intercept else len(outList)
        combinations_dic[idx] = {"r2"       : lm_fit.rsquared     ,
                                 "r2_adj"   : lm_fit.rsquared_adj ,
                                 "bic"      : lm_fit.bic          ,
                                 "aic"      : lm_fit.aic          ,
                                 "ssr"      : lm_fit.ssr     ,
                                 "vars"     : outList             }

        while len(searchList)!=1:
            
            rsquared_track = -np.Inf
            rsquared_adj_track = 0
            bic_track = 0
            aic_track = 0
            ssr_track = 0
            
            for col in searchList:
                #columns to fit
                fitCol = outList[:]
                fitCol.remove(col)
                lm_fit = sm.OLS(self.df[self.endog_name],self.df[fitCol]).fit()
                if lm_fit.rsquared > rsquared_track:
                    best_pars = fitCol
                    colToRemove = col
                    rsquared_track = lm_fit.rsquared
                    rsquared_adj_track = lm_fit.rsquared_adj
                    bic_track = lm_fit.bic
                    aic_track = lm_fit.aic
                    ssr_track = lm_fit.ssr
                
            idx = len(outList)-2 if self.intercept else len(outList)-1
            combinations_dic[idx] = {"r2"       : rsquared_track      ,
                                     "r2_adj"   : rsquared_adj_track  ,
                                     "bic"      : bic_track           ,
                                     "aic"      : aic_track           ,
                                     "ssr"      : ssr_track           ,
                                     "vars"     : best_pars           }
            
            outList = best_pars
            searchList.remove(colToRemove)
        
        self.summary = pd.DataFrame(combinations_dic).T
