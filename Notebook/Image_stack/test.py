import matplotlib.pyplot as plt
from os import listdir
import matplotlib.animation as animation
import numpy as np
from scipy import ndimage
from joblib import Parallel, delayed
import multiprocessing
import hyperspy.api as hs

def parallel_check(i):
    l=0
    for k in range(1,10):
        l = l+k
    l=l+i
    return(l)

def parallel_save(i):
    vmin_mul = 0
    vmax_mul = 1
    fig, axes = plt.subplots(nrows=1, ncols=1)
    filename = '-4mA_100kHz_1s_5pr_Hour_00_Minute_00_'+'Second_'+str(i).zfill(2)+'_'
    ##path = 'Hour_00/Minute_00/Second_' + str(i).zfill(2)
    path = '../../Demo_data/Minute_00/Second_' + str(i).zfill(2) #The path needs to be taken from the main notebook
    FFMpegWriter = animation.writers['ffmpeg']
    metadata = dict(title=path, artist='J.Vas')
    writer = FFMpegWriter(fps=0.5, metadata=metadata, bitrate=200)
    ##k_max = len(listdir('Hour_00/Minute_00/Second_'+str(i).zfill(2)))
    k_max = len(listdir(path))
    #targetfile = '/videos/second'+str(i).zfill(2)+'.mp4'
    targetfile = 'second'+str(i).zfill(2)+'.mp4'
    with writer.saving(fig, targetfile, dpi=200):
        for k in range(0, k_max):
            TEM = hs.load(path +'/'+filename+'Frame_00' + str(k).zfill(2) + '.dm4')
            if np.max(TEM.data) - np.min(TEM.data) > 1000:
                TEM = ndimage.rotate(TEM, 250, reshape=False)
                TEM = TEM[300:3700, 750:3100]
                im = axes.imshow(ndimage.gaussian_filter(TEM.data, 6), cmap='gray', \
                                         vmin=vmin_mul * np.mean(TEM.data), vmax=vmax_mul * np.mean(TEM.data))
                print('Hour_00/Minute_00' + '/' + 'Second_' + str(i).zfill(2) + '/Frame' + str(k).zfill(2))
                axes.set_yticklabels([])
                axes.set_xticklabels([])
                plt.ioff()
                plt.xticks([])
                plt.yticks([])
                plt.hlines(2900, 325, 665)
                plt.text(328, 2800, '1 ' + u"\u03bcm")
                writer.grab_frame()
