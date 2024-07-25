from dataclasses import dataclass


@dataclass
class Milling:

    retract_height: float = 10

    plunge_rate: int = 100
    feed_rate: int = 1000

    width_of_cut = 4  # xy-step per xy-lane
    depth_of_cut = 2  # z-step per z-layer
    angle_of_cut = 5  # Angle steps during creation of fillets

    margin: float = 0.25

