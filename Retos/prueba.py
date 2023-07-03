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

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------

# Matrices

# class cupo:
#     table = numpy.zeros((6,10), int)

#     def __init__(self):
#         self.op()
        

#     def op(self):
#         op = input("Coge tu opcion: ")


#         while True:
#             if op == '1':
#                 self.asig()
                
#             elif op == '2':
#                 self.dev()

#             elif op == '3':
#                 fila = int(input("Fila: "))
#                 columna = int(input("Columna: "))                
#                 self.consult(fila, columna)

#             elif op == '4':
#                 self.status()

#             elif op == '5':
#                 print("Me la saco compa")
#                 exit()

#             else:
#                 print("Introduce una de las opciones. Baboso")
#                 self.op()

#             op = input("Coge tu opcion: ")

#     def asig(self):
#         matricula = int(input("Matricula: "))
#         fila = input("Fila: ")
#         columna = input("Columna: ")

#         consulta = self.consult(fila, columna)

#         if consulta == 0:
#             self.table[int(fila)][int(columna)] = matricula

#             print(self.table[int(fila)][int(columna)])
#         else:
#             print("Negativo pana, ocupado")


#     def dev(self):
#         fila = input("Fila: ")
#         columna = input("Columna: ")

#         consulta = self.consult(fila, columna)

#         if consulta != 0:
#             self.table[int(fila)][int(columna)] = 0

#         else:
#             print("Está vacío pana")
        

#     def consult(self, fila, columna):

#         dato = self.table[int(fila)][int(columna)]

#         if dato != 0:
#             print("Ocupado mi llave\n")

#             return 1

#         print("positivo para agregarte compa (Y)")

#         return 0
    
#     def status(self):
#         cont = 0
#         total = 0
#         for i in range(len(self.table[0])):
#             for x in range(len(self.table)):
#                 total += 1
#                 if self.table[x][i] != 0:
#                     cont += 1

#         print(f'{cont} usados de {total}')

    
# cupo()

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------

# Escriba una función validaid(cédula) que valide si un número de cédula ingresado es válido.
# Para validar una cédula de identidad ecuatoriana el proceso es el siguiente:

# Ejemplo:	0909407173
# El décimo es dígito verificador que se validará: 3 es el dígito verificador
# Se trabaja con los primeros 9 dígitos de la cédula: 090940717
# Cada dígito de posición impar se lo duplica, si el resultado es mayor que nueve se resta nueve: 090980515
# Se suman todos los resultados de posición impar: 0+0+8+5+5 = 18
# Se suman todos los dígitos de posición par: 9+9+0+1 = 19
# Se suman los dos resultados.: 18+19 = 37
# Se resta de la decena inmediata superior; en caso de ser 10, el resultado se vuelve a restar 10: 40 – 37 = 3
# Este es el verificador “calculado”: 3
# Si el dígito verificador es igual al verificador “calculado”, la cédula es válida, caso contrario es falsa: 3 = 3 Cédula válida

def validId(cedula):
    par = 0
    impar = 0

    validador = int(cedula[-1])

    for i in range((len(cedula))):
        if i % 2 != 0:
            par += int(cedula[i])
        elif i % 2 == 0:
            if int(cedula[i]) * 2 > 9:
                    impar -= 9
            impar += int(cedula[i]) * 2

    var = (par - int(cedula[-1])) + impar

    var_ = var - (var % 10) + 10

    r = var_ - var

    if r == validador:
        print("Positivo mijo")
    else:
        print("Negativo flaco")





validId(input("C.I: "))