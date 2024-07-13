# OpenQS
quantum simulations

Initialize the qubit:
>>> q = Qbit([complex(1,0), complex(0,0)])

    complex(1,0) -- the probability of a qubit collapsing into a state of 0
    complex(0,0) -- the probability of a qubit collapsing into a state of 1
    
Use gate:
>>> q.gate('H')

    'H' -- Hadamard Gate

Collapse the qubit to state 0 or state 1 with a probability corresponding to the state (condition)

>>> q.collapse()

Initialize the qubit system:
>>> qsys = Qsystem([q0,q1])

    q0, q1 -- objects of the Qbit data type

Apply a combination of operators to the qubit system:
>>> sys.gate('*$H*')

        sys -- qubit system
        *, $, H -- gates

 Collapse the system into one of the states with a probability corresponding to the condition of the system:
>>> sys.collapse()

        sys -- qubit system
