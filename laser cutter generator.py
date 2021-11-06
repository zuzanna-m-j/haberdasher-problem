import copy
import numpy as np
import matplotlib.pyplot as plt

A = [(-0.5223290993692602, -0.16516412776125292), (0.47767090063073975, -0.16516412776125292),
     (0.04465819873852046, 0.3303282555225058)]
B = [(-0.5534779580863476, -0.2274853687848006), (0.44652204191365247, -0.2274853687848006),
     (0.33762976744895196, 0.32497372029196253), (-0.3079855748025888, 0.197719911933842)]
C = [(-0.46196653872316695, -0.2417397096265952), (0.538033461276833, -0.2417397096265952),
     (0.28352584456059177, 0.1990804134392008), (-0.24936389836384554, 0.38100648201528425)]
D = [(-0.7425143969508786, 0.00812615065931594), (0.12351100683355996, -0.49187384934068407),
     (0.6190033901173186, -0.05886114744846476), (0.12351100683355996, 0.508126150659316)]

A = np.array(A)
B = np.array(B)
C = np.array(C)
D = np.array(D)

shapes = [A, B, C, D]
names = ['A','B','C','D']

def ShiftToOrigin():
    global shapes
    for i in range(len(shapes)):
        x,y = shapes[i][0,0], shapes[i][0,1]
        shapes[i][:,0] -= x
        shapes[i][:,1] -= y

def vLen(ps):
    """p1 = (x1,y1)"""
    p1 = ps[0]
    p2 = ps[1]
    x1,y1 = p1
    x2,y2 = p2
    return np.sqrt((x2 - x1)**2 +(y2 - y1)**2)

def MaxDim(A):
    if len(A) == 3:
        p = [(A[0],A[1]),(A[1],A[2]),(A[2],A[0])]
        edges = list(map(vLen,p))
        edge = max(edges)
        print(f"Max edge: {edge}")
        return edge

    if len(A) == 4:
        p = [(A[0],A[1]),(A[1],A[2]),(A[2],A[3]),(A[3],A[0])]
        p2 = [(A[0],A[2]),(A[1],A[3])]
        edges = list(map(vLen,p))
        edge = max(edges)
        diags = list(map(vLen,p2))
        diag = max(diags)
        print(f"Max diagonal: {diag}, max edge: {edge}")
        return diag, edge

def ScaleShape(a,A):
    newA = []
    for p in A:
        newp = (a * p[0], a * p[1])
        newA.append(newp)
    return newA

def NewShape(l):

    if len(l) == 3:
        a,b,c = FindIntersection(l[2],l[0]), FindIntersection(l[0],l[1]), FindIntersection(l[1],l[2])
        return np.array([a,b,c])

    if len(l) == 4:
        a,b,c,d = FindIntersection(l[3],l[0]), FindIntersection(l[0],l[1]), FindIntersection(l[1],l[2]), FindIntersection(l[2],l[3])
        return np.array([a, b, c, d])


def SplitToLines(shape):

    if len(shape) == 3:

        l1 = [shape[0], shape[1]]
        l2 = [shape[1], shape[2]]
        l3 = [shape[2], shape[0]]

        return l1,l2,l3

    if len(shape) == 4:

        l1 = [shape[0], shape[1]]
        l2 = [shape[1], shape[2]]
        l3 = [shape[2], shape[3]]
        l4 = [shape[3], shape[0]]

        return l1, l2, l3, l4

def FindIntersection(l1,l2):

    x11, y11 = l1[0]
    x12, y12 = l1[1]

    x21, y21 = l2[0]
    x22, y22 = l2[1]

    A1 = y12 - y11
    B1 = x11 - x12
    C1 = A1 * x11 + B1 * y11

    A2 = y22 - y21
    B2 = x21 - x22
    C2 = A2 * x21 + B2 * y21

    det = A1 * B2 - A2 * B1

    if det == 0:
        print("Error")

    else:
        x = (B2 * C1 - B1 * C2)/det
        y = (A1 * C2 - A2 * C1)/det
        return (x, y)


def ShiftLine(d,l):

    """l = [(x1,y1),(x2,y2)"""

    x1, y1 = l[0]
    x2, y2 = l[1]

    r = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    dx = d/r * (y1 - y2)
    dy = d/r * (x2 - x1)

    x1 = x1 + dx
    x2 = x2 + dx
    y1 = y1 + dy
    y2 = y2 + dy

    return [(x1,y1),(x2,y2)]

if __name__ == "__main__":


    ShiftToOrigin()
    scales = [15] * len(shapes)
    shapes = list(map(ScaleShape,scales,shapes))
    old_shapes = copy.deepcopy(shapes)
    new_shapes = []
    d_iter = iter([1.5,2.0,2.0,2.5])

    switch = True

    for shape in shapes:
        d = next(d_iter)
        print(d)
        print(MaxDim(shape))
        A_lines = SplitToLines(shape)
        A_lines = np.array(A_lines)
        A_new_lines = []
        for i,l in enumerate(A_lines):
            A_new_lines.append(ShiftLine(d,l))
        A_new_lines = np.array(A_new_lines)
        newA = NewShape(A_new_lines)
        new_shapes.append(newA)

        if switch == True:

            for line in A_new_lines:
                plt.plot(line[:,0],line[:,1],color = 'red')
            for line in A_lines:
                plt.plot(line[:, 0], line[:, 1], color = 'blue')
            plt.plot(newA[:, 0], newA[:, 1], 'o')
            plt.show()

    with open("lasercut.txt", 'w') as fout:
        for i,shape in enumerate(shapes):
            fout.write(f'Shape: {names[i]}\n')
            fout.write('Old shape:\n')
            fout.write(f'{old_shapes[i]}\n')
            fout.write('New shape:\n')
            fout.write(f'{new_shapes[i]}\n####################\n\n')


















