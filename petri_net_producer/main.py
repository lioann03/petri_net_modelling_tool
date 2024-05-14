#!/usr/bin/env python3

import argparse
import math
import generator_general as pngen
import generator_component as gc
import generator_bridge as gb

DEF_TRANS = 30
DEF_DEG = 5

def parse_args():
    parser = argparse.ArgumentParser(description='Creates a Petri Net')
    parser.add_argument('filename')
    parser.add_argument('--transitions', type=int,nargs=1,help='Total Number of Transitions',default=DEF_TRANS)
    parser.add_argument('--max_degree', type=int,nargs=1,help='Max Degree',default=DEF_DEG)
    return vars(parser.parse_args())

def generate_petri_net(ptb,filename,num_trans,max_deg):
    ptb.set_total_trans(num_trans)
    ptb.set_degree(max_deg)
 
def find_existing_tokens(placement):   
    tokens = set()
    for tb in placement.values():
      if type(tb) == tuple:
        tokens.update(tb)
      else:
        tokens.add(tb)

def generate_component(cb,name,p,t,tok,bonds,out_tok,out_bonds,arcs,placement):
    cb.set_name(name)
    cb.set_places(p)
    cb.set_transitions(t)
    cb.set_tokens(find_existing_tokens(placement))
    cb.set_needed_tokens(tok)
    cb.set_needed_bonds(bonds)
    cb.set_out_tokens(out_tok)
    cb.set_out_bonds(out_bonds)
    cb.set_arcs(arcs)
    cb.set_placements(placement)
    #cb.component.print_component()



