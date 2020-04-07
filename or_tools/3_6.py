#!/usr/bin/env python
# encoding: utf-8

"""
@author: leidelong
@contact: leidl8907@gmail.com
@time: 2020/4/6 17:06
"""

#N皇后问题

from __future__ import print_function
import sys
from ortools.sat.python import cp_model


def main(board_size):
  model = cp_model.CpModel()
  # Creates the variables.
  # The array index is the column, and the value is the row.
  # 1.直接内含了N个皇后在不同的列（queens的下标即列号）
  queens = [model.NewIntVar(0, board_size - 1, 'x%i' % i)
            for i in range(board_size)]
  print("queens : ",len(queens))
  # Creates the constraints.
  # The following sets the constraint that all queens are in different rows.
  # 2.明确限制行号不同
  model.AddAllDifferent(queens)

  # Note: all queens must be in different columns because the indices of queens are all different.

  # The following sets the constraint that no two queens can be on the same diagonal.
  for i in range(board_size):
    # Note: is not used in the inner loop.
    diag1 = []
    diag2 = []
    for j in range(board_size):
      # Create variable array for queens(j) + j.
      # a.取值
      q1 = model.NewIntVar(0, 2 * board_size, 'diag1_%i' % i)
      diag1.append(q1)
      # b.约束
      model.Add(q1 == queens[j] + j)
      # Create variable array for queens(j) - j.
      q2 = model.NewIntVar(-board_size, board_size, 'diag2_%i' % i)
      diag2.append(q2)
      # b.约束
      model.Add(q2 == queens[j] - j)

    #3.上升对角线不重合(c.约束)
    model.AddAllDifferent(diag1)
    #4.下降对角线不重合（c.约束）
    model.AddAllDifferent(diag2)
  ### Solve model.
  solver = cp_model.CpSolver()
  # solution_printer = SolutionPrinter(queens)
  solution_printer = DiagramPrinter(queens)
  status = solver.SearchForAllSolutions(model, solution_printer)
  print('Solutions found : %i' % solution_printer.SolutionCount())


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self, variables):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__variables = variables
    self.__solution_count = 0

  def OnSolutionCallback(self):
    self.__solution_count += 1
    for v in self.__variables:
      print('%s = %i' % (v, self.Value(v)), end = ' ')
    print()

  def SolutionCount(self):
    return self.__solution_count


class DiagramPrinter(cp_model.CpSolverSolutionCallback):
  def __init__(self, variables):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__variables = variables
    self.__solution_count = 0

  #Callback，存在一个解决方案时就会回调一次。
  def OnSolutionCallback(self):
    self.__solution_count += 1

    print("@@@")
    for v in self.__variables:
      queen_col = int(self.Value(v))
      board_size = len(self.__variables)
      # Print row with queen.
      for j in range(board_size):
        if j == queen_col:
          # There is a queen in column j, row i.
          print("Q", end=" ")
        else:
          print("_", end=" ")
      print()
    print()

  def SolutionCount(self):
    return self.__solution_count


if __name__ == '__main__':
  # By default, solve the 8x8 problem.
  board_size = 8
  if len(sys.argv) > 1:
    board_size = int(sys.argv[1])
  main(board_size)

