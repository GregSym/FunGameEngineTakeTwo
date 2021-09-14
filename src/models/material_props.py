
from dataclasses import dataclass

@dataclass
class MaterialProperties:
    mu_coefficient: float
    friction: float
    luminence: float
    hardness: float
    consistency: float 
    opacity: float
    """ do other objects pass through it """