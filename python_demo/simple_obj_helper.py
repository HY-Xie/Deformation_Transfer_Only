import numpy as np 

def simple_obj_loader(fileName):
    V = []
    F = []
    f = open(fileName, 'r')
    all_lines = f.readlines()
    f.close()

    for line in all_lines:
        if line[0] == 'v' and line[1] == ' ':
            this_line = line.split()
            x = float(this_line[1])
            y = float(this_line[2])
            z = float(this_line[3])
            v = [x, y, z]
            V.append(v)
        if line[0] == 'f':
            this_line = line.split()
            v1 = int(this_line[1]) - 1
            v2 = int(this_line[2]) - 1
            v3 = int(this_line[3]) - 1
            f = [v1, v2, v3]
            F.append(f)
    V = np.array(V)
    F = np.array(F)
    return V, F

def simple_writer(fileName, V, F):
    f = open(fileName, 'w')
    for i in range(V.shape[0]):
        f.write("v {:.4f} {:.4f} {:.4f}\n".format(float(V[i, 0]), float(V[i, 1]), float(V[i, 2])))
    for i in range(F.shape[0]):
        f.write('f {} {} {}\n'.format(int(F[i, 0])+1, int(F[i, 1])+1, int(F[i, 2])+1))
    f.close()

    
if __name__ == '__main__':
    in_file = "/Users/haoyang/Downloads/Meshes/SPRING_MALE_SWAPED_100/SPRING0001.obj"
    out_file = "/Users/haoyang/Desktop/temp_spring.obj"

    V, F = simple_obj_loader(in_file)
    print(V.shape)
    print(F.shape)
    simple_writer(out_file, V, F)