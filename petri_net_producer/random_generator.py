from typing import NamedTuple, Set, Tuple, Union, List
import random
import math
import itertools
from enum import Enum

class ArcType(Enum):
   INCOMING = 1
   OUTCOMING = 2

class Place(NamedTuple):
    name:str
    ind:int

class Transition(NamedTuple):
    name:str
    ind:int

class Token(NamedTuple):  
    name:str
    ind:int

Bond = Tuple[Token, Token]

Token_Or_Bond = Union[Token, Bond]

class Arc(NamedTuple):
  label: Token_Or_Bond
  place: Place
  trans: Transition
  type: ArcType
     

class PetriNet:
  def __init__(self):
    self.places: set[Place] = set([])
    self.transitions: set[Transition] = set([])
    self.arcs_tp: set[Arc] = set([])
    self.arcs_pt: set[Arc] = set([])
    self.tokens: set[Token] = set([])
    self.bonds: set[Bond] = set([]) 
    self.placement: dict[Place,list[Token_Or_Bond]] = []

  def add_place(self, place: Place):
    self.places.append(place)

  def add_transition(self, transition: Transition):
    self.transitions.append(transition)

  def place_token_or_bond(self, place: Place, token_or_bond: Token_Or_Bond):
    pass

class Petri_Net_Builder():
  def __init__(self):
    self.petri_net = PetriNet()

  def get_petri_net(self):
     ret = self.petri_net
     self.reset()
     return ret

  def reset(self):
     self.petri_net = PetriNet()


  def set_places(self,num_places):
     places = []
     for i in range(num_places):
        places.append(f'place{i}')
     self.petri_net.places = set(places)

  def set_trans(self,num_trans):
    trans = []
    for i in range(num_trans):
      trans.append(f'transition{i}')
    self.petri_net.transitions = set(trans)

  
  def choose_rand_tokens(self, rand_tokens):
     rand_tokens = min(len(self.petri_net.tokens),rand_tokens)
     return set(random.sample(list(self.petri_net.tokens), k=rand_tokens))
  
     
  #TODO: Tokens and Bonds must not have duplicate values
  def set_tokens_or_bonds(self,num_tokens,num_bonds):
    tokens = []
    bonds = []
    tokens = [f'token{i}' for i in range(num_tokens)]

    # Generate num_bonds bonds
    #k = random.randrange(num_bonds) 
    bonds = _produce_rand_bonds(tokens,num_bonds)
    toks = [*filter(lambda t: all(t not in [t1, t2] for t1, t2 in bonds), tokens)]
    self.petri_net.tokens = set(toks)
    self.petri_net.bonds = set(bonds)

    
  def new_arc(self,label,place,trans,type):
    return Arc(label,place,trans,type)
  
  def build_arcs(self,tokens_bonds_x_places,t,type_arc):
      used = set([])
      for x in tokens_bonds_x_places:
        if (x[0] in used) or (type(x[0]) == tuple and swap_bond(x[0]) in used): 
          continue
        arc = self.new_arc(x[0],x[1],t,type_arc)
        if type_arc == ArcType.INCOMING:
          self.petri_net.arcs_pt.add(arc)
        else:
          self.petri_net.arcs_tp.add(arc)
        used.add(x[0]) 
        connected_to_x = []
        connected_to_x.append(x[0])   
        for y in tokens_bonds_x_places:
          if (y[0] not in used) and (type(y[0]) == tuple) and \
            (any(y[0][0] in c for c in connected_to_x) or (any(y[0][1] in c for c in connected_to_x))):
            arc2 = self.new_arc(y[0],x[1],t,type_arc)
            if type_arc == ArcType.INCOMING:
              self.petri_net.arcs_pt.add(arc2)
            else:
              self.petri_net.arcs_tp.add(arc2)
            used.add(y[0])
            connected_to_x.append(y[0])
      return used

  def set_arcs(self,max_arcs):
    # Create >= max_arcs arcs for EACH trasnition t
    for t in self.petri_net.transitions:  
      # Choose random tokens   
      inc_tokens = set([])
      if len(self.petri_net.tokens) > 0:
        rand_tokens = random.randint(1,len(self.petri_net.tokens))
        inc_tokens = self.choose_rand_tokens(rand_tokens)
      # Produce some possible bonds (note: these bonds have nothing to do with the bonds of the petri net)
      all_tokens = _all_tokens(self.petri_net.tokens,self.petri_net.bonds)
      # Note: /2 so to limit down the number of bonds (the more bonds the more difficult to fire)
      inc_bonds = _produce_rand_bonds(all_tokens,math.comb(int(len(all_tokens)/2),2)) 
      bonded = set(itertools.chain(*inc_bonds))
      inc_tokens = set(x for x in inc_tokens if x not in bonded) #TODO:
      inc_tokens_bonds = inc_tokens.union(inc_bonds)
      
      rand_inc_arcs = random.randint(1,max_arcs)
      tokens_bonds_x_places = _cartesian_subset(inc_tokens_bonds,self.petri_net.places,rand_inc_arcs)
      
      # Create the incoming arcs
      used = self.build_arcs(tokens_bonds_x_places,t,ArcType.INCOMING)
      out_tokens_bonds_x_places= _cartesian_subset_out(used,self.petri_net.places,len(used))
      self.build_arcs(out_tokens_bonds_x_places,t,ArcType.OUTCOMING)

  def set_placement(self):
    tokensxbonds = self.petri_net.tokens.union(self.petri_net.bonds)
    self.petri_net.placement = _placetokensbonds(self.petri_net.places,tokensxbonds)
    
     
  def print_petri_net(self):
    print ('% Print Transitions %')
    for i in self.petri_net.transitions:
      print(f'trans({i}).')

    print ('% Print Places %')
    for i in self.petri_net.places:
     print(f'place({i}).')

    all_tokens = _all_tokens(self.petri_net.tokens,self.petri_net.bonds)
    print ('% Print Tokens %')
    for i in all_tokens:
      print(f'token({i}).')
  
    print ('% Print Incoming Arcs %')
    for i in self.petri_net.arcs_pt:
      if type(i.label) == tuple:
         print(f'incomingbond({i.place},{i.trans},{i.label[0]},{i.label[1]}).')
      else:
         print(f'incoming({i.place},{i.trans},{i.label}).')

    print ('% Print Outcoming Arcs %')
    for i in self.petri_net.arcs_tp:
      if type(i.label) == tuple:
         print(f'outcomingbond({i.trans},{i.place},{i.label[0]},{i.label[1]}).')
      else:
         print(f'outcoming({i.trans},{i.place},{i.label}).')
    
    print('% Print Placements %')
    for place,tok_bond_arr in self.petri_net.placement.items():
      for tok_bond in tok_bond_arr:
        if type(tok_bond) == tuple:
          print(f'placeholdsbond({place},{tok_bond[0]},{tok_bond[1]},0).')
        else:
          print(f'placeholds({place},{tok_bond},0).')
      


