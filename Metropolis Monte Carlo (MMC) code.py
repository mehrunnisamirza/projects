import numpy as np
import matplotlib.pyplot as plt
import random

nx = int(input("Enter the value of nx: "))      #dimensions of lattice
n_moves = int(input("Enter number of moves: ")) #number of moves
T = int(input("Enter value of Temperature: "))  #temperature
k = 1.380649 * 10 ** -23                        #boltzman constant

density_AB = float(input('Enter density of both A and B discs: '))
f_A = float(input("Enter value of f_A: "))
f_B = 1 - (f_A)

E_AA = int(input("Enter the value of E_AA: "))  #energy contribution for type A on both interacting vertices
E_BB = int(input("Enter the value of E_BB: "))  #energy contribution for type B on both interacting vertices
E_AB = int(input("Enter the value of E_AB: "))  #energy contribution for type A on one vertex type B on the other vertex

lattice0 = np.zeros((nx,nx), dtype = int)       #initialize lattice with all 0 entries

density_A = density_AB * f_A                    #randomly distribute type A and type B disks according to their densities
density_B = density_AB * f_B                    #here I have calculated the densitities based on the combined density dnesity_AB inputted by the user
density_0 = 1 - density_AB

lattice = np.random.choice([1,2,0],size = np.shape(lattice0),p = [density_A, density_B,density_0])

pos_of_A = np.where(lattice == 1)               #find coordinates of type As in the lattice
pos_of_B = np.where(lattice == 2)               #find coordinates of type Bs in the lattice
pos_of_0 = np.where(lattice == 0)               #find coordinates of vacancies in the lattice

print(lattice)
print()
list_pos_of_A = list(zip(pos_of_A[0], pos_of_A[1]))    #zip together to get exact coordinates of type A in a list
list_pos_of_B = list(zip(pos_of_B[0], pos_of_B[1]))    #zip together to get exact coordinates of type B in a list
list_pos_of_0 = list(zip(pos_of_0[0], pos_of_0[1]))    #zip together to get exact coordinates of vacancies in a list

x_0, y_0 = pos_of_0                         #find x,y coordinates of A by unpacking
x_1, y_1 = pos_of_A                         #find x,y coordinates of B by unpacking
x_2, y_2 = pos_of_B                         #same for vacancies

fig, axs = plt.subplots(1,2)                              #plot 2 horizontally stacked plots
fig.suptitle('before and after')                          #this one is for the initial configuration
axs[0].plot(x_1, y_1,'bs',markersize = 4,label ='A' )     #plot type A disks
axs[0].plot(x_0,y_0,'ks',markersize = 4,label ='Vacant')  #plot type B disks
axs[0].plot(x_2, y_2,'sr',markersize = 4,label ='B')      #plot type 0 disks

plt.legend(loc=(1.04, 0))

"""""""""""""""""""""""""""""""""""""""""""initial configuration"""""""""""""""""""""""""""""""""""""""""""""""""""""""

def find_non_0_neigbour(i,j):                       #define funtion to find neighbours for disk  with coordinates (i, j)
    neighbours_coordinates = dict()                 #Empty dict to store coordinates of neighbours
                                                    #here I only check for 2 neighbours in the upwards and right direction to avoid double counting
    if i - 1 < 0:
        #U = lattice[lattice.shape[0] - 1][j]
        neighbours_coordinates["U"] = (lattice.shape[0] - 1, j) #up
    else:
        #U = lattice[i - 1][j]
        neighbours_coordinates["U"] = (i - 1, j)

    if j + 1 > (lattice.shape[1] - 1):
        #R = lattice[i][0]
        neighbours_coordinates["R"] = (i, 0)                   #right
    else:
        #R = lattice[i][j + 1]  # right
        neighbours_coordinates["R"] = (i, j + 1)

    non_0_neighbour_types = []
    non_0_neighbour_coordinates = []

    for neighbour, coordinates in neighbours_coordinates.items():     #Loop through coordinates of neighbours
        neighbour_type = lattice[coordinates[0]][coordinates[1]]

        if neighbour_type != 0:                                       #Keep only neighbours that are not 0
            non_0_neighbour_types.append(neighbour_type)              #append neighbour types
            non_0_neighbour_coordinates.append(coordinates)           #append coordinates of neighbours


    return non_0_neighbour_coordinates, non_0_neighbour_types         #function returns neighbour types and neighbours

store_non_0_coordinates_A = []   #stores coordinates of non-0 neighbours for A
store_non_0_types_A = []         #stores types of non-0 neighbours for A
store_non_0_coordinates_B = []   #stores coordinates of non-0 neighbours for B
store_non_0_types_B = []         # stores types of non-0 neighbours for A

