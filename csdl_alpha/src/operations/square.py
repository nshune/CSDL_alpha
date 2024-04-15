from csdl_alpha.src.operations.operation_subclasses import ComposedOperation
from csdl_alpha.utils.inputs import validate_and_variablize

class Square(ComposedOperation):

    def __init__(self,x):
        super().__init__(x)
        self.name = 'sqr'

    def evaluate_composed(self,x):
        return evaluate_square(x)

def evaluate_square(x):
    return x*x

def square(x):
    """
    doc strings
    """
    x = validate_and_variablize(x)

    return Square(x).finalize_and_return_outputs()
