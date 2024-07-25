from dataclasses import dataclass


@dataclass
class Workpiece:

    width: float = 300  # x
    depth: float = 400  # y
    height: float = 30  # z

    # Workpiece offset in relation to the router home position.
    # Default origin (0,0,0) in left front top.
    offset: tuple[float, float, float] = (0, 0, 0)

    @property
    def left(self):
        return self.offset[0]

    @property
    def right(self):
        return self.left + self.width

    @property
    def front(self):
        return self.offset[1]

    @property
    def back(self):
        return self.front + self.depth

    @property
    def top(self):
        return self.offset[2]

    @property
    def bottom(self):
        return self.top - self.height
