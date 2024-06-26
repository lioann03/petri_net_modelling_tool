from dataclasses import dataclass
from typing import NamedTuple, Set, Tuple, Union, List
import random
import itertools
from enum import Enum
import generator_component as comp
import generator_bridge as brid
from collections import deque

class ArcType(Enum):
   INCOMING = 1
   OUTCOMING = 2

class Role(Enum):
   INIT = 1
   FIN = 2
   MID = 3
   INIT_FIN = 4

#class CompBrid(Enum):
#   COMP = 1
#   BRID = 2

class Place(NamedTuple):
    name:str
    #ind:int
    role:Role

class Transition(NamedTuple):
    name:str
    #ind:int

class Token(NamedTuple):  
    name:str
    #ind:int

Bond = Tuple[Token, Token]

Token_Or_Bond = Union[Token, Bond]

class Arc(NamedTuple):
  label: Token_Or_Bond
  place: Place
  trans: Transition
  type: ArcType

Comp_Or_Brid = Union[comp.Component,brid.Bridge]   

class Sequence(NamedTuple):
    comp_brid: List[Tuple[Comp_Or_Brid,int]] = []
    tokens: List[Token_Or_Bond] = []
    init_tokens: List[Tuple[Token,int]] = []
    init_bonds: List[Tuple[Bond,int]] = []

@dataclass
class CountedComp():
  comp:comp.Component
  freq:int

@dataclass
class CountedBrid():
  brid:brid.Bridge
  freq:int

class PetriNet:
  def __init__(self): 
    self.init_placement: dict[Place,list[Token_Or_Bond]] = {}
    self.total_trans: int
    self.transitions_used: int = 0
    self.max_degree: int
    self.components: List[CountedComp] = []
    self.bridges: List[CountedBrid] = []
    self.extra_bridges: List[Tuple[CountedBrid,int,int]] = [] # CounterBrid, # of sequence, # of component
    self.seq: list[Sequence] = [] 
    self.init_comp: comp.Component
    self.init_brid: list[brid.Bridge] = []
    

