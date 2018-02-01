from .node import Node
from .pattern import Pattern
from .transformation import Transformation

class RPMSolver(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.problem = None
        self.pattern_a = None
        self.pattern_b = None
        self.pattern_c = None
        self.options = []

    def solve_problem(self, problem):
        self.reset()
        self.problem = problem
        self.read_problem(problem)
        self.establish_transformations()
        return -1

    def read_problem(self, problem):
        self.extract_patterns(problem)
        self.extract_options(problem)

    def generate_pattern(self, figure):
        pattern = Pattern()
        for node_name, node_object in figure.objects.items():
            pattern.add_node(Node(node_name, node_object.attributes))
        return pattern

    def extract_problems2x2(self, problem):
        self.pattern_a = self.generate_pattern(problem.figures['A'])
        self.pattern_b = self.generate_pattern(problem.figures['B'])
        self.pattern_c = self.generate_pattern(problem.figures['C'])

    def extract_problems3x3(self, problem):
        self.extract_problems2x2(problem)

    def extract_patterns(self, problem):
        if problem.problemType == "2x2" and problem.hasVerbal:
            return self.extract_problems2x2(problem)
        elif problem.problemType == "3x3" and problem.hasVerbal:
            return self.extract_problems3x3(problem)
        else:
            pass

    def extract_options(self, problem):
        self.options.append(self.generate_pattern(problem.figures['1']))
        self.options.append(self.generate_pattern(problem.figures['2']))
        self.options.append(self.generate_pattern(problem.figures['3']))
        self.options.append(self.generate_pattern(problem.figures['4']))
        self.options.append(self.generate_pattern(problem.figures['5']))
        self.options.append(self.generate_pattern(problem.figures['6']))

    def establish_transformations2x2(self):
        self.transform_ab = self.pattern_a.transforms_to(self.pattern_b)
        self.transform_ac = self.pattern_a.transforms_to(self.pattern_c)

    def establish_transformations3x3(self):
        pass

    def establish_transformations(self):
        if self.problem.problemType == "2x2":
            self.establish_transformations2x2()
        elif self.problem.problemType == "3x3":
            self.establish_transformations3x3()
        else:
            pass


    def log_problem(self, problem):
        print problem.problemType
        print problem.problemSetName
        print problem.figures