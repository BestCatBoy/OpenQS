from SQS import Qbit, Qsystem
from SAT import Formula
from tkinter import *
from threading import Thread

sys = None

def sim_form():

    def new_thread_init():

        t = Thread(target = init)
        t.start()

    def new_thread_apply():

        t = Thread(target = apply)
        t.start()

    def new_thread_collapse_():

        t = Thread(target = collapse_)
        t.start()

    def init():

        global sys

        sim.title("Загрузка...")

        try:
            sys = Qsystem([Qbit([complex(1,0),complex(0,0)]) if i == '0'
                else Qbit([complex(0,0),complex(1,0)]) if i == '1'
                else i
                for i in RegisterInput.get()])

        except:
            error()

        else:
            register_output()

        sim.title("Симулятор")

    def apply():

        sim.title("Загрузка...")

        try:
            sys.gate(RegisterInput.get())

        except:
            error()

        else:
            register_output()

        sim.title("Симулятор")

    def register_output():

        global sys

        RegisterInput.delete(0, END)
        RegisterOutput.delete(1.0, END)

        for cond in range(len(sys.condition)):
            RegisterOutput.insert(float(cond+1), f'{sys.condition[cond]}\n')

    def collapse_():

        global sys

        sim.title("Загрузка...")

        try:
            CollapseOutput.insert(END, f'{sys.collapse()}\n')
        except:
            error()

        sim.title("Симулятор")

    def clear():

        RegisterInput.delete(0, END)
        CollapseOutput.delete(1.0, END)
        RegisterOutput.delete(1.0, END)
        sys = None

    def Help_():

        Help = Tk()

        screenwidth = Help.winfo_screenwidth()
        screenheight = Help.winfo_screenheight()
        Help.geometry('%dx%d+%d+%d'%(325, 346, (screenwidth-325)/2, (screenheight-346)/2))
        Help.title("Помощь")

        Help.iconbitmap('Qicon.ico')

        HelpLabel = Label(Help, text =
'''Поле Ввод принимает регистр кубитов и инициализирует
его в систему посредством соответствующей кнопки.
Регистр должен включать в себя 1 или 0. В противном
случае инициализация не произойдёт.

Также поле Ввод принимает регистр логических
операторов (гейтов) и применяет их к
инициализированной системе посредством нажатия
на соответствующую кнопку. Регистр должен
включать в себя доступные операторы и равняться
количеству кубитов в инициализированной системе.

Кнопка Измерить коллапсирует состояние системы в
набор классических битов с вероятностью,
соответствующей этому состоянию.

Пример регистра кубитов:
001100100

Пример регистра операторов:
HX*$$Y*ST''',
anchor='w', justify='left')
        HelpLabel.grid(column = 0, row = 0)

        Close = Button(Help, width = 45, text = "Закрыть", command = lambda: Help.destroy())
        Close.grid(column = 0, row = 1)
        Close.place(x = 0, y = 320)

    def back():

        global sys

        sys = None
        sim.destroy()
        main_form()

    sim = Tk()

    def error():

        RegisterInput.delete(0, END)

        error = Tk()

        screenwidth = error.winfo_screenwidth()
        screenheight = error.winfo_screenheight()
        error.geometry('%dx%d+%d+%d'%(227, 186, (screenwidth-227)/2, (screenheight-186)/2))
        error.title("Ошибка")

        error.iconbitmap('Qicon.ico')

        ErrorLbl = Label(error, text = "Неподдерживаемый формат записи")
        ErrorLbl.grid(column = 0, row = 0)
        ErrorLbl.place(x = 11, y = 70)

        Close = Button(error, width = 31, text = "Закрыть", command = lambda: error.destroy())
        Close.grid(column = 0, row = 1)
        Close.place(x = 0, y = 160)

        error.mainloop()

    screenwidth = sim.winfo_screenwidth()
    screenheight = sim.winfo_screenheight()
    sim.geometry('%dx%d+%d+%d'%(434, 199, (screenwidth-434)/2, (screenheight-199)/2))
    sim.title("Симулятор")

    sim.iconbitmap('Qicon.ico')

    CollapseColumn = Label(sim, text = "Измерения")
    CollapseColumn.grid(column = 0, row = 0)

    RegisterColumn = Label(sim, text = "Состояние")
    RegisterColumn.grid(column = 1, row = 0)

    InputColumn = Label(sim, text = "Ввод")
    InputColumn.grid(column = 2, row = 0)

    CollapseOutput = Text(sim, width = 19, height = 11)
    RegisterOutput = Text(sim, width = 19, height = 11)

    scrollReg = Scrollbar(command = RegisterOutput.yview)
    scrollCol = Scrollbar(command = CollapseOutput.yview)

    CollapseOutput.config(yscrollcommand = scrollCol.set)
    CollapseOutput.grid(column = 0, row = 1, rowspan = 8)

    RegisterOutput.config(yscrollcommand = scrollReg.set)
    RegisterOutput.grid(column = 1, row = 1, rowspan = 8)

    RegisterInput = Entry(sim, width = 19)
    RegisterInput.grid(column = 2, row = 1)

    Init = Button(sim, width = 16, text = "Инициализировать", command = new_thread_init)
    Init.grid(column = 2, row = 2)

    Apply = Button(sim, width = 16, text = "Применить", command = new_thread_apply)
    Apply.grid(column = 2, row = 3)

    Collapse = Button(sim, width = 16, text = "Измерить", command = new_thread_collapse_)
    Collapse.grid(column = 2, row = 4)

    Clear = Button(sim, width = 16, text = "Очистить", command = clear)
    Clear.grid(column = 2, row = 5)

    Help = Button(sim, width = 16, text = "Помощь", command = Help_)
    Help.grid(column = 2, row = 6)

    Back = Button(sim, width = 16, text = "Назад", command = back)
    Back.grid(column = 2, row = 7)

    sim.mainloop()