def _cartesian_subset(xs, ys, k):
  xs = list(xs)
  ys = list(ys)
  mn = len(xs) * len(ys)
  k = min(k, mn)
  p = set()
  while len(p) < k:
    x = random.choice(xs)
    y = random.choice(ys)
    p.add((x, y))
  return list(p)

def _cartesian_subset_out(used, places, out_arcs):
  p = set()
  used_inc_tokens = [t for t in used if type(t) != tuple]
  used_inc_bonds = [t for t in used if type(t) == tuple]
  all_tokens = _all_tokens(used_inc_tokens,used_inc_bonds)
  # Force bonds from the incoming arcs of each transition to appear in one outgoing arc
  for b in used_inc_bonds:
    c = random.choice(list(places))
    p.add((b,c))

  new_bonds = _produce_rand_bonds(all_tokens,math.comb(int(len(all_tokens)/2),2))
  new_bonds = set(x for x in new_bonds if x not in used_inc_bonds)
  out_bonds = new_bonds.union(used_inc_bonds)
  bonded = set(itertools.chain(*out_bonds))
  #out_tokens = set(x for x in used_inc_tokens if x not in bonded)
  #out_tokens_bonds = out_tokens.union(out_bonds)
  rand_out_arcs = random.randint(len(used), out_arcs)
  p2 = set(_cartesian_subset(new_bonds,places,rand_out_arcs))
  p.update(p2)

  # Force tokens from the incoming arcs of each transition to appear in one outgoing arc
  for t in used_inc_tokens:
    if any(x for x in p if (type(x)==tuple and (x[0]==t or x[1]==t)) or (type(x)!=tuple and x==t)):
      continue
    c = random.choice(list(places))
    is_bonded = random.randint(0,1)
    if is_bonded == 1:
      t2 = random.choice(list(all_tokens))
      assert len(all_tokens) > 1
      while t2 == t:
        t2 = random.choice(list(all_tokens))
      bond = (t,t2)
      p.add((bond,c))
    else:
      p.add((t,c))
  
  return list(p)


def _produce_rand_bonds(tokens,rand_bonds):
    if(len(tokens) > 1):
      bonds = [*itertools.combinations(tokens, 2)]
      rand_bonds = min(len(bonds) , rand_bonds)
      ret = set(random.sample(bonds, k=rand_bonds))
      return ret
    return []

def eq_tuple(x, y):
   return x == y or (x[0] == y[1] and x[1] == y[0])

def swap_bond(t):
   x, y = t
   return y, x

def _all_tokens(tokens,bonds):
  all_tokens = list(tokens) + list(itertools.chain(*bonds))
  return set(all_tokens)

def _placetokensbonds(places, tokensxbonds):
  used = {}
  for x in tokensxbonds:
    if (any(x for i in used.values() if x in i)):  
      continue
    place = random.choice(list(places))
    try:
      used[place] += [x]
    except KeyError:
      used[place] = [x]
    connected_to_x = []
    connected_to_x.append(x)  
    for y in tokensxbonds:
      if (any(y for i in used.values() if y in i)):
        continue 
      if (type(y) == tuple and (any(y[0] in c for c in connected_to_x) or any(y[1] in c for c in connected_to_x)))\
      or (type(y) != tuple and any(y in c for c in connected_to_x)):
        used[place] += [y]
        connected_to_x.append(y)
  return used