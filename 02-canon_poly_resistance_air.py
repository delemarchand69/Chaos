
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

plt.rcParams['animation.ffmpeg_path'] = r'C:\projets\ffmpeg-4.1-win64-static/bin/ffmpeg'

FIGSIZE = (16,9)
DPI = 120  # 240 For 4K, 120 for 1080p, 80 for 720p

###############################################################################

''' Parameters & Differential equation '''

g = 9.81
k = 0.15 #coefficient de resistance dans l'air 

def derivs(state, t):
    
    res = np.zeros_like(state) # x vx z vz

    # if above the floor
    if state[2]>=0: 
        res[0] = state[1] # dx/dt = vx 
        res[1] = -k*state[1] # dvx/dt = -k.vx 
        res[2] = state[3] # dz/dt = vz
        res[3]= -g -k*state[3] # dvz/dt = -g -k.vz
    else:
        res[0] = 0 
        res[1] = 0
        res[2] = 0
        res[3] = 0

    return res

###############################################################################

# Time range
dt = 0.033
t = np.arange(0.0, 16, dt)
v = 100
a1, a2, a3 = 35,38,51
# initial state

init_state_list = [[0, v*cos(a1*3.14/180) ,0 , v*sin(a1*3.14/180)],
                   [0, v*cos(a2*3.14/180) ,0 , v*sin(a2*3.14/180)],
                   [0, v*cos(a3*3.14/180) ,0 , v*sin(a3*3.14/180)]]

# integration
res_list = [integrate.odeint(derivs, init_state, t) for init_state in init_state_list]

###############################################################################

fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
ax = fig.add_subplot(111)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_aspect('equal')

#on determine le projectile qui va le + loin pour dimensionner l'axe des x
index_max_x_1 = np.amax((res_list[0][:,2] >= 0).nonzero())
index_max_x_2 = np.amax((res_list[1][:,2] >= 0).nonzero())
index_max_x_3 = np.amax((res_list[2][:,2] >= 0).nonzero())
max_x_1 = res_list[0][index_max_x_1,0]
max_x_2 = res_list[1][index_max_x_2,0]
max_x_3 = res_list[2][index_max_x_3,0]
max_x = max(max_x_1,max_x_2,max_x_3)

#on evalue le temps auquel le dernier boulet touche le sol et on coupe les observations à ce temps là
max_index_t = max(index_max_x_1,index_max_x_2,index_max_x_3)
res_list_ajust = [res_list[0][:max_index_t], res_list[1][:max_index_t], res_list[2][:max_index_t]]

ax.set_xlim(0,max_x*1.1)

#on determine le projectile qui va le + haut pour dimensionner l'axe des y
max_y_1 = np.amax(res_list[0][:,2])
max_y_2 = np.amax(res_list[1][:,2])
max_y_3 = np.amax(res_list[2][:,2])
max_y = max(max_y_1,max_y_2,max_y_3)

ax.set_ylim(0,max_y*1.1)
fig.tight_layout()

#on utilise res_list_ajust pour la video (on a enlevé les observations non pertinentes)
lines = [ax.plot(res[:,0],res[:,1], '-', lw=1)[0] for res in res_list_ajust]
balls = [ax.plot(res[0:1,0],res[0:1,1], 'o', lw=1)[0] for res in res_list_ajust]

def init():
    for line in lines:
        line.set_data([], [])
    return lines 


def animate(i):
    print("Computing frame",i)
    for line,res,ball in zip(lines,res_list_ajust,balls):
        x, y = res[:,0], res[:,2]
        line.set_data(x[:i], y[:i])
        ball.set_data(x[i],y[i])
    return lines 

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(res_list_ajust[0][:,0])),
                              repeat=False, interval=33, blit=True, init_func=init)
writer = animation.FFMpegWriter(fps=30, bitrate=5000)

ani.save('02-canon_poly_resistance_air.mp4', writer = writer)
#plt.show()