def SAT_form():

    def new_thread():

        ResultOutput.config(text = 'Загрузка...')

        t = Thread(target = output)
        t.start()

    def output():

        try:
            ResText = f'Выполнима с вероятностью {Formula(FormulaInput.get()).grov()} %'

        except:
            ResText = "Неподдерживаемый формат записи"
            FormulaInput.delete(0,END)

        ResultOutput.config(text = ResText)

    def clear():

        FormulaInput.delete(0, END)
        ResultOutput.config(text = '')

    def Help_():

        Help = Tk()

        screenwidth = Help.winfo_screenwidth()
        screenheight = Help.winfo_screenheight()
        Help.geometry('%dx%d+%d+%d'%(325, 154, (screenwidth-325)/2, (screenheight-154)/2))
        Help.title("Помощь")

        Help.iconbitmap('Qicon.ico')

        HelpLabel = Label(Help, text =
'''Данный алгоритм принимает логическую формулу и
возвращает вероятность того, что эта формула является
выполнимой (даёт 1 в ответе). В формуле не должно
присутствовать других символов, кроме латинских букв
нижнего и верхнего регистров, а также знака *.

Пример формулы:
ACD*bcD*aBd*AbC''',
anchor='w', justify='left')
        HelpLabel.grid(column = 0, row = 0)

        Close = Button(Help, width = 45, text = "Закрыть", command = lambda: Help.destroy())
        Close.grid(column = 0, row = 1)
        Close.place(x = 0, y = 128)


    def back():

        SAT.destroy()
        main_form()

    SAT = Tk()

    screenwidth = SAT.winfo_screenwidth()
    screenheight = SAT.winfo_screenheight()
    SAT.geometry('%dx%d+%d+%d'%(233, 180, (screenwidth-233)/2, (screenheight-180)/2))
    SAT.title("SAT")

    SAT.iconbitmap('Qicon.ico')

    TipLabel = Label(SAT, text = "Формула: ")
    TipLabel.grid(column = 0, row = 0, sticky = W)

    FormulaInput = Entry(SAT, width = 38)
    FormulaInput.grid(column = 0, row = 1)

    ResultOutput = Label(SAT, height = 2)
    ResultOutput.grid(column = 0, row = 2)

    StartGrover = Button(SAT, width = 32, text = "Рассчитать", command = new_thread)
    StartGrover.grid(column = 0, row = 3)

    Clear = Button(SAT, width = 32, text = "Очистить", command = clear)
    Clear.grid(column = 0, row = 4)

    Help = Button(SAT, width = 32, text = "Помощь", command = Help_)
    Help.grid(column = 0, row = 5)

    Back = Button(SAT, width = 32, text = "Назад", command = back)
    Back.grid(column = 0, row = 6)

    SAT.mainloop()

def main_form():

    def sim():

        main.destroy()
        sim_form()

    def SAT():

        main.destroy()
        SAT_form()

    main = Tk()
    screenwidth = main.winfo_screenwidth()
    screenheight = main.winfo_screenheight()
    main.geometry('%dx%d+%d+%d'%(233, 78, (screenwidth-233)/2, (screenheight-78)/2))
    main.title("Главная")

    main.iconbitmap('Qicon.ico')

    Simulator = Button(main, width = 32, text = "Открыть симулятор", command = sim)
    Simulator.grid(column = 0, row = 0)

    SAT = Button(main, width = 32, text = "Рассчитать SAT", command = SAT)
    SAT.grid(column = 0, row = 1)

    CloseForm = Button(main, width = 32, text = "Закрыть", command = lambda: main.destroy())
    CloseForm.grid(column = 0, row = 2)

    main.mainloop()

main_form()