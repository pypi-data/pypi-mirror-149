# 4олшемди алгебралар модули

# Aвтор - Актоты

from math import sqrt

c = [0, 0, 0, 0]


# Еки 4 олшемди санды косу
def qosu(list1,list2):
    add = list()
    for i in range(len(list1)):
        item = list1[i] + list2[i]
        add.append(item)
    return add

# Еки 4 олшемди сан айырмасы
def alu(list1,list2):
    substract = list()
    for i in range(len(list1)):
        item = list1[i] - list2[i]
        substract.append(item)
    return substract

# Еки 4 олшемди санды кобейту
def kobeytu(list1,list2):
    result = list()
    z1 = (list1[0]*list2[0]) - (list1[1]*list2[1]) + (list1[2]*list2[2]) - (list1[3]*list2[3])
    z2 = (list1[0]*list2[1]) + (list1[1]*list2[0]) + (list1[2]*list2[3]) + (list1[3]*list2[2])
    z3 = (list1[0]*list2[2]) - (list1[1]*list2[3]) + (list1[2]*list2[0]) - (list1[3]*list2[1])
    z4 = (list1[0]*list2[3]) + (list1[1]*list2[2]) + (list1[2]*list2[1]) + (list1[3]*list2[0])
    result.append(z1)
    result.append(z2)
    result.append(z3)
    result.append(z4)
    return result

# Еки 4 олшемди санды болу
def bolu(a, b):
    if (((b[0] + b[2]) ** 2 + (b[1] + b[3]) ** 2) *
        ((b[0] - b[2]) ** 2 + (b[1] - b[3]) ** 2) <= 0):
        return ("Екинши сан айкын емес, болуге келмейди")
    d = [0, 0, 0, 0]
    d[0] = ((b[0] + b[2]) / ((b[0] + b[2]) ** 2 + (b[1] + b[3]) ** 2) +
           (b[0] - b[2]) / ((b[0] - b[2]) ** 2 + (b[1] - b[3]) ** 2)) / 2
    d[1] = -((b[1] + b[3]) / ((b[0] + b[2]) ** 2 + (b[1] + b[3]) ** 2) +
            (b[1] - b[3]) / ((b[0] - b[2]) ** 2 + (b[1] - b[3]) ** 2)) / 2
    d[2] = ((b[0] + b[2]) / ((b[0] + b[2]) ** 2 + (b[1] + b[3]) ** 2) -
            (b[0] - b[2]) / ((b[0] - b[2]) ** 2 + (b[1] - b[3]) ** 2)) / 2
    d[3] = -((b[0] + b[2]) / ((b[0] + b[2]) ** 2 + (b[1] + b[3]) ** 2) -
            (b[0] - b[2]) / ((b[0] - b[2]) ** 2 + (b[1] - b[3]) ** 2)) / 2
    c = kobeytu(a, d)
    return c

# 4 олшемди сан нормасы
def norma(list1):
    result = (((((list1[0]+list1[2])**2)+ ((list1[1]+list1[3])**2)) **0.5) + ((((list1[0]-list1[2])**2)+ ((list1[1]-list1[3])**2)) **0.5)) *0.5
    return result


# 4 олшемди сан модули
def abs4d(a):
    return (((a[0] + a[2]) ** 2 + (a[1] + a[3]) ** 2) *
            (a[0] - a[2]) ** 2 + (a[1] - a[3]) ** 2) ** 1 / 4


# 4 олшемди сан спектры
def spectr(list1):
    result = ((((list1[0]+list1[2])**2) + ((list1[1]+list1[3])**2)) * (((list1[0]-list1[2])**2)+((list1[1]-list1[3])**2)))**0.25
    return result


# 4 олшемди саннын 2ши дарежесин табу
def d4_pow(san):
    result = list()
    for i in range(len(san)):
        item = san[i] ** 2
        result.append(item)
    return result

# 4 олшемди саннын тубир астынан шыгару
def d4_sqrt(san):
    result = list()
    for i in range(len(san)):
        item = san[i] ** 0.5
        result.append(item)
    return result

