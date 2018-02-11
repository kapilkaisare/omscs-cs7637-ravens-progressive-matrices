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
        self.draw_analogies()
        self.generate_solution()
        return self.solution_validity()
        # return -1

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
        self.transform_ab = self.pattern_a.transforms_to(self.pattern_b)
        self.transform_ac = self.pattern_a.transforms_to(self.pattern_c)

    def draw_analogies(self):
        self.analogy_ac = Analogy(self.pattern_a, self.pattern_c)

    def generate_solution(self):
        print "---"
        print self.problem.name
        self.solution_pattern = Pattern()
        for node_name, node in self.pattern_c.nodes.items():
            analogue = self.analogy_ac.get_analogue_for(node)
            if not analogue:
                print "analogue not found. boo hoo"
                break
            changes = self.transform_ab.nodes_changed[analogue]
            solution_node = Node(node.name, {})
            solution_node.attributes = node.apply_changes(changes)
            self.solution_pattern.add_node(solution_node)

    def solution_validity(self):
        for solution_index, solution_option in self.options.items():
            test_transformation = self.solution_pattern.transforms_to(solution_option)
            if not test_transformation.changes_observed():
                print "Solution found: " + solution_index
                return int(solution_index)
            else:
                print "option: " + solution_index
                test_transformation.log_changes()
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