import schemdraw
import schemdraw.elements as elm
from kilojoule.schemdraw import thermo
from schemdraw import flow

def refrigeration_cycle(labels={},**kwargs):
    '''Basic Refrigeration Cycle'''
    lbls={ # Default labels
        'q_out':'$\dot{Q}_{out}$',
        'q_in':'$\dot{Q}_{in}$',
        'w_in':'$\dot{W}_{in}$',
        'T_H':'$T_{H}$',
        'T_L':'$T_{L}$',
        'Condenser':'Condenser',
        'Evaporator':'Evaporator',
        'Compressor':'Comp.',
        'Throttle':'Throttle',
    }
    lbls.update(labels)

    with schemdraw.Drawing(**kwargs) as d:
        line_len = 1
        # Evaporator
        d += (evap := thermo.HX().label(lbls['Evaporator']))
        d += thermo.StateLabelInline().label('1').right().length(1.5*line_len)
        d += elm.Line().up(line_len)
        # Compressor
        d += (comp := thermo.Compressor().label(lbls['Compressor'],loc='center',valign='center').right().anchor('in1'))
        d += (comp_shaft := thermo.Shaft().right().at(comp.E))
        d += elm.Arrow().reverse().right().label(lbls['w_in']).length(line_len)
        d += elm.Line().up(2*line_len).at(comp.out1)
        d += thermo.StateLabelInline().label('2').left().tox(evap.E)
        # Condenser
        d += (cond := thermo.HX().label(lbls['Condenser'],loc='bottom').left())
        d += thermo.StateLabelInline().label('3').left(line_len)
        d += elm.Line().down(2*line_len)
        # Throttle
        d += thermo.Throttle().label(lbls['Throttle'])
        d += elm.Line().down().toy(evap.W)
        d += thermo.StateLabelInline().label('4').to(evap.W)
        # Q out
        d += elm.Arrow().up().length(line_len).at(cond.S).label(lbls['q_out'])
        d += flow.Ellipse().label(lbls['T_H'])
        # Q in
        d += elm.Arrow().down().reverse().length(line_len).at(evap.S).label(lbls['q_in'])
        d += flow.Ellipse().label(lbls['T_L'])

        return d


def refrigeration_multizone(labels={},file=None,**kwargs):
    '''Modified Refrigeration cycle with 2 coolings zone and one compressor'''
    lbls={ # Default labels
        'q_out':'$\dot{Q}_{out}$',
        'q_in_1':'$\dot{Q}_{in,1}$',
        'q_in_2':'$\dot{Q}_{in,2}$',
        'w_in':'$\dot{W}_{in}$',
        'T_H':'$T_H$',
        'T_L_1':'$T_{L,1}$',
        'T_L_2':'$T_{L,2}$',
        'Mixing Chamber':'Mixing\nChamber',
        'Condenser':'Condenser',
        'Evaporator 1':'Evaporator 1',
        'Evaporator 2':'Evaporator 2',
        'Compressor':'Comp.'
    }
    lbls.update(labels)

    with schemdraw.Drawing(file=file,**kwargs) as d:
        line_len = 0.5
        # Mixing chamber
        d += (mix := thermo.HX(coils=False,passes=2,width=.5).label(lbls['Mixing Chamber']))
        d += thermo.StateLabelInline().up(1).at(mix.NNW).label('1')
        # Compressor
        d += (comp := thermo.Compressor().right().anchor('in1').label(lbls['Compressor'],loc='center'))
        d += thermo.Shaft().right().at(comp.E)
        d += elm.Arrow().reverse().label(lbls['w_in']).length(2*line_len)
        d += elm.Line().at(comp.out1).up(2*line_len)
        d += thermo.StateLabelInline().left().label('2')
        # Condenser
        d += (cond := thermo.HX().anchor('E').label(lbls['Condenser'],loc='bottom'))
        d += elm.Arrow().up(2*line_len).label(lbls['q_out']).at(cond.N)
        d += flow.Ellipse().label(lbls['T_H'])
        d += thermo.StateLabelInline().label('3').at(cond.W).left()
        d += elm.Line().down(2)
        # Throttle 1
        d += thermo.Throttle()
        d += thermo.StateLabelInline().label('4').toy(mix.W)
        d.push()
        # Evap 2
        d += elm.Arrow().right(2*line_len)
        d += (evap2 := thermo.HX().label(lbls['Evaporator 2']).right())
        d += elm.Arrow().down(2*line_len).reverse().at(evap2.S).label(lbls['q_in_2'],loc='bottom')
        d += flow.Ellipse().label(lbls['T_L_2'])
        d += thermo.StateLabelInline().at(evap2.E).right(2*line_len).label('7')
        # Throttle
        d += thermo.Throttle().right()
        d += thermo.StateLabelInline().to(mix.W).label('8')
        # Throttle 2
        d.pop()
        d += elm.Arrow().down(2.5)
        d += thermo.Throttle()
        d += thermo.StateLabelInline().label('5').length(2)
        # Evap 1
        d += elm.Line().right(2.5)
        d += (evap1 := thermo.HX().label(lbls['Evaporator 1']))
        d += elm.Arrow().down(1).at(evap1.S).reverse().label(lbls['q_in_1'])
        d += flow.Ellipse().label(lbls['T_L_1'])
        d += thermo.StateLabelInline().label('6').at(evap1.E).tox(mix.SSW)
        d += elm.Line().up().to(mix.SSW)

        return d



