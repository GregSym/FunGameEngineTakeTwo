try:
    from .functions import direction
    from .functions import random_item_generation
except ModuleNotFoundError:
    from gamethonic.enginebits.functions import direction
    from gamethonic.enginebits.functions import random_item_generation

if __name__ == "__main__":
    direction
    random_item_generation
