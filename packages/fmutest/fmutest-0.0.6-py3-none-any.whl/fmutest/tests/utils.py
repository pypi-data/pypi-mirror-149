# refs: https://www.geeksforgeeks.org/decorator-to-print-function-call-details-in-python/

# Decorator to print function call details
def function_details(func):
    
    # Getting the argument names of the
    # called function
    argnames = func.__code__.co_varnames[:func.__code__.co_argcount]

      
    # Getting the Function name of the
    # called function
    fname = func.__name__
      
      
    def inner_func(*args, **kwargs):
          
        print("\nstart", fname, "(", end = "")
          
        # printing the function arguments
        print(', '.join( '% s = % r' % entry for entry in zip(argnames, args[:len(argnames)])), end = ", ")
          
        # Printing the variable length Arguments
        print("args =", list(args[len(argnames):]), end = ", ")
          
        # Printing the variable length keyword
        # arguments
        print("kwargs =", kwargs, end = "")
        print(")")

        #print(func())

        print('end', fname)
      
    return inner_func