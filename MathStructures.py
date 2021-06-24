import myTimerModule

OPERATORS = ['+', '-', '*', '/']
TEST = False

class MathTree():

    @myTimerModule.timer_func    
    def __init__(self, expression, *, sort=True, tree=False, prefix=False, infix=False, postfix=False, fromMerge=False):
        """
        MathTree object attributes:
         - tree
         - working_tree
         - result
         - redundant
        """
        
        self.redundant = False
        
        if sum([tree, prefix, infix, postfix]) != 1:
            raise TypeError("MathTree requires (only) one of the keyword arguments, tree, prefix, infix, postfix, to be True")
        
        if tree:
            self.tree = expression.copy()
            
        elif prefix:
            self.tree = []
            self.create_tree(expression)
            
        elif infix or postfix:
            raise ValueError("Input must be a binary tree or prefix expression.")
        
        # If the MathTree is a result of a merge between other trees, it should 
        #    be a valid, sorted tree.\
        if not self.redundant:
            if fromMerge:
                self.result = self.process_tree()
            else:
                self.result = self.process_tree(recurse=True)
        else:
            self.result = None
        

    # --------------------------------------------------------
    #    Built-in Tree Functions
    # --------------------------------------------------------    
        
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
    
    
    # --------------------------------------------------------
    #    Tree Creation Functions
    # --------------------------------------------------------    
    
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
        
        new_MathTree = MathTree(new_tree, tree=True, fromMerge=True)
        
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
            
        self.iterate_tree_top_down(func=copy_left)
        tree.iterate_tree_top_down(func=copy_right)
        
        return new_MathTree
        
   
    # --------------------------------------------------------
    #    Tree Processing Functions
    # --------------------------------------------------------        
    
    @myTimerModule.timer_func
    def process_tree(self, *, recurse=False):
        """
        Simultaneously verify, evaluate and sort the tree using a single tree
            traversal.
        """
        self.working_tree = self.tree.copy()
        
        if TEST or recurse:
            f_list = [self.verify_node, self.evaluate_atom, self.sort_node]
        else:
            f_list = [self.evaluate_atom, self.sort_node]
        
        if recurse:
            self.recurse_tree_bottom_up(f_list)
        else:
            for f in f_list:
                f(0)
        
        if not self.redundant:
            return int(self.working_tree[0])
        else:
            return None
     
     
    @myTimerModule.timer_func
    def verify_node(self, node):
        """
        The function that verifies one node is a valid mathematical expression
            and is passed to the tree traversal funciton
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

        
    @myTimerModule.timer_func
    def sort_node(self, parent):
        
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
    
                
    @myTimerModule.timer_func
    def evaluate_atom(self, parent):
        op = self.working_tree[parent]
        if op.isdigit():
            return True
        
        a, b = (self.working_tree[2 * parent + 1],
                self.working_tree[2 * parent + 2])
        
        try:
            a, b = int(a), int(b)
        except TypeError:
            self.working_tree[parent] = None
            self.redundant = True
            return False
        
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
    
    
    # --------------------------------------------------------
    #    Tree Traversal Functions
    # --------------------------------------------------------
        
    @myTimerModule.timer_func        
    def iterate_tree_bottom_up(self, func):
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

            
    @myTimerModule.timer_func        
    def iterate_tree_top_down(self, func):
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
    def recurse_tree_bottom_up(self, *funcs, i=0):
        """Function for iteratively traversing over the tree. Works bottom up
              (skipping leaves) and applies the given function to each node.
        """
        if self.redundant:
            return None
        elif self[i].isdigit():
            for f in funcs[0]:
                f(i)
        else:
            self.recurse_tree_bottom_up(*funcs, i=2 * i + 1)
            self.recurse_tree_bottom_up(*funcs, i=2 * i + 2)
            for f in funcs[0]:
                f(i)            
    

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



class MathList(list):
    
    @myTimerModule.timer_func   
    def __init__(self, expression, result):
        super().__init__(expression)
        
        if type(result) is int:
            self.result = result
        else:
            raise TypeError("The result of a MathList is an int")
        
        
    @myTimerModule.timer_func   
    def __add__(self, other_expression):
        new_expression = ['+'] + self + other_expression
        
        assert self.result >= other_expression.result
        new_result = self.result + other_expression.result
        
        return MathList(new_expression, new_result)
    
    
    @myTimerModule.timer_func   
    def __sub__(self, other_expression):
        new_expression = ['-'] + self + other_expression
        
        if self.result == other_expression.result:
            return None       
        
        assert self.result >= other_expression.result
        new_result = self.result - other_expression.result
        
        return MathList(new_expression, new_result)
    
    
    @myTimerModule.timer_func   
    def __mul__(self, other_expression):
        new_expression = ['*'] + self + other_expression
        
        if self.result == 1 or other_expression.result == 1:
            return None
        
        assert self.result >= other_expression.result
        new_result = self.result * other_expression.result
        
        return MathList(new_expression, new_result)
    
    
    @myTimerModule.timer_func   
    def __truediv__(self, other_expression):
        new_expression = ['/'] + self + other_expression
        
        if self.result == 1 or other_expression.result == 1:
            return None
        if self.result % other_expression.result != 0:
            return None
        
        assert self.result >= other_expression.result
        
        new_result = int(self.result / other_expression.result)
        
        return MathList(new_expression, new_result)
    
    
    def __hash__(self):
        return tuple(self).__hash__()
    
    
    def sort_atom(self):
        pass
    
    
    def verify_atom(self):
        pass
    
    
    def evaluate_atom(self):
        pass
    
    
    def iterate_bottom_up(self, func):
        pass
    
    
    def iterate_top_down(self, func):
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
        
    
    def recurse_bottom_up(self, func):
        pass
    
    
    @myTimerModule.timer_func
    def recurse_top_down(self, func, sub_expression=None, i=0):
        """Recursively breaks down a prefix expression in more basic expressions
           to be evaluated.
        """
        if sub_expression is None:
            sub_expression = list(self)
        # Return if all that is left is a single number
        if len(sub_expression) == 1:
            func(self, i)
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
            operand_a = self.recurse_top_down(func, sub_expression[1:index], 1)
            operand_b = self.recurse_top_down(func, sub_expression[index:], index)
            
            func(self, i)
            
            # Check if an input was erroneus
            if operand_a is '' or operand_b is '':
                return ''
            
            #return func([sub_expression[0], 
                         #operand_a,
                         #operand_b])

        
    def to_infix(self):
        
        def recurse(sub_expression=None):
            if sub_expression is None:
                sub_expression = list(self)
            # Return if all that is left is a single number
            if len(sub_expression) == 1:
                return sub_expression
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
                operand_a = recurse(sub_expression[1:index])
                operand_b = recurse(sub_expression[index:])
                
                # Check if an input was erroneus
                if operand_a is '' or operand_b is '':
                    return ''
                
                return ['('] + operand_a + [' ', sub_expression[0], ' '] + operand_b + [')']
        
        expression = ''.join(recurse())
        
        return expression[1:-1] if len(self) > 1 else expression


if __name__ == "__main__":
    #a = MathTree(['+', '2', '1'], prefix=True, sort=True)
    a = MathList(['+', '2', '1'], 3)
    b = MathList(['-', '4', '3'], 1)
    print(a + b)
    print(a - b)
    print(a * b)
    print(a / b)
    print((a + b).to_infix())
    print(b.to_infix())