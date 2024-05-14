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

class PetriNet:
  def __init__(self):
    self.tokens: set[Token] = set([])
    self.bonds: set[Bond] = set([]) 
    self.placement: dict[Place,list[Token_Or_Bond]] = []
    self.total_trans: int
    self.transitions_used: int
    self.max_degree: int
    self.initial_place: Place
    self.components: Union[(comp.Component,int)] = set([])
    #self.bridges: set[br.Bridge]
    self.paths: List[List[Comp_Or_Brid]] = []



class Petri_Net_Builder():
    def __init__(self):
      self.petri_net = PetriNet()
      self.petri_net.transitions_used = 0
      self.pending: deque = []
    
    def set_total_trans(self,trans):
      self.petri_net.total_trans = trans
    
    def set_degree(self,max_deg):
      self.petri_net.max_degree = max_deg

    def get_petri_net(self):
      ret = self.petri_net
      self.reset()
      return ret

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