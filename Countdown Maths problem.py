"""
Version where trees created by merge_trees are processed at every node rather
than just the root. bruteforce_solutions2 is 4x slower than bruteforce_solutions
when there are 4 numbers.


Test trees:
MathTree(['+', '2', '1'], sort=True, prefix=True)
MathTree(['+', '2', '*', '4', '3'], sort=True, prefix=True)
['*', '+', '9', '-', '1', '', '', '100', '10']
"""

import random, math, itertools, time, bisect
from os import system, name
import myTimerModule

TEST = False

TOTAL_NUMBERS = 6
SMALL_NUMBERS = sorted([x for x in range(1, 11)] * 2)
LARGE_NUMBERS = [25, 50, 75, 100]
OPERATORS = ('+', '-', '*', '/')
POWERS_OF_2 = [2 ** x for x in range(8)]


# ---------------
# Random Utility
# ---------------
def clear():
    """clear cmd output
    """
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


# ---------------
# Choose numbers
# ---------------
def choose_numbers():
    small_count = 0
    while small_count < 2:
        try:
            small_count = int(input('How many small numbers? (At least 2): '))
        except ValueError:
            print('Must be an integer, try again.', end='\r')
        #clear() # For clearing output when run in cmd
        
    large_count = TOTAL_NUMBERS - small_count
    
    numbers = []
    
    for _ in range(large_count):
        tmp = None
        while tmp is None:
            index = random.randint(0, len(LARGE_NUMBERS) - 1)
            tmp = LARGE_NUMBERS[index]
            LARGE_NUMBERS[index] = None
        numbers.append(tmp)
        
        
    for _ in range(small_count):
        tmp = None
        while tmp is None:
            index = random.randint(0, len(SMALL_NUMBERS) - 1)
            tmp = SMALL_NUMBERS[index]
            SMALL_NUMBERS[index] = None
        numbers.append(tmp)
        
    target_number = random.randint(100, 999)
    
    print(f'Target number: {target_number}')
    print(*numbers)
    return numbers, target_number

