import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter(action = "ignore", category = FutureWarning)

import cmocean as cmo
from matplotlib import cm
from scripts import catchmentErosion as eroCatch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import badlands_companion.morphoGrid as morph
import badlands_companion.stratalAnalyse as strata
import badlands_companion.simpleSection as sec
from scipy.ndimage.filters import gaussian_filter1d
import os
import pandas as pd

mpl.rcParams['font.family'] = 'Arial'
plt.rcParams.update({'font.size': 13})

def sedero(path, t1, t2, t3, t4, t5, t6, suptitle, file, savefig=False):
    
    fig, ax = plt.subplots(figsize=(7.5,18), nrows=6, ncols=2, constrained_layout=True)
        
    x = 0

    paths = [f.path for f in os.scandir(path) if f.is_dir()]
    paths.sort()
    
    sh_i = [100000, 100000, 0, 300000]
    slu_i = [100000, 150000, 0,  300000]
    # sll_i = [100000, 150000, 0, 300000]
    b_i = [150000, 300000, 0, 300000]

    for i in paths:
        print(i)
        dataTIN = eroCatch.catchmentErosion(folder=i,timestep=100)
        dataTIN.regridTINdataSet()
        dataTIN.plotdataSet(data=dataTIN.dz, color='RdBu_r',  
                crange=[-60, 60], erange=[0, 300000, 0, 300000],
                depctr=[-30, -20, -10, 10, 20, 30], lw=0.5, size=(3,3), ax=ax[x, 0])

        if 'sw' in i:
            shelf = 100000
            ax[x, 0].plot([shelf, shelf], [0, 300000], c='k', lw=1.5, linestyle='dashed')
            shelf += 10000
        
        else: 
            ax[x, 0].plot([130000, 130000], [0, 300000], c='k', lw=1.5, linestyle='dashed')

        if x == 0:
            ax[x, 0].set_title(t1)
        if x == 1:
            ax[x, 0].set_title(t2)
        if x == 2:
            ax[x, 0].set_title(t3)
        if x == 3:
            ax[x, 0].set_title(t4)
        if x == 4:
            ax[x, 0].set_title(t5)
        if x == 5:
            ax[x, 0].set_title(t6)

        vst_so = []
        vst_sh = []
        vst_slu = []
        vst_ba = []
        
        vet_so = []
        vet_sh = []
        vet_slu = []
        vet_ba = []
        
        time = 10000

        if 'sw' in i:
            
            for j in np.arange(0, 100, 1):

                dataTIN = eroCatch.catchmentErosion(folder=i, timestep=j)
                dataTIN.regridTINdataSet()
                
#                 vs_so = (dataTIN.getDepositedVolume(time=time, erange= [0, 100000, 0, 300000])/time)
#                 ve_so = (dataTIN.getErodedVolume(time=time, erange= [0, 100000, 0, 300000])/time)
#                 vst_so.append(vs_so)
#                 vet_so.append(ve_so)
                
                vs_sh = (dataTIN.getDepositedVolume(time=time, erange=sh_i)/time)
                vs_slu = (dataTIN.getDepositedVolume(time=time, erange=slu_i)/time)
                vs_ba = (dataTIN.getDepositedVolume(time=time, erange=b_i)/time)

                ve_sh = (dataTIN.getErodedVolume(time=time, erange=sh_i)/time)
                ve_slu = (dataTIN.getErodedVolume(time=time, erange=slu_i)/time)
                ve_ba = (dataTIN.getErodedVolume(time=time, erange=b_i)/time)

                vst_sh.append(vs_sh)
                vst_slu.append(vs_slu)
                vst_ba.append(vs_ba)
                
                vet_sh.append(ve_sh)
                vet_slu.append(ve_slu)
                vet_ba.append(ve_ba)

            sh_i[1] = sh_i[1] + 10000
            slu_i[:2] = [x + 10000 for x in slu_i[:2]]
    #       sll_i[:2] = [x + 10000 for x in sll_i[:2]]
            b_i[1] = b_i[1] + 10000
        
        else:
            
            ax[x, 0].plot([130000, 130000], [0, 300000], c='k', lw=1.5, linestyle='dashed')

            for j in np.arange(0, 100, 1):
                
                dataTIN = eroCatch.catchmentErosion(folder=i, timestep=j)
                dataTIN.regridTINdataSet()
                
