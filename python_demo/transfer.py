import numpy as np 
import time 
from simple_obj_helper import * 
import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])

# source_file = 'C:\\Users\\haoya\\Desktop\\Deformation_Transfer_Only\\data\\s0.obj'
# deformed_source_file = 'C:\\Users\\haoya\\Desktop\\Deformation_Transfer_Only\\data\\s1.obj'
# target_file = 'C:\\Users\\haoya\\Desktop\\Deformation_Transfer_Only\data\\t0.obj'
# target_output = 'C:\\Users\\haoya\\Desktop\\Deformation_Transfer_Only\data\\t0_output.obj'

source_file = "../data/s0.obj"
deformed_source_file = "../data/s1.obj"
target_file = "../data/t0.obj"
target_output = "../data/t0_output.obj"


def get_V(fileName):
    vertices, faces = simple_obj_loader(fileName)
    V1 = vertices[faces[:,0],:]
    V2 = vertices[faces[:,1],:]
    V3 = vertices[faces[:,2],:]
    
    # V4 = V1 + np.cross(V2-V1, V3-V1) / np.linalg.norm(np.cross(V2-V1, V3-V1))  # [nF x 3]

    V4 = np.zeros((faces.shape[0], 3))
    for f_idx, face in enumerate(faces):
        v1 = vertices[face[0]]
        v2 = vertices[face[1]]
        v3 = vertices[face[2]]

        v4 = v1 + np.cross(v2-v1, v3-v1) / np.linalg.norm(np.cross(v2-v1, v3-v1))
        V4[f_idx, :] = v4

    V = np.zeros((V4.shape[0], 9))

    V[:,  :3] = V2 - V1
    V[:, 3:6] = V3 -  V1
    V[:, 6: ] = V4 - V1
    print(V.shape)
    return V # [nF, 3]



# build A
vertices, faces = simple_obj_loader(target_file)
nV = vertices.shape[0]
nF = faces.shape[0]
A = np.zeros((3*nF, nV+nF))
for f_idx, face in enumerate(faces):
    for count in range(len(face)):
        A[3*f_idx + count][face[0]] = -1
        if count < 2:
            A[3*f_idx + count][face[count+1]] = 1
        else:
            A[3*f_idx + count][nV+f_idx] = 1


src_V = get_V(source_file)               
def_src_V = get_V(deformed_source_file)  
tar_V = get_V(target_file)

tar_vertices, tar_faces = simple_obj_loader(target_file)

# build C  C's shape [3*nF, 3]
C = np.zeros((3*nF, 3))
for f_idx, face in enumerate(faces):
    V = src_V[f_idx, :].reshape((3, 3)).T
    V_tilde = def_src_V[f_idx, :].reshape((3, 3)).T
    Q = np.dot(V_tilde, np.linalg.inv(V))   # 不能用V_tilde * np.linalg.inv(V)

    tar_vert = tar_V[f_idx, :].reshape((3, 3)).T

    c = np.dot(Q, tar_vert).T
    C[3*f_idx:3*f_idx+3, :] = c

print(A.shape)
print(C.shape)

A = np.matrix(A)
C = np.matrix(C)
AtA = A.T * A
AtC = A.T * C 

print('begin solve...')
start = time.time()
X_tilde = np.linalg.solve(AtA, AtC)
end = time.time()
print('duration: ', end-start)
# X_tilde = A.I * C

deformed_tar_V = X_tilde[:nV, :]

simple_writer(target_output, deformed_tar_V, faces)

