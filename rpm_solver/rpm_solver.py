from .node import Node
from .pattern import Pattern
from .transformation import Transformation
from .analogy import Analogy

class RPMSolver(object):

    def __init__(self):
        self.problem = None
        self.pattern_a = None
        self.pattern_b = None
        self.pattern_c = None
        self.transform_ab = None
        self.transform_ac = None
        self.analogy_ac = None
        self.options = []

    def reset(self):
        self.problem = None
        self.pattern_a = None
        self.pattern_b = None
        self.pattern_c = None
        self.transform_ab = None
        self.transform_ac = None
        self.analogy_ac = None
        self.options = []

    def solve_problem(self, problem):
        self.reset()
        self.problem = problem
        self.read_problem(problem)
        self.establish_transformations()
        self.draw_analogies()
        self.generate_solution()
        return -1

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
        self.options.append(self.generate_pattern(problem.figures['1']))
        self.options.append(self.generate_pattern(problem.figures['2']))
        self.options.append(self.generate_pattern(problem.figures['3']))
        self.options.append(self.generate_pattern(problem.figures['4']))
        self.options.append(self.generate_pattern(problem.figures['5']))
        self.options.append(self.generate_pattern(problem.figures['6']))

    def establish_transformations(self):
        self.transform_ab = self.pattern_a.transforms_to(self.pattern_b)
        self.transform_ac = self.pattern_a.transforms_to(self.pattern_c)

    def draw_analogies(self):
        self.analogy_ac = Analogy(self.pattern_a, self.pattern_c)

    def generate_solution(self):
        pass

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