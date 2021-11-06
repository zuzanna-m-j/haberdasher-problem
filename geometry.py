import numpy as np
import matplotlib.pyplot as plt

def DegToRad(deg):
    return 0.0174533 * deg

def Rotation(angle, vertex):
    theta = DegToRad(angle)
    v = np.array(vertex)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])

    return np.dot(R, v)

def Shift(vect,vertex):
    x,y = vect
    return vertex[0] + x, vertex[1] + y

A = [(-0.5223290993692602, -0.16516412776125292), (0.47767090063073975, -0.16516412776125292), (0.04465819873852046, 0.3303282555225058)]
B =  [(-0.5534779580863476, -0.2274853687848006), (0.44652204191365247, -0.2274853687848006), (0.33762976744895196, 0.32497372029196253), (-0.3079855748025888, 0.197719911933842)]
C =  [(-0.46196653872316695, -0.2417397096265952), (0.538033461276833, -0.2417397096265952), (0.28352584456059177, 0.1990804134392008), (-0.24936389836384554, 0.38100648201528425)]
D =  [(-0.7425143969508786, 0.00812615065931594), (0.12351100683355996, -0.49187384934068407), (0.6190033901173186, -0.05886114744846476), (0.12351100683355996, 0.508126150659316)]


cA = (0.027 , -0.716)
cB = (0.552 , -0.511)
cC = (-0.548 , -0.536)
cD = (-0.015 , 0.139)


#-0.0023111772376280815 -0.1641244632564251
#rotate 180, displace

a2 = 0
cx = 0
cy = 0

A_temp = []
d = (0.025 + 0.0023111772376280815,-0.88 + 0.1641244632564251 + 5.551115123125783e-17)
for v in A:
    A_temp.append(Rotation(0,v))
A_temp = [Shift(d, v) for v in A_temp]
A_temp = [Rotation(a2, v) for v in A_temp]
A_temp = [Shift((cx,cy), v) for v in A_temp]


d = (0.55 + 0.0023111772376280815,-0.675 + 0.1641244632564251 + 5.551115123125783e-17)
B_temp = []
for v in B:
    B_temp.append(Rotation(120,v))
B_temp = [Shift(d,v) for v in B_temp]
B_temp = [Rotation(a2, v) for v in B_temp]
B_temp = [Shift((cx,cy),v) for v in B_temp]

C_temp = []
d = (-0.55 + 0.0023111772376280815,-0.70 + 0.1641244632564251 + 5.551115123125783e-17)
for v in C:
    C_temp.append(Rotation(-120,v))
C_temp = [Shift(d,v) for v in C_temp]
C_temp = [Rotation(a2, v) for v in C_temp]
C_temp = [Shift((cx,cy),v) for v in C_temp]

D_temp = []
D_temp = []
d = (-0.0175 + 0.0023111772376280815,-0.0255 + 0.1641244632564251 + 5.551115123125783e-17)
a = -90.5
D_temp = [Rotation(a, v) for v in D]
D_temp = [Shift(d,v) for v in D_temp]
D_temp = [Rotation(a2, v) for v in D_temp]
D_temp = [Shift((cx,cy),v) for v in D_temp]

triangle = [A_temp,B_temp,C_temp,D_temp]

plot_shapes = []

xmin = 0
xmax = 0
ymin = 0
ymax = 0

for shape in triangle:
    x = np.asarray(shape)[:,0]
    y = np.asarray(shape)[:,1]
    plot_shapes.append((x,y))
    if min(x) < xmin:
        xmin = min(x)
    if max(x) > xmax:
        xmax = max(x)
    if min(y) < ymin:
        ymin = min(y)
    if max(y) > ymax:
        ymax = max(y)

xspan = xmax - ymin
yspan = ymax - ymin
cx,cy = 1/2 * (xmin + xmax), 1/2 * (ymin + ymax)
print(cx,cy)

centroids = [cA,cB,cC,cD]

