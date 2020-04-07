#!/usr/bin/env python
# encoding: utf-8

"""
@author: leidelong
@contact: leidl8907@gmail.com
@time: 2020/4/5 19:26
"""

from __future__ import print_function
import sys
from ortools.constraint_solver import pywrapcp

def main():
  solver = pywrapcp.Solver("simple_example")
  # Create the variables.
  num_vals = 3
  x = solver.IntVar(0, num_vals - 1, "x")
  y = solver.IntVar(0, num_vals - 1, "y")
  z = solver.IntVar(0, num_vals - 1, "z")
  # Create the constraints.
  solver.Add(x != y)
  # Call the solver.
  db = solver.Phase([x, y, z], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)
  solver.Solve(db)
  print_solution(solver, x, y, z)
def print_solution(solver, x, y, z):
  count = 0

  while solver.NextSolution():
    count += 1
    print("x =", x.Value(), "y =", y.Value(), "z =", z.Value())
  print("\nNumber of solutions found:", count)

if __name__ == "__main__":
  main()