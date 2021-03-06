import sys
import math, cmath


yotta = 1000000000000000000000000
zetta = 1000000000000000000000
exa =  1000000000000000000
peta = 1000000000000000
tera = 1000000000000         #
giga = 1000000000          #
mega = 1000000          #
kilo = 1000          #
hecto = 100       #
deca = 10       #
deci = 0.1     #
centi = 0.01      #
milli = 0.001       #
micro = 0.00001       #
nano = 0.00000001        #
pico = 0.000000000001      #
femto = 0.000000000000001    #
atto = 0.000000000000000001    #
zepto = 0.000000000000000000001 #
yocto = 0.000000000000000000000001

pi = 3.14159
Vbe= 0.7 # volts

scale_converter_unit_list = {"mega"  : mega  , "kilo" : kilo , "hecto" : hecto , \
                             "deca"  : deca  , "deci" : deci , "milli" : milli ,\
                             "micro" : micro , "pico" : pico , "nano"  : nano }

def scale_converter(unit_num : list):
    """
    This function is used to convert numbers input by the user to something the
    Program can understand. It allows the user to say, for example :

    jazzy_prompt #> 150 milli volts * 200 milli amps

    unit_num : list
        { unit , number }

    Example:
        user_input = { 'milli' , 20 }
        scale_converter(user_input)

    """
    unit   = unit_num[0]
    number = unit_num[1]
    if unit in scale_converter_unit_list:
        return number * scale_converter_unit_list.get(unit)

class Resistor():
    '''
    Required inputs:
    resistance      : list
    current         : list
    voltage         : list
    e.g :        
        (unit, number)
            unit   : str
            number : int OR float

    '''
    def __init__ (self, resistance : list , current : list, voltage : list):
        
        if (voltage and current)      and (isinstance(voltage , list) and isinstance(current, list)):
            #solve for resistance
            self.voltage      = scale_converter((voltage[0]     , voltage[1]))
            self.current      = scale_converter((current[0]     , current[1]))
            self.resistance   = self.voltage / self.current

        elif (voltage and resistance) and (isinstance(voltage   , list) and isinstance(resistance, list)):
            #solve for current
            self.resistance   = scale_converter((resistance[0]  , resistance[1]))
            self.voltage      = scale_converter((voltage[0]     , voltage[1]))
            self.current      = self.voltage / self.resistance

        elif (resistance and current) and (isinstance(resistance , list) and isinstance(current, list)):
            #solve for voltage
            self.resistance   = scale_converter((resistance[0]  , resistance[1]))
            self.current      = scale_converter((current[0]     , current[1]))
            self.voltage      = self.resistance * self.current

        else:
            #shit went wrong
            reply_to_query("user input sopmething wrong")

        self.loss         = self.voltage^2 / self.resistance


class Inductor():
    '''
    v = L * dI/dT

    v     = instantaneous voltage
    L     = Inductance ( in Henries)
    dI/dT = rate of current change (amps/second)

    In DC applications, an inductor works like a short circuit.
    So we assume all inputs to be a "snapshot" of the circuit at any given moment

    This object will be used in loops for SIMULATION
    This object can be used alone for node analysis.

    inputs:
    inductance    : list
        { unit_of_measure , value }

    current       : list
        { unit_of_measure , value }
   
    voltage       : list
        { unit_of_measure , value }

    frequency     : list
        default = 0
        { unit_of_measure , value }

    dc_resistance : list
        default = 0
        optional
        { unit_of_measure , value }

        physical resistance of the conductor material.

    '''
    def __init__ (self, inductance, delta_current, voltage, frequency = 0.0 , dc_resistance = 0.0):
        if (voltage and delta_current)      and (isinstance(voltage , list) \
                                            and isinstance(delta_current, list)):
            #solve for inductance
            self.voltage      = scale_converter((voltage[0]     , voltage[1]))
            self.current      = scale_converter((delta_current[0]     , delta_current[1]))
            self.inductance   = self.voltage / self.current

        elif (voltage and inductance)       and (isinstance(voltage   , list) \
                                            and isinstance(inductance, list)):
            #solve for current
            self.inductance   = scale_converter((inductance[0]  , inductance[1]))
            self.voltage      = scale_converter((voltage[0]     , voltage[1]))
            self.current      = self.voltage / self.inductance

        elif (inductance and delta_current) and (isinstance(inductance, list) \
                                            and isinstance(delta_current, list)):
            #solve for voltage, given inductance and current plus initial current at time = 0
            self.inductance   = scale_converter((inductance[0]    , inductance[1]))
            self.current      = scale_converter((delta_current[0] , delta_current[1]))
            self.voltage      = self.inductance * self.delta_current

        else:
            #shit went wrong
            reply_to_query("user input sopmething wrong")

        self.inductance    = inductance
        self.current       = current
        self.voltage       = voltage
        self.frequency     = frequency
        self.dc_resistance = dc_resistance
        self.stored_e      = 1.0/2.0 * (inductance * current^2.0)
        self.reactance     = 2.0 * pi * self.frequency * self.inductance
        # requires DC resistance of inductor material
        if self.dc_resistance != 0.0 : 
            self.qfactor = self.reactance / self.dc_resistance


class Capacitor():
    def __init__(self, capacitance, voltage, frequency):
        self.capacitance    = capacitance
        self.voltage        = voltage
        self.frequency      = frequency
        self.charge_ratio   = self.capacitance * self.voltage
        self.efield_energy  = 1/2 * voltage * self.charge_ratio
        self.reactance      = -(1/(2 * pi * self.frequency * self.capacitance))
        self.impedance      = -(1j/(2 * pi * self.frequency * self.capacitance))



