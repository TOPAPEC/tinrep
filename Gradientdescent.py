# Функция, для которой мы хотим найти точку локального минимума.
func = '6*(x**6) + 2*(x**4)*(y**2) + 10*(x**2) + 6*x*y + 10*(y**2) - 6*x + 4'
# Её частная производная по Х.
derx = '36*(x**5) + 8*(x**3)*(y**2) + 20*x + 6*y - 6'
# Её частная производная по Y.
dery = '4*x**4 + 6*x + 20*y'

# Множитель длины градиента.
step = 2
# Коэффициент, на который на каждой итерации делется множитель длины вектора градиента.
stepDiv = 3.0/2
# Минимальная величина шага.
delta = 0.0000000001
# Начальная и, в дальнейшем, текущая точка.
l = [0, 0]

# Мы проводим вычисления, пока шаг не меньше длины delta.
while step > delta:
    # Считаем координаты вектора градиента.
    gradxRaw = eval(derx.replace('x', str(l[0])).replace('y', str(l[1])))
    gradyRaw = eval(dery.replace('x', str(l[0])).replace('y', str(l[1])))
    # Нормируем его.
    gradx = gradxRaw / (gradxRaw**2 + gradyRaw**2)**(1/2)
    grady = gradyRaw / (gradxRaw**2 + gradyRaw**2)**(1/2)
    # Вычисляем новые координаты текущей точки.
    tl1 = l[0] - step * gradx
    tl2 = l[1] - step * grady
    l = [tl1, tl2]
    # Уменьшаем шаг по мере приближения к минимуму.
    step /= stepDiv
# Вывод найденных точек.
print(l[0], l[1])