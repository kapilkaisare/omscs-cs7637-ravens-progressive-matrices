"""
    rpm_solver.py

    1. Provides AgentType, which showcases the different solvers available.
    2. Defines RPMSolver, the facade for all solvers
"""
from operator import itemgetter
from .common.logger import log
from .visual.image_analogy_network_2x2 import ImageAnalogyNetwork2x2
from .visual.transformation.transform import Transform
from .visual.transformation.image_operations import ImageOperations
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
        expected_solution = None
        if not problem.hasVisual or problem.problemType == "3x3":
            log("[RPMSolver/solve] No visual representation. Giving up.")
        else:
            candidate_matches = []
            self.load_candidates(problem)
            self.load_network(problem)
            self.semantic_network.establish_transformations()

            transforms = self.semantic_network.get_transforms()
            for transform in transforms:
                expected_solution = self.apply_transform(transform)
                for key, candidate in self.solution_candidates.iteritems():
                    candidate_image = ImageOperations.load_from_ravens_figure(candidate)
                    candidate_matches.append((key, ImageOperations.minus(candidate_image, expected_solution)))

            candidate_matches.sort(key=lambda tup: tup[1])
            if len(candidate_matches) > 0:
                candidate_solution = candidate_matches[0]
                expected_solution.save("/home/kapilkaisare/Projects/src/github.com/kapilkaisare/omscs-cs7637-ravens-progressive-matrices/output/" + problem.name + ".png")
                solution = int(candidate_solution[0])
        print("[RPMSolver/solve] Solution key for " + problem.name + " : " + str(solution))
        return solution

    def load_network(self, problem):
        log("[RPMSolver/load_network]")
        if problem.problemType == "2x2":
            self.semantic_network = ImageAnalogyNetwork2x2()
            self.load_figure(problem, 'A')
            self.load_figure(problem, 'B')
            self.load_figure(problem, 'C')

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

    def apply_transform(self, transform):
        log("[RPMSolver/apply_transform] " + str(transform))
        node_count = len(self.semantic_network.nodes)
        if transform[0] == 'vertical' and node_count == 3:
            return self.apply_transform_to('B', transform)
        elif transform[0] == 'horizontal' and node_count == 3:
            return self.apply_transform_to('C', transform)
        else:
            return None

    def apply_transform_to(self, node_key, transform):
        log("[RPMSolver/apply_transform_to] Transform: " + str(transform) + "   Key: " + node_key)
        image = self.semantic_network.nodes.data[node_key].image
        return Transform.apply_transform(transform[1], image)

    def establish_transformations(self):
        log("[RPMSolver/establish_transformations]")


    def load_figure(self, problem, figure_label):
        log("[RPMSolver/load_figure] figure_label: " + figure_label)
        node_data = problem.figures[figure_label]
        self.semantic_network.construct_node(node_data, figure_label)