#                 vs_so = (dataTIN.getDepositedVolume(time=time, erange= [0, 100000, 0, 300000])/time) 
#                 ve_so = (dataTIN.getErodedVolume(time=time, erange= [0, 100000, 0, 300000])/time) # source-transfer
#                 vst_so.append(vs_so)
#                 vet_so.append(ve_so

                vs_sh = (dataTIN.getDepositedVolume(time=time, erange= [100000, 130000, 0, 300000])/time)
                vs_slu = (dataTIN.getDepositedVolume(time=time, erange=[130000, 180000, 0,  300000])/time)
                vs_ba = (dataTIN.getDepositedVolume(time=time, erange=[180000, 300000, 0, 300000])/time)
                
                ve_sh = (dataTIN.getErodedVolume(time=time, erange= [100000, 130000, 0, 300000])/time)
                ve_slu = (dataTIN.getErodedVolume(time=time, erange=[130000, 180000, 0,  300000])/time)
                ve_ba = (dataTIN.getErodedVolume(time=time, erange=[180000, 300000, 0, 300000])/time)
                
                vst_sh.append(vs_sh)
                vst_slu.append(vs_slu)
                vst_ba.append(vs_ba)
                
                vet_sh.append(ve_sh)
                vet_slu.append(ve_slu)
                vet_ba.append(ve_ba)
                
        ax2 = ax[x, 1].twinx()
        
        # source-transfer
#         ax[x, 1].plot(np.linspace(0, 1, 100), [x / 1e6 for x in vst_so], 
#                       c = 'indianred', linestyle='solid', label = 'source +\ntransfer')
#         ax2.plot(np.linspace(0, 1, 100), [x / 1e6 for x in vet_so], 
#                  c = 'tab:blue', linestyle='solid')
                
        ax[x, 1].plot(np.linspace(0, 1, 100), [x / 1e6 for x in vst_sh], 
                      c = 'indianred', linestyle='solid', label = 'shelf')
        ax[x, 1].plot(np.linspace(0, 1, 100), [x / 1e6 for x in vst_slu], 
                      c = 'indianred', linestyle='dashed', label = 'u. slope')
        ax[x, 1].plot(np.linspace(0, 1, 100), [x / 1e6 for x in vst_ba], 
                      c = 'indianred', linestyle=(0, (1,1)), label = 'l. slope &\nbasin floor')
        ax[x, 1].set_xlabel('Time [myr]')
        ax[x, 1].set_ylabel('Qs [m$^3$/myr]', color='indianred')
        ax[x, 1].legend(loc='upper left', fontsize=11, frameon=False)    
        ax[x, 1].set_xlim(left = 0, right = 1)
        ax[x, 1].set_ylim(bottom = 0, top = 70) # normal
#         ax[x, 1].set_ylim(bottom = 0, top = 2100) # cumsum
#         ax[x, 1].set_ylim(bottom = 0, top = 0.005) # source-transfer
        ax[x, 1].tick_params(axis='y', labelcolor='indianred')
        
        ax[x, 1].set_title('Erosion-deposition vs. time')

        ax2.plot(np.linspace(0, 1, 100), [x / 1e6 for x in vet_sh], 
                 c = 'tab:blue', label = 'Shelf', linestyle='solid')
        ax2.plot(np.linspace(0, 1, 100), [x / 1e6 for x in vet_slu],
                 c = 'tab:blue', label = 'Upper slope', linestyle='dashed')
        ax2.plot(np.linspace(0, 1, 100), [x / 1e6 for x in vet_ba], 
                 c = 'tab:blue', label = 'Lower slope &\nBasin floor', linestyle=(0, (1,1)))
        ax2.set_ylabel('Qe [m$^3$/myr]', color='tab:blue')   
        ax2.set_xlim(left = 0, right = 1)
        ax2.set_ylim(top = 0, bottom = -14) # normal
