"""
    rpm_solver.py

    1. Provides AgentType, which showcases the different solvers available.
    2. Defines RPMSolver, the facade for all solvers
"""

from .verbal.semantic_networks.semantic_network_solver import SNSolver

"""
    AgentType

    At the time of this writing, only SIMONE is planned.
"""
class AgentType(object):
    SIMONE = 1  # Uses simple semantic networks


"""
    NoAgentException, for when no agent is provided.
"""
class NoAgentException(Exception):
    pass


"""
    RPMSolver:

    The facade through which other solvers are invoked and put to work.
"""
class RPMSolver(object):

    def __init__(self, agent_type):
        self.agent = None
        if agent_type == AgentType.SIMONE:
            self.agent = SNSolver()
        else:
            raise NoAgentException()

    def solve(self, problem):
        return self.agent.solve(problem)