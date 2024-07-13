from math import sqrt, e, pi, log
import numpy as np
from random import random as rnd

class _Desk:

    def __init__(self, name):
        self.__name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value

class Qbit():
    """
    Initialize the qubit

    Example:
    >>> q = Qbit([complex(1,0), complex(0,0)])

    complex(1,0) -- the probability of a qubit collapsing into a state of 0
    complex(0,0) -- the probability of a qubit collapsing into a state of 1
    """

    # Operators
    Gates = {

        # Identifier
        'I': np.eye(2),

        # Pauli elements
        'X': np.matrix([
            [0, 1],
            [1, 0]]),

        'Y': np.matrix([
            [0, -1j],
            [1j, 0]]),

        'Z': np.matrix([
            [1, 0],
            [0,-1]]),

        # Hadamard element
        'H': (1/sqrt(2))*np.matrix([
            [1, 1],
            [1,-1]]),

        # 90 degree rotation
        'S': np.matrix([
            [1, 0],
            [0, 1j]]),

        # 45 degree rotation
        'T': np.matrix([
            [1,0],
            [0,e**((1j*pi)/4)]]),

        # Projection operators
        'P00': np.matrix([
            [1,0],
            [0,0]]),

        'P11': np.matrix([
            [0,0],
            [0,1]]),

        'E10': np.matrix([
            [0,0],
            [1,0]]),

        'E01': np.matrix([
            [0,1],
            [0,0]])}

    condition = _Desk('condition')
    def __init__(self, condition):

        self.condition = np.array(Qbit.__verify_condition(condition))

    @classmethod
    def __verify_condition(cls,condition):

        if len(condition) != 2:
            raise ValueError(
        "Qubit condition should be characterized by two basis vectors")

        elif len(set([isinstance(i,complex)for i in condition])) != 1:
            raise TypeError(
        "Basis vectors must have the data type complex")

        elif round(sum([(i**2).real + (i**2).imag for i in condition])) != 1:
            raise ValueError(
        "Sum of the squares of the basis vectors of the qubit should be equal to 1")

        else:
            return condition

    def gate(self, gate):
        """
        Apply a one-qubit operator to the state of a qubit (object)

        Example:
        >>> q.Gate('X')

        X -- operator
        """
        Qbit.__verify_gate(gate)
        self.condition = self.condition@Qbit.Gates[gate]

    @classmethod
    def __verify_gate(cls, gate):

        if not isinstance(gate, str):
            raise TypeError(
        "Operator must be represented by the str data type")

    def collapse(self):
        """
        Collapse the qubit to state 0 or state 1
        with a probability corresponding to the state (condition)

        Example:
        >>> q.collapse()
        """
        rand = rnd()
        p = [(i.real**2)+(i.imag**2) for i in self.condition]

        for cond, prob in enumerate(p):
            rand-= prob

            if rand < 0.0:
                break

        return '0'*(int(log(len(self.condition),2))-len(f'{cond:b}'))+f'{cond:b}'

