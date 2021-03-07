import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import plotly.io as pio
import os
import badlands_companion.morphoGrid as morph
from scripts import catchmentErosion as eroCatch


from matplotlib import cm
from scipy.ndimage.filters import gaussian_filter1d


def new(path):

    files = os.listdir(path)

    paths = [os.path.join(path, basename) for basename in files]

    return max(paths, key=os.path.getctime)


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
        
def sea_plot(sea_fall):
    
    age = np.linspace(0, 1000000, 11)
    sea = np.sin(np.linspace(0, np.pi, len(age))) * sea_fall
    sea = np.round(sea, 2)

    plt.figure(figsize = (8, 3))
    plt.plot(age, sea, 'tab:blue')
    plt.plot(age, sea, 'o')
    plt.ylabel('sea-level (m)')
    plt.xlabel('time (years)')
    plt.xlim(0, 1000000)

    sea_level = pd.DataFrame({"age" : age, "sea" : sea}, dtype = float)
    sea_level = sea_level["age"].astype(str).str.zfill(2) + ' ' + sea_level["sea"].astype(str).str.zfill(2)
    sea_level.to_csv("data/sea.csv", index = False, header = False)
      
    
def time_slice(path, sea, crange, title):
    
    fig, ax = plt.subplots(figsize=(22, 4), ncols = 5)

    x = 0

    for i in [1, 2, 5, 8, 10]:
        
        print(f'Loading {(i / 10)} my..')
        
        contours = np.arange(crange[0], crange[1], 10)
        contours = np.delete(contours, np.where(contours == 0))

        dataTIN = eroCatch.catchmentErosion(folder = path, timestep = i)
        dataTIN.regridTINdataSet()
        dataTIN.plotdataSet(data = dataTIN.dz, color='RdBu_r', 
                            depctr = contours,
                crange=crange, erange=[0, 50000, 0, 50000], lw=0.5, size=(2, 2), ax=ax[x])
        
        ax[x].set_title(f'{(i / 10)} my')
        
        df = pd.read_csv(sea, names = ['head'])
        df[['age', 'sea']] = df['head'].str.split(' ', 1, expand=True)
        df = df.drop(columns = 'head')
        df = df.astype('float64')
        
        if df.sea[i] > dataTIN.z.min():
        
            ax[x].contour(dataTIN.xi, dataTIN.yi, dataTIN.z, (df.sea[i],), linestyles = '-',
                  colors='k', linewidths = 2)
        
        x += 1
        
    print(f'Done.')

    plt.suptitle(title, x = 0.495, y = 1.01, fontsize = 14)

    plt.tight_layout(w_pad=2)
    
    plt.savefig(f'figures/{title}_maps.jpg', dpi = 300)
    
    
def section(file, title):
        
    fig, ax = plt.subplots(figsize=(10, 5))

    morpho = morph.morphoGrid(folder=file+'/h5', bbox = [0, 0, 50000, 50000], dx=1000)

    color = iter(cm.viridis(np.linspace(0, 1, 5)))

    for i in [0, 2, 5, 8, 10]:
        
            c = next(color)

            morpho.loadHDF5(timestep=i)
            ax.plot(gaussian_filter1d(morpho.z[25, :], sigma=3), c=c, lw=1.5, label = '{} myr'.format(i/10))

            ax.fill_between(range(51), (gaussian_filter1d(morpho.z[25, :], sigma = 3)), 
                               morpho.z.min()-10, color = c, alpha = 0.2)

            handles, labels = ax.get_legend_handles_labels()
            
            ax.legend(reversed(handles), reversed(labels), loc='upper right', fontsize=12)

            ax.set(ylabel = 'elevation [m]', xlabel = 'downslope distance [km]')

    morpho.loadHDF5(timestep = 0)            
    ax.fill_between(range(51), (gaussian_filter1d(morpho.z[25, :], sigma = 3)), 
                       morpho.z.min()-10, color = 'lightgrey')
    
    ax.plot([0, 50], [0, 0], 'k', linestyle = '--')
    
#     figure_title = file.rsplit('/', 1)[-1]

    plt.suptitle(title, x = 0.53, y = 0.96, fontsize = 14)

    plt.tight_layout()

    plt.savefig(f'figures/{title}_section.jpg', dpi = 300)