# ---------------
# Calculate numbers
# ---------------
class MathTree():

    @myTimerModule.timer_func    
    def __init__(self, expression, *, sort=True, tree=False, prefix=False, infix=False, postfix=False):
        """
        MathTree object attributes:
         - tree
         - working_tree
         - result
        """
        
        self.redundant = False
        
        if sum([tree, prefix, infix, postfix]) != 1:
            raise TypeError("MathTree requires one of the keyword arguments, tree, prefix, infix, postfix, to be True")
        
        if tree:
            self.tree = expression.copy()
            
        elif prefix:
            self.tree = []
            self.create_tree(expression)
            
        elif infix or postfix:
            raise ValueError("Input must be a binary tree or prefix expression.")
        
        # If the MathTree is a result of a merge between other trees, it should 
        #    be a valid, sorted tree.
        if not self.redundant:
            self.verify_tree()
            self.result = self.sum_tree()
            self.sort()
        else:
            self.result = None
        
    def __str__(self):
        return 'Redundant' if self.redundant else ''.join(self.extract_expression(infix=True))
    
    
    def __repr__(self):
        return 'Redundant' if self.redundant else ' '.join(self.extract_expression(prefix=True))
    
    
    def __eq__(self, tree):
        try:
            return self.tree == tree.tree
        except AttributeError:
            return False
    
    
    def __hash__(self):
        return tuple(self.tree).__hash__()
    
    def __setitem__(self, i, val):
        self.tree[i] = val
    
    def __getitem__(self, i):
        return self.tree[i]
    
    
    
    @myTimerModule.timer_func
    def create_tree(self, expression):
        """Iterative method for creating a tree from a prefix expression
        """
        notDone = True
        index = 0
        for i in expression:
            try:
                self.tree[index] = i
            except IndexError:
                self.tree.extend((index - len(self.tree) + 1) * [''])
                self.tree[index] = i
            if i in OPERATORS:
                index = 2 * index + 1
            else:
                
                if i == '1':
                    if self.tree[(index - 1) // 2] == '/':
                        self.redundant = True
                    elif self.tree[(index - 1) // 2] == '*':
                        self.redundant = True
                
                if index % 2 == 1:
                    index += 1
                else:
                    index = (index + 1) // 2
                    while self.tree[(index - 1) // 2] == '':
                        index = (index - 1) // 2
                
    @myTimerModule.timer_func
    def merge_trees(self, operator, tree):
        if self.result == '1' or tree.result == '1':
            if operator == '/':
                self.redundant = True
            elif operator == '*':
                self.redundant = True
                
        if self.redundant or tree.redundant:
            return None
        
        # Create first node of tree
        new_tree = [''] * 3
        
        new_tree[0] = operator
        new_tree[1] = str(self.result)
        new_tree[2] = str(tree.result)
        
        new_MathTree = MathTree(new_tree, tree=True)
        
        # Calculate overall length of new tree from old trees
        len_a, len_b = len(self.tree), len(tree.tree)
        i, j = (bisect.bisect_right(POWERS_OF_2, len_a) - 1,
                bisect.bisect_right(POWERS_OF_2, len_b) - 1)
        new_length = max(POWERS_OF_2[i] + len_a - 1, POWERS_OF_2[j + 1] + len_b - 1) + 1
        
        new_MathTree.tree += [''] * (new_length - 3)
        
        # Initialise parameters for copyinh functions
        tree_left = self.tree
        tree_right = tree.tree
        
        # copy_left and copy_right are called to copy the values from their old
        #    to their new position depending on which tree they belonged to.
        def copy_left(self, index, d):
            try:
                new_MathTree[2 ** d + index] = self[index]
            except IndexError:
                pass

        def copy_right(self, index, d):
            try:
                new_MathTree[2 ** (d + 1) + index] = tree[index]  
            except IndexError:
                pass      
            
        self.traverse_tree_top_down(func=copy_left)
        tree.traverse_tree_top_down(func=copy_right)
        
        return new_MathTree
        
    
    @myTimerModule.timer_func
    def verify_tree(self):
        """ 
        Verifies that a tree is a valid mathematical expression. Raises error
            on any cases that are not.
        """
        
        @myTimerModule.timer_func
        def verify_node(self, node):
            """
            The function that verifies one node and is passed to the tree 
                traversal funciton
            """
            
            @myTimerModule.timer_func
            def raise_error(self, problem_node):
                """
                Raises a TypeError on a node within a tree when called by verify_node.
                """
                raise TypeError(
                    f"Invalid input for MathTree: tree[{problem_node}] = '{self.tree[problem_node]}' ({type(self.tree[(problem_node - 1) // 2])})")
            
            child_a, child_b = 2 * node + 1, 2 * node + 2
            childAInList, childBInList = True, True
            
            if type(self.tree[node]) is str:
                # Check that the children of node either do not exist or are of
                #    type string
                try:
                    if not type(self.tree[child_a]) is str:
                        raise_error(child_a)
                except IndexError:
                    if self.tree[node] in OPERATORS:
                        raise_error(self, node)
                    childAInList = False
                try:
                    if not type(self.tree[child_b]) is str:
                        raise_error(self, child_b)
                except IndexError:
                    if self.tree[node] in OPERATORS:
                        raise_error(self, node)
                    childBInList = False
                
                # If the child addresses of the node are within the list
                if childAInList and childBInList:
                    if self.tree[node] in OPERATORS:
                        if not (self.tree[child_a].isdigit() 
                                or self.tree[child_a] in OPERATORS):
                            raise_error(self, child_a)
                        if not (self.tree[child_b].isdigit() 
                                or self.tree[child_b] in OPERATORS):
                            raise_error(self, child_b)
                        
                    elif self.tree[node].isdigit():
                        if not self.tree[child_a] == '':
                            raise_error(self, child_a)
                        if not self.tree[child_b] == '':
                            raise_error(self, child_b)
                        
                    else:
                        raise_error(self, node)
                elif childAInList or childBInList:
                    raise_error(self, node)
                    
                    
            else:
                raise_error(self, node)
                        
            
        self.recurse_tree(verify_node)

        
    @myTimerModule.timer_func
    def sort(self):
        
        @myTimerModule.timer_func
        def func(tree, parent):
            
            mutable_operators = ('+', '*')            
            
            @myTimerModule.timer_func
            def swap_branches(self, a, d=1):
                b = 2 ** (d - 1) + a
                tmp = len(self.tree)
                if tmp <= max(a, b):
                    n = (max(a, b) - len(self.tree) + 1) * ['']
                    self.tree.extend(n)
                    self.working_tree.extend(n)
                
                self.tree[a], self.tree[b] = self.tree[b], self.tree[a]
                (self.working_tree[a], 
                 self.working_tree[b]) = (self.working_tree[b],
                                          self.working_tree[a])
                
                
                if self.tree[a] in OPERATORS or self.tree[b] in OPERATORS:
                    swap_branches(self, 2 * a + 1, d + 1)
                    swap_branches(self, 2 * a + 2, d + 1)
                
            if self.tree[parent] in mutable_operators:
                
                a, b = 2 * parent + 1, 2 * parent + 2
                
                if (self.working_tree[a] is not None 
                    and self.working_tree[b] is not None):
                    if int(self.working_tree[a]) < int(self.working_tree[b]):
                        swap_branches(self, a)
                    elif self.working_tree[a] == self.working_tree[b]:
                        # Need to figure out a consistant method of sorting nodes
                        #    with equal value. What about edge cases with very 
                        #    similar nodes?
                        tmp_a, tmp_b = a, b
                        try:
                            while self.working_tree[tmp_a] == self.working_tree[tmp_b]:
                                child_a, child_b = 2 * tmp_a + 1, 2 * tmp_b + 1
                                if (not self.working_tree[child_a].isdigit()
                                    and self.working_tree[child_b].isdigit()):
                                    swap_branches(self, a)
                                    break
                                tmp_a, tmp_b = child_a, child_b
                        except IndexError:
                            pass
                        else:
                            if self.working_tree[tmp_b] > self.working_tree[tmp_a]:
                                swap_branches(self, a)
                
            return None
        
        self.recurse_tree(func)
        
        index = len(self.tree) - 1
        while self.tree[index] == '':
            index -= 1
            
        self.tree = self.tree[:index + 1]
        self.working_tree = self.working_tree[:index + 1]

        
    @myTimerModule.timer_func
    def recurse_prefix(self, sub_expression, func):
        """Recursively breaks down a prefix expression in more basic expressions
           to be evaluated.
        """
        # Return if all that is left is a single number
        if len(sub_expression) == 1:
            return sub_expression[0]
        else:
            # Find index of point between two operands in expression
            tmp1, tmp2 = 0, 0
            while tmp2 < 99: # Just in case, should be impossible
                if sub_expression[tmp2] in OPERATORS:
                    tmp1 += 1
                elif sub_expression[tmp2].isdigit():
                    tmp1 -= 1
                if tmp1 <= 0:
                    break
                tmp2 += 1
                
            index = tmp2 + 1
            
            # Recurse after dividing into operator, operand a and operand b
            operand_a = self.recurse_prefix(sub_expression[1:index], func)
            operand_b = self.recurse_prefix(sub_expression[index:], func)
            
            # Check if an input was erroneus
            if operand_a is '' or operand_b is '':
                return ''
            
            return func([sub_expression[0], 
                         operand_a,
                         operand_b])

        
    @myTimerModule.timer_func        
    def traverse_tree_bottom_up(self, func):
        """Function for iteratively traversing over the tree. Works bottom up
              (skipping leaves) and applies the given function to each node.
        """
        queue = []
        
        i = len(self.tree) - 1
        while self[i] is '':
            i -= 1
        
        while i >= 0:
            
            while self[i] == '':
                i -= 1    
                
            func(self, i)
            
            if self.redundant:
                return False
            
            i -= 1
            
        # ---------------------------------------
        
        #queue = [0]
        #stack = []
        
        #while queue:
            #i = queue.pop()
            
            #if self[i] in OPERATORS:
                #queue.extend([2 * i + 1, 2 * i + 2])
            
            #d = bisect.bisect_right(POWERS_OF_2, i + 1) - 1
            
            #stack.append(self[i])
            
            #if self.redundant:
                #return False
            
        #while stack:
            #func(self, stack.pop())
            
    @myTimerModule.timer_func        
    def traverse_tree_top_down(self, func):
        """Function for iteratively traversing over the tree. Works bottom up
              (skipping leaves) and applies the given function to each node.
        """
        queue = [0]
        
        while queue:
            i = queue.pop() 
            
            if self[i] in OPERATORS:
                queue.extend([2 * i + 1, 2 * i + 2])
            
            d = bisect.bisect_right(POWERS_OF_2, i + 1) - 1
            
            func(self, i, d)
            
            if self.redundant:
                return False
            
    
    @myTimerModule.timer_func        
    def recurse_tree(self, func, i=0):
        """Function for iteratively traversing over the tree. Works bottom up
              (skipping leaves) and applies the given function to each node.
        """
        if self[i].isdigit():
            func(self, i)
        else:
            self.recurse_tree(func, 2 * i + 1)
            self.recurse_tree(func, 2 * i + 2)
            func(self, i)            

            
    @myTimerModule.timer_func
    def sum_tree(self):
        
        self.working_tree = self.tree.copy()
        
        @myTimerModule.timer_func
        def evaluate_atom(self, parent):
            op = self.working_tree[parent]
            if op.isdigit():
                return True
            
            a, b = (int(self.working_tree[2 * parent + 1]),
                    int(self.working_tree[2 * parent + 2]))
            
            if op == '+':
                tmp = a + b
            elif op == '-':
                tmp = a - b
            elif op == '*':
                tmp = a * b
            elif op == '/':
                if a % b != 0:
                    self.working_tree[parent] = None
                    self.redundant = True
                    return False                
                tmp = int(a / b)
                    
            if tmp == 0:
                self.working_tree[parent] = None
                self.redundant = True
                return False
            
            self.working_tree[parent] = str(int(tmp))
                
            return True
        
        self.recurse_tree(evaluate_atom)
        
        if not self.redundant:
            return int(self.working_tree[0])
        else:
            return None
    

    @myTimerModule.timer_func    
    def extract_expression(self, *, prefix=False, infix=False, postfix=False, func=None):
        """list -> list
        """
        
        if not any([prefix, infix, postfix]) and func is None:
            infix = True
            
        
        expression = []
        processed = set()        
        
        funcProvided = True
        if func is None:
            def func(self, i, _):
                expression.append(self[i])
            funcProvided = False
                
        index, d = 0, 0
        while not(index <= 0 and 0 in processed):
            child1, child2, parent = 2 * index + 1, 2 * index + 2, (index - 1) // 2
            
            # self.tree[index] is a leaf node
            if child1 >= len(self.tree) or (self.tree[child1] == '' and not funcProvided):
                
                func(self, index, d)
                
                if infix and 2 * parent + 1 in processed:
                    expression.append(')')
                
                processed.add(index)   
                
                index = parent
                d -= 1
            
            # self.tree[index] isn't a leaf node
            else:
                if child1 not in processed:
                    if infix:
                        expression.append('(')
                    if prefix:
                        func(self, index, d)
                    
                    index = child1
                    d += 1
                    
                elif child2 not in processed:
                    if infix:
                        func(self, index, d)
                    
                    index = child2
                    d += 1
                    
                else: 
                    
                    if postfix or funcProvided:
                        func(self, index, d)
                    if infix and 2 * parent + 1 in processed:
                        expression.append(')')
                    
                    processed.add(index)
                    
                    index = parent
                    d -= 1

        return expression


class EquationGenerator():
    
    def __init__(self, numbers):
        """
        Attributes:
         - numbers
         - structure
        """
        
        self.numbers = numbers
        self.generate_structure()
        
    @myTimerModule.timer_func
    def generate_structure(self):
        """
        self.structure = {
            (operands): ({combinations of n-1 operands}, {result: {expressions, ...}}),
            tuple(str(), ...): tuple(set(tuple(), ...), dict(int(): set(MathTree(), ...))),
            ('1,'): ({set()}, {1: 1}),
            ...
        }
        """
        
        structure = {tuple(): (set(), {})}
        
        def recurse(group, options):
            if len(group) == len(options):
                return None
            
            for option in options:
                if option not in group:
                    new_group = tuple(sorted(list(group) + [option], key=int))
                    
                    structure[new_group] = structure.get(new_group, (set(), {}))
                    structure[group][0].add(new_group)
                    recurse(new_group, options)
        
        recurse(tuple(), self.numbers)
        
        
        
        for number_set in structure[tuple()][0]:
            structure[number_set][1][int(number_set[0])] = set([MathTree(list(number_set), prefix=True)])
        
        self.structure = structure
    

    def find_combinations(self, operands, i):
        queue = []
        tmp = []
        j = 0
        k = 1
        while len(queue) < (math.factorial(len(operands)) 
                            / (math.factorial(i) * math.factorial(len(operands) - i))):
            while len(tmp) < i:
                tmp.append(operands[j])
                j += 1
            queue.append(tmp.copy())
            tmp.pop()
            if j > len(operands) - 1:
                tmp.pop()
                j -= len(operands) - i + k
                k -= 1
        return queue

    @myTimerModule.timer_func    
    def generate_expressions(self):
        
        def add_components(self, branch1, branch2):
            viable_trees = []
            for operator in OPERATORS:            
                tree = branch1.merge_trees(operator, branch2)     
                if not tree.redundant and tree.result > 0:
                    viable_trees.append(tree)
                
            return viable_trees
                
        
        queue = [tuple([n]) for n in self.numbers]
        
        while queue != []:
            operands = queue.pop(0)
            queue.extend(self.structure[operands][0])
            n = len(operands) - 1
            m = n // 2
            
            # Find all ways of choose between n and m numbers from operands
            for i in range(n, m, -1):
                components = itertools.combinations(operands, i)
                
                for component in components:
                    complement = tuple(sorted(list(set(operands).difference(set(component))), key=int))
                   
                    # Iterate results found with numbers in components
                    for i in self.structure[component][1]:
                        
                        # Iterate results found with numbers in complement
                        for j in self.structure[complement][1]:
                            
                            # Iterate expressions that give results in component
                            for x in self.structure[component][1][i]:
                                
                                # Iterate expressions that give results in complement
                                for y in self.structure[complement][1][j]:
                                    # Make sure that expressions are accurately assigned results
                                    #assert i == x.result and j == y.result
                                    
                                    if i > j:
                                        viable_trees = add_components(self, x, y)
                                    elif j > i:
                                        viable_trees = add_components(self, y, x)
                                    else:
                                        viable_trees = add_components(self, x, y)
                                    
                                    for new_tree in viable_trees:
                                        self.structure[operands][1][new_tree.result] = self.structure[operands][1].get(new_tree.result, set())
                                        self.structure[operands][1][new_tree.result].add(new_tree)
# ------------------------------
# Functions
# ------------------------------

@myTimerModule.timer_func
def bruteforce_solutions(numbers, n=None):
    """list, int -> dict
       Using a recursion tree, bruteforce all possible workings using the given
          numbers, then evaluate and store their results.
    """
    results_dict = {}#{key: None for key in range(100, 1000)}
    if n is None:
        n = 2 * len(numbers) - 1
    operator_limit = len(numbers) - 1
    operand_limit = len(numbers)
    buffer_length = (len(numbers) + len(OPERATORS)) * len(OPERATORS)
    buffer_progress = [0]
    
    def recurse(expression, operator_count, operand_count, options, max_length=n):
        # Catch final recursion. A finished expression always ends with None.
        if len(expression) > 0 and expression[-1] is None:
            expression = MathTree(expression[:-1], sort=True, prefix=True)
            result = expression.result
            if not result is None and not expression.redundant and result >= 0:
                if result not in results_dict.keys():
                    results_dict[result] = []
                    
                if expression not in results_dict[result]:
                    results_dict[result] += [expression]
        
        # Continue recursion
        else:
            # If it gives a proper expression, terminate
            if operand_count - 1 == operator_count:
                recurse(expression + [None], operator_count, 
                        operand_count, options)
            else:
                for i in options:
                    if len(expression) == 1:
                        buffer_progress[0] += 1
                        #print(f'|{"."*buffer_progress[0]}{" "*(buffer_length - buffer_progress[0])}|')
                        
                    # If it is an operator, check it is within limits
                    if i in OPERATORS:
                        if operator_count < operator_limit:
                            recurse(expression + [i], operator_count + 1, 
                                    operand_count, options)
                        
                    # Check the number of operands is within limits before 
                    #    adding one.
                    elif (operand_count < 2 * operator_count 
                          and operand_count < operand_limit):
                        # Is this a leaf node with a sibling?
                        if (len(expression) > 2 
                            and expression[-1].isdigit()):
                            # Ensure the subtraction doesn't give a negative number
                            if (expression[-2] == '-' 
                                and int(i) > int(expression[-1])):
                                return None
                            # Ensure a division gives a whole number
                            if (expression[-2] == '/' 
                                and (int(expression[-1])) % int(i) != 0
                                     or int(expression[-1]) / int(i) == 0):
                                return None                        
                        options_tmp = options.copy()
                        options_tmp.remove(i)
                        recurse(expression + [i], operator_count, 
                                operand_count + 1, options_tmp)
    
    # Run bruteforce recursion to find all operations using the given numbers
    options = [str(x) for x in numbers]
    options.extend(OPERATORS)
    recurse([], 0, 0, options)
    return results_dict
        

@myTimerModule.timer_func
def bruteforce_solutions2(numbers):
    generator = EquationGenerator([str(x) for x in numbers])
    generator.generate_expressions()
    values = {}
    for i in generator.structure.values():
        i = i[1]
        for j in i:
            values[j] = values.get(j, []) + list(i[j])
    #for value in values:
        #print(value)
        #for expression in values[value]:
            #print(expression)
    return values


@myTimerModule.timer_func
def print_closest_answers(results_dict, target):
    """Find and print the result closest to the target, and all workings for
          this number. For ties, the first encountered is selected.
    """
    results = results_dict.keys()
    closest_results = [list(results)[0]]
    for result in results:
        if abs(target - closest_results[0]) > abs(target - result):
            closest_results = [result]
        if (abs(target - closest_results[0]) == abs(target - result)
            and closest_results[0] != result):
            closest_results.append(result)
    for result in closest_results:
        print(f'\t{result}')
        [print(' '.join(x.extract_expression(prefix=True)),'\t', ''.join(x.extract_expression(infix=True))) for x in results_dict[result]]


def test_infix_utilities():

    tests = {
        1: (list('+54'), 9),
        2: (list('*+546'), 54),
        3: (list('-/63*22'), -2)
    }
    
    for t in tests.values():
        result = int(recurse_prefix(t[0], evaluate_infix))
        infix = ''.join(extract_expression(t[0][1:-1], infix=True))
        print(infix, '=', result, result == t[1])
        
        
def main():
    if TEST:
        pass#test_infix_utilities()
    
    numbers, target_number = [2, 3], 10
    results_dict = {}
    quit = False
    while not quit:
        numbers, target_number = [100, 1, 9, 10], 364#[100, 25, 8, 1, 9, 10], 364#choose_numbers()
    
        results_dict = bruteforce_solutions(numbers)
        if TEST:
            [print(x) for x in results_dict.items()]
            
        print_closest_answers(results_dict, target_number)
        print(f'\n{len(results_dict.keys())} distinct numbers found.')
        tmp = 0
        for num in range(100, 1000):
            if results_dict.get(num, None) is None:
                tmp += 1
        print(f'{tmp} numbers between 100 and 999 (inclusive) were unable to be found.')
        
        
        tmp = input('Restart? [y/n]: ')
        quit = None
        while quit is None:
            if tmp.lower() == 'n':
                quit = True
            elif tmp.lower() == 'y':
                quit = False
            else:
                tmp = input('What was that? [y/n]: ')
                
    return results_dict
    

if __name__ == '__main__':
    #a = main()

    #dict_a = bruteforce_solutions([100, 1, 9, 10])
    #print(sorted(list(dict_a.keys())))
         
    dict_b = bruteforce_solutions2([100, 1, 9, 10])
    print(sorted(list(dict_b.keys())))
    
    myTimerModule.print_results()
    
    #a = MathTree(['+', '2', '1'], sort=True, prefix=True)
    #b = MathTree(['+', '2', '*', '4', '3'], sort=True, prefix=True)
    #print(a, a.result, b, b.result)
    #c = a.merge_trees('+', b)
    #d = b.merge_trees('+', a)  
    #print()
    #print(c, c.result, d, d.result)