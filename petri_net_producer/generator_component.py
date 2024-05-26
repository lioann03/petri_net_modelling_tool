import generator_general as gg


class Component:
    def __init__(self):
        self.name: int
        self.transitions: set[gg.Transition] = set([])
        self.places: set[gg.Place] = set([])
        self.arcs: set[gg.Arc] = set([])
        self.tokens: set[gg.Token] = set([])
        self.placements: dict[gg.Place,list[gg.Token_Or_Bond]] = {}
        self.needed_tokens: set[gg.Token] = set([])
        self.needed_bonds: set[gg.Bond] = set([])
        self.out_tokens: set[gg.Token] = set([])
        self.out_bonds: set[gg.Bond] = set([])
        self.total_trans: int
    
    def get_init_place(self):
        for place in self.places:
            if place.role == gg.Role.INIT or place.role == gg.Role.INIT_FIN:
                return place
        assert False,'Unreachable'
        return None
            
    def get_final_place(self):
        for place in self.places:
          if place.role == gg.Role.FIN or place.role == gg.Role.INIT_FIN:
              return place
        assert False,'Unreachable'
        return None 
     
    def print_component(self):
        for t in self.transitions:
            print(f'trans({t.name}).')

        for p in self.places:
            print(f'place({p.name}).') 

        if len(self.tokens) != 0:
            for t in self.tokens:
                print(f'token({t.name}).')
        
        for a in self.arcs:
            print(f'arc({a.place.name},{a.trans.name},{a.label},{a.type}).')
    
    def set_placement(self,place,tokens_bonds):
        self.placements[place] = tokens_bonds
          
                          

class ComponentBuilder:
    def __init__(self):
        self.component = Component()

    def set_name(self,name):
        self.component.name = name

    def set_arcs(self,arcs):
        self.component.arcs = set(arcs)

    def set_transitions(self,transitions):
        self.component.transitions = set(transitions)
        self.component.total_trans = len(self.component.transitions)
    
    def set_places(self,places):
        self.component.places = set(places)
    
    def set_tokens(self,tokens):
        self.component.tokens = set(tokens)
    
    def set_placements(self,placements):
        self.component.placements = dict(placements)
    
    def set_needed_tokens(self,tokens):
        self.component.needed_tokens = set(tokens) 
    
    def set_needed_bonds(self,bonds):
        self.component.needed_bonds = set(bonds) 
    
    def set_out_tokens(self,tokens):
        self.component.out_tokens = set(tokens) 
    
    def set_out_bonds(self,bonds):
        self.component.out_bonds = set(bonds) 
    

    def rename_place(self,suffix):
        pass


