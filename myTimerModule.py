import time

function_info_dict = {}
open_functions = []


def timer_func(func):
    
    def timer_wrapper(*args, **kwargs):
        function_name = func.__qualname__
        
        if function_name not in function_info_dict:
            function_info_dict[function_name] = [0, 0, 0, {}]
        
        open_functions.append(function_name)
        function_info_dict[function_name][2] += 1
        
        # Time function
        initial_time = time.time()
        
        result = func(*args, **kwargs)
        
        finish_time = time.time()
        
        time_elapsed = finish_time - initial_time
        
        assert open_functions.pop() == function_name
        
        if len(open_functions) > 0 and open_functions[-1] != function_name:
            function_info_dict[open_functions[-1]][1] += time_elapsed
            
            # Assign the time elapsed to the child entry for this func in the parent function entry
            if function_info_dict[open_functions[-1]][3].get(function_name, False):
                function_info_dict[open_functions[-1]][3][function_name] += time_elapsed
            else:
                function_info_dict[open_functions[-1]][3][function_name] = time_elapsed
        
        function_info_dict[function_name][0] += time_elapsed
        
        return result
    
    return timer_wrapper

def print_results(limit=None):
    results = []
    longest = 0
    for key in function_info_dict.keys():
        results.append((key, function_info_dict[key]))
        if len(key) > longest:
            longest = len(key)
        
    results.sort(key=lambda a: a[1][0] - a[1][1], reverse=True)
    
    if limit is not None and 0 < limit <= len(results):
        results = results[:limit]
    
    for result in results:
        #print(result)
        print(f"{result[0]}:{' '*(longest - len(result[0]) + 5)}{int((result[1][0] - result[1][1]) * 1000) / 1000} s ({int((result[1][0]) * 1000) / 1000} s)")
        print(f"{result[1][2]} function call{'s' if result[1][2] != 1 else ''}.")
        for child in result[1][3]:
            print(f"\t{child}:{' '*(longest - len(result[0]) + 1)}{int(result[1][3][child] * 1000) / 1000} s")
        print()
        

@timer_func
def test():
    h = 0
    for i in range(1, 10000000):
        h += i
    
    print(h)
    

@timer_func
def test2():
    h = 0
    for i in range(1, 1000000):
        h += i
    
    print(h)
    

@timer_func
def test3():
    h = 0
    for i in range(1, 100000):
        h += i
    
    print(h)
    
if __name__ == '__main__':
    test()
    test2()
    test3()
    print_results()