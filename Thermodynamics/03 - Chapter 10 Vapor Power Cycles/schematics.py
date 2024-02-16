from kilojoule.templates.default import *
import schemdraw
import schemdraw.elements as elm
from kilojoule.schemdraw import thermo
from kilojoule.schemdraw import flow

def rankine(**kwargs):
    with schemdraw.Drawing(**kwargs) as d:
        line_len = d.unit/4

        # Pump
        d += (pump := thermo.Pump().up().label('Pump',loc='center'))
        d += (pump_shaft := thermo.Shaft().right().at(pump.bottom))
        d += elm.Arrow().reverse().right().label('$w_{pump,in}$', ofst=(0,.25)).length(1)

        # Connect to Boiler (State 2)
        d += thermo.StateLabelInline(label='2').at(pump.exit).up(2*line_len)
        d += elm.Line().right(2*line_len)

        # Boiler
        d += (boiler := thermo.HX().label('Boiler',loc='bottom'))
        d += elm.Arrow().up(2*line_len).reverse().label('$q_{in}$').at(boiler.N)

        # High temperature reservoir
        d += (reservoir_H := flow.Ellipse().label('$T_H$'))

        # Connect to Turbine (State 3)
        d += thermo.StateLabelInline(label='3').right(2*line_len).at(boiler.E1)
        d += elm.Line().down().toy(pump.SE)

        # Vapor Turbine
        d += (turb := thermo.Turbine().anchor('intop').right().label('Turb.',loc='center',ofst=0))
        d += (turb_shaft := thermo.Shaft().right().at(turb.E))
        d += elm.Arrow().right().label('$w_{turb,out}$', ofst=(0,.25)).length(1)

        # Connect to Turbine (State 4)
        d += thermo.StateLabelInline(label=4).at(turb.out1).down(2*line_len)
        d += elm.Line().left().tox(boiler.E)

        # Condenser
        d += (cond := thermo.HX().anchor('E1')).label('Condenser',loc='top')
        d += elm.Arrow().down(2*line_len).label('$q_{out}$').at(cond.S)

        # Low temperature reservoir
        d += (reservoir_L := flow.Ellipse().label('$T_L$'))

        # Connect to Pump (State 1)
        d += elm.Line().at(cond.W1).tox(pump.inlet)
        d += thermo.StateLabelInline(label='1').to(pump.inlet)

        return d


def rankine_with_reheat(**kwargs):
    with schemdraw.Drawing(**kwargs) as d:
        line_len = d.unit/4

        # Pump
        d += (pump := thermo.Pump().up().label('Pump',loc='center'))
        d += (pump_shaft := thermo.Shaft().left().at(pump.N))
        d += elm.Arrow().reverse().left().label('$w_{pump,in}$', loc='bottom',ofst=(0,.25)).length(1)

        # Connect to Boiler (State 2)
        d += thermo.StateLabelInline(label='2',loc='top').at(pump.exit).up(2*line_len)
        d += elm.Line().right(3*line_len)

        # Boiler
        d += (boiler := thermo.HX(passes=2).label('Boiler',loc='bottom'))
        d += elm.Arrow().up(2*line_len).reverse().label('$q_{in}$').at(boiler.N)

        # High temperature reservoir
        d += (reservoir_H := flow.Ellipse().label('$T_H$'))

        # Connect to Turbine (State 3)
        d += thermo.StateLabelInline(label='3').right().at(boiler.E1)
        d += elm.Line().down(line_len)#.toy(pump.SE)

        # Turbines
        d += (turb_high := thermo.Turbine().anchor('intop').right().label('High P.\nTurb.',loc='center',ofst=0))
        d += (turb_high_shaft := thermo.Shaft(cut=False).right().at(turb_high.E))
        d += (turb_low := thermo.Turbine().anchor('W').label('Low P.\nTurb.',loc='center',ofst=0))
        d += (turb_low_shaft := thermo.Shaft().right().at(turb_low.E))
        d += elm.Arrow().right().label('$w_{turb,out}$', ofst=(0,.25)).length(1)

        # Connect High Pressure Turbine to Reheat (State 4)
        d += elm.Line().at(turb_high.out1).down(line_len)
        d += thermo.StateLabelInline(label='4').left(4*line_len)
        d += elm.Line().toy(boiler.E2)
        d += elm.Line().to(boiler.E2)

        # Connect Reheat to Low Pressure Turbine (State 5)
        d += elm.Line().left(line_len/2).at(boiler.W2)
        d += elm.Line().down(4.5*line_len)
        d += thermo.StateLabelInline(label='5').right().tox(turb_low.in2)
        d += elm.Line().to(turb_low.in2)

        # Low Pressure Turbine to Condenser (State 6)
        d += thermo.StateLabelInline(label='6').down(3.5*line_len).at(turb_low.out1)
        d += elm.Line().left().tox(boiler.E)

        # Condenser
        d += (cond := thermo.HX().anchor('E1')).label('Condenser',loc='top')
        d += elm.Arrow().down(2*line_len).label('$q_{out}$').at(cond.S)

        # Low temperature reservoir
        d += (reservoir_L := flow.Ellipse().label('$T_L$'))

        # Connect to Pump (State 1)
        d += elm.Line().at(cond.W1).tox(pump.inlet)
        d += thermo.StateLabelInline(label='1').to(pump.inlet)

        return d


