from .node import Node
from .pattern import Pattern
from .analogy import PatternAnalogy
from .transform import PatternTransform
import sys

class RPMSolver(object):

    def __init__(self):
        self.problem = None
        self.pattern_a = None
        self.pattern_b = None
        self.pattern_c = None
        self.transform_ab = None
        self.transform_ac = None
        self.analogy_ac = None
        self.solution_pattern = None
        self.options = {}

    def reset(self):
        self.problem = None
        self.pattern_a = None
        self.pattern_b = None
        self.pattern_c = None
        self.transform_ab = None
        self.transform_ac = None
        self.analogy_ac = None
        self.solution_pattern = None
        self.options = {}

    def solve_problem(self, problem):
        self.reset()
        self.problem = problem
        self.read_problem(problem)
        self.establish_transformations()
        return self.generate_solution()

    def read_problem(self, problem):
        self.extract_patterns(problem)
        self.extract_options(problem)

    def generate_pattern(self, figure):
        pattern = Pattern()
        for node_name, node_object in figure.objects.items():
            pattern.add_node(Node(node_name, node_object.attributes))
        return pattern

    def extract_problems(self, problem):
        self.pattern_a = self.generate_pattern(problem.figures['A'])
        self.pattern_b = self.generate_pattern(problem.figures['B'])
        self.pattern_c = self.generate_pattern(problem.figures['C'])

    def extract_patterns(self, problem):
        self.extract_problems(problem)
        self.extract_options(problem)

    def extract_options(self, problem):
        self.options['1'] = self.generate_pattern(problem.figures['1'])
        self.options['2'] = self.generate_pattern(problem.figures['2'])
        self.options['3'] = self.generate_pattern(problem.figures['3'])
        self.options['4'] = self.generate_pattern(problem.figures['4'])
        self.options['5'] = self.generate_pattern(problem.figures['5'])
        self.options['6'] = self.generate_pattern(problem.figures['6'])

    def establish_transformations(self):
        self.transform_ab = PatternTransform(self.pattern_a, self.pattern_b)

    def generate_solution(self):
        for solution_index, solution_option in self.options.items():
            test_transform = PatternTransform(self.pattern_c, solution_option)
            if test_transform == self.transform_ab:
                print "Solution found for problem " + self.problem.name + " : " + solution_index
                return int(solution_index)
        return -1

    def log(self):
        self.log_problem(self.problem)
        print self.pattern_a
        print self.pattern_b
        print self.pattern_c


    def log_problem(self, problem):
        print problem.problemType
        print problem.problemSetName
        print problem.figures
        print problem.hasVerbal