# with open("upright_triangle_vertices.txt",'w') as fout:
#     for name,shape in zip(['A','B','C','D'],triangle):
#         fout.write(name + '= ')
#         for v in shape:
#             fout.write(str(v) + ',')
#         fout.write('\n')

print(f"Centroids for the up triangle: {centroids}")
with open("up_triangle_centered_at_the_origin.txt",'w') as fout:
    for c, shape in zip(centroids,triangle):
        for v in shape:
            x,y = v
            x = x - c[0]
            y = y - c[1]
            fout.write(str((x,y)) + ',')
        fout.write('\n')

plot_shapes = []

# for c, shape in zip(centroids,triangle):
#     x = np.asarray(shape)[:, 0] - c[0]
#     y = np.asarray(shape)[:, 1] - c[1]
#     plot_shapes.append((x, y))

# fig, (ax1, ax2, ax3, ax4,ax) = plt.subplots(1,5, figsize=(9, 3),
#                                     subplot_kw={'aspect': 'equal'})
#
# fig.suptitle('Triangle rearranged')
# ax1.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax2.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax3.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax4.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
#
# ax.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
# plt.show()

# with open("upright_triangle_vertices.txt",'w') as fout:
#     for name,shape in zip(['A','B','C','D'],triangle):
#         fout.write(name + '= ')
#         for v in shape:
#             fout.write(str(v) + ',')
#         fout.write('\n')

plot_shapes = []
centroids = [cA, cB, cC, cD]
for c, shape in zip(centroids, triangle):
    x = np.asarray(shape)[:, 0]
    y = np.asarray(shape)[:, 1]
    plot_shapes.append((x, y))
triangle_up = plot_shapes
fig, (ax1, ax2, ax3, ax4,ax) = plt.subplots(1,5, figsize=(9, 3),
                                    subplot_kw={'aspect': 'equal'})

fig.suptitle('Triangle')
ax1.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
ax2.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
ax3.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
ax4.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')

ax.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
ax.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
ax.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
ax.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
plt.show()

A = [(-0.5223290993692602, -0.16516412776125292), (0.47767090063073975, -0.16516412776125292), (0.04465819873852046, 0.3303282555225058)]
B =  [(-0.5534779580863476, -0.2274853687848006), (0.44652204191365247, -0.2274853687848006), (0.33762976744895196, 0.32497372029196253), (-0.3079855748025888, 0.197719911933842)]
C =  [(-0.46196653872316695, -0.2417397096265952), (0.538033461276833, -0.2417397096265952), (0.28352584456059177, 0.1990804134392008), (-0.24936389836384554, 0.38100648201528425)]
D =  [(-0.7425143969508786, 0.00812615065931594), (0.12351100683355996, -0.49187384934068407), (0.6190033901173186, -0.05886114744846476), (0.12351100683355996, 0.508126150659316)]


cA = (-0.027 , 0.716)
cB = (-0.552 , 0.511)
cC = (0.548 , 0.536)
cD = (-0.015 , 0.139)


#-0.0023111772376280815 -0.1641244632564251
#rotate 180, displace

a2 = 180
cx = 1.1831002741935492e-06
cy = -3.336410032694914e-07

A_temp = []
d = (0.025 + 0.0023111772376280815,-0.88 + 0.1641244632564251 + 5.551115123125783e-17)
for v in A:
    A_temp.append(Rotation(0,v))
A_temp = [Shift(d, v) for v in A_temp]
A_temp = [Rotation(a2, v) for v in A_temp]
A_temp = [Shift((cx,cy), v) for v in A_temp]


d = (0.55 + 0.0023111772376280815,-0.675 + 0.1641244632564251 + 5.551115123125783e-17)
B_temp = []
for v in B:
    B_temp.append(Rotation(120,v))
B_temp = [Shift(d,v) for v in B_temp]
B_temp = [Rotation(a2, v) for v in B_temp]
B_temp = [Shift((cx,cy),v) for v in B_temp]

