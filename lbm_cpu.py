import numpy as np
from matplotlib.pyplot import imsave, imshow
import time as tm
import matplotlib.pyplot as plt
import cProfile
import pstats

# Flow definition
Re          = 150.0                 # Reynolds number
nx, ny      = 420, 180              # Numer of lattice nodes
ly          = ny-1                  # Height of the domain in lattice unit.
cx, cy, r   = nx//4, ny//2, ny//9   # Coordinates of the cylinder
uLB         = 0.04                  # Velocity in lattice units
nulb        = uLB*r/Re              # Viscoscity in lattice units
omega       = 1 / (3*nulb+0.5)      # Relaxation parameter

# Lattice: D2Q9
#   6   3   0
#    \  |  /
#     \ | /
#   7---4---1
#     / | \
#    /  |  \
#   8   5   2
v = np.array([
    [1,1], [1,0], [1,-1],
    [0,1], [0,0], [0,-1],
    [-1,1], [-1,0], [-1,-1]])
t = np.array([
    1/36, 1/9, 1/36,
    1/9, 4/9, 1/9,
    1/36, 1/9, 1/36])
col1 = np.array([0, 1, 2])
col2 = np.array([3, 4, 5])
col3 = np.array([6, 7, 8])

# Setup: cylindrical obstacle and velocity inlet with perturbation
def obstacle_fun(x, y):
    return (x-cx)**2 + (y-cy)**2 < r**2

# Initial velocity profile: almost zero, with a
# slight perturbation to trigger the instability.
def inivel(d, x, y):
    return (1-d) * uLB * (1 + 1e-4*np.sin(y/ly*2*np.pi))

def rho_clc(fin):
    return np.sum(fin, axis=0)

def macroscopic(fin, rho):
    u = np.zeros((2, nx, ny))
    for i in range(9):
        u[0,:,:] += v[i,0] * fin[i,:,:]
        u[1,:,:] += v[i,1] * fin[i,:,:]
    u /= rho
    return u

def equilibrium(rho, u):
    usqr = 3/2 * (u[0]**2 + u[1]**2)
    feq = np.zeros((9,nx,ny))
    for i in range(9):
        cu = 3 * (v[i,0]*u[0,:,:] + v[i,1]*u[1,:,:])
        feq[i,:,:] = rho*t[i] * (1 + cu + 0.5*cu**2 - usqr)
    return feq

def main(maxIter, saveat, notebook=False):
    if not notebook:
        print("Initializing Simulation...")

    # create obstacle mask array from element-wise function
    obstacle = np.fromfunction(obstacle_fun, (nx,ny))

    # initial velocity field vx,vy from element-wise function
    # vel is also used for inflow border condition
    vel = np.fromfunction(inivel, (2,nx,ny))

    # Initialization of the populations at equilibrium 
    # with the given velocity.
    fin = equilibrium(1, vel)

    if not notebook:
        print("Starting Simulation...")
        figures = {}
        start = tm.time()
    for time in range(maxIter):
        print(time)
        # Right wall: outflow condition.
        # we only need here to specify distrib. function for velocities
        # that enter the domain (other that go out, are set by the streaming step)
        fin[col3,nx-1,:] = fin[col3,nx-2,:] 

        # Compute macroscopic variables, density and velocity.
        rho = rho_clc(fin)
        u = macroscopic(fin, rho)

        # Left wall: inflow condition.
        u[:,0,:] = vel[:,0,:]
        rho[0,:] = 1/(1-u[0,0,:]) * ( np.sum(fin[col2,0,:], axis=0) + 2*np.sum(fin[col3,0,:], axis=0) )

        # Compute equilibrium.
        feq = equilibrium(rho, u)
        fin[[0,1,2],0,:] = feq[[0,1,2],0,:] + fin[[8,7,6],0,:] - feq[[8,7,6],0,:]

        # Collision step.
        fout = fin - omega * (fin - feq)

        # Bounce-back condition for obstacle.
        # in python language, we "slice" fout by obstacle
        for i in range(9):
            fout[i, obstacle] = fin[8-i, obstacle]

        # streaming step
        # take every single nodal velocity and move it to its corresponding neighbour
        # which means that it is moving in the direction of its discrete velocity
        for i in range(9):
            fin[i,:,:] = np.roll(np.roll(fout[i,:,:], v[i,0], axis=0),v[i,1], axis=1)
 
        # Recording the velocity.
        if (not notebook and time % saveat == 0):
            fig = np.sqrt(u[0]**2+u[1]**2).transpose()
            plt.imshow(fig)
            # plt.imshow(curl,cmap='bwr')
            plt.pause(0.01)
            plt.cla()
            # figures[time//saveat] = fig


    if not notebook:
        end = tm.time()
        print("Ended in %d seconds." % (end-start))
        # print("Saving visual simulation...")
        # for inst, fig in figures.items():
        #     imsave("out/vel.{0:04d}.png".format(inst), fig, cmap="autumn")
    else:
        figure = np.sqrt(u[0]**2+u[1]**2).transpose()
        imshow(figure, cmap="autumn")

if __name__ == "__main__":
    with cProfile.Profile() as profile:
        main(20000, 100)
    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.CUMULATIVE)
    results.print_stats()
    results.dump_stats("results.prof")