for i, j in list_pos_of_A:       #find neighbour types and their coordinates for A by using function defined above
    non_0_neighbour_coordinates, non_0_neighbour_types = find_non_0_neigbour(i, j)
    store_non_0_coordinates_A.append(non_0_neighbour_coordinates)
    store_non_0_types_A.append(non_0_neighbour_types)

    #print(f"Vertex A with coordinates ({i}, {j}) has non-zero neighbours types {non_0_neighbour_types} with coordinates {non_0_neighbour_coordinates}")

all_A = list(zip(store_non_0_types_A, store_non_0_coordinates_A))    #stores both types and coordinates of neighbours for A


for i, j in list_pos_of_B:      #find neighbour types and their coordinates for B by using function defined above
    non_0_neighbour_coordinates, non_0_neighbour_types  = find_non_0_neigbour(i, j)
    store_non_0_coordinates_B.append(non_0_neighbour_coordinates)
    store_non_0_types_B.append(non_0_neighbour_types)

    #print(f"Vertex B with coordinates ({i}, {j}) has non-zero neighbours types {non_0_neighbour_types} with coordinates {non_0_neighbour_coordinates}")

all_B = list(zip(store_non_0_types_B, store_non_0_coordinates_B))    #stores both types and coordinates of neighbours for A

Energies = []                     #stores epsilon values for initial configuration

for i in all_A:                   #checking neighbour types for disk A

    if [2] in i:                  #if neighbour is of type 2 (type B) then append E_AB
        Energies.append(E_AB)

    if [2, 2] in i:              #if two neighbours are of type 2 (type B) then append E_AB twice
        Energies.append(E_AB)
        Energies.append(E_AB)

    if [2, 1] in i:
        Energies.append(E_AB)    #one neighbour is of type 2 (type B) so append E_AB and
        Energies.append(E_AA)    #other neighbour is of type 1 (type A) so append E_AA

    if [1, 2] in i:
        Energies.append(E_AA)
        Energies.append(E_AB)     #other neighbour is of type 2 (type B) so append E_AB

    if [1] in i:
        Energies.append(E_AA)     #if neighbour is of type 1 (type A) then append E_AA

    if [1, 1] in i:
        Energies.append(E_AA)
        Energies.append(E_AA)

for i in all_B:                   #checking neighbour types for disk B

    if [2] in i:                  #if neighbour is of type 2 (type B) then append E_BB
        Energies.append(E_BB)

    if [1] in i:
        Energies.append(E_AB)     #if neighbour is of type 1 (type A) then append E_AB

    if [2, 2] in i:
        Energies.append(E_BB)    #if two neighbours are of type 2 (type B) then append E_BB twice
        Energies.append(E_BB)

    if [1, 1] in i:
        Energies.append(E_AB)    #if two neighbours are of type 1 (type A) then append E_AB twice
        Energies.append(E_AB)

    if [1, 2] in i:
        Energies.append(E_AB)    #one neighbour is of type 1 (type A) so append E_AB
        Energies.append(E_BB)    #and one neighbour is of type 2 (type B) so append E_EB

    if [2, 1] in i:
        Energies.append(E_BB)
        Energies.append(E_AB)
print()
sum_E1 = np.sum(Energies)         #energy for initial configuration
Initial_E = sum_E1

pos_of_A_and_B = list_pos_of_A + list_pos_of_B              #combined list of coordinates for A and B
pos_of_all = list_pos_of_0 + list_pos_of_A + list_pos_of_B  #combined list of coordinates for A and B and vacancies

print()

"""""""""""""""""""""""""""""""""""""""""""""""""Swap"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def find_non_0_neigbour_swap(i,j):                   #Find all 4 neighbours this time for disk with coordinates (i, j)
    neighbours_coordinates = dict()                  #Empty dict to store coordinates of neighbours

    if i + 1 > (lattice.shape[0] - 1):
        # D = lattice[0][j]
        neighbours_coordinates["D"] = (0, j)  #down
    else:
        # D_A = lattice[i + 1][j]
        neighbours_coordinates["D"] = (i + 1, j)

    if i - 1 < 0:
        # U_A = lattice[lattice.shape[0] - 1][j]
        neighbours_coordinates["U"] = (lattice.shape[0] - 1, j) #up
    else:
        # U_A = lattice[i - 1][j]
        neighbours_coordinates["U"] = (i - 1, j)

    if j + 1 > (lattice.shape[1] - 1):
        # R_A = lattice[i][0]
        neighbours_coordinates["R"] = (i, 0)                   #right
    else:
        # R_A = lattice[i][j + 1]  # right
        neighbours_coordinates["R"] = (i, j + 1)

    if j - 1 < 0:
        # L_A = lattice[i][lattice.shape[0] - 1]
        neighbours_coordinates["L"] = (i, lattice.shape[0] - 1) #left
    else:
        # L_A = lattice[i][j - 1]
        neighbours_coordinates["L"] = (i, j - 1)

    non_0_neighbour_types = []              # Keep only neighbours that are not 0
    non_0_neighbour_coordinates = []

    for neighbour, coordinates in neighbours_coordinates.items():     # Loop through coordinates of neighbours
        neighbour_type = lattice[coordinates[0]][coordinates[1]]

        if neighbour_type != 0:
            non_0_neighbour_types.append(neighbour_type)
            non_0_neighbour_coordinates.append(coordinates)


    return non_0_neighbour_coordinates, non_0_neighbour_types