#         ax2.set_ylim(top = 0, bottom = -320) # cumsum
#         ax2.set_ylim(top = 0, bottom = -50) # source-transfer
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        x += 1

    plt.suptitle(suptitle, fontweight='bold', x = 0.46, y = 1.01, fontsize=15)
    plt.tight_layout(w_pad=1.2)
    if savefig == True:
        plt.savefig('figures/compare_{}.pdf'.format(file), dpi = 400, bbox_inches = 'tight')

def volumes(path, title, labels, xlabel, ax1, ax2, legend=False):

        ax1 = ax1
        ax2 = ax2
        
        paths = [f.path for f in os.scandir(path) if f.is_dir()]
        paths.sort()

        vst_sh = []
        vst_slu = []
        vst_ba = []
        
        vet_sh = []
        vet_slu = []
        vet_ba = []

        time = 10000
        
        sh_i = [100000, 100000, 0, 300000]
        slu_i = [100000, 150000, 0,  300000]
        b_i = [150000, 300000, 0, 300000]

        for i in paths:
            
            if 'sw' in i:
                
                dataTIN = eroCatch.catchmentErosion(folder=i, timestep=100)
                dataTIN.regridTINdataSet()
        
                vs_sh = (dataTIN.getDepositedVolume(time=time, erange=sh_i)/time)/1e6
                vs_slu = (dataTIN.getDepositedVolume(time=time, erange=slu_i)/time)/1e6
                vs_ba = (dataTIN.getDepositedVolume(time=time, erange=b_i)/time)/1e6

                ve_sh = (dataTIN.getErodedVolume(time=time, erange=sh_i)/time)/1e6
                ve_slu = (dataTIN.getErodedVolume(time=time, erange=slu_i)/time)/1e6
                ve_ba = (dataTIN.getErodedVolume(time=time, erange=b_i)/time)/1e6

                vst_sh.append(vs_sh)
                vst_slu.append(vs_slu)
                vst_ba.append(vs_ba)

                vet_sh.append(ve_sh)
                vet_slu.append(ve_slu)
                vet_ba.append(ve_ba)

                sh_i[1] = sh_i[1] + 10000
                slu_i[:2] = [x + 10000 for x in slu_i[:2]]
                b_i[1] = b_i[1] + 10000
                
            else:
                
                dataTIN = eroCatch.catchmentErosion(folder=i, timestep=100)
                dataTIN.regridTINdataSet()
                    
                vs_sh = (dataTIN.getDepositedVolume(time=time, erange= [100000, 130000, 0, 300000])/time)/1e6
                vs_slu = (dataTIN.getDepositedVolume(time=time, erange=[130000, 180000, 0,  300000])/time)/1e6
                vs_ba = (dataTIN.getDepositedVolume(time=time, erange=[180000, 300000, 0, 300000])/time)/1e6
                
                ve_sh = (dataTIN.getErodedVolume(time=time, erange= [100000, 130000, 0, 300000])/time)/1e6
                ve_slu = (dataTIN.getErodedVolume(time=time, erange=[130000, 180000, 0,  300000])/time)/1e6
                ve_ba = (dataTIN.getErodedVolume(time=time, erange=[180000, 300000, 0, 300000])/time)/1e6
                
                vst_sh.append(vs_sh)
                vst_slu.append(vs_slu)
                vst_ba.append(vs_ba)
                
                vet_sh.append(ve_sh)
                vet_slu.append(ve_slu)
                vet_ba.append(ve_ba)
        
        size = 5
        
        ax1.plot(vst_sh, c='indianred', label='shelf', zorder=1)
        ax1.plot(vst_slu, c='indianred', linestyle='dashed', label='u. slope', zorder=1)
        ax1.plot(vst_ba, c='indianred', linestyle='dotted', label='l. slope/basin', zorder=1)
        
        ax1.plot(vst_sh, 'o', markersize = size, c='indianred', zorder=1)
        ax1.plot(vst_slu, 'o', markersize = size, c='indianred', zorder=1)
        ax1.plot(vst_ba, 'o', markersize = size, c='indianred', zorder=1)
        ax1.set_xlim(-0.5, 5.5)
        ax1.set_ylim(0, 70)
        ax1.set_xticks([0, 1, 2, 3, 4, 5])
        ax1.set_xticklabels(labels)
        ax1.set_title(title)
        ax1.set_ylabel('Deposited volume (km³)', color='indianred')
        ax1.set_xlabel(xlabel)
        ax1.tick_params(axis='y', labelcolor='indianred')
        if legend == True:
            ax1.legend(fontsize=9, loc='center left', frameon=False)
        
        ax2.plot(vet_sh, c='tab:blue', label='shelf', zorder=0)
        ax2.plot(vet_slu, c='tab:blue', label='u. slope', linestyle='dashed', zorder=0)
        ax2.plot(vet_ba, c='tab:blue', label='basin', linestyle='dotted', zorder=0)
        
        ax2.plot(vet_sh, 'o', markersize = size, c = 'tab:blue', zorder=0)
        ax2.plot(vet_slu, 'o', markersize = size, c='tab:blue', zorder=0)
        ax2.plot(vet_ba, 'o', markersize = size, c='tab:blue', zorder=0)
        ax2.set_ylim(-14, 0)
        ax2.set_ylabel('Eroded volume (km³)', color='tab:blue')
        ax2.tick_params(axis='y', labelcolor='tab:blue')
        ax2.set_xticks([0, 1, 2, 3, 4, 5])
        ax2.set_xticklabels(labels)
        ax2.set_title(title)
        ax2.set_xlabel(xlabel)
        ax2.tick_params(axis='y', labelcolor='tab:blue')
        if legend == True:
            ax2.legend(fontsize=9, loc='upper left', bbox_to_anchor=(0.0, 0.8), frameon=False)

        x =+ 1

