"""
    rpm_solver.py

    1. Provides AgentType, which showcases the different solvers available.
    2. Defines RPMSolver, the facade for all solvers
"""

from .common.logger import log
from .visual.affine_analogy_network import AffineAnalogyNetwork

"""
    RPMSolver:

    The facade through which other solvers are invoked and put to work.
"""
class RPMSolver(object):

    def __init__(self):
        self.semantic_network = None
        self.solution_candidates = None

    def solve(self, problem):
        log("[RPMSolver/solve] Problem: " + problem.name)
        solution = -1
        if not problem.hasVisual or not problem.problemType == "2x2":
            log("[RPMSolver/solve] No visual representation. Giving up.")
        else:
            self.load_candidates(problem)
            print(self.solution_candidates)
            for solution_key, candidate in self.solution_candidates.iteritems():
                log("[RPMSolver/solve] Attempting solution: " + solution_key)
                self.load_network(problem)
                self.add_candidate(candidate, problem)
                self.semantic_network.establish_transformations()
                self.test_coherence(problem)
        log("[RPMSolver/solve] Solution key: " + str(solution))
        return solution

    def load_network(self, problem):
        log("[RPMSolver/load_network]")
        self.semantic_network = AffineAnalogyNetwork()
        self.load_figure(problem, 'A')
        self.load_figure(problem, 'B')
        self.load_figure(problem, 'C')
        if problem.problemType == "3x3":
            self.load_figure(problem, 'D')
            self.load_figure(problem, 'E')
            self.load_figure(problem, 'F')
            self.load_figure(problem, 'G')
            self.load_figure(problem, 'H')

    def load_candidates(self, problem):
        log("[RPMSolver/load_candidates]")
        self.solution_candidates = {}
        self.solution_candidates['1'] = problem.figures['1']
        self.solution_candidates['2'] = problem.figures['2']
        self.solution_candidates['3'] = problem.figures['3']
        self.solution_candidates['4'] = problem.figures['4']
        self.solution_candidates['5'] = problem.figures['5']
        self.solution_candidates['6'] = problem.figures['6']

    def add_candidate(self, candidate, problem):
        log("[RPMSolver/add_candidate]")
        candidate_label = "I"
        if problem.problemType == "2x2":
            candidate_label = 'D'
        self.semantic_network.construct_node(candidate, candidate_label)

    def test_coherence(self, problem):
        log("[RPMSolver/test_coherence]")
        number_of_nodes = len(self.semantic_network.nodes)
        if number_of_nodes == 4:
            pass
        else:
            pass

    def establish_transformations(self):
        log("[RPMSolver/establish_transformations]")


    def load_figure(self, problem, figure_label):
        log("[RPMSolver/load_figure] figure_label: " + figure_label)
        node_data = problem.figures[figure_label]
        self.semantic_network.construct_node(node_data, figure_label)