"""""""""""""""""""""""""""""""""""Pick 2 random disks and find all 4 neighbours"""""""""""""""""""""""""""""""""""""""""

E_delta = []
accepted_move = 0
acceptance_ratio_list = []

for i in range(n_moves):                                   #loop through to swap n_moves times
    print('Move number:', i+1)
    E_before_swap = []                                       #stores energies before swap move
    E_after_swap = []                                        #stores energies before swap move

    rand_disk1 = random.choice(pos_of_A_and_B)               #randomly pick disk from combined list of coordinates for A and B
    rand_disk2 = random.choice(pos_of_all)                   #randomly pick disk from combined list of coordinates for A and B and vacancies

    types_of_vertices = [lattice[rand_disk1]] + [lattice[rand_disk2]]  #group types of randomly picked neighbours together in a list
    combine = [rand_disk1] + [rand_disk2]                    #group coordinates of randomly picked neighbours together in a list

    combine_types = []                                       #store types of neighbours in here
    for i, j in combine:
        non_0_neighbour_coordinates, non_0_neighbour_types = find_non_0_neigbour_swap(i, j)  #find 4 neighbours of the randomly picked disks using function defined earlier
        combine_types.append(non_0_neighbour_types)
        #print(f"Vertex {lattice[i][j]} with coordinates ({i}, {j}) has non-zero neighbours types {non_0_neighbour_types} with coordinates {non_0_neighbour_coordinates}")

    type_neighbours = [types_of_vertices] + [combine_types]  #list that stores types of randomly picked vertices and types of their neighbours
    X, Y = type_neighbours                                   #unpack to seprate types of randomly picked vertices and types of their neighbours
    #print(type_neighbours)

    type_disc_1 = X[0]                      #type of one randomly picked disk is equal to the first element of X
    neighbour_types_disc_1 = Y[0]           #type of neighbour for that is equal to first elemnt of Y

    type_disc_2 = X[1]                      #type of the other randomly picked disk is equal to the second element of X
    neighbour_types_disc_2 = Y[1]           #type of neighbour for that is equal to first elemnt of Y

    epsilon_map = {1: {1: E_AA, 2: E_AB},2: {1: E_AB, 2: E_BB},0: {1: 0,2: 0,}}   #dictionary to store epsilon values for different types

    for neighbour_type in neighbour_types_disc_1:     #loop through neighbour_types_disc_1 to find epsilon value from dictionary
        #print("random disk", type_disc_1)
        #print("neighbour_type", neighbour_type)
        epsilon_vertex = epsilon_map[type_disc_1][neighbour_type]  #use keys for type of vertex and type of neighbour to fnd epsilon value from dictionary
        E_before_swap.append(epsilon_vertex)                       #append to E before swap

    for neighbour_type in neighbour_types_disc_2:                  #same for neighbour_types_disc_2
        #print("random disk", type_disc_2)
        #print("neighbour_type", neighbour_type)
        epsilon_vertex = epsilon_map[type_disc_2][neighbour_type]
        E_before_swap.append(epsilon_vertex)

    E_1 = np.sum(E_before_swap)                                   #sum up energies in E_before_swap list

    """""""""""""""""""""""""""""""""Swap and find energies due to neighbours again"""""""""""""""""""""""""""""""""

    a, b = rand_disk1
    c, d = rand_disk2
    tmp = lattice[a][b]
    lattice[a][b] = lattice[c][d]                                 #swap
    lattice[c][d] = tmp
    print(f'vertex {lattice[a][b]} {rand_disk2} is swapped with {lattice[c][d]} {rand_disk1}')

    types_of_vertices2 = [lattice[a][b]] + [lattice[c][d]]
    combine2 = [rand_disk1] + [rand_disk2]

    combine_types2 = []
    for i, j in combine2:                                         #repeat same steps to find energy after swap
        non_0_neighbour_coordinates, non_0_neighbour_types = find_non_0_neigbour_swap(i, j)
        combine_types2.append(non_0_neighbour_types)
        #print(f"Vertex {lattice[i][j]} with coordinates ({i}, {j}) has non-zero neighbours types {non_0_neighbour_types} with coordinates {non_0_neighbour_coordinates}")

    type_neighbours2 = [types_of_vertices2] + [combine_types2]
    W, Z = type_neighbours2

    type_disc_1 = W[0]
    neighbour_types_disc_1 = Z[0]

    type_disc_2 = W[1]
    neighbour_types_disc_2 = Z[1]

    for neighbour_type in neighbour_types_disc_1:
        epsilon_vertex2 = epsilon_map[type_disc_1][neighbour_type]
        E_after_swap.append(epsilon_vertex2)

    for neighbour_type in neighbour_types_disc_2:
        epsilon_vertex2 = epsilon_map[type_disc_2][neighbour_type]
        E_after_swap.append(epsilon_vertex2)

    E_2 = np.sum(E_after_swap)                  #energy after swap
    delta_E = E_2 - E_1                         #difference in energy before and after swapping
    R = random.uniform(0, 1)                    #generate random number between 0 and 1
    W = - (delta_E / (k * T))
    Final_Energy = sum_E1 + delta_E
    """""""""""""""""""""""""""""""""""""""""""""Metropolis Criteria"""""""""""""""""""""""""""""""""""""""""""""""""""
    if delta_E < 0:
        print('accepted swap move')
        sum_E1 = sum_E1 + delta_E                     #initial energy of the configuration increases by delta_E in each iteration
        E_delta.append(sum_E1)                        #append new energy to E_delta to get a list of energies to plot evolution of energy
        accepted_move = accepted_move + 1
        acceptance_ratio = accepted_move / (i + 1)    
        acceptance_ratio_list.append(acceptance_ratio)
        print("Acceptance ratio:", acceptance_ratio)

    elif R < np.exp(W):
        print('accepted swap move')
        sum_E1 = sum_E1 + delta_E
        E_delta.append(sum_E1)
        accepted_move = accepted_move + 1
        acceptance_ratio = accepted_move / (i + 1)
        acceptance_ratio_list.append(acceptance_ratio)
        print("Acceptance ratio:", acceptance_ratio)

    else:
        print('Move rejected!')                        #if none of the above conditions are satisfied then the move is rejected
        tmp = lattice[c][d]                            #swap back
        lattice[c][d] = lattice[a][b]
        lattice[a][b] = tmp
        print(f'vertex {lattice[c][d]} {rand_disk1} is swapped back with {lattice[a][b]} {rand_disk2} as this move was rejected')  #swap back because move is rejected

    print(f"Energy after attempted move: {Final_Energy} kcal/mol")
    print()