class Qsystem(Qbit):
    """
    Initialize the qubit system

    Example:
    >>> qsys = Qsystem([q0,q1])

    q0, q1 -- objects of the Qbit data type
    """
    condition = _Desk('condition')
    def __init__(self, Qbits):

        Qsystem.__verify_condition(Qbits)

        self.condition = Qsystem.__create_tensor_system(
            [np.array([qbit.condition]) for qbit in Qbits]).ravel()

    @classmethod
    def __verify_condition(cls, condition):

        if set([isinstance(i,Qbit)for i in condition]) != {True}:
            raise TypeError(
        "Condition of the system should be represented by a list of objects having the Qbit data type")

    @classmethod
    def __verify_gate(cls, condition, gate):

        cls._Qbit__verify_gate(gate)

        if len(gate) != log(len(condition),2):
            raise SyntaxError(
        "Number of operators must be equal to the number of qubits in the qubit system")

    @classmethod
    def __create_tensor_system(cls,lst):

        while len(lst) >= 2:
            lst[-2] = np.kron(lst[-2], lst[-1])
            lst.pop()

        return np.array(lst)

    def gate(self, gate_form):

        """
        Apply a combination of operators to the qubit system

        Example:
        >>> sys.Gate('*$H*')

        sys -- qubit system
        *, $, H -- operators
        """
        Qsystem.__verify_gate(self.condition,gate_form)

        pxx = {
            '0': 'P00',
            '1': 'P11'}

        exx = {
            '1': 'E01',
            '0': 'E10'}

        def check_equality_moved_qubits(q1, q2):

            if q1 == q2:
                q1 = q2 = pxx[q1]

            else:
                q1, q2 = exx[q1], exx[q2]

            return q1,q2

        def format_ops(all_conds, Gates):

            all_conds = [i.split(' ')for i in set([' '.join(i)for i in all_conds])]
            ops = [[Gates[i]for i in j]for j in all_conds]

            return ops

        I_inds = [с for с, ltr in enumerate(gate_form) if ltr == "I"]
        C_inds = [с for с, ltr in enumerate(gate_form) if ltr == "*"]
        NC_inds = list(set([i for i in range(len(gate_form))]) - set(C_inds))
        Swap_inds = [с for с, ltr in enumerate(gate_form) if ltr == "$"]
        U_inds = list(set([i for i in range(len(gate_form))]) - set(Swap_inds) - set(C_inds) - set(I_inds))

        all_conds = [list(i)for i in['0'*(len(f'{2**len(gate_form)-1:b}')-
                len(str(f'{i:b}')))+
                f'{i:b}' for i in range(2**len(gate_form))]]

        if len(C_inds) == 0:

            if len(Swap_inds) == 0:

                ops = [[Qbit.Gates[i]for i in j]for j in list(gate_form)]
                self.condition = sum([Qsystem.__create_tensor_system(ops) for i in ops])@self.condition.ravel()
                self.condition = np.array([complex(round(v.real,5), round(v.imag,5)) for v in self.condition[0][0]]).ravel()

            else:

                all_conds = [list(i)for i in all_conds]
                U_inds = list(set([i for i in range(len(gate_form))]) - set(Swap_inds))

                for i in all_conds:
                    i[Swap_inds[0]], i[Swap_inds[1]] = check_equality_moved_qubits(i[Swap_inds[0]],i[Swap_inds[1]])

                    for j in U_inds:
                        i[j] = gate_form[j]

                ops = format_ops(all_conds, Qbit.Gates)
                self.condition = sum([Qsystem.__create_tensor_system(i) for i in ops])@self.condition.ravel()
                self.condition = np.array([complex(round(v.real,5), round(v.imag,5)) for v in self.condition[0]]).ravel()

        else:

            # Selection of the necessary conditions of the system from the vector 'all_conds'
            i = 0
            while i < len(all_conds):

                c_indexes = sum([int(all_conds[i][ind])for ind in C_inds])
                nc_indexes = sum([int(all_conds[i][ind])for ind in NC_inds])
                """
                if (c_indexes == 0 and i != 0) or \
                (c_indexes == gate_form.count('*')-1 and nc_indexes != gate_form.count('*')-1):
                    del all_conds[i]
                """
                if c_indexes != gate_form.count('*') and nc_indexes != gate_form.count('*'):
                    del all_conds[i]

                else:
                    i+=1

            # Replace system conditions with combinations of temporary operator mappings
            for i in all_conds:

                for j in C_inds:
                    i[j] = pxx[i[j]]

                if len(Swap_inds) != 0:

                    if len(set([i[j]for j in C_inds])) == 1 and set([i[j]for j in C_inds]) == {'P11'}:
                        i[Swap_inds[0]], i[Swap_inds[1]] = check_equality_moved_qubits(i[Swap_inds[0]],i[Swap_inds[1]])

                    else:
                        for y in NC_inds:
                            i[y] = 'I'

                if len(U_inds) != 0:

                    for j in U_inds:

                        if len(set([i[j]for j in C_inds])) == 1 and set([i[j]for j in C_inds]) == {'P11'}:
                            i[j] = gate_form[j]

                        else:
                            i[j] = 'I'

            for i in NC_inds:
                all_conds[0][i] = 'I'

            for i in all_conds:

                for j in I_inds:
                    i[j] = 'I'

            ops = format_ops(all_conds, Qbit.Gates)
            self.condition = sum([Qsystem.__create_tensor_system(i) for i in ops])@self.condition.ravel()
            self.condition = np.array([complex(round(v.real,5), round(v.imag,5)) for v in self.condition[0]])
        print(all_conds)
    def collapse(self):
        """
        Collapse the system into one of the states
        with a probability corresponding to the condition of the system

        Example:
        >>> sys.collapse()

        sys -- qubit system
        """
        return super().collapse()