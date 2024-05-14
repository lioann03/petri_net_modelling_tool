import generator_component as gc
import generator_general as gg

class Bridge:
    def __init__(self):
        self.start_component:gc.Component
        self.end_component: gc.Component
        self.trans: gg.Transition
        self.arcs: set[gg.Arc]
        self.total_trans: int = 0


class BridgeBuilder:
    def __init__(self):
        self.bridge = Bridge()

    def set_start_component(self,comp):
        self.bridge.start_component = comp
    
    def set_end_component(self,comp):
        self.bridge.end_component = comp

    def set_transition(self,trans):
        self.bridge.trans = trans

    