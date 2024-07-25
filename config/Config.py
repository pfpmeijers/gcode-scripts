from dataclasses import dataclass, field

from config.Spindle import Spindle
from config.Workpiece import Workpiece
from config.Mill import Mill
from config.Milling import Milling
from config.Tab import Tab


@dataclass
class Config:

    workpiece: Workpiece = field(default_factory=Workpiece)
    mill: Mill = field(default_factory=Mill)
    spindle: Spindle = field(default_factory=Spindle)
    tab: Tab = field(default_factory=Tab)
    milling: Milling = field(default_factory=Milling)