def volumes_pct(path, title, labels, xlabel, ax1, ax2, legend=False):
    
        ax1 = ax1
        ax2 = ax2
        
        paths = [f.path for f in os.scandir(path) if f.is_dir()]
        paths.sort()

        vst_so = []
        vst_tr = []
        vst_sh = []
        vst_slu = []
        vst_ba = []
        
        vet_so = []
        vet_tr = []
        vet_sh = []
        vet_slu = []
        vet_ba = []
        
        t_dep = []
        t_ero = []

        time = 10000
        
        sh_i = [100000, 100000, 0, 300000]
        slu_i = [100000, 150000, 0,  300000]
        b_i = [150000, 300000, 0, 300000]

        for i in paths:
            
            if 'sw' in i:
                
                dataTIN = eroCatch.catchmentErosion(folder=i, timestep=100)
                dataTIN.regridTINdataSet()
                
                dep = (dataTIN.getDepositedVolume(time=time, erange= [0, 300000, 0, 300000])/time)/1e6
                ero = (dataTIN.getErodedVolume(time=time, erange= [0, 300000, 0, 300000])/time)/1e6
                
                vs_so = (dataTIN.getDepositedVolume(time=time, erange= [0, 50000, 0, 300000])/time)/1e6
                ve_so = (dataTIN.getErodedVolume(time=time, erange= [0, 50000, 0, 300000])/time)/1e6
                vs_tr = (dataTIN.getDepositedVolume(time=time, erange= [50000, 100000, 0, 300000])/time)/1e6
                ve_tr = (dataTIN.getErodedVolume(time=time, erange= [50000, 100000, 0, 300000])/time)/1e6
                
                t_dep.append(dep)
                t_ero.append(ero)
                vst_so.append(vs_so)
                vet_so.append(ve_so)
                vst_tr.append(vs_so)
                vet_tr.append(ve_so)
                
                vs_sh = (dataTIN.getDepositedVolume(time=time, erange=sh_i)/time)/1e6
                vs_slu = (dataTIN.getDepositedVolume(time=time, erange=slu_i)/time)/1e6
                vs_ba = (dataTIN.getDepositedVolume(time=time, erange=b_i)/time)/1e6

                ve_sh = (dataTIN.getErodedVolume(time=time, erange=sh_i)/time)/1e6
                ve_slu = (dataTIN.getErodedVolume(time=time, erange=slu_i)/time)/1e6
                ve_ba = (dataTIN.getErodedVolume(time=time, erange=b_i)/time)/1e6
                
                vst_sh.append(vs_sh)
                vst_slu.append(vs_slu)
                vst_ba.append(vs_ba)

                vet_sh.append(ve_sh)
                vet_slu.append(ve_slu)
                vet_ba.append(ve_ba)

                sh_i[1] = sh_i[1] + 10000
                slu_i[:2] = [x + 10000 for x in slu_i[:2]]
                b_i[1] = b_i[1] + 10000
                
            else:
                
                dataTIN = eroCatch.catchmentErosion(folder=i, timestep=100)
                dataTIN.regridTINdataSet()
                
                dep = (dataTIN.getDepositedVolume(time=time, erange= [0, 300000, 0, 300000])/time)/1e6
                ero = (dataTIN.getErodedVolume(time=time, erange= [0, 300000, 0, 300000])/time)/1e6
                
                vs_so = (dataTIN.getDepositedVolume(time=time, erange= [0, 50000, 0, 300000])/time)/1e6
                ve_so = (dataTIN.getErodedVolume(time=time, erange= [0, 50000, 0, 300000])/time)/1e6
                vs_tr = (dataTIN.getDepositedVolume(time=time, erange= [50000, 100000, 0, 300000])/time)/1e6
                ve_tr = (dataTIN.getErodedVolume(time=time, erange= [50000, 100000, 0, 300000])/time)/1e6
                
                t_dep.append(dep)
                t_ero.append(ero)
                vst_so.append(vs_so)
                vet_so.append(ve_so)
                vst_tr.append(vs_so)
                vet_tr.append(ve_so)
                
                vs_sh = (dataTIN.getDepositedVolume(time=time, erange= [100000, 130000, 0, 300000])/time)/1e6
                vs_slu = (dataTIN.getDepositedVolume(time=time, erange=[130000, 180000, 0,  300000])/time)/1e6
                vs_ba = (dataTIN.getDepositedVolume(time=time, erange=[180000, 300000, 0, 300000])/time)/1e6
                
                ve_sh = (dataTIN.getErodedVolume(time=time, erange= [100000, 130000, 0, 300000])/time)/1e6
                ve_slu = (dataTIN.getErodedVolume(time=time, erange=[130000, 180000, 0,  300000])/time)/1e6
                ve_ba = (dataTIN.getErodedVolume(time=time, erange=[180000, 300000, 0, 300000])/time)/1e6
                
                vst_sh.append(vs_sh)
                vst_slu.append(vs_slu)
                vst_ba.append(vs_ba)
                
                vet_sh.append(ve_sh)
                vet_slu.append(ve_slu)
                vet_ba.append(ve_ba)
        
        size = 5
        
        sed = [x + y for x, y in zip(vet_so, vet_tr)]
        sed = [x + y for x, y in zip(sed, vst_tr)]
        
        ax1.plot([((int(a) / int(b))*-100) for a,b in zip(vst_sh, sed)], c='indianred', label='shelf', zorder=1)
        ax1.plot([((int(a) / int(b))*-100) for a,b in zip(vst_slu, sed)], c='indianred', linestyle='dashed', label='u. slope', zorder=1)
        ax1.plot([((int(a) / int(b))*-100) for a,b in zip(vst_ba, sed)], c='indianred', linestyle='dotted', label='l. slope/basin', zorder=1)
        
        ax1.plot([((int(a) / int(b))*-100) for a,b in zip(vst_sh, sed)], 'o', markersize = size, c='indianred', zorder=1)
        ax1.plot([((int(a) / int(b))*-100) for a,b in zip(vst_slu, sed)], 'o', markersize = size, c='indianred', zorder=1)
        ax1.plot([((int(a) / int(b))*-100) for a,b in zip(vst_ba, sed)], 'o', markersize = size, c='indianred', zorder=1)
        ax1.set_xlim(-0.5, 5.5)
        ax1.set_ylim(0, 120)
        ax1.set_xticks([0, 1, 2, 3, 4, 5])
        ax1.set_xticklabels(labels)
        ax1.set_title(title)
        ax1.set_ylabel('Sediment distribution [% of s-t]', color='indianred')
        ax1.set_xlabel(xlabel)
        ax1.tick_params(axis='y', labelcolor='indianred')
        if legend == True:
            ax1.legend(fontsize=9, loc='center left', frameon=False)
        # if ax1 == ax[0, 0]:
        #     ax1.annotate('submarine source', (3.8, 104), ha='center')            
        #     ax1.annotate('subaerial source', (3.8, 91), ha='center')
        ax1.plot([-0.5, 5.5], [100, 100], c='k', lw=1)
        
        ax2.plot([((int(a) / int(b))*100) for a,b in zip(vet_sh, sed)], c='tab:blue', label='shelf', zorder=0)
        ax2.plot([((int(a) / int(b))*100) for a,b in zip(vet_slu, sed)], c='tab:blue', label='u. slope', linestyle='dashed', zorder=0)
        ax2.plot([((int(a) / int(b))*100) for a,b in zip(vet_ba, sed)], c='tab:blue', label='basin', linestyle='dotted', zorder=0)
        
        ax2.plot([((int(a) / int(b))*100) for a,b in zip(vet_sh, sed)], 'o', markersize = size, c = 'tab:blue', zorder=0)
        ax2.plot([((int(a) / int(b))*100) for a,b in zip(vet_slu, sed)], 'o', markersize = size, c='tab:blue', zorder=0)
        ax2.plot([((int(a) / int(b))*100) for a,b in zip(vet_ba, sed)], 'o', markersize = size, c='tab:blue', zorder=0)
        ax2.set_ylim(0, 100)
        ax2.set_ylabel('Erosion distribution [% of s-t]', color='tab:blue')
        ax2.tick_params(axis='y', labelcolor='tab:blue')
        ax2.set_xticks([0, 1, 2, 3, 4, 5])
        ax2.set_xticklabels(labels)
        ax2.set_title(title)
        ax2.set_xlabel(xlabel)
        ax2.tick_params(axis='y', labelcolor='tab:blue')
        if legend == True:
            ax2.legend(fontsize=9, loc='upper right', frameon=False)

        x =+ 1

