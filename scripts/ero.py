import pandas as pd
import numpy as np

def ero(surface, erodibility):

        xyz = pd.read_csv(surface, sep=r'\s+', engine='c', header=None, 
                          na_filter=False, dtype=np.float, low_memory=False)
        xr = xyz.values[:,0]
        yr = xyz.values[:,0]
        dx = xr[1]-xr[0]

        nx = int((xr[-1]-xr[0])/dx)+1
        ny = int((yr[-1]-yr[0])/dx)+1

        assert nx*ny==len(xr), 'Values not matching'

        xm = xr.reshape((nx,ny),order='F')
        ym = yr.reshape((nx,ny))

        print('Regular grid resolution:',nx,ny)

        xyz.columns = ['x', 'y', 'z']

        ## Marine

        xyz.loc[xyz['z'] >= 0, 'k'] = erodibility
        xyz.loc[xyz['z'] <= 0, 'k'] = erodibility

        ero = xyz.drop(columns=['x', 'y', 'z'])

        ero.to_csv('data/ero.csv', sep=' ', index=False , header=0)