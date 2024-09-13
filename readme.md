# HPC group project

## Group Members :
1. Akash Kulkarni (S20210010011)
2. Animesh Shree (S20210010020)
3. Priyansh Singhal (S20210010178)

## Topic: Parallelisation of Simulation of Fluid Dynamics using Lattice-Boltzmann Approximation using CUDA in Numba

## Steps:
1. run "pip install -r requirements.txt" in terminal .
2. Lattice_cpu.py,lattice_gpu_naive.py, lattice_gpu_opt.py are created to do benchmarking. If you want to run and check the bencharmaking then simply go to benchmark.ipynb and run all the cells to get average of 7 runs and it's standard deviation.
3. Run the codes in the following way :
    1. For lbm_cpu.py do "python lbm_cpu.py" in terminal
    2. For lbm_gpu_1.py do "python lbm_gpu_1.py" in terminal.This will start the parallelised version of the code.
    3. For lbm_gpu_2.py do "python lbm_gpu_2.py" in terminal.This will start the parallelised and optimised version of the code.

    ### After running the codes, every 100th pic will be stored in respective folder. 