def main():
    args = parse_args()
    filename = args['filename']
    tot_transitions, = args['transitions']
    max_degree, = args['max_degree']
  
    
    ptb = pngen.Petri_Net_Builder()
    generate_petri_net(ptb,filename,tot_transitions,max_degree)

    # first component (0)
    cb0 = gc.ComponentBuilder()
    p0 = [pngen.Place('x0',pngen.Role.INIT), pngen.Place('x1',pngen.Role.MID), pngen.Place('x2',pngen.Role.FIN)]
    t0 = [pngen.Transition('t0')]
    tok0 = [pngen.Token('token1'),pngen.Token('token2'),pngen.Token('token3'),pngen.Token('token4')]
    
    arcs0: set[pngen.Arc] = set([])
    arcs0.add(pngen.Arc(tok0[0],p0[0],t0[0],pngen.ArcType.INCOMING))
    arcs0.add(pngen.Arc(tok0[1],p0[0],t0[0],pngen.ArcType.INCOMING))
    arcs0.add(pngen.Arc(tok0[2],p0[1],t0[0],pngen.ArcType.INCOMING))
    arcs0.add(pngen.Arc(tok0[3],p0[1],t0[0],pngen.ArcType.INCOMING))
    arcs0.add(pngen.Arc(tok0[0],p0[2],t0[0],pngen.ArcType.OUTCOMING))
    arcs0.add(pngen.Arc(tok0[1],p0[2],t0[0],pngen.ArcType.OUTCOMING))
    arcs0.add(pngen.Arc(tok0[2],p0[2],t0[0],pngen.ArcType.OUTCOMING))
    arcs0.add(pngen.Arc(tok0[3],p0[2],t0[0],pngen.ArcType.OUTCOMING))
    
    placement0: dict[pngen.Place,list[pngen.Token_Or_Bond]] = []
    placement0.append((p0[1],tok0[2]))
    placement0.append((p0[1],tok0[3]))

    needed_tok0 = tok0
    out_tok0 = tok0
    generate_component(cb0,0,p0,t0,needed_tok0,[],out_tok0,[],arcs0,placement0)
    
    cb1 = gc.ComponentBuilder()
    p1 = [pngen.Place('y0',pngen.Role.INIT), pngen.Place('y1',pngen.Role.FIN)]
    t1 = [pngen.Transition('t1'),pngen.Transition('t2'),pngen.Transition('t3')]
    tok1 = [pngen.Token('token1'),pngen.Token('token2'),pngen.Token('token3'),pngen.Token('token4')]
    
    arcs1: set[pngen.Arc] = set([])
    arcs1.add(pngen.Arc(tok1[0],p1[0],t1[1],pngen.ArcType.INCOMING))
    arcs1.add(pngen.Arc(tok1[1],p1[0],t1[1],pngen.ArcType.INCOMING))
    arcs1.add(pngen.Arc(tok1[2],p1[0],t1[2],pngen.ArcType.INCOMING))
    arcs1.add(pngen.Arc(tok1[3],p1[0],t1[2],pngen.ArcType.INCOMING))
    arcs1.add(pngen.Arc((tok1[0],tok1[1]),p1[1],t1[1],pngen.ArcType.OUTCOMING))
    arcs1.add(pngen.Arc((tok1[0],tok1[1]),p1[1],t1[2],pngen.ArcType.OUTCOMING))
    arcs1.add(pngen.Arc((tok1[0],tok1[1]),p1[1],t1[0],pngen.ArcType.INCOMING))
    arcs1.add(pngen.Arc((tok1[2],tok1[3]),p1[1],t1[0],pngen.ArcType.INCOMING))
    arcs1.add(pngen.Arc((tok1[0],tok1[1]),p1[0],t1[0],pngen.ArcType.OUTCOMING))
    arcs1.add(pngen.Arc((tok1[2],tok1[3]),p1[0],t1[0],pngen.ArcType.OUTCOMING))

    needed_tok1 = tok1
    out_bond1 = [(tok1[0],tok1[1]),(tok1[2],tok1[3])]
    generate_component(cb1,1,p1,t1,needed_tok1,[],[],out_bond1,arcs1,[])
    cb1.component.print_component()

    cb2 = gc.ComponentBuilder()
    p2 = [pngen.Place('z0',pngen.Role.INIT), pngen.Place('z1',pngen.Role.MID), pngen.Place('z2',pngen.Role.FIN)]
    t2 = [pngen.Transition('t4')]
    tok2 = [pngen.Token('token5'),pngen.Token('token6')]
    bond2 = [(pngen.Token('token1'),pngen.Token('token2')),(pngen.Token('token3'),pngen.Token('token4'))]

    arcs2: set[pngen.Arc] = set([])
    arcs2.add(pngen.Arc(bond2[0],p2[0],t2[0],pngen.ArcType.INCOMING))
    arcs2.add(pngen.Arc(bond2[1],p2[0],t2[0],pngen.ArcType.INCOMING))
    arcs2.add(pngen.Arc(tok2[0],p2[1],t2[0],pngen.ArcType.INCOMING))
    arcs2.add(pngen.Arc(tok2[1],p2[1],t2[0],pngen.ArcType.INCOMING))
    arcs2.add(pngen.Arc(bond2[0],p2[2],t2[0],pngen.ArcType.OUTCOMING))
    arcs2.add(pngen.Arc(bond2[1],p2[2],t2[0],pngen.ArcType.OUTCOMING))
    arcs2.add(pngen.Arc(tok2[0],p2[2],t2[0],pngen.ArcType.OUTCOMING))
    arcs2.add(pngen.Arc(tok2[1],p2[2],t2[0],pngen.ArcType.OUTCOMING))

    placement2: dict[pngen.Place,list[pngen.Token_Or_Bond]] = []
    placement2.append((p2[1],tok0[0]))
    placement2.append((p2[1],tok0[1]))

    needed_tok2 = bond2
    out_tok2 = tok2
    out_bond2 = bond2
    generate_component(cb2,2,p2,t2,needed_tok2,[],out_tok2,out_bond2,arcs2,placement2)
    #cb2.component.print_component()

    cb3 = gc.ComponentBuilder()
    p3 = [pngen.Place('w0',pngen.Role.INIT), pngen.Place('w1',pngen.Role.MID),\
        pngen.Place('w2',pngen.Role.MID), pngen.Place('w3',pngen.Role.FIN)]
    t3 = [pngen.Transition('t5'),pngen.Transition('t6'),pngen.Transition('t7')]
    bond3 = [(pngen.Token('token1'),pngen.Token('token2')),\
        (pngen.Token('token3'),pngen.Token('token4')),(pngen.Token('token5'),pngen.Token('token6')),\
        (pngen.Token('token2'),pngen.Token('token3')),(pngen.Token('token4'),pngen.Token('token5'))]

    arcs3: set[pngen.Arc] = set([])
    arcs3.add(pngen.Arc(bond3[0],p3[0],t3[0],pngen.ArcType.INCOMING))
    arcs3.add(pngen.Arc(bond3[1],p3[0],t3[0],pngen.ArcType.INCOMING))
    arcs3.add(pngen.Arc(bond3[0],p3[1],t3[0],pngen.ArcType.OUTCOMING))
    arcs3.add(pngen.Arc(bond3[1],p3[1],t3[0],pngen.ArcType.OUTCOMING))
    arcs3.add(pngen.Arc(bond3[2],p3[0],t3[1],pngen.ArcType.INCOMING))
    arcs3.add(pngen.Arc(bond3[2],p3[2],t3[1],pngen.ArcType.OUTCOMING))
    arcs3.add(pngen.Arc(bond3[0],p3[1],t3[2],pngen.ArcType.INCOMING))
    arcs3.add(pngen.Arc(bond3[1],p3[1],t3[2],pngen.ArcType.INCOMING))
    arcs3.add(pngen.Arc(bond3[2],p3[2],t3[2],pngen.ArcType.INCOMING))
    arcs3.add(pngen.Arc(bond3[0],p3[3],t3[2],pngen.ArcType.OUTCOMING))
    arcs3.add(pngen.Arc(bond3[1],p3[3],t3[2],pngen.ArcType.OUTCOMING))
    arcs3.add(pngen.Arc(bond3[2],p3[3],t3[2],pngen.ArcType.OUTCOMING))
    arcs3.add(pngen.Arc(bond3[3],p3[3],t3[2],pngen.ArcType.OUTCOMING))
    arcs3.add(pngen.Arc(bond3[4],p3[3],t3[2],pngen.ArcType.OUTCOMING))

    needed_bond3 = {bond3[0],bond3[1],bond3[2]}
    out_bond3 = bond3
    generate_component(cb3,3,p3,t3,[],needed_bond3,[],out_bond3,arcs3,[])
    #cb3.component.print_component()

    cb4 = gc.ComponentBuilder()
    bond4 = [(pngen.Token('token1'),pngen.Token('token2')),\
        (pngen.Token('token3'),pngen.Token('token4')),(pngen.Token('token5'),pngen.Token('token6')),\
        (pngen.Token('token2'),pngen.Token('token3')),(pngen.Token('token4'),pngen.Token('token5'))]
    t4 = [pngen.Transition('t8')]
    p4 = [pngen.Place('p0',pngen.Role.INIT),pngen.Place('p1',pngen.Role.FIN)]

    arcs4: set[pngen.Arc] = set([])
    arcs4.add(pngen.Arc(bond4[0],p4[0],t4[0],pngen.ArcType.INCOMING))
    arcs4.add(pngen.Arc(bond4[1],p4[0],t4[0],pngen.ArcType.INCOMING))
    arcs4.add(pngen.Arc(bond4[2],p4[0],t4[0],pngen.ArcType.INCOMING))
    arcs4.add(pngen.Arc(bond4[3],p4[0],t4[0],pngen.ArcType.INCOMING))
    arcs4.add(pngen.Arc(bond4[4],p4[0],t4[0],pngen.ArcType.INCOMING))
    arcs4.add(pngen.Arc(bond4[0],p4[0],t4[0],pngen.ArcType.OUTCOMING))
    arcs4.add(pngen.Arc(bond4[1],p4[0],t4[0],pngen.ArcType.OUTCOMING))
    arcs4.add(pngen.Arc(bond4[2],p4[0],t4[0],pngen.ArcType.OUTCOMING))
    arcs4.add(pngen.Arc(bond4[3],p4[0],t4[0],pngen.ArcType.OUTCOMING))
    arcs4.add(pngen.Arc(bond4[4],p4[0],t4[0],pngen.ArcType.OUTCOMING))
    arcs4.add(pngen.Arc(bond4[0],p4[1],t4[0],pngen.ArcType.INCOMING))
    arcs4.add(pngen.Arc(bond4[1],p4[1],t4[0],pngen.ArcType.INCOMING))
    arcs4.add(pngen.Arc(bond4[2],p4[1],t4[0],pngen.ArcType.INCOMING))
    arcs4.add(pngen.Arc(bond4[3],p4[1],t4[0],pngen.ArcType.INCOMING))
    arcs4.add(pngen.Arc(bond4[4],p4[1],t4[0],pngen.ArcType.INCOMING))

    needed_bond4 = bond4
    out_bond4 = bond4
    generate_component(cb4,4,p4,t4,[],needed_bond4,[],out_bond4,arcs4,set([]))

    cb5 = gc.ComponentBuilder()
    p5 = [pngen.Place('q0',pngen.Role.INIT), pngen.Place('q1',pngen.Role.MID), pngen.Place('q2',pngen.Role.FIN)]
    t5 = [pngen.Transition('t9'),pngen.Transition('t10')]
    tok5 = [pngen.Token('token1'),pngen.Token('token2'),pngen.Token('token3'),pngen.Token('token4'),\
        pngen.Token('token5'),pngen.Token('token6'),pngen.Token('token7'),pngen.Token('token8')]
    bond5 = [(tok5[0],tok5[1]),(tok5[2],tok5[3]),(tok5[4],tok5[5]),(tok5[6],tok5[7])]

    arcs5: set[pngen.Arc] = set([])
    arcs5.add(pngen.Arc(tok5[0],p5[0],t5[0],pngen.ArcType.INCOMING))
    arcs5.add(pngen.Arc(tok5[1],p5[0],t5[0],pngen.ArcType.INCOMING))
    arcs5.add(pngen.Arc(tok5[2],p5[0],t5[0],pngen.ArcType.INCOMING))
    arcs5.add(pngen.Arc(tok5[3],p5[0],t5[0],pngen.ArcType.INCOMING))
    arcs5.add(pngen.Arc(tok5[4],p5[1],t5[1],pngen.ArcType.INCOMING))
    arcs5.add(pngen.Arc(tok5[5],p5[1],t5[1],pngen.ArcType.INCOMING))
    arcs5.add(pngen.Arc(tok5[6],p5[1],t5[1],pngen.ArcType.INCOMING))
    arcs5.add(pngen.Arc(tok5[7],p5[1],t5[1],pngen.ArcType.INCOMING))
    arcs5.add(pngen.Arc(bond5[0],p5[2],t5[0],pngen.ArcType.OUTCOMING))
    arcs5.add(pngen.Arc(bond5[1],p5[2],t5[0],pngen.ArcType.OUTCOMING))
    arcs5.add(pngen.Arc(bond5[2],p5[2],t5[1],pngen.ArcType.OUTCOMING))
    arcs5.add(pngen.Arc(bond5[3],p5[2],t5[1],pngen.ArcType.OUTCOMING))

    placement5: dict[pngen.Place,list[pngen.Token_Or_Bond]] = []
    placement5.append((p5[1],tok5[4]))
    placement5.append((p5[1],tok5[5]))
    placement5.append((p5[1],tok5[6]))
    placement5.append((p5[1],tok5[7]))
    
    needed_tok5 = {tok5[0],tok5[1],tok5[2]}
    out_bond5 = bond5
    generate_component(cb5,5,p5,t5,needed_tok5,[],[],out_bond5,arcs5,placement5)

    cb6 = gc.ComponentBuilder()
    p6 = [pngen.Place('r0',pngen.Role.INIT_FIN)]
    t6 = [pngen.Transition('t11')]
    bond6 = [(pngen.Token('token1'),pngen.Token('token2')),\
        (pngen.Token('token3'),pngen.Token('token4')),(pngen.Token('token5'),pngen.Token('token6')),\
        (pngen.Token('token7'),pngen.Token('token8'))]

    arcs6: set[pngen.Arc] = set([])
    arcs6.add(pngen.Arc(bond6[0],p6[0],t6[0],pngen.ArcType.INCOMING))
    arcs6.add(pngen.Arc(bond6[1],p6[0],t6[0],pngen.ArcType.INCOMING))
    arcs6.add(pngen.Arc(bond6[2],p6[0],t6[0],pngen.ArcType.INCOMING))
    arcs6.add(pngen.Arc(bond6[3],p6[0],t6[0],pngen.ArcType.INCOMING))
    arcs6.add(pngen.Arc(bond6[0],p6[0],t6[0],pngen.ArcType.OUTCOMING))
    arcs6.add(pngen.Arc(bond6[1],p6[0],t6[0],pngen.ArcType.OUTCOMING))
    arcs6.add(pngen.Arc(bond6[2],p6[0],t6[0],pngen.ArcType.OUTCOMING))
    arcs6.add(pngen.Arc(bond6[3],p6[0],t6[0],pngen.ArcType.OUTCOMING))

    needed_bond6 = bond6
    out_bond6 = bond6
    generate_component(cb6,6,p6,t6,[],needed_bond6,[],out_bond6,arcs6,[])

if __name__ == '__main__':
    main()