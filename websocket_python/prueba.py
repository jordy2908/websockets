import numpy
# Recoger el número.
# Separar entero y decimal.
# Redondear y retornar decimal

# def s_num(num):
#     l = []
#     num = round(float(num), 2)
#     num = str(num)
#     num = num.split('.')

#     l.append(int(num[1]))
    
#     for i in reversed(num[0]):
#         l.append(int(i))

#     print(l)
        
# s_num(input('Introduce un número: '))

# Matrices

class cupo:
    table = numpy.zeros((6,10), int)

    def __init__(self):
        self.op()
        

    def op(self):
        op = input("Coge tu opcion: ")


        while True:
            if op == '1':
                self.asig()
                
            elif op == '2':
                self.dev()

            elif op == '3':
                fila = int(input("Fila: "))
                columna = int(input("Columna: "))                
                self.consult(fila, columna)

            elif op == '4':
                self.status()

            elif op == '5':
                print("Me la saco compa")
                exit()

            else:
                print("Introduce una de las opciones. Baboso")
                self.op()

            op = input("Coge tu opcion: ")

    def asig(self):
        matricula = int(input("Matricula: "))
        fila = input("Fila: ")
        columna = input("Columna: ")

        consulta = self.consult(fila, columna)

        if consulta == 0:
            self.table[int(fila)][int(columna)] = matricula

            print(self.table[int(fila)][int(columna)])
        else:
            print("Negativo pana, ocupado")


    def dev(self):
        fila = input("Fila: ")
        columna = input("Columna: ")

        consulta = self.consult(fila, columna)

        if consulta != 0:
            self.table[int(fila)][int(columna)] = 0

        else:
            print("Está vacío pana")
        

    def consult(self, fila, columna):

        dato = self.table[int(fila)][int(columna)]

        if dato != 0:
            print("Ocupado mi llave\n")

            return 1

        print("positivo para agregarte compa (Y)")

        return 0
    
    def status(self):
        cont = 0
        total = 0
        for i in range(len(self.table[0])):
            for x in range(len(self.table)):
                total += 1
                if self.table[x][i] != 0:
                    cont += 1

        print(f'{cont} usados de {total}')

    
cupo()
