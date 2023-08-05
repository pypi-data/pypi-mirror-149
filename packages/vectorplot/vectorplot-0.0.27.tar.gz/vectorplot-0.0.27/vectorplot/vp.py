import numpy as np
import matplotlib.pyplot as plt
import math as mt


def resultant_module(module_vector1, module_vector2, angle):
    vector1 = float(module_vector1)
    vector2 =float(module_vector2)
    angle = mt.radians(float(angle))

    return mt.sqrt((pow(vector1, 2)+pow(vector2, 2)+2*vector1*vector2*mt.cos(angle)))


def vector_module(vector):
    norm_vector = np.linalg.norm(vector)
    return norm_vector


def equivalent2d(lista_vetores):
    comp_x_eq = None
    comp_y_eq = None

    verif = str(type(lista_vetores[0]))
    if verif == "<class 'tuple'>":
        for i in range(len(lista_vetores)):
            comp_x = lista_vetores[i][2] - lista_vetores[i][0]
            comp_y = lista_vetores[i][3] - lista_vetores[i][1]

            if (comp_x_eq == None) and (comp_y_eq == None):
                comp_x_eq = comp_x
                comp_y_eq = comp_y
            else:
                if (comp_x_eq != comp_x) or (comp_y_eq != comp_y):
                    return False
        return True
    else:
        for vector in lista_vetores:
            comp_x = vector[0]
            comp_y = vector[1]
            if (comp_x_eq == None) and (comp_y_eq == None):
                comp_x_eq = comp_x
                comp_y_eq = comp_y
            else:
                if (comp_x_eq != comp_x) or (comp_y_eq != comp_y):
                    return False
        return True


def equivalent3d(lista_vetores):
    comp_x_eq = None
    comp_y_eq = None
    comp_z_eq = None

    verif = str(type(lista_vetores[0]))
    if verif == "<class 'tuple'>":
        for i in range(len(lista_vetores)):
            comp_x = lista_vetores[i][3] - lista_vetores[i][0]
            comp_y = lista_vetores[i][4] - lista_vetores[i][1]
            comp_z = lista_vetores[i][5] - lista_vetores[i][2]

            if (comp_x_eq == None) and (comp_y_eq == None) and (comp_y_eq == None):
                comp_x_eq = comp_x
                comp_y_eq = comp_y
                comp_z_eq = comp_z
            else:
                if (comp_x_eq != comp_x) or (comp_y_eq != comp_y) or (comp_z_eq != comp_z):
                    return False
        return True
    else:
        for vector in lista_vetores:
            comp_x = vector[0]
            comp_y = vector[1]
            comp_z = vector[2]
            if (comp_x_eq == None) and (comp_y_eq == None):
                comp_x_eq = comp_x
                comp_y_eq = comp_y
                comp_z_eq = comp_z
            else:
                if (comp_x_eq != comp_x) or (comp_y_eq != comp_y) or (comp_z_eq != comp_z):
                    return False
        return True


def angle_vectors(v, u):
    verif_v = str(type(v))
    verif_u = str(type(u))
    if (verif_v == "<class 'list'>"):
        v = np.array(v)
    if (verif_u == "<class 'list'>"):
        u = np.array(u)
    r = prod_vectors(v, u) / (vector_module(v)*vector_module(u))
    angle = np.arccos(r)
    return 180/np.pi*angle


def prod_vectors(v, u):
    verif_v = str(type(v))
    verif_u = str(type(u))
    if (verif_v == "<class 'list'>"):
        v = np.array(v)
    if (verif_u == "<class 'list'>"):
        u = np.array(u)
    return v.dot(u)


def plot2d(lista_vetores, lista_cores, lista_limites):
    plt.figure()
    plt.axvline(x=0, color='#A9A9A9', zorder=0)
    plt.axhline(y=0, color='#A9A9A9', zorder=0)

    for i in range(len(lista_vetores)):
        if str(type(lista_vetores[i])) == "<class 'tuple'>":
            plt.quiver([lista_vetores[i][0]],
                       [lista_vetores[i][1]],
                       [lista_vetores[i][2] - lista_vetores[i][0]],
                       [lista_vetores[i][3] - lista_vetores[i][1]],
                       angles='xy', scale_units='xy', scale=1, color=lista_cores[i],
                       alpha=1)
        else:
            x = np.concatenate([[0, 0], lista_vetores[i]])
            plt.quiver([x[0]],
                       [x[1]],
                       [x[2]],
                       [x[3]],
                       angles='xy', scale_units='xy', scale=1, color=lista_cores[i],
                       alpha=1)

    plt.grid()
    plt.axis([lista_limites[0],lista_limites[1],lista_limites[2],lista_limites[3]])
    plt.show()


def plot3d(lista_vetores, lista_cores, lista_limites):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim3d([lista_limites[0], lista_limites[1]])
    ax.set_ylim3d([lista_limites[2], lista_limites[3]])
    ax.set_zlim3d([lista_limites[4], lista_limites[5]])
    for i in range(len(lista_vetores)):
        if str(type(lista_vetores[i])) == "<class 'tuple'>":
            ax.quiver([lista_vetores[i][0]],[lista_vetores[i][1]],[lista_vetores[i][2]],
                       [lista_vetores[i][3] - lista_vetores[i][0]],
                       [lista_vetores[i][4] - lista_vetores[i][1]],
                       [lista_vetores[i][5] - lista_vetores[i][2]],
                      length=1, normalize=False, color=lista_cores[i])
        else:
            x = np.concatenate([[0, 0, 0], lista_vetores[i]])
            ax.quiver([x[0]], [x[1]],
                      [x[2]], [x[3]],
                      [x[4]], [x[5]],
                      length=1, normalize=False, color=lista_cores[i])

    plt.show()