C_temp = []
d = (-0.55 + 0.0023111772376280815,-0.70 + 0.1641244632564251 + 5.551115123125783e-17)
for v in C:
    C_temp.append(Rotation(-120,v))
C_temp = [Shift(d,v) for v in C_temp]
C_temp = [Rotation(a2, v) for v in C_temp]
C_temp = [Shift((cx,cy),v) for v in C_temp]

D_temp = []
D_temp = []
d = (-0.0175 + 0.0023111772376280815,-0.0255 + 0.1641244632564251 + 5.551115123125783e-17)
a = -90.5
D_temp = [Rotation(a, v) for v in D]
D_temp = [Shift(d,v) for v in D_temp]
D_temp = [Rotation(a2, v) for v in D_temp]
D_temp = [Shift((cx,cy),v) for v in D_temp]

triangle = [A_temp,B_temp,C_temp,D_temp]

plot_shapes = []

xmin = 0
xmax = 0
ymin = 0
ymax = 0

for shape in triangle:
    x = np.asarray(shape)[:,0]
    y = np.asarray(shape)[:,1]
    plot_shapes.append((x,y))
    if min(x) < xmin:
        xmin = min(x)
    if max(x) > xmax:
        xmax = max(x)
    if min(y) < ymin:
        ymin = min(y)
    if max(y) > ymax:
        ymax = max(y)

xspan = xmax - ymin
yspan = ymax - ymin
cx,cy = 1/2 * (xmin + xmax), 1/2 * (ymin + ymax)
print(cx,cy)


# with open("upside_down_triangle.txt",'w') as fout:
#     for name,shape in zip(['A','B','C','D'],triangle):
#         fout.write(name + '= ')
#         for v in shape:
#             fout.write(str(v) + ',')
#         fout.write('\n')
#
# plot_shapes = []
# centroids = [cA,cB,cC,cD]
# for c, shape in zip(centroids,triangle):
#     x = np.asarray(shape)[:, 0] - c[0]
#     y = np.asarray(shape)[:, 1] - c[1]
#     plot_shapes.append((x, y))
#
# fig, (ax1, ax2, ax3, ax4,ax) = plt.subplots(1,5, figsize=(9, 3),
#                                     subplot_kw={'aspect': 'equal'})
#
# fig.suptitle('Triangle rearranged 2')
# ax1.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax2.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax3.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax4.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
#
# ax.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
# plt.show()

plot_shapes = []
centroids = [cA, cB, cC, cD]
for c, shape in zip(centroids, triangle):
    x = np.asarray(shape)[:, 0]
    y = np.asarray(shape)[:, 1]
    plot_shapes.append((x, y))

triangle_down = plot_shapes

# fig, (ax1, ax2, ax3, ax4,ax) = plt.subplots(1,5, figsize=(9, 3),
#                                     subplot_kw={'aspect': 'equal'})
#
# fig.suptitle('Triangle updide down')
# ax1.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax2.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax3.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax4.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
#
# ax.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
# plt.show()

plt.title("Together")

plot_shapes = triangle_up

ax.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
ax.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
ax.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
ax.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')

plot_shapes = triangle_down

ax.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
ax.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
ax.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
ax.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')


plt.show()
#
# with open("triangle.txt",'w') as fout:
#     for name,shape in zip(['A','B','C','D'],triangle):
#         fout.write(name + '= ')
#         for v in shape:
#             fout.write(str(v)+ ',')
#         fout.write('\n')
#
#
# print("Triangle")
# print(f'xmin: {xmin}, xmax: {xmax}, ymin: {ymin}, ymax: {ymax}')
# print(f'Triangle dimensions: x-span: {xspan}, y-span: {yspan}')

# Square

# cA = (-0.451 , 0.419)
# cB = (0.269 , 0.419)
# cC = (-0.391 , -0.321)
# cD = (0.239 , -0.221)

