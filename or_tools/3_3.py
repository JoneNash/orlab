#!/usr/bin/env python
# encoding: utf-8

"""
@author: leidelong
@contact: leidl8907@gmail.com
@time: 2020/4/5 19:17
"""

from ortools.sat.python import cp_model


def main():
  # Declare the model
  model = cp_model.CpModel()
  #Create the variables
  var_upper_bound = max(50, 45, 37)
  x = model.NewIntVar(0, var_upper_bound, 'x')
  y = model.NewIntVar(0, var_upper_bound, 'y')
  z = model.NewIntVar(0, var_upper_bound, 'z')
  #Define the constraints
  model.Add(2*x + 7*y + 3*z <= 50)
  model.Add(3*x - 5*y + 7*z <= 45)
  model.Add(5*x + 2*y - 6*z <= 37)

  #Define the objective function
  model.Maximize(2*x + 2*y + 3*z)

  #Call the solver
  solver = cp_model.CpSolver()
  status = solver.Solve(model)

  if status == cp_model.OPTIMAL:
    print('Maximum of objective function: %i' % solver.ObjectiveValue())
    print()
    print('x value: ', solver.Value(x))
    print('y value: ', solver.Value(y))
    print('z value: ', solver.Value(z))


if __name__ == '__main__':
  main()