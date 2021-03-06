# -*- coding: utf-8 -*-
"""Copy of solver.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vq_okmdWHEC_MvVn8km4vFa6Sf0puGVL

# **Linear Equation Solver**
In this problem, we will use three methods to solve linear systems of equations with unique solutions. In particular, we will:

1) create a function "gauss_jordan_solve" that solves a system of equations using Gauss-Jordan elimination on the augmented matrix A|b.

2) create a function "inverse_solve" that solves a system of equations by first finding the matrix inverse of A and then using that inverse to compute the solution directly, x = inverse(A)*b.

3) create a fuction "numpy_solve" that makes use of NumPy, a numerical computation library, to solve the problem with minimal use of our own helper functions.

For all of these functions you can assume well formed input that describes a valid linear systems of equations with a unique solution. That is to say, you don't have to do error handling nor input validation.

---



Copy this file to your Google Drive (File -> Save a copy in drive), then complete the assignment. When the assignment is complete, download this notebook as a .py file (File -> Download .py). Submit the completed file to gradescope with the filename "solver.py". For this assignment, no libraries are permitted with the exception of numpy in the final function, "numpy_solve".

# Helper functions
First, let's implement a few functions to perform the basic operations of gaussian elimination.
"""

"""
These are two functions to help you test your implementations.
"""
def lists_equal(a,b):
  if (len(a) != len(b)):
    return False
  for i in range(len(a)):
    if (abs(a[i] - b[i]) > 0.00001):
      return False
  return True

def matrices_equal(a,b):
  if (len(a) != len(b)):
    return False
  for i in range(len(a)):
    if (not lists_equal(a[i],b[i])):
      return False
  return True

assert(lists_equal([1.00000001,2.000000001],[1,2]))
assert(matrices_equal([[1.00000000001,2.00000000001],[3.00000000001,4]], [[1,2],[3,4.00000001]]))

"""The first function we will implement is the "swap" function which will swap two rows of an arbitrary n by m matrix represented by a 2-d array."""

"""
Inputs:
   mat: a n by m matrix represented by a 2-d array
   i: int
   j: int
Output:
   A 2-d array that is a copy of mat where the ith row and jth row are swapped (where rows are 0-indexed)
"""
def swap(mat, i,j):
    result = mat[::]
    result[i], result[j] = result[j], result[i]

    return result

#Test
m = [[1,2,3],[4,5,6]]
m = swap(m,0,1)
assert(matrices_equal(m,[[4,5,6],[1,2,3]]))

"""The subtract function will subtract a multiple of one row from another row."""

"""
Inputs:
   mat: a n x m matrix represented by a 2-d array
   i: int
   j: int
Output:
   A 2-d array that is a copy of mat where l times the j-th row is subtracted
   from the i-th row (where rows are 0-indexed)
"""
def sub(mat, i, j, l):
  result = mat[::]
  for col, value in enumerate(mat[j]):
    result[i][col] -= value * l

  return result
  
#Test 
m = [[1.0,1.0,1.0],[3.5,3.5,3.5]]
m = sub(m,1,0,2.5)
assert(m == [[1.0,1.0,1.0],[1.0,1.0,1.0]])

"""For use as a helper function, implement a function that divides each row of a matrix by its pivot."""

"""
Inputs:
   mat: a n x m matrix represented by a 2-d array
Output:
   A 2-d array that is a copy of mat where every element of each row is divided by the 
   pivot (the first nonzero entry) of the row 
"""
def normalize(mat):
  result = mat[::]

  for idx, row in enumerate(mat):
    pivot = 0
    for value in row:
      if value != 0:
        pivot = value
        break

    for col in range(len(row)):
      result[idx][col] = result[idx][col]/pivot

  return result


mat = [[1, 2, 3], [0, 5, 10],[0, 0, 10]]

"""For convenience, let's make a function that horizontally appends two matrices together and another function that generates the identity matrix."""

"""
Inputs:
   n: a positive integer
Output:
   A 2-d array of reprensenting an n x n matrix where every element along the diagonal
   is one and all other elements are zero
"""
def identity(n:int):
  mat = [ [0] * n for _ in range(n) ]
  
  for i in range(n):
    mat[i][i] = 1

  return mat

"""
Inputs:
   a: a n x m matrix represented by a 2-d array
   b: a n x m matrix represented by a 2-d array
Output:
   A 2-d array of where the ith element is the result of appending the ith 
   element of "a" to the ith element of b (i.e the rows of b are appended to 
   the rows of a).
"""
def append(a,b):
  mat = []
  for i in range(len(a)):
    row = a[i][::]
    row.extend(b[i])
    mat.append( row )

  return mat

#Test
i_mat = identity(2)
a = [[1.0,2.0],[3.0,4.0]]
assert(matrices_equal(append(a,i_mat),[[1.0,2.0,1.0,0.0],[3.0,4.0,0.0,1.0]]))

"""Now let's use these functions to implement the Gauss-Jordan algorithm."""

"""
Inputs:
   mat: an n x m matrix represented by a 2-d array 
Output:
  A 2-d array representing the result of running gauss jordan elimination on the 
  the matrix "mat".
"""
def gauss_jordan(mat):
  m = mat.copy()
  """
  For k from 1 to n:
    Find the next row with nonzero value in the kth column
    Swap that row and the kth row
    For each row not equal to the kth row:
      remove a multiple of the kth row such that the value in the pivot column is zero
  """
  for k in range(0, len(m)):
    pivot = 0
    for row in range(k, len(m)):
      pivot = m[row][k]
      if pivot != 0:
        swap(m, row, k)
        break
    if pivot != 0:
      for i in range(len(m[k])):
        m[k][i] = m[k][i] / pivot
      for row in range(len(m)):
        if row != k:
          l = m[row][k]  
          sub(m, row, k, l)
  return m

