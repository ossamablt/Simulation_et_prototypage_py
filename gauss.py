import numpy as np
def swap_lines(A, i, j):
#Echange les lignes i et j danas la matrice A
 tmp = A[i, :].copy()
 A[i, :] = A[j, :]
 A[j, :] = tmp
 return A
def transvection_lines(A, i, j, x):
#A_j <- A_j + xA_j 
 A[j, :] = A[j, :] + x * A[i, :]
 return A