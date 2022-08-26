-- execution --
to execute the program (in bash):

hybrid:
mpif90 -fopenmp -o project project.f90
export OMP_NUM_THREADS=2
mpirun -np 3 --hostfile host_file ./project

The cip-pool computers only have 6 cores each. if processors from omp and mpi multipied
result in more than 6, then the program will run very slowly for some reason. to run 
with more processors, it is a lot faster to run the program without omp and only use mpi 
on the cip-pool computers.

mpi only:
mpif90 -o project project.f90
mpirun -np 16 --hostfile host_file ./project


-- to the code --
to plot the binary file with gnuplot did not work as was stated on the sheet.
i used a python script and included the binary file "phi_func_total.bin" 
created by 12 processors and a grid size of 198x200. the produced plot from 
this file is also provided.

i could have forced the user to only input a "nice" grid size but i chose
instead to let the user choose freely and let the program do the recalculation.
this means that i can have final grids of size 198x200. in python there is the
function numpy.linspace(1,L=50,grid_size(0)) that divides the length L=50
into evenly spaced points, which leads to the image not looking distorted in
the end. i am only mentioning this because i do not know if you will look at
the python code or only use gnuplot.


-- grade --
I think you mentioned that you will e-mail us if we wish to. i would like to 
know both my grades. my grade of the written exam and of this project and the 
resulting end grade.
 

View the (binary) file contents using: od -t f4 vector.(bin/dat)