def rankine_reheat_ofh_regen(**kwargs):
    with schemdraw.Drawing(**kwargs) as d:
        line_len = d.unit/4

        # Pump
        d += (pump_high := thermo.Pump().up().label('Pump',loc='center'))
        d += (pump_high_shaft := thermo.Shaft().left().at(pump_high.N))
        d += elm.Arrow().reverse().left().label('$w_{pump,in}$', loc='bottom',ofst=(0,.25)).length(1)

        # Connect to Boiler (State 2)
        d += thermo.StateLabelInline(label='2',loc='top').at(pump_high.exit).up(2*line_len)
        d += elm.Line().right(3*line_len)

        # Boiler
        d += (boiler := thermo.HX(passes=2).label('Boiler',loc='bottom'))
        d += elm.Arrow().up(2*line_len).reverse().label('$q_{in}$').at(boiler.N)

        # High temperature reservoir
        d += (reservoir_H := flow.Ellipse().label('$T_H$'))

        # Connect to Turbine (State 3)
        d += thermo.StateLabelInline(label='3').right().at(boiler.E1)
        d += elm.Line().down(line_len)#.toy(pump.SE)

        # Turbines
        d += (turb_high := thermo.Turbine().anchor('intop').right().label('High P.\nTurb.',loc='center',ofst=0))
        d += (turb_high_shaft := thermo.Shaft(cut=False).right().at(turb_high.E))
        d += (turb_low := thermo.Turbine().anchor('W').label('Low P.\nTurb.',loc='center',ofst=0))
        d += (turb_low_shaft := thermo.Shaft().right().at(turb_low.E))
        d += elm.Arrow().right().label('$w_{turb,out}$', ofst=(0,.25)).length(1)

        # Connect High Pressure Turbine to Reheat (State 4)
        d += elm.Line().at(turb_high.out1).down(line_len)
        d += thermo.StateLabelInline(label='4').left(4*line_len)
        d += elm.Line().toy(boiler.E2)
        d += elm.Line().to(boiler.E2)

        # Connect Reheat to Low Pressure Turbine (State 5)
        d += elm.Line().left(line_len/2).at(boiler.W2)
        d += elm.Line().down(4*line_len)
        d.push()
        d += thermo.StateLabelInline(label='5').right().tox(turb_low.in2)
        d += elm.Line().to(turb_low.in2)
        d.pop()
        d += elm.Line().right(2*line_len).label('$\dot{m}(1-y)$',halign='left')

        # Low Pressure Turbine to Condenser (State 6)
        d += thermo.StateLabelInline(label='6').down(6*line_len).at(turb_low.out1)
        d += elm.Line().left(line_len)

        # Condenser
        d += (cond := thermo.HX().anchor('E1')).label('Condenser',loc='top')
        d += elm.Arrow().down(2*line_len).label('$q_{out}$').at(cond.S)

        # Low temperature reservoir
        d += (reservoir_L := flow.Ellipse().label('$T_L$'))

        # Connect to Low Pressure Pump (State 1)
        d += thermo.StateLabelInline(label='1').at(cond.W1).left(line_len)

        # Low Pressure Pump
        d += (pump_low := thermo.Pump().left().label('Pump',loc='center').flip())
        d += (pump_low_shaft := thermo.Shaft().down().at(pump_low.bottom))
        d += elm.Arrow().reverse().down().label('$w_{pump,in}$', loc='bottom',ofst=(0,.25)).length(1)

        # Connect Low Pressure Pump to OFH
        d += thermo.StateLabelInline(label='2').at(pump_low.outlet).left(line_len)

        # Open Feedwater Heater
        d += (ofh := thermo.HX(h=2,w=2,passes=2,coils=False).anchor('E2').label('Open\nFWH',loc='center',valign='center'))

        # Connect Bleed-off to OFH
        d += elm.Line().at(turb_high.out1).down(line_len)
        d += elm.Line().down().toy(ofh.E1).label('$\dot{m}(y)$')
        d += thermo.StateLabelInline(label='4').to(ofh.E1)

        # Connect to High Pressure Pump (State 1)
        d += elm.Line().at(ofh.W).tox(pump_high.inlet)
        d += thermo.StateLabelInline(label='1').to(pump_high.inlet)

        return d

if __name__ == '__main__':
    rankine(file='Figures/Rankine.png')