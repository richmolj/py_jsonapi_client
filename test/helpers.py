from functools import wraps

# Compare 2 arrays independent of order
def matchArray(array1, array2):
    return sorted(array1) == sorted(array2)

def raises(error_class):
    def outer(fn):
        @wraps(fn)
        def assert_raise(self,*args,**kwargs):
            raised = False
            try:
                fn(self, *args, **kwargs)
            except error_class as e:
                raised = True
            except Exception as e:
                was = 'Error raised was ' + type(e).__name__
                expected = ', expected ' + error_class.__name__
                raise Exception(was + expected)
            assert raised
        return assert_raise
    return outer