print()
print(f"Energy for initial configuration: {Initial_E} kcal/mol")     #energy for initial configuration
print(f"Energy for final configuration: {Final_Energy} kcal/mol")    #Energy of final configuration

#find positions for all disks in the final configuration
pos_of_A2 = np.where(lattice == 1)                               #final positions of type A
pos_of_B2 = np.where(lattice == 2)                               #final positions of type B
pos_of_02 = np.where(lattice == 0)                               #final positions of vacancies

x_0_2, y_0_2 = pos_of_02                                         #unpack to find x,y coordinates of disks A, B and 0
x_1_2, y_1_2 = pos_of_A2
x_2_2, y_2_2 = pos_of_B2

#plot new positions
axs[1].plot(x_1_2, y_1_2,'bs',markersize = 4,label ='A')          #plot final positions of type A
axs[1].plot(x_0_2,y_0_2,'ks',markersize = 4,label ='Vacant')      #plot final positions of vacancies
axs[1].plot(x_2_2, y_2_2,'sr',markersize = 4,label ='B' )         #plot final positions of type B
plt.legend(loc=(1.04, 0))

#plotted this separately to see the evolution of energy and acceptance ratio
# plt.subplot(1, 2, 1)
# plt.plot(E_delta, 'b')
# plt.title("Evolution of Energy")
# plt.xlabel("No.of moves")
# plt.ylabel('Energy')
#
# plt.subplot(1, 2, 2)
# plt.plot(acceptance_ratio_list, 'b')
# plt.title("Evolution of Acceptance ratio")
# plt.xlabel("No. of moves")
# plt.ylabel('Acceptance ratio')


plt.show()