# A_temp = []
# d = (-0.31 - 0.14096254863377533, 0.45 - 0.030792906816074883)
# a = 49
# A_temp = [Rotation(a,v) for v in A]
# A_temp = [Shift(d,v) for v in A_temp]
#
# B_temp = []
# d = (0.41 - 0.14096254863377533, 0.45 - 0.030792906816074883)
# a = -10
# B_temp = [Rotation(a,v) for v in B]
# B_temp = [Shift(d,v) for v in B_temp]
#
# C_temp = []
# d = (-0.25 - 0.14096254863377533, -0.29 - 0.030792906816074883)
# a = 109
# C_temp = [Rotation(a,v) for v in C]
# C_temp = [Shift(d,v) for v in C_temp]
#
# D_temp = []
# d = (0.38 - 0.14096254863377533, -0.19 - 0.030792906816074883)
# a = -40.5
# D_temp = [Rotation(a,v) for v in D]
# D_temp = [Shift(d,v) for v in D_temp]
#
# plot_shapes = []
# square = [A_temp,B_temp,C_temp,D_temp]
#
# xmin = 0
# xmax = 0
# ymin = 0
# ymax = 0
#
# for shape in square:
#     x = np.asarray(shape)[:,0]
#     y = np.asarray(shape)[:,1]
#     plot_shapes.append((x,y))
#     if min(x) < xmin:
#         xmin = min(x)
#     if max(x) > xmax:
#         xmax = max(x)
#     if min(y) < ymin:
#         ymin = min(y)
#     if max(y) > ymax:
#         ymax = max(y)
#
# xspan = xmax - ymin
# yspan = ymax - ymin
# cx,cy = 1/2 * (xmin + xmax), 1/2 * (ymin + ymax)
# print(cx,cy)
#
# for shape in square:
#     x = np.asarray(shape)[:, 0]
#     y = np.asarray(shape)[:, 1]
#     plot_shapes.append((x, y))
#
# fig, (ax1, ax2, ax3, ax4,ax) = plt.subplots(1,5, figsize=(9, 3),
#                                     subplot_kw={'aspect': 'equal'})
#
# fig.suptitle('Square')
# ax1.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax2.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax3.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax4.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
#
# ax.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
# plt.show()
#
# print('\n')
# print("Square")
# print(f'xmin: {xmin}, xmax: {xmax}, ymin: {ymin}, ymax: {ymax}')
# print(f'Square dimensions: x-span: {xspan}, y-span: {yspan}')
#
# with open("regular_square.txt",'w') as fout:
#     for name,shape in zip(['A','B','C','D'],square):
#         fout.write(name + '= ')
#         for v in shape:
#             fout.write(str(v) + ',')
#         fout.write('\n')
#
# plot_shapes = []
# centroids = [cA,cB,cC,cD]
# for c, shape in zip(centroids,square):
#     x = np.asarray(shape)[:, 0] - c[0]
#     y = np.asarray(shape)[:, 1] - c[1]
#     plot_shapes.append((x, y))
#
# fig, (ax1, ax2, ax3, ax4,ax) = plt.subplots(1,5, figsize=(9, 3),
#                                     subplot_kw={'aspect': 'equal'})
#
# fig.suptitle('Square rearranged')
# ax1.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax2.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax3.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax4.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
#
# ax.fill(plot_shapes[0][0],plot_shapes[0][1], facecolor ="tab:purple")
# ax.fill(plot_shapes[1][0],plot_shapes[1][1], facecolor='tab:red')
# ax.fill(plot_shapes[2][0],plot_shapes[2][1], facecolor='tab:blue')
# ax.fill(plot_shapes[3][0],plot_shapes[3][1], facecolor='tab:green')
# plt.show()
#
#
# with open("shifted_square.txt",'w') as fout:
#     for c, shape in zip(centroids,square):
#         for v in shape:
#             x,y = v
#             x = x - c[0]
#             y = y - c[1]
#             fout.write(str((x,y)) + ',')
#         fout.write('\n')
