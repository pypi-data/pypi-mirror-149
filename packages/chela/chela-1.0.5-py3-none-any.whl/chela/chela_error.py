"""Module containg the definition of Error classes inherited from ValueError.
   The following error are desinged to individuate mispelled or inexistent
   chemical formulas.
"""

class EmptyFormula(ValueError):
    """Error indicating the string that should contain the chemical formula is empty"""
    pass

class FirstElementAbsent(ValueError):
    """Error indicatig the first atomic symbol in the chemical formula is absent"""
    pass

class NonAlphaNumericValue(ValueError):
    """Error indicating the presence of non alphanumeric value  in the chemical formula"""
    pass

class NegativeQuantityElement(ValueError):
    """Error indicating the presence of negative quantity in the chemical formula"""
    pass

class NonExistentElement(ValueError):
    """Error indicating the formula contain letters that don't represent atomic symbols"""
    pass

class ZeroQuantityElement(ValueError):
    """Error indicating the presence of elements with 0 quantity in the formula"""
    pass

class RepeatedElement(ValueError):
    """Error indicating the presence of repeated atomic symbols in the chemical formula"""
    pass
