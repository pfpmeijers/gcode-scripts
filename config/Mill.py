from dataclasses import dataclass


@dataclass
class Mill:

    index: int = 1
    diameter: float = 6
    corner_diameter: float = 0

    @property
    def radius(self):
        return self.diameter / 2