m = [[1.0,0,0],[4.0,4.0,6.0],[0.0,1.0,0.0]]
i_mat = identity(3)
i_mat = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
assert(matrices_equal(gauss_jordan(append(m,i_mat)),[[1.0, 0.0, 0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0, 0.0, 1.0], [-0.0, -0.0, 1.0, -2/3, 1/6, -2/3]]))

"""To implement our inverse solver, let's make a function that finds the inverse of a square matrix. We can use our gauss_jordan function to simplify our implementation."""

"""
Inputs:
   m: a square matrix represented by a 2-d array
Output:
   Returns the inverse of the matrix m represented by a 2-d array
"""
def my_inverse(m):
  n = len(m)
  i_mat = identity(n)
  mat = append(m, i_mat)
  mat = gauss_jordan(mat)
  res = m
  for i in range(0, n):
    for j in range(0, n):
      res[i][j] = mat[i][j + n]
  return res

#Test
assert(matrices_equal(my_inverse([[1.0,0,0],[4.0,4.0,6.0],[0.0,1.0,0.0]]), [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [-2/3, 1/6, -2/3]]))

"""We'll also need a function to compute the product of a matrix by a vector. Let's just create a function to compute the product of two matrices and simply convert vectors into n x 1 matrices."""

def convert_to_mat(vec):
  if not isinstance(vec[0], list):
    return [[el] for el in vec]
  else:
    return vec.copy()

"""
Inputs:
   a: an n x m matrix represented by a 2-d array
   b: an m x p matrix represented by a 2-d array
Output:
   Returns the n x p matrix product, ab, represented by a 2-d array.
"""
def matmul(a,b):
  a_mat = convert_to_mat(a)
  b_mat = convert_to_mat(b)
  ab =[ [0] * len(b[0]) for _ in range(len(a))]

  n = len(a)
  p = len(b[0])

  for i in range(n):
    for j in range(p):
      total = 0
      for k in range(n):
        total += a[i][k] * b[k][j]

      ab[i][j] = total

  return ab

#Test
a = [[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0]]
b = [[1.0,1.0,1.0],[2.0,2.0,2.0],[3.0,4.0,5.0]]
assert(matrices_equal(matmul(a,b), [[14.0, 17.0, 20.0],[32.0, 38.0, 44.0],[50.0,59.0,68.0]]))

"""# Solvers
Finally, lets put it all together to create three functions, each of which use a slightly different method to solve the system of linear equations.
"""

def convert_to_vec(mat):
  if (len(mat[0]) == 1):
    return [row[0] for row in mat]
  else:
    return mat.copy()

"""
Inputs:
   ---- A system of equations in matrix form, Ax = b -----
   a_mat: a matrix representing the left hand side of a system of equations
   b_vec: a vector reprenting the right hand side of a system of equations
Output:
   Returns the solution using gauss-jordan elimination on the augmented matrix, A|b
"""
def gauss_jordan_solve(a_mat,b_vec):
  n = len(a_mat)
  a = append(a_mat, convert_to_mat(b_vec))
  a = gauss_jordan(a)
  res = [0] * n
  for i in range(n):
    res[i] = a[i][n]
  return res 

#Test
m = [[1.0,0,0],[4.0,4.0,6.0],[0.0,1.0,0.0]]
b = [1.0, 1.0, 2.0]
assert(lists_equal(gauss_jordan_solve(m,b), [1.0, 2.0, -11/6]))

"""
Inputs:
   ---- A system of equations in matrix form, Ax = b -----
   a_mat: a n x n matrix representing the left hand side of a system of equations
   b_vec: a n-dimensional vector reprenting the right hand side of a system of equations
Output:
   Returns the solution using the matrix product of the inverse of a_mat with 
   b_vec, inverse(a)*b. The inverse is found using your inverse function, my_inverse.
"""
def inverse_solve(a_mat,b_vec):
  a_inv = my_inverse(a_mat)
  tmp = matmul(a_inv, convert_to_mat(b_vec))
  res = [0] * len(a_mat)
  for i in range(len(a_mat)):
    res[i] = tmp[i][0]
  return res

#Test
m = [[1.0,0,0],[4.0,4.0,6.0],[0.0,1.0,0.0]]
b = [1.0, 1.0, 2.0]
assert(lists_equal(inverse_solve(m,b), [1.0, 2.0, -11/6]))

import numpy as np

"""
Inputs:
   ---- A system of equations in matrix form, Ax = b -----
   a_mat: a n x n matrix representing the left hand side of a system of equations
   b_vec: a n-dimensional vector reprenting the right hand side of a system of equations
Output:
   Returns the solution using NumPy. For example, this could be done replacing our call
   to my_inverse in inverse_solve with a call to numpy.linalg.inv. However, there may be a better way.
"""
def numpy_solve(a_mat,b_vec):
  a_inv = np.linalg.inv(a_mat)
  tmp = a_inv @ (np.array([b_vec]).T)
  res = tmp.T[0]
  return res

#Test
m = [[1.0,0,0],[4.0,4.0,6.0],[0.0,1.0,0.0]]
b = [1.0, 1.0, 2.0]
assert(lists_equal(numpy_solve(m,b), [1.0, 2.0, -11/6]))