def volumes_pct_bar(path, title, labels, xlabel, ax1, ax2, legend=False):
    
        ax1 = ax1
        ax2 = ax2
        
        paths = [f.path for f in os.scandir(path) if f.is_dir()]
        paths.sort()

        vst_so = []
        vst_tr = []
        vst_sh = []
        vst_slu = []
        vst_ba = []
        
        vet_so = []
        vet_tr = []
        vet_sh = []
        vet_slu = []
        vet_ba = []
        
        t_dep = []
        t_ero = []

        time = 10000
        
        sh_i = [100000, 100000, 0, 300000]
        slu_i = [100000, 150000, 0,  300000]
        b_i = [150000, 300000, 0, 300000]

        for i in paths:
            
            if 'sw' in i:
                
                dataTIN = eroCatch.catchmentErosion(folder=i, timestep=100)
                dataTIN.regridTINdataSet()
                
                dep = (dataTIN.getDepositedVolume(time=time, erange= [0, 300000, 0, 300000])/time)/1e6
                ero = (dataTIN.getErodedVolume(time=time, erange= [0, 300000, 0, 300000])/time)/1e6
                
                vs_so = (dataTIN.getDepositedVolume(time=time, erange= [0, 50000, 0, 300000])/time)/1e6
                ve_so = (dataTIN.getErodedVolume(time=time, erange= [0, 50000, 0, 300000])/time)/1e6
                vs_tr = (dataTIN.getDepositedVolume(time=time, erange= [50000, 100000, 0, 300000])/time)/1e6
                ve_tr = (dataTIN.getErodedVolume(time=time, erange= [50000, 100000, 0, 300000])/time)/1e6
                
                t_dep.append(dep)
                t_ero.append(ero)
                vst_so.append(vs_so)
                vet_so.append(ve_so)
                vst_tr.append(vs_so)
                vet_tr.append(ve_so)
                
                vs_sh = (dataTIN.getDepositedVolume(time=time, erange=sh_i)/time)/1e6
                vs_slu = (dataTIN.getDepositedVolume(time=time, erange=slu_i)/time)/1e6
                vs_ba = (dataTIN.getDepositedVolume(time=time, erange=b_i)/time)/1e6

                ve_sh = (dataTIN.getErodedVolume(time=time, erange=sh_i)/time)/1e6
                ve_slu = (dataTIN.getErodedVolume(time=time, erange=slu_i)/time)/1e6
                ve_ba = (dataTIN.getErodedVolume(time=time, erange=b_i)/time)/1e6
                
                vst_sh.append(vs_sh)
                vst_slu.append(vs_slu)
                vst_ba.append(vs_ba)

                vet_sh.append(ve_sh)
                vet_slu.append(ve_slu)
                vet_ba.append(ve_ba)

                sh_i[1] = sh_i[1] + 10000
                slu_i[:2] = [x + 10000 for x in slu_i[:2]]
                b_i[1] = b_i[1] + 10000
                
            else:
                
                dataTIN = eroCatch.catchmentErosion(folder=i, timestep=100)
                dataTIN.regridTINdataSet()
                
                dep = (dataTIN.getDepositedVolume(time=time, erange= [0, 300000, 0, 300000])/time)/1e6
                ero = (dataTIN.getErodedVolume(time=time, erange= [0, 300000, 0, 300000])/time)/1e6
                
                vs_so = (dataTIN.getDepositedVolume(time=time, erange= [0, 50000, 0, 300000])/time)/1e6
                ve_so = (dataTIN.getErodedVolume(time=time, erange= [0, 50000, 0, 300000])/time)/1e6
                vs_tr = (dataTIN.getDepositedVolume(time=time, erange= [50000, 100000, 0, 300000])/time)/1e6
                ve_tr = (dataTIN.getErodedVolume(time=time, erange= [50000, 100000, 0, 300000])/time)/1e6
                
                t_dep.append(dep)
                t_ero.append(ero)
                vst_so.append(vs_so)
                vet_so.append(ve_so)
                vst_tr.append(vs_so)
                vet_tr.append(ve_so)
                
                vs_sh = (dataTIN.getDepositedVolume(time=time, erange= [100000, 130000, 0, 300000])/time)/1e6
                vs_slu = (dataTIN.getDepositedVolume(time=time, erange=[130000, 180000, 0,  300000])/time)/1e6
                vs_ba = (dataTIN.getDepositedVolume(time=time, erange=[180000, 300000, 0, 300000])/time)/1e6
                
                ve_sh = (dataTIN.getErodedVolume(time=time, erange= [100000, 130000, 0, 300000])/time)/1e6
                ve_slu = (dataTIN.getErodedVolume(time=time, erange=[130000, 180000, 0,  300000])/time)/1e6
                ve_ba = (dataTIN.getErodedVolume(time=time, erange=[180000, 300000, 0, 300000])/time)/1e6
                
                vst_sh.append(vs_sh)
                vst_slu.append(vs_slu)
                vst_ba.append(vs_ba)
                
                vet_sh.append(ve_sh)
                vet_slu.append(ve_slu)
                vet_ba.append(ve_ba)
        
        size = 5
        
        sed = [x + y for x, y in zip(vet_so, vet_tr)]
        sed = [x + y for x, y in zip(sed, vst_tr)]
        
        s = np.array([((int(a) / int(b))*-100) for a,b in zip(vst_sh, sed)])
        sl = np.array([((int(a) / int(b))*-100) for a,b in zip(vst_slu, sed)])
        b = np.array([((int(a) / int(b))*-100) for a,b in zip(vst_ba, sed)])
        
        s_ero = np.array([((int(a) / int(b))*100) for a,b in zip(vet_sh, sed)])
        sl_ero = np.array([((int(a) / int(b))*100) for a,b in zip(vet_slu, sed)])
        b_ero = np.array([((int(a) / int(b))*100) for a,b in zip(vet_ba, sed)])
    
        ax1.bar(range(6), s, bottom = sl + b, color='indianred', label='shelf')
        ax1.bar(range(6), sl, bottom = b, color='dimgrey', label='u. slope')
        ax1.bar(range(6), b, color='lightgrey', label='l. slope/\nbasin floor')
        
        ax1.set_xlim(-0.5, 5.5)
        ax1.set_ylim(0, 120)
        ax1.set_xticks([0, 1, 2, 3, 4, 5])
        ax1.set_xticklabels(labels)
        ax1.set_title(title)
        ax1.set_ylabel('Sediment distribution [% of s-t]', color='indianred')
        ax1.set_xlabel(xlabel)
        ax1.tick_params(axis='y', labelcolor='indianred')
        if legend == True:
