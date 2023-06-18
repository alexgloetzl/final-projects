import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#enter the path to the binary file
#path = R".\week14_project\phi_func_total.bin"
path = R"C:\Users\aleX\Desktop\phi_func_total.bin"
data = np.fromfile(path, dtype=np.float32)

#enter the N_j and N_i given on the console output of project.f90:
# -> N_i steps in y- and N_j in x-direction: N_i x N_j
N_i = 400; N_j = 400

data = data.reshape((N_j, N_i))
x = np.linspace(1,50,N_i)
y = np.linspace(1,50,N_j)
X,Y = np.meshgrid(x,y)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, data)
# plt.savefig("./week14_project/phi_func"+str(N_j)+"x"+str(N_i)+".png", dpi=300)
plt.show()