class Petri_Net_Builder():
    def __init__(self):
      self.petri_net = PetriNet()
      #self.pending: deque = []

    def set_total_trans(self,trans):
      self.petri_net.total_trans = trans
    
    def set_max_degree(self,max_deg):
      self.petri_net.max_degree = max_deg
    
    def set_components(self,comp):
      for c in comp:
        countedcomp = CountedComp(c,0)
        self.petri_net.components.append(countedcomp)

    def set_bridges(self,brid):
      for b in brid:
        countedbrid = CountedBrid(b,0) 
        self.petri_net.bridges.append(countedbrid)
        
    def set_seq(self,ind):
      pass
    
    def update_component_frequency(self,comp:CountedComp):
      assert comp.freq>=0, 'comp.freq<0'
      comp.freq+=1
    
    def update_bridge_frequency(self,brid:CountedBrid):
      assert brid.freq>=0, 'brid.freq<0'
      brid.freq+=1
       
    def get_petri_net(self):
      ret = self.petri_net
      self.reset()
      return ret
      
    def create_init_comp(self): 
      init_place = set()
      init_place.add(Place('init_place',Role.INIT))
      comp_builder = comp.ComponentBuilder()
      comp_builder.set_name('init')
      comp_builder.set_places(init_place)
      self.petri_net.init_comp = comp_builder.component
      comp_builder.set_transitions([])

      #TODO: place init tokens to init comp
      #for i in range(self.petri_net.max_degree):
      #  c = self.petri_net.seq[i].comp_brid[0]
      #  needed_tb = []
      #  assert type(c[0]) == comp.Component
      #  needed_tb.append(c[0].tokens)
      #  for t in c[0].tokens:
      #    pass

    def create_init_bridges(self):
      for i in range(self.petri_net.max_degree):
        bridgeb = brid.BridgeBuilder()
        #print(self.petri_net.seq[i].comp_brid[0][0])
        assert type(self.petri_net.seq[i].comp_brid[0][0]) == comp.Component
        c = self.petri_net.seq[i].comp_brid[0][0]
        bridgeb.set_start_component(self.petri_net.init_comp)
        bridgeb.set_end_component(c)
        bridgeb.set_transition(Transition(f'inittrans{i}'))
        bridgeb.set_arcs_init()
        self.petri_net.init_brid.append(bridgeb.bridge)
      for b in self.petri_net.init_brid:
        self.petri_net.transitions_used += b.total_trans
        
    
    # find all possible components that can connect with thed init component
    # must have 1 transition
    def _possible_starting_comp(self):
      starting_comp = []
      for c in self.petri_net.components:
        if c.comp.total_trans == 1:
           starting_comp.append(c.comp)
      return starting_comp
    
    ###########################
    def set_seq_init_tokens(self):
      for i in range(self.petri_net.max_degree):
        s = self.petri_net.seq[i]
        assert type(s.comp_brid[0][0]) == comp.Component
        for t in s.comp_brid[0][0].needed_tokens:
          s.init_tokens.append((t,i))
        for b in s.comp_brid[0][0].needed_bonds:
          s.init_bonds.append((b,i))
        
    def set_first_comp_in_seq(self):
      starting_comp = self._possible_starting_comp()
      for i in range(self.petri_net.max_degree):
        s=self.petri_net.seq
        first_of_seq_comp = random.choice(starting_comp)
        s[i].comp_brid.append((first_of_seq_comp,self.get_freq(first_of_seq_comp)))
        self.set_freq(first_of_seq_comp)

    def get_freq(self,comp_brid:Comp_Or_Brid):
      if type(comp_brid) == comp.Component:
        for c in self.petri_net.components:
          if(c.comp == comp_brid):
            return c.freq 
      if type(comp_brid) == brid.Bridge:
        for c in self.petri_net.bridges:
          if(c.brid == comp_brid):
            return c.freq
      assert(False), 'unreachable'

    def set_freq(self,comp_brid:Comp_Or_Brid):
      if type(comp_brid) == comp.Component:
        for c in self.petri_net.components:
          if(c.comp == comp_brid):
            c.freq += 1
            return None 
      if type(comp_brid) == brid.Bridge:
        for c in self.petri_net.bridges:
          if(c.brid == comp_brid):
            c.freq += 1
            return None
      assert(False), 'unreachable'

    def add_comp_in_seq(self,seq:Sequence):
      #assert len(self.petri_net.seq) > ind, 'seq out of bounds'
      for c in self.petri_net.bridges:   
        comp_brid_list = seq.comp_brid
        last_comp = comp_brid_list[len(comp_brid_list)-1]
        assert type(last_comp[0]) == comp.Component, 'last comp in seq not Component'
        if c.brid.start_component == last_comp[0] and \
        (c.brid.total_trans + self.petri_net.transitions_used) <= self.petri_net.total_trans:
          seq.comp_brid.append((c.brid,c.freq))
          seq.comp_brid.append((c.brid.end_component, self.get_freq(c.brid.end_component)))
          c.freq += 1
          self.set_freq(c.brid.end_component)
          self.petri_net.transitions_used += c.brid.total_trans
          return True
      return False

    def add_extra_bridges(self):
      remaining = self.petri_net.total_trans - self.petri_net.transitions_used
      assert remaining > 0, 'extra bridges must not be added'
      for i in range(remaining):
        rand_seq = random.choice(self.petri_net.seq)
        end = False
        while not end: 
          rand_comp = random.choice(rand_seq.comp_brid)
          if type(rand_comp[0]) == comp.Component:
            end = True
        new_bridge = brid.BridgeBuilder()
        new_bridge.set_start_component(rand_comp[0])
        new_bridge.set_end_component(self.petri_net.init_comp)
        new_bridge.set_transition(Transition(f'extra{i}'))
        new_bridge.set_arcs_extra()
        self.petri_net.extra_bridges.append((CountedBrid(new_bridge.bridge,0),i,rand_comp[1]))
        #.comp_brid.append((new_bridge.bridge,0))
        #rand_seq.comp_brid.append((self.petri_net.init_comp,0))
        self.petri_net.bridges.append(CountedBrid(new_bridge.bridge,0))

    # the first component of each sequence is always c0.
    def build(self):
      for i in range(self.petri_net.max_degree):
        self.petri_net.seq.append(Sequence([],[],[],[]))

      self.set_first_comp_in_seq()
      self.create_init_comp()
      self.create_init_bridges()
      self.set_seq_init_tokens()
      

      proceed = True
      while self.petri_net.transitions_used < self.petri_net.total_trans and proceed:  
        for s in self.petri_net.seq:
          if not proceed:
            break
          proceed = self.add_comp_in_seq(s)
   
      if self.petri_net.transitions_used < self.petri_net.total_trans and not proceed:
        self.add_extra_bridges()
      self.print_petri_net()

    def print_transitions(self):
      for seq in self.petri_net.seq:
        for comp_brid in seq.comp_brid:
          if type(comp_brid[0]) == comp.Component:
            for trans in comp_brid[0].transitions:
              print("trans({}{}).".format(trans.name,comp_brid[1]))
          if type(comp_brid[0]) == brid.Bridge:
            print("trans({}{}).".format(comp_brid[0].trans.name,comp_brid[1]))
      for btrans in self.petri_net.init_brid:
        print("trans({}).".format(btrans.trans.name))
      for extra in self.petri_net.extra_bridges:
        print("trans({}).".format(extra[0].brid.trans.name))

    def print_places(self):
      for seq in self.petri_net.seq:
        for comp_brid in seq.comp_brid:
          if type(comp_brid[0]) == comp.Component:
            for pl in comp_brid[0].places:
              print("place({}{}).".format(pl.name,comp_brid[1]))
      for p in self.petri_net.init_comp.places:
        print("place({}).".format(p.name)) 

    def print_placement(self):
      init_tok:List[Tuple[Token, int]] = []
      init_bonds:List[Tuple[Bond, int]] = []
      init_comp = self.petri_net.init_comp
      for s in self.petri_net.seq:
        for t in s.init_tokens:
          init_tok.append(t)
        for b in s.init_bonds:
          init_bonds.append(b)

      for t in init_tok:
        assert len(init_comp.places) == 1, 'more than one init places'
        for place in init_comp.places:
          print("placeholds({},{}{},0).".format(place.name,
                                                t[0].name,t[1])) 
      for b in init_bonds:
        assert len(init_comp.places) == 1, 'more than one init places'
        for place in init_comp.places:
          print("placeholdsbond({},{}{},{}{},0).".format(place.name,b[0][0].name,b[1],b[0][1].name,b[1]))
      
      for i in range(self.petri_net.max_degree):
        s = self.petri_net.seq[i]
        for comp_brid in s.comp_brid:
          if type(comp_brid[0]) == comp.Component:
            for place in comp_brid[0].placements:
              for tok_bond in comp_brid[0].placements[place]:
                if type(tok_bond) == Token:
                  print("placeholds({},{}{},0).".format(place.name,tok_bond.name,i))
                if type(tok_bond) == Bond:
                  print("placeholdsbond({},{}{},{}{},0).".format(place.name,tok_bond[0].name,i,tok_bond[1].name,i))
          
    def print_comp_arcs(self,i,cb):
      for arc in cb[0].arcs:
        if arc.type == ArcType.INCOMING:
          if type(arc.label) == Token:
            print("incoming({}{},{}{},{}{}).".format(arc.place.name,cb[1],arc.trans.name,cb[1],arc.label.name,i))
          elif type(arc.label) == tuple:
            print("incomingbond({}{},{}{},{}{},{}{}).".format(arc.place.name,cb[1],arc.trans.name,cb[1],
                                                                    arc.label[0].name,i,arc.label[1].name,i))
        elif arc.type == ArcType.OUTCOMING:
          if type(arc.label) == Token: 
            print("outcoming({}{},{}{},{}{}).".format(arc.trans.name,cb[1],arc.place.name,cb[1],arc.label.name,i))
          elif type(arc.label) == tuple:
            print("outcomingbond({}{},{}{},{}{},{}{}).".format(arc.trans.name,cb[1],arc.place.name,cb[1],arc.label[0].name,i,arc.label[1].name,i))
      
    def print_brid_arcs(self,i:int,j:int):
      current_brid = self.petri_net.seq[i].comp_brid[j]
      assert j>0
      next = None
      prev = self.petri_net.seq[i].comp_brid[j-1]
      assert type(prev[0]) == comp.Component
      if j < len(self.petri_net.seq[i]) - 1:
        next = self.petri_net.seq[i].comp_brid[j+1]
        
      for arc in current_brid[0].arcs:
        if arc.type == ArcType.INCOMING:
          if type(arc.label) == Token:
            print("incoming({}{},{}{},{}{}).".format(prev[0].get_final_place().name,prev[1],arc.trans.name,current_brid[1],arc.label.name,i))
          elif type(arc.label) == tuple:
            print("incomingbond({}{},{}{},{}{},{}{}).".format(prev[0].get_final_place().name,prev[1],arc.trans.name,current_brid[1],
                                                                    arc.label[0].name,i,arc.label[1].name,i))
        elif arc.type == ArcType.OUTCOMING and type(next) != None:
          assert type(next) == Tuple[Comp_Or_Brid,int]
          assert type(next[0]) == comp.Component
          if type(arc.label) == Token: 
            print("outcoming({}{},{}{},{}{}).".format(arc.trans.name,current_brid[1],next[0].get_init_place().name,next[1],arc.label.name,i))
          elif type(arc.label) == tuple:
              print("outcomingbond({}{},{}{},{}{},{}{}).".format(arc.trans.name,current_brid[1],next[0].get_init_place().name,next[1],arc.label[0].name,i,arc.label[1].name,i))

    def print_init_bridges(self):
      for i in range(self.petri_net.max_degree):
        b = self.petri_net.init_brid[i]
        s = self.petri_net.seq[i]
        assert type(s.comp_brid[0][0]) == comp.Component
        for arc in b.arcs:
          if arc.type == ArcType.INCOMING:
            if type(arc.label) == Token:
              print("incoming({},{},{}{}).".format(self.init_comp_place_name(),b.trans.name,
                                                     arc.label.name,i))
            elif type(arc.label) == tuple:
              print("incomingbond({},{},{}{},{}{}).".format(self.init_comp_place_name(),b.trans.name,
                                                     arc.label[0].name,i,arc.label[1].name,i))
          elif arc.type == ArcType.OUTCOMING:
            if type(arc.label) == Token: 
              print("outcoming({},{}{},{}{}).".format(b.trans.name,s.comp_brid[0][0].get_init_place().name,s.comp_brid[0][1],
                                                     arc.label.name,i))
            elif type(arc.label) == tuple:
              print("outcomingbond({},{}{},{}{},{}{}).".format(b.trans.name,s.comp_brid[0][0].get_init_place().name,s.comp_brid[0][1],
                                                   arc.label[0].name,i,arc.label[1].name,i))
    def print_extra_bridges_arcs(self):
      for i in range(len(self.petri_net.extra_bridges)):
        br = self.petri_net.extra_bridges[i]
        for arc in br[0].brid.arcs:
          if arc.type == ArcType.INCOMING:
            if type(arc.label) == Token:
              print("incoming({}{},{},{}{}).".format(arc.place.name,br[2],arc.trans.name,arc.label.name,br[1]))                                        
            elif type(arc.label) == tuple:
              print("incomingbond({}{},{},{}{},{}{}).".format(arc.place.name,br[2],arc.trans.name,
                                                              arc.label[0].name,br[1],arc.label[1].name,br[1]))
          elif arc.type == ArcType.OUTCOMING:
            if type(arc.label) == Token: 
              print("outcoming({},{},{}{}).".format(arc.trans.name,arc.place.name,arc.label.name,br[1]))
            elif type(arc.label) == tuple:
              print("outcomingbond({},{},{}{},{}{}).".format(arc.trans.name,arc.place.name,
                                                               arc.label[0].name,br[1],arc.label[1].name,br[1]))

    def print_arcs(self):
      self.print_init_bridges()
      # print arcs of the initial bridges
      for i in range(self.petri_net.max_degree):
        s = self.petri_net.seq[i]
        for j in range(len(s.comp_brid)):
          cb = s.comp_brid[j]
          if type(cb[0]) == comp.Component:
            self.print_comp_arcs(i,cb) 
          if type(cb[1]) == brid.Bridge:
            self.print_brid_arcs(i,j)
      if len(self.petri_net.extra_bridges) > 0:
        self.print_extra_bridges_arcs()

    def init_comp_place_name(self):
      for p in self.petri_net.init_comp.places:
        return p.name

    def print_tokens(self):
      for i in range(self.petri_net.max_degree):
        s = self.petri_net.seq[i]
        for needed_tok in s.init_tokens:
          print("token({}{}).".format(needed_tok[0].name,needed_tok[1]))
        for needed_b in s.init_bonds:
          print("token({}{}).".format(needed_b[0][0].name,needed_b[1]))
          print("token({}{}).".format(needed_b[0][1].name,needed_b[1]))
        for com in s.comp_brid[0]:
          if type(com) == comp.Component:
            for tok in com.tokens:
             assert type(tok) == Token
             print("token({}{}).".format(tok.name,i))

    def print_goal_state(self):
      if len(self.petri_net.extra_bridges) > 0:
        extra = random.choice(self.petri_net.extra_bridges)
        for arc in extra[0].brid.arcs:
            tok_bond = arc.label
            if type(tok_bond) == Token:
              print('placeholds({},{}{},ts).'.format(self.init_comp_place_name(),tok_bond.name,extra[1]))
            else:
              assert type(tok_bond) == tuple
              print('placeholdsbond({},{}{},{}{},ts).'.format(self.init_comp_place_name(),
                                                                tok_bond[0].name,extra[1],tok_bond[1].name,extra[1]))
        return None
      
      #for i in range(self.petri_net.max_degree):
      i = random.randint(0,self.petri_net.max_degree-1)
      s = self.petri_net.seq[i]
      last_component = s.comp_brid[len(s.comp_brid)-1][0]
      last_index = s.comp_brid[len(s.comp_brid)-1][1]
      assert type(last_component) == comp.Component, 'last item of a sequence is not a component'
      last_place = last_component.get_final_place()
      for tok in last_component.out_tokens:
        print('placeholds({}{},{}{},ts).'
              .format(last_place.name,last_index,tok.name,i))
      for bond in last_component.out_bonds:
        print('placeholdsbond({}{},{}{},{}{},ts).'
              .format(last_place.name,last_index,bond[0].name,i,bond[1].name,i))
      return


    def print_petri_net(self):
      #for s in self.petri_net.seq:
      #  assert type(s.comp_brid[0][0]) == comp.Component
      #  print(s.comp_brid[0][0].name)
      self.print_transitions()
      self.print_tokens()
      self.print_places()
      self.print_placement()
      self.print_arcs()
      self.print_goal_state()
        
    def reset(self):
      self.petri_net = PetriNet()

def _produce_rand_bonds(tokens,rand_bonds):
    if(len(tokens) > 1):
      bonds = [*itertools.combinations(tokens, 2)]
      rand_bonds = min(len(bonds) , rand_bonds)
      ret = set(random.sample(bonds, k=rand_bonds))
      return ret
    return set([])

def _filter_tokens(tokens,bonds):
  return set(*filter(lambda t: all(t not in [t1, t2] for t1, t2 in bonds), tokens))