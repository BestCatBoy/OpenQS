from SQS import Qbit, Qsystem
import string
from math import sqrt, pi

class Formula():
    """
    Initialize the formula

    Example:
    >>> f = Formula('ACD*bcD*aBd*AbC')
    """
    def __init__(self, form):
        Formula.__verify_form(form)
        self.__form = form

    @classmethod
    def __verify_form(cls, form):

        if not isinstance(form, str):
            raise TypeError(
        "Formula must be represented by the str data type")

        elif len(form) < 1:
            raise ValueError(
        "Number of conjunctions in the formula must not be equal to 0")

        elif len(set([i.lower() in f'{string.ascii_lowercase}*' for i in form])) != 1:
            raise SyntaxError(
        "Formula must contain only uppercase and lowercase letters of the Latin alphabet, as well as the multiplication sign")

        else:
            flst = [list(i) for i in form.split('*')]
            fset = list(set("".join(["".join([i.lower() for i in j])for j in flst])))

            if (max([string.ascii_lowercase.index(i) for i in fset]) + 1) != len(fset):
                raise SyntaxError(
            "Index of a variable in the Latin alphabet \
            must not exceed the number of literals")

    def grov(self):
        """
        Apply Grover's algorithm to the formula
        and get the probability that the formula is feasible, as a percentage
        """
        flst = [list(i) for i in self.__form.split('*')]
        fset = list(set("".join(["".join([i.lower() for i in j])for j in flst])))

        I = ['I' for i in range(len(fset))]
        for i in fset:
            I[string.ascii_lowercase.index(i)] = i
        fset = I

        qregln = len(fset)

        opsC = list()
        for i in [[string.ascii_lowercase.index(i.lower()) for i in j]for j in flst]:
            I = ['I' for i in range(len(fset))]
            for j in i:
                I[j] = '*'
            opsC.append("".join(I))
        opsX = list()

        for i in flst:
            I = ['I' for i in range(len(fset))]
            for j in range(len(i)):
                if i[j].islower():
                    I[string.ascii_lowercase.index(i[j])] = 'X'
            I = I[::-1]
            I.insert(0,'I')
            opsX.append(I)

        opsX = [[i]*2 for i in [('I'*len(flst))+i for i in["".join(i) for i in opsX]]]

        opsC_line = [[('I'*len(flst))[i:]+'X'+('I'*len(flst))[:i]for i in range(len(flst))][i]+opsC[i][::-1] for i in range(len(opsC))]
        for i in range(len(opsC_line)):
            opsX[i].insert(1,opsC_line[i])

        I = ['I' for i in range(len(opsX[0][0]))]
        opsF = []

        for i in range(len(opsX)-1):
            I = ['I' for i in range(len(opsX[0][0]))]
            ind = list(set([j for j in range(len(list(opsX[i][-1])))if list(opsX[i][-1])[j] == 'X'] +\
            [j for j in range(len(list(opsX[i+1][0])))if list(opsX[i+1][0])[j] == 'X']))
            for j in ind:
                I[j] = 'X'
            opsF.append("".join(I))

        oracle = [opsX[0][0]]

        i = j = y = 0
        while True:
            if i%2 == 0:
                oracle.append(opsC_line[j])
                j+=1
            else:
                oracle.append(opsF[y])
                y += 1
            if y == len(opsF) and j == len(opsC_line):
                oracle.append(opsX[-1][0])
                break
            else:
                i += 1

        for i in oracle:
            if set(i) == {'I'}:
                del oracle[oracle.index(i)]

        if '*' not in oracle[-1]:
            oracle[-1] = ('I'+'X'*len(flst) + oracle[-1][len('I'+'X'*len(flst)):])

        else:
            oracle.append('I'+'X'*len(flst) + 'I'*(len(oracle[-1])-(len(flst)+1)))

        oracle.append('X'+'*'*len(flst) + 'I'*(len(oracle[-1])-(len(flst)+1)))
        oracle.append('I'+'X'*len(flst) + 'I'*(len(oracle[-1])-(len(flst)+1)))

        init_conf = 'I'*(len(flst)+1) + 'X'*qregln
        init_conf = [init_conf,'I'*(len(flst)+1) + 'H'*qregln]

        diff_core = 'I'*(len(flst)+1) + 'Z' + '*'*(qregln-1)

        diff = []
        if len(flst) > 1:
            for i in range(5):
                if i in range(2):
                    diff.append(init_conf[i])
                elif i == 2:
                    diff.append(diff_core)
                else:
                    diff.append(init_conf[::-1][i-3])

        phase = 'Z' + 'I'*(len(flst)+qregln)

        sys = Qsystem([Qbit([complex(1,0),complex(0,0)]) for q in range(int(len(flst)+qregln+1))])

        # Grover 's algorithm
        [sys.gate(ops) for ops in init_conf]

        for i in range(round((pi/4) * (sqrt((2**len(fset))/1)))):

            [sys.gate(ops) for ops in oracle]
            sys.gate(phase)

            if i < round((pi/4) * (sqrt((2**len(fset))/1)))-1:

                [sys.gate(ops) for ops in oracle[::-1]]
                [sys.gate(ops) for ops in diff]

        return round((sum([sys.condition[p]**2 for p in range(int(len(sys.condition)/2),
    len(sys.condition))])*100).real,1)