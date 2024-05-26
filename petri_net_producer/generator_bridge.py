import generator_component as gc
import generator_general as gg

class Bridge:
    def __init__(self):
        self.start_component:gc.Component
        self.end_component: gc.Component 
        self.trans: gg.Transition
        self.arcs: set[gg.Arc] = set()
        self.total_trans: int = 0


class BridgeBuilder:
    def __init__(self):
        self.bridge = Bridge()

    def set_start_component(self,comp):
        self.bridge.start_component = comp
    
    def set_end_component(self,comp):
        self.bridge.end_component = comp
        

    def set_transition(self,trans):
        #print(f'{self.bridge=}')
        self.bridge.trans = trans
        assert type(self.bridge.end_component) == gc.Component, 'components not given'
        self.bridge.total_trans = 1 + self.bridge.end_component.total_trans

    def set_arcs(self):
        comp_start = self.bridge.start_component
        comp_end = self.bridge.end_component

        for tok in comp_start.out_tokens:
            self.bridge.arcs.add(gg.Arc(tok,comp_start.get_final_place(),self.bridge.trans,gg.ArcType.INCOMING))
        
        for bond in comp_start.out_bonds:
           self.bridge.arcs.add(gg.Arc(bond,comp_start.get_final_place(),self.bridge.trans,gg.ArcType.INCOMING))

        for tok in comp_end.needed_tokens:
            self.bridge.arcs.add(gg.Arc(tok,comp_end.get_init_place(),self.bridge.trans,gg.ArcType.OUTCOMING))
        
        for bond in comp_end.needed_bonds:
           self.bridge.arcs.add(gg.Arc(bond,comp_end.get_init_place(),self.bridge.trans,gg.ArcType.OUTCOMING))

    def set_arcs_init(self):
        comp_start = self.bridge.start_component
        comp_end = self.bridge.end_component
        for p in comp_start.places:
            init_place = p
       
        for tok in comp_end.needed_tokens:
            self.bridge.arcs.add(gg.Arc(tok,init_place,self.bridge.trans,gg.ArcType.INCOMING))
        
        for bond in comp_end.needed_bonds:
            self.bridge.arcs.add(gg.Arc(bond,init_place,self.bridge.trans,gg.ArcType.INCOMING))

        for tok in comp_end.needed_tokens:
            self.bridge.arcs.add(gg.Arc(tok,comp_end.get_init_place(),self.bridge.trans,gg.ArcType.OUTCOMING))
        
        for bond in comp_end.needed_bonds:
           self.bridge.arcs.add(gg.Arc(bond,comp_end.get_init_place(),self.bridge.trans,gg.ArcType.OUTCOMING))

    def set_arcs_extra(self):
        comp_start = self.bridge.start_component
        comp_end = self.bridge.end_component

        for tok in comp_start.out_tokens:
            self.bridge.arcs.add(gg.Arc(tok,comp_start.get_final_place(),self.bridge.trans,gg.ArcType.INCOMING))
        
        for bond in comp_start.out_bonds:
           self.bridge.arcs.add(gg.Arc(bond,comp_start.get_final_place(),self.bridge.trans,gg.ArcType.INCOMING))

        for tok in comp_start.out_tokens:
            self.bridge.arcs.add(gg.Arc(tok,comp_end.get_init_place(),self.bridge.trans,gg.ArcType.OUTCOMING))
        
        for bond in comp_start.out_bonds:
           self.bridge.arcs.add(gg.Arc(bond,comp_end.get_init_place(),self.bridge.trans,gg.ArcType.OUTCOMING))