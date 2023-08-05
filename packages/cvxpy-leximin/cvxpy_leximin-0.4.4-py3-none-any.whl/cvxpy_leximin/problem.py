"""
Extend cvxpy.Problem by adding support to the Leximin and Leximax objectives.

EXAMPLE 1:  leximin resource allocation. There are four resources to allocate among two people.
Alice values the resources at 5, 3, 0, 0.
George values the resources at 2, 4, 9, 0.
The variables a[0], a[1], a[2], a[3] denote the fraction of each resource given to Alice.
>>> a = cvxpy.Variable(4)
>>> feasible_allocation = [x>=0 for x in a] + [x<=1 for x in a]

>>> utility_Alice = a[0]*5 + a[1]*3 + a[2]*0
>>> utility_George   = (1-a[0])*2 + (1-a[1])*4 + (1-a[2])*9
>>> objective = Leximin([utility_Alice, utility_George])
>>> problem = Problem(objective, constraints=feasible_allocation)
>>> problem.solve()
[8.0, 9.0]
>>> round(utility_Alice.value), round(utility_George.value)
(8, 9)
>>> [round(x.value) for x in a]  # Alice gets all of resources 0 and 1; George gets all of resources 2 and 3.
[1, 1, 0, 0]

EXAMPLE 2: leximax chores allocation. There are four chores to allocate among two people.
>>> utility_Alice = a[0]*5 + a[1]*2 + a[2]*0
>>> utility_George   = (1-a[0])*2 + (1-a[1])*4 + (1-a[2])*9
>>> objective = Leximax([utility_Alice, utility_George])
>>> problem = Problem(objective, constraints=feasible_allocation)
>>> problem.solve()
[2.0, 2.0]
>>> round(utility_Alice.value), round(utility_George.value)
(2, 2)
>>> [round(x.value) for x in a]  # Alice gets all of resources 0 and 1; George gets all of resources 2 and 3.
[0, 1, 1, 0]

Author: Erel Segal-Halevi
Since: 2022-02
"""

import logging
from typing import List, Optional, Union

import cvxpy
from cvxpy import Maximize, Minimize, error, Problem
from cvxpy.constraints.constraint import Constraint
from cvxpy.interface.matrix_utilities import scalar_value
from cvxpy.problems.problem import SizeMetrics, SolverStats

from cvxpy_leximin.objective import Leximax, Leximin
from copy import deepcopy

LOGGER = logging.getLogger("__cvxpy_leximin__")


def __new__init(self,
    objective: Union[Minimize, Maximize, Leximin, Leximax],
    constraints: Optional[List[Constraint]] = None,
    upper_tolerance: float = 1.01,  # for comparing floating-point numbers
    lower_tolerance: float = 0.999,
) -> None:
    if constraints is None:
        constraints = []
    # Check that objective is Minimize or Maximize.
    if not isinstance(objective, (Minimize, Maximize, Leximin, Leximax)):
        raise error.DCPError("Problem objective must be Minimize, Maximize, Leximin or Leximax.")
    # Constraints and objective are immutable.
    self._objective = objective
    self._constraints = [
        cvxpy.problems.problem._validate_constraint(c) for c in constraints
    ]

    self._value = None
    self._status: Optional[str] = None
    self._solution = None
    self._cache = cvxpy.problems.problem.Cache()
    self._solver_cache = {}
    # Information about the shape of the problem and its constituent parts
    self._size_metrics: Optional["SizeMetrics"] = None
    # Benchmarks reported by the solver:
    self._solver_stats: Optional["SolverStats"] = None
    self._compilation_time: Optional[float] = None
    self._solve_time: Optional[float] = None
    self.args = [self._objective, self._constraints]
    self.upper_tolerance = upper_tolerance
    self.lower_tolerance = lower_tolerance


Problem.__init__ = __new__init


def __new__value(self):
    """float : The value/s from the last time the problem was solved."""
    if self._value is None:
        return None
    elif isinstance(self._value, list):
        return [scalar_value(v) for v in self._value]
    else:
        return scalar_value(self._value)


Problem.value = property(__new__value)


def _solve_sub_problem(self, sub_problem: cvxpy.Problem, *args, **kwargs):
    kwargs = deepcopy(kwargs)  # cvxpy.Problem.solve might modify kwargs.
    sub_problem.solve(*args, **kwargs)
    if sub_problem.status == "infeasible":
        self._status = sub_problem.status
        LOGGER.warning("Sub-problem is infeasible")
        return False
    elif sub_problem.status == "unbounded":
        self._status = sub_problem.status
        LOGGER.warning("Sub-problem is unbounded")
        return False
    else:
        return True


Problem._solve_sub_problem = _solve_sub_problem


