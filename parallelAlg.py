# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: Duarte Mateus
"""

import galois
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def forward_elimination(A, b, GF):
    n = len(A)
    for i in range(n):
        # Find the pivot
        max_row = max(range(i, n), key=lambda r: A[r, i])
        if A[max_row, i] == 0:
            raise ValueError("Matrix is singular!")

        # Swap the rows
        A[[i, max_row]] = A[[max_row, i]]
        b[[i, max_row]] = b[[max_row, i]]

        # Make the diagonal contain all 1s
        inv = GF(1)/A[i, i]
        A[i] = [x * inv for x in A[i]]
        b[i] = b[i] * inv

        # Eliminate column entries below the pivot
        def eliminate_row(j):
            factor =A[j, i]
            A[j] = [A[j, k] - factor * A[i, k] for k in range(n)]
            b[j] = b[j] - factor * b[i]

        # Eliminate rows belos the pivot in parallel
        with ThreadPoolExecutor() as executor:
            executor.map(eliminate_row, range(i + 1, n))

    return A, b

def back_substitution(A, b, GF):
    n = len(A)
    x = [GF(0) for _ in range(n)]
    for i in reversed(range(n)):
        s=GF(0);
        for j in range(i + 1, n): 
            s+=A[i, j] * x[j] 
        x[i] = b[i] - s
    return x
        



def gaussian_elimination(A, b, GF):
    A, b = forward_elimination(A, b, GF)
    return back_substitution(A, b, GF)


def matrix_add_worker(A_slice, B_slice):
    return A_slice + B_slice

def parallel_matrix_add(A, B, num_workers):
    chunks_A = np.array_split(A, num_workers)
    chunks_B = np.array_split(B, num_workers)
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(matrix_add_worker, chunk_A, chunk_B) for chunk_A, chunk_B in zip(chunks_A, chunks_B)]
        results = [future.result() for future in futures]
    
    result = np.vstack(results)
    return result


def minor(matrix, row, col):
    """Return the minor of the matrix excluding the specified row and column."""
    minor_matrix = np.delete(matrix, row, axis=0)
    minor_matrix = np.delete(minor_matrix, col, axis=1)
    return minor_matrix

def determinant_worker(matrix, col, num_workers):
    """Calculate the cofactor expansion along the first row."""
    sign = (-1) ** col
    sub_matrix = minor(matrix, 0, col)
    sub_det = parallel_determinant(sub_matrix, num_workers)
    return sign * matrix[0, col] * sub_det

def parallel_determinant(matrix, num_workers):
    n = matrix.shape[0]
    
    if n == 1:
        return matrix[0, 0]
    elif n == 2:
        return matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(determinant_worker, matrix, col, num_workers) for col in range(n)]
        results = [future.result() for future in futures]
    
    return sum(results)

def matrix_multiply_worker(A_slice, B):
    return np.dot(A_slice, B)

def parallel_matrix_multiply(A, B, num_workers):
    # Split A into chunks
    chunks = np.array_split(A, num_workers)
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Map the worker function to the chunks
        futures = [executor.submit(matrix_multiply_worker, chunk, B) for chunk in chunks]
        results = [future.result() for future in futures]
    
    # Concatenate the results from each worker
    result = np.vstack(results)
    return result


if __name__ == "__main__":
    # Define the Galois Field GF(2^m)
    m = 8
    GF = galois.GF(2**m)
  
    # Example matrix A and vector b
    A = np.array([[GF(1), GF(67), GF(0)], [GF(0), GF(61), GF(0)], [GF(0), GF(0), GF(1)]], dtype=GF)
    b = np.array([GF(1), GF(1), GF(0)], dtype=GF)


    result = parallel_matrix_multiply(A, A, 3)
    
   # Solve Ax = b using Gaussian elimination
    x = gaussian_elimination(A, b, GF)
    print(x)
    print(result)
    
 