#             ax1.legend(fontsize=9, loc= 'upper left', bbox_to_anchor = (0.03, 1.03), frameon=False, ncol = 3, 
#                        handlelength=1, handletextpad=0.3, columnspacing=1)
            ax1.legend(fontsize=9, loc= 'lower left',
                       handlelength=1, handletextpad=0.3, columnspacing=1)
        ax1.plot([-0.5, 5.5], [100, 100], c='k', lw=1)

        for rect in ax1.patches:
            
            height = rect.get_height()
            width = rect.get_width()
            x = rect.get_x()
            y = rect.get_y()
            
            label_text = '{}'.format(int(round(height,0))) 

            if height > 14:
                
                label_x = x + width - 0.4  
                label_y = y + height / 2
                ax1.text(label_x, label_y, label_text, ha='center', va='center', fontsize=9)
            
            if label_text == '13':
                
                label_x = x + width - 0.4 
                label_y = 95
                ax1.text(label_x, label_y, label_text, ha='center', va='center', fontsize=9)
        
        ax2.bar(range(6), s_ero, bottom = sl_ero + b_ero, color='indianred', label='shelf')
        ax2.bar(range(6), sl_ero, bottom = b_ero, color='dimgrey', label='u. slope')
        ax2.bar(range(6), b_ero, color='lightgrey', label='l. slope/\nbasin floor')
        
        ax2.set_ylim(0, 100)
        ax2.set_ylabel('Erosion distribution [% of s-t]', color='tab:blue')
        ax2.tick_params(axis='y', labelcolor='tab:blue')
        ax2.set_xticks([0, 1, 2, 3, 4, 5])
        ax2.set_xticklabels(labels)
        ax2.set_title(title)
        ax2.set_xlabel(xlabel)
        ax2.tick_params(axis='y', labelcolor='tab:blue')
        if legend == True:
            ax2.legend(fontsize=9, loc='upper right', frameon=False)
            
        for rect in ax2.patches:

            height = rect.get_height()
            width = rect.get_width()
            x = rect.get_x()
            y = rect.get_y()

            label_text = '{}'.format(int(round(height,0))) 
            
            if height > 3:

                label_x = x + width - 0.4  
                label_y = y + height / 2
                ax2.text(label_x, label_y, label_text, ha='center', va='center', fontsize=9)
        
        x =+ 1
        
        