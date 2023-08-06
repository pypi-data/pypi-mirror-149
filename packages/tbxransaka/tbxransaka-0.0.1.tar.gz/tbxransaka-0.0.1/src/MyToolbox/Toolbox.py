# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 11:13:53 2022

@author: Ransaka_09914
"""

import pandas as pd
import warnings
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from yellowbrick.cluster import kelbow_visualizer
# except:
#     subprocess.check_call([sys.executable, "-m", "pip", "install", 'yellowbrick'])
    # from yellowbrick.cluster import kelbow_visualizer
from datetime import datetime
from tqdm import tqdm
from sklearn.experimental import enable_iterative_imputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder,StandardScaler,OrdinalEncoder,OneHotEncoder
from sklearn.impute import IterativeImputer,SimpleImputer
import matplotlib.font_manager

warnings.filterwarnings('ignore')
bc = '#FF4F39'

class RFM():
    def __init__(self):
        self.recency_df = None
        self.frequency_df = None
        self.monetary_df = None
        self.rfm_segmentation = None
        
    def RScore(self,x,p,d):
        if x <= d[p][0.25]:
            return 4
        elif x <= d[p][0.50]:
            return 3
        elif x <= d[p][0.75]: 
            return 2
        else:
            return 1
    
    def FMScore(self,x,p,d):
        if x <= d[p][0.25]:
            return 1
        elif x <= d[p][0.50]:
            return 2
        elif x <= d[p][0.75]: 
            return 3
        else:
            return 4
    
    def fit(self,data,cusomer_id_col,date_column,amount_col,trans_id_col='index'):
        data = data.reset_index().copy()
        data[amount_col] = data[amount_col].astype(float)
        now = datetime.now()
        
        self.recency_df = data.groupby(by=cusomer_id_col, as_index=False)[date_column].max()
        self.recency_df.columns = ['CustomerID','LastPurshaceDate']
        self.recency_df['Recency'] = self.recency_df['LastPurshaceDate'].apply(lambda x: (now - x).days)
        
        self.frequency_df = data.groupby(by=[cusomer_id_col], as_index=False)[trans_id_col].count()
        self.frequency_df.columns = ['CustomerID','Frequency']
        
        self.monetary_df = data.groupby(by=cusomer_id_col,as_index=False).agg({amount_col: 'sum'})
        self.monetary_df.columns = ['CustomerID','Monetary']
        
        temp_df = self.recency_df.merge(self.frequency_df,on='CustomerID')
        rfm_df = temp_df.merge(self.monetary_df,on='CustomerID')
        rfm_df.set_index('CustomerID',inplace=True)
        
        self.quantiles = rfm_df.quantile(q=[0.25,0.5,0.75])
        
        self.rfm_segmentation = rfm_df
        self.rfm_segmentation['R_Quartile'] = self.rfm_segmentation['Recency'].apply(self.RScore, args=('Recency',self.quantiles,))
        self.rfm_segmentation['F_Quartile'] = self.rfm_segmentation['Frequency'].apply(self.FMScore, args=('Frequency',self.quantiles,))
        self.rfm_segmentation['M_Quartile'] = self.rfm_segmentation['Monetary'].apply(self.FMScore, args=('Monetary',self.quantiles,))
        
        self.rfm_segmentation['RFMScore'] = self.rfm_segmentation.R_Quartile.map(str) \
                            + self.rfm_segmentation.F_Quartile.map(str) \
                            + self.rfm_segmentation.M_Quartile.map(str)
        return self

def fillna_based_on_mode(df):
    
    """Helper function for fillna based on mode of each column"""
    
    df = df.copy()
    cat_cols = df.select_dtypes(exclude='number').columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode().values[0])
        
    return df

def fillna_based_on_mean(df):
    
    """Helper function for fillna based on mean of each column"""
    
    df = df.copy()
    num_cols = df.select_dtypes('number').columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].mean())
        
    return df

class Clustering():
    
    """Clustering model with Linear and Non-Linear dimensionality reduction techniquess"""
    
    def __init__(self,data,model=KMeans, dim_technique=PCA, max_k=10, n_components=2,n_clusters=10,n_neighbors=100,n_epochs=100,scaler=True,perplexity=25):
        self.data = data.select_dtypes('number').values
        self.model = model
        self.dim_technique = dim_technique
        self.clusters = None
        self.X = None
        self.max_k = max_k
        self.n_components = n_components
        self.n_clusters = n_clusters
        self.perplexity = perplexity
        self.scaler = scaler
        if self.scaler:
            self._scaler = StandardScaler().fit(data.select_dtypes('number').values)
            self.data = self._scaler.transform(data.select_dtypes('number').values)
        else:
            self.data = data.select_dtypes('number').values
        self._is_tsne = False
            
        n_neighbors=n_neighbors
        n_epochs=n_epochs
        
    def kelbow_visualizer(self):
        kelbow_visualizer(self.model(),self.data,k=(2,self.max_k))
    
    def _dim_reduction(self):
        try:
            dim_reduction = self.dim_technique(n_components=self.n_components,random_state=1234)
        except TypeError:
            dim_reduction = self.dim_technique(n_components=self.n_components,perplexity=self.perplexity,n_job=-1)
        
        if dim_reduction.__repr__()=='UMAP()':
            dim_reduction = dim_reduction(**{'n_neighbors':n_neighbors,'n_epochs':n_epochs})
        
        if self.dim_technique().__repr__()=='TSNE()':
            self.transformer = dim_reduction.fit(self.data)
            return dim_reduction.fit_transform(self.data)
        else:
            self.transformer = dim_reduction.fit(self.data)
            return self.transformer.transform(self.data)
    
    def _clustering(self,n_clusters):
        self.X = self._dim_reduction()
        try:
            model = self.model(n_clusters=n_clusters,random_state=1234)
        except:
            model = self.model()
        self._fitted_model = model.fit(self.X)
        self.clusters = self._fitted_model.predict(self.X)
    
    def plot_results(self,n_clusters=None):
        if n_clusters :
            pass
        else:
            n_clusters=self.n_clusters
            
        self._clustering(n_clusters)
        sns.scatterplot(self.X[:,0], self.X[:,1], hue=self.clusters,palette='Set1')
        plt.show()
    
    def predict(self,test):
        
        """
        Predict results for unseen samples
        Expect test as pandas df
        """
        
        if self.scaler:
            test = self._scaler.transform(test.select_dtypes('number').values)
        else:
            test = test.select_dtypes('number').values
        
        if test.shape[1]!= self.data.shape[1]:
            raise ValueError("Invalid number of train and test features")
        else:
            if self.dim_technique().__repr__()=='TSNE()':
                test = self.transformer.fit_transform(test)
            else:
                test = self.transformer.transform(test)
        return self._fitted_model.predict(test)
    
class Encoder():
    def __init__(self):
        self.pipeline = None
    
    def fit(self,data):
        self.feature_names = data.columns.tolist()
        self.index = data.index
        self.numeric_features = data.select_dtypes("number").columns.tolist()
        self.categorical_features = data.select_dtypes('object').columns.tolist()
        
        numeric_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy='median')), ("scaler", StandardScaler())])
        categorical_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy='most_frequent')),("encode",OrdinalEncoder())])
        
        preprocessor = ColumnTransformer(
                                    transformers = [("num", numeric_transformer, self.numeric_features),
                                                    ("cat", categorical_transformer, self.categorical_features)
                                                   ],
            remainder='passthrough'
        )
        self.pipeline = Pipeline(steps=[("preprocessor",preprocessor)])
        self.pipeline.fit(data)
#         self.feature_names = preprocessor.get_feature_names_out()
        return self
    
    def transform(self,data):
        X = self.pipeline.transform(data)
        return pd.DataFrame(X)
    
    def fit_transform(self,data):
        self.fit(data)
        return self.transform(data)
    
    
def kde_target(df, target_col, var_name,verbose=False):
        
    """Helper function for plotting given target vs given feature. Both var_name and target_col data types should be numeric
    """
        
    df = df.copy()

    if df[var_name].dtype=='object':
        print("Not a numeric column")
        return None

    corr = df[target_col].corr(df[var_name])

    plt.figure(figsize = (12, 6))

    for i in df[target_col].unique():
        sns.kdeplot(df.loc[df[target_col] == i, var_name], label = i)


    plt.xlabel(var_name)
    plt.ylabel('Density')
    plt.title('%s Distribution' % var_name)
    plt.legend()

    if verbose:print('The correlation between %s and the TARGET is %0.4f' % (var_name, corr))
    
def target_vs_cat(df,feature,target_col,figsize=(15,8)):
    
    """Helper function for plotting given feature vs. target varible. feature name should be categorical and target_col should be a numericle column"""
    
    df = df.copy()
    
    if df[feature].nunique()<=10:
        nrows = round(df[feature].nunique()/2)
        ncols = 2
    elif df[feature].nunique()<=30:
        nrows = round(df[feature].nunique()/3)
        ncols = 3
    else:
        print("Large unique values...skipping")
        return None
    
#     mapper = {value:key for key,value in dict(enumerate(df[feature].unique())).items()}
    
    fig,ax = plt.subplots(nrows=nrows,ncols=ncols,figsize=figsize)
    for axi,val in zip(ax.flatten(),df[feature].unique()):
        e = df.query(f"{feature}=='{val}'").reset_index(drop=True)
#         e[target_col] = e[target_col].map(mapper)
        e = pd.DataFrame(e[target_col].value_counts()).reset_index()
        colors = sns.color_palette('pastel')[0:len(e)]
        axi.pie(e[target_col], labels = e['index'], colors = colors, autopct='%.0f%%')
        axi.set_title(val,fontweight='bold')
    plt.show()

def plot_decomposition(decompose,data):
    """Function for plotting recomposed results"""

    _,ax = plt.subplots(nrows=4, ncols=1,figsize=(15,12))
    axi = ax.flatten()

    # orginal data
    axi[0].plot(decompose.observed,color='black',alpha=0.6)
    axi[0].set_title('Original data',fontfamily='serif',fontsize=16,bbox=dict(facecolor=bc, edgecolor='black', boxstyle='round'))

    axi[1].plot(decompose.trend,color='black',alpha=0.6)
    axi[1].set_title('Trend',fontfamily='serif',fontsize=16,bbox=dict(facecolor=bc, edgecolor='black', boxstyle='round'))
    axi[1].grid()

    axi[2].plot(decompose.seasonal,color='black',alpha=0.6)
    axi[2].set_title('Seasonal',fontfamily='serif',fontsize=16,bbox=dict(facecolor=bc, edgecolor='black', boxstyle='round'))

    y_resid = pd.date_range(min(data.index),periods=len(data))
    axi[3].bar(y_resid, decompose.resid, color='black', alpha=0.6)
    axi[3].set_title('Residuals',fontfamily='serif',fontsize=16,bbox=dict(facecolor=bc, edgecolor='black', boxstyle='round'))
    axi[3].grid()

    plt.tight_layout()
    plt.show()