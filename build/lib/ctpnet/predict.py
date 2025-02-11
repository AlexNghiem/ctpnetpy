import numpy as np
import torch.nn as nn
import pandas as pd
import torch.nn.functional as F
import torch
import sys
from . import network

def predict(X,model_file_path):
    """
    Main function: imputation of 12 surface protein abundance from single cell
    RNA-seq matrix.

    Parameters
    ----------
    arg1 : pandas DataFrame
        X: A pandas data.frame with dimension DxN, where D equals to 12611 as 
        the number of genes we trained the neural network; and N is the number 
        of cells. N>=1
    arg2 : str
        path to the trained cTPnet pytorch model for the prediction

    Returns
    -------
    pandas DataFrame
        Impuated surface protein abundance DataFrame, with rows for proteins and
        columns for cells

    """
    print('python package loaded')
    sys.stdout.flush()
    X=X.apply(lambda x: np.log((x*10000.0/sum(x))+1.0), axis=0)
    print('convert input')
    sys.stdout.flush()
    cells=X.columns
    proteins=['CD45RA', 'CD19', 'CD14', 'CD8', 'CD16', 'CD3', 'CD11c', 'CD4','CD56','CD34','CD2','CD57']
    net=network.Net()
    print('init network')
    sys.stdout.flush()
    net.load_state_dict(torch.load(model_file_path))
    print('load network')
    sys.stdout.flush()
    X=torch.t(torch.tensor(X.values))
    X=X.type(torch.FloatTensor)
    y_pred = list(net(X))
    print('imputation')
    sys.stdout.flush()
    y_pred=torch.transpose(torch.stack(y_pred),0,1).view(X.shape[0],-1)
    y_pred=pd.DataFrame(y_pred.detach().numpy().T)
    y_pred.index=proteins
    y_pred.columns=cells
    print('convert format')
    sys.stdout.flush()
    print('python done')
    return(y_pred)

