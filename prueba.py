# Recoger el número.
# Separar entero y decimal.
# Redondear y retornar decimal

def s_num(num):
    l = []
    num = round(float(num), 2)
    num = str(num)
    num = num.split('.')

    l.append(int(num[1]))
    
    for i in num[0]:
        l.append(int(i))

    print(l)
        
s_num(44.5666)