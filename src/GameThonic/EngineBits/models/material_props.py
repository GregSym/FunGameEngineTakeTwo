
from dataclasses import dataclass

@dataclass
class MaterialProperties:
    mu_coefficient: float
    friction: float
    luminence: float
    """
        no lighting system currently exists, so ignored for now
    """
    hardness: float
    """ should probably have a different name, but this measures the % of
        force dissipated on impact
    """
    consistency: float 
    """ do other objects pass through it """
    opacity: float
    """ transparency of the object """