def _solve_leximin(self, *args, **kwargs):
    """
    Find a leximin-optimal vector of utilities, subject to the given constraints.

    The algorithm is based on:
    > [Stephen J. Willson](https://faculty.sites.iastate.edu/swillson/),
    > "Fair Division Using Linear Programming" (1998).
    > Part 6, pages 20--27.

    I am grateful to Sylvain Bouveret for his help with the algorithm. All remaining errors and bugs are my own.
    """
    if type(self.objective) == Leximax:
        sub_objectives = [-arg for arg in self.objective.args]
    else:  # Leximin
        sub_objectives = self.objective.args

    constraints = self.constraints
    num_of_objectives = len(sub_objectives)

    # During the algorithm, the objectives are partitioned into "free" and "saturated".
    # * "free" objectives are those that can potentially be made higher, without harming the smaller objectives.
    # * "saturated" objectives are those that have already attained their highest possible value in the leximin solution.
    # Initially, all objectives are free, and no objective is saturated:
    free_objectives = list(range(num_of_objectives))
    map_saturated_objective_to_saturated_value = num_of_objectives * [None]

    while True:
        LOGGER.info("Saturated values: %s.",map_saturated_objective_to_saturated_value)
        minimum_value_for_free_objectives = cvxpy.Variable()
        inequalities_for_free_objectives = [
            sub_objectives[i] >= minimum_value_for_free_objectives
            for i in free_objectives
        ]
        inequalities_for_saturated_objectives = [
            (sub_objectives[i] >= value)
            for i, value in enumerate(map_saturated_objective_to_saturated_value)
            if value is not None
        ]

        sub_problem = cvxpy.Problem(
            objective=cvxpy.Maximize(minimum_value_for_free_objectives),
            constraints=constraints + inequalities_for_saturated_objectives + inequalities_for_free_objectives,
        )
        if not self._solve_sub_problem(sub_problem, *args, **kwargs):
            return

        max_min_value_for_free_objectives = minimum_value_for_free_objectives.value.item()
        values_in_max_min_allocation = [objective.value for objective in sub_objectives]
        LOGGER.info("  max min value: %g, value-profile: %s", max_min_value_for_free_objectives, values_in_max_min_allocation)
        max_min_value_upper_threshold = (
            self.upper_tolerance * max_min_value_for_free_objectives
            if max_min_value_for_free_objectives > 0
            else (2 - self.upper_tolerance) * max_min_value_for_free_objectives
        )
        max_min_value_lower_threshold = (
            self.lower_tolerance * max_min_value_for_free_objectives
            if max_min_value_for_free_objectives > 0
            else (2 - self.lower_tolerance) * max_min_value_for_free_objectives
        )

        for ifree in free_objectives:  # Find whether i's value can be improved
            if (values_in_max_min_allocation[ifree] > max_min_value_upper_threshold):
                LOGGER.info("  Max value of objective #%d is %g, which is above %g, so objective remains free.", ifree, values_in_max_min_allocation[ifree], max_min_value_upper_threshold)
                continue
            inequalities_for_other_free_objectives = [
                sub_objectives[i] >= max_min_value_lower_threshold
                for i in free_objectives
                if i != ifree
            ]
            sub_problem_for_ifree = cvxpy.Problem(
                objective=cvxpy.Maximize(sub_objectives[ifree]),
                constraints=constraints + inequalities_for_saturated_objectives + inequalities_for_other_free_objectives,
            )
            if not self._solve_sub_problem(sub_problem_for_ifree, *args, **kwargs):
                return
            max_value_for_ifree = sub_objectives[ifree].value.item()

            if max_value_for_ifree > max_min_value_upper_threshold:
                LOGGER.info("  Max value of objective #%d is %g, which is above %g, so objective remains free.", ifree, max_value_for_ifree, max_min_value_upper_threshold)
                continue
            else:
                LOGGER.info("  Max value of objective #%d is %g, which is below %g, so objective becomes saturated.", ifree, max_value_for_ifree, max_min_value_upper_threshold)
                map_saturated_objective_to_saturated_value[ifree] = max_min_value_for_free_objectives

        new_free_agents = [
            i for i in free_objectives
            if map_saturated_objective_to_saturated_value[i] is None
        ]
        if len(new_free_agents) == len(free_objectives):
            raise ValueError("No new saturated objectives - this contradicts Willson's theorem! Are you sure the domain is convex?")
        elif len(new_free_agents) == 0:
            LOGGER.info("All objectives are saturated -- values are %s.", map_saturated_objective_to_saturated_value)
            if not self._solve_sub_problem(sub_problem, *args, **kwargs):
                return
            LOGGER.info("Final objective values: %s", [o.value for o in sub_objectives])

            self._status = sub_problem.status
            self._solution = sub_problem.solution

            if type(self.objective) == Leximax:
                for i in range(num_of_objectives):
                    self.objective.args[i] = -sub_objectives[i]
            self._value = self.objective.value
            return self.value

        else:
            free_objectives = new_free_agents
            continue


Problem._solve_leximin = _solve_leximin


def __new__solve(self, *args, **kwargs):
    if type(self.objective) == Leximin or type(self.objective) == Leximax:
        return self._solve_leximin(*args, **kwargs)
    else:  # Copied from cvxpy.problems.problem.Problem.solve
        func_name = kwargs.pop("method", None)
        if func_name is not None:
            solve_func = Problem.REGISTERED_SOLVE_METHODS[func_name]
        else:
            solve_func = Problem._solve
        return solve_func(self, *args, **kwargs)


Problem.solve = __new__solve

if __name__ == "__main__":
    LOGGER.addHandler(logging.StreamHandler())
    LOGGER.setLevel(logging.INFO)

    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