def refrigeration_2_stage_compression(labels={},**kwargs):
    """Modified refrigeration cycle with 2 compression stages"""
    lbls={ # Default labels
        'q_out':'$\dot{Q}_{out}$',
        'q_in':'$\dot{Q}_{in}$',
        'w_in_1':'$\dot{W}_{in,1}$',
        'w_in_2':'$\dot{W}_{in,2}$',
        'T_H':'$T_{H}$',
        'T_L':'$T_{L}$',
        'Mixing Chamber':'Mixing\nChamber',
        'Flash Chamber':'Flash\nChamber',
        'Condenser':'Condenser',
        'Evaporator':'Evaporator',
        'Compressor 1':'Comp. 1',
        'Compressor 2':'Comp. 2',
    }
    lbls.update(labels)

    with schemdraw.Drawing(**kwargs) as d:
        # Evaporator
        d += (evaporator := thermo.HX().label(lbls['Evaporator']))
        d += elm.Arrow().down(1).reverse().label(lbls['q_in']).at(evaporator.S)
        d += flow.Ellipse().label(lbls['T_H'])
        # State 1
        d += thermo.StateLabelInline().label('1').at(evaporator.E).right(2)
        d += elm.Arrow().up(1)
        # Compressor 1
        d += (compressor1 := thermo.Compressor().label(lbls['Compressor 1'],loc='center').anchor('in1').right())
        d += (compressor1_shaft := thermo.Shaft().right().at(compressor1.E))
        d += elm.Arrow().right(1).reverse().label(lbls['w_in_1'],halign='left')
        # State 2
        d += thermo.StateLabelInline().label('2').up(1.5).at(compressor1.out1)
        # Mixing Chamber
        d += (mix := thermo.HX(coils=False,passes=2).anchor('SSE').label(lbls['Mixing Chamber']))
        # State 9
        d += thermo.StateLabelInline().label('9').up(1).at((compressor1.in1.x,mix.NNW.y))
        # Compressor 2
        d += (compressor2 := thermo.Compressor().right().anchor('in1').label(lbls['Compressor 2'],loc='center'))
        d += (compressor2_shaft := thermo.Shaft().right().at(compressor2.E))
        d += elm.Arrow().right(1).reverse().label(lbls['w_in_2'],halign=('left'))
        # State 4
        d += elm.Line().up(2).at(compressor2.out1)
        d += thermo.StateLabelInline().label('4').left().tox(evaporator.E)
        # Condenser
        d += (condenser := thermo.HX().anchor('E').label(lbls['Condenser'],loc='bottom'))
        d += elm.Arrow().up(1).label(lbls['q_out']).at(condenser.N)
        d += flow.Ellipse().label(lbls['T_H'])
        # State 5
        d += (state5 := thermo.StateLabelInline().label('5').left(2).at(condenser.W))
        # Throttle 1
        d += (throttle1 := thermo.Throttle().at((state5.end.x,compressor2.center.y)).anchor('center').down())
        d += elm.Arrow().at(state5.end).to(throttle1.inlet)
        # State 6
        d += thermo.StateLabelInline().label('6').at(throttle1.outlet).down().toy(mix.N)
        # Flash Chamber
        d += (flash := thermo.HX(passes=2, coils=False).anchor('NNW').label(lbls['Flash Chamber']))
        # State 3
        d += thermo.StateLabelInline().right().at(flash.E).to(mix.W).label('3')
        # Throttle 2
        d += (throttle2 := thermo.Throttle().at((throttle1.center.x,compressor1.center.y)).anchor('center').down())
        d += thermo.StateLabelInline().label('7').at(flash.SSW).to(throttle2.inlet)
        # State 8
        d += thermo.StateLabelInline().at(throttle2.outlet).down().toy(evaporator.E).label('8')
        d += elm.Arrow().to(evaporator.W)

        return d