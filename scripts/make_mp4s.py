# Import the python packages we need to use
from athena_read import athdf
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
from glob import glob
# CHANGE THIS FILENAME TO ACCESS DIFFERENT DATA!
directories = glob("../data/rt_dr*/")
nframes = 200  # Number of frames of the animation you want to plot (more is slower)
################


for directory in directories:
    dratstr = directory.split('_dr')[1].replace('/', '')
    filename = directory+'rt_dr'+dratstr+'.out2.00000.athdf'
    data = athdf(filename)

    # Load density ratio from code output log
    logpath = filename.replace('.out2.00000.athdf', '.txt')
    drat = np.nan
    with open(logpath, 'r') as f:
        log = f.readlines()
        for l in log:
            if "drat" in l:
                drat = float(l.split("=")[1].strip())

    fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
    image = ax.imshow(data['rho'][0], origin='lower', cmap='viridis_r')
    contour = ax.contour(data['rho'][0], [1.25], origin='lower', colors=['white'])
    text = ax.text(0.85, 0.9, 'drat={:.1f}  time={:.3f}'.format(drat, data['Time']), color='white')
    plt.close()

    def animate(i):
        global contour
        data = athdf(filename.replace("00000", "{:05d}".format(i)))
        image.set_data(data['rho'][0])
        text.set_text("drat={:.1f}  time={:.3f}".format(drat, data['Time']))
        for c in contour.collections:
            c.remove()
        contour = ax.contour(data['rho'][0], [1.25], origin='lower', colors=['white'])
        return [image]

    anim = matplotlib.animation.FuncAnimation(fig, animate, frames=nframes, save_count=nframes)
    anim.save('rt_dr'+dratstr+'.mp4') # Run this line to save the animation as an .mp4