class RL_Circuit():
    def __init__(self, resistance , inductance , frequency, voltage_in, series = 1, parallel = 0 ):
        self.resistance        = resistance
        self.inductance        = inductance
        self.frequency         = frequency
        self.voltage_in        = voltage_in
        self.complex_frequency = 1j * (2 * pi * self.frequency)
        self.complex_impedance = self.inductance * self.complex_frequency

class LC_circuit():
    def __init__(self, inductance, capacitance, voltage, current = 0,  series = 1, parallel = 0):
        '''
        LC circuit calculator.
            LC_circuit(inductance , capactitance, voltage, current = 0, series = 1, parallel = 0)
        REQUIRED parameters are inductance, capacitance, and voltage.
        Booleans required for the others, don't XOR yourself
        '''
        self.inductance               = inductance
        self.capacitance              = capacitance
        self.voltage                  = voltage
        self.current                  = current
        self.resonant_frequency_hertz = 1/(2 * pi * math.sqrt(self.inductance * self.capacitance))
        self.resonant_frequency_w     = math.sqrt(1/(self.inductance * self.capacitance))
        if series:
            self.impedance = ((math.pow(self.resonant_frequency_w , 2) * self.inductance * self.capacitance - 1)*\
                                          1j) / (self.resonant_frequency_w * self.capacitance)
        elif parallel:
            self.impedance            = (-1j * self.resonant_frequency_w * self.inductance)/ \
                                        (math.pow(self.resonant_frequency_w , 2) * \
                                        self.inductance * self.capacitance -1)
        else:
            print("AGGGGHHHHH MY LC_circuit IS BURNING AGHHHHHHH!!!")

class Transistor_NPN():
    def __init__ (self, gain , current_in, voltage_in,frequency, resistor1, resistor2, resistor3):
        """
        Transistor_NPN(gain,current_in, voltage_in, frequency, res1, res2, res3))
        The resistors are as follows, r1 is collector, r2 is base, r3 is emitter
        REQUIRED parameters are current, voltage, resistors 1-3
        """

        self.gain             = gain
        self.current_in       = current_in
        self.voltage_in       = voltage_in
        self.basecurrent      = (voltage_in - Vbe) / self.resistor2.resistance
        self.emittercurrent   = (voltage_in - Vbe) / (self.resistor2.resistance/gain)
        self.collectorcurrent = self.basecurrent - self.emittercurrent
        self.DCcurrentGain    = self.collectorcurrent / self.basecurrent
        self.emitteralpha     = self.collectorcurrent / self.emittercurrent
        self.resistor1        = Resistor(resistor1) # collector
        self.resistor2        = Resistor(resistor2) # base
        self.resistor3        = Resistor(resistor3) # emitter

    
    #def Validate_user_input(self, gain , current_in, voltage_in,frequency, resistor1, resistor2, resistor3):
    #    self.gain           = gain
    #    self.current_in     = current_in
    #    self.voltage_in     = voltage_in
    #    self.DCcurrentGain  = self.collectorcurrent / self.basecurrent
    #    self.emitteralpha   = self.collectorcurrent / self.emittercurrent
    #    self.resistor1      = Resistor(resistor1) # collector
    #    self.resistor2      = Resistor(resistor2) # base
    #    self.resistor3      = Resistor(resistor3) # emitter
    #    self.basecurrent    = (voltage_in - Vbe) / self.resistor2.resistance
    #    self.emittercurrent = (voltage_in - Vbe) / (self.resistor2.resistance/gain)


class RLC_circuit():
    def _init_(self, resistance, inductance, capacitance, voltage, current, frequency ):

        self.resistance               = resistance
        self.inductance               = inductance
        self.capacitance              = capacitance
        self.voltage                  = voltage
        self.current                  = current
        self.resonant_frequency_w = 2 * pi * frequency
        if series:
            self.attenuation = self.resistance / 2 * self.inductance
            self.resonant_frequency = 1/(math.sqrt(self.inductance * self.capacitance))
            self.damping_factor = (self.resistance/2) * (math.sqrt(self.capacitance * self.inductance))
            self.q_factor = 1/self.resistance * math.sqrt(self.inductance/self.capacitance)
            self.bandwidth = 2 * self.attenuation / self.resonant_frequency
            if self.damping_factor < 1:
                self.underdamped = 1
            elif self.damping_factor > 1:
                self.overdamped = 1
            else:
                print("you managed to make a number that is neither greater than or less than or even equal to 1 ... GOOD JOB!")
        elif parallel:
            self.attenuation = 1 / (2 * self.resistance * self.capacitance)
            self.damping_factor = (1/(2 * self.resistance))* math.sqrt(self.inductance / self.capacitance)
            self.q_factor = self.resistance * math.sqrt(self.capacitance/self.inductance)
            self.bandwidth = (1/ self.resistance) * math.sqrt(self.inductance/self.capacitance)
            self.frequency_domain = 1/(1j * self.resonant_frequency * self.inductance) + 1j * \
                                    self.resonant_frequency * self.capacitance + 1/self.resistance
            if self.damping_factor < 1:
                self.underdamped = 1
            elif self.damping_factor > 1:
                self.overdamped = 1
            else:
                print("you managed to make a number that is neither greater than or less than or even equal to 1 ... GOOD JOB!")


