
def test() -> str:
    "returns hello world"
    return "hello world"

def get_variables_in_class(cls) -> list: 
    """
    returns list of variables in the class
    """  
    return [i for i in cls.__dict__.keys() if i[:1] != '_'] 
