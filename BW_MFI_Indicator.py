import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as DT
import numpy as np
import math as mt

# Данные с сервера YAHOO
def Data_YAHOO(Stock, Start, End):

    # Возвращает ряды данных с сайта YAHOO на временном отрезке
    Arr = web.get_data_yahoo(Stock, Start, End)

    # Получаем данные с YAHOO
    Data            = pd.DataFrame(Arr['High'])
    Data['Low']     = pd.DataFrame(Arr['Low'])
    Data['Volume']  = pd.DataFrame(Arr['Volume'])

    # Возвращаем данные индикатора
    return Data

# Индекс облегчения рынка Билла Вильямса
def BM_MFI(Arr): return (Arr['High'] - Arr['Low']) / Arr['Volume']

# Модификатор
def Operator(Mx, My, PW=False):

    # Проверка от левых данных
    Xs, Ys = [], []
    for i in Mx:
        if (mt.isnan(My[i]) != True):
            Xs.append(i)
            Ys.append(My[i])

    # Масштабируем сигнал от 0 до Pi
    Xpi = np.linspace(0, np.pi, len(Xs))

    # Метод для конвертации массива данных в функцию от 0 до pi
    def F(x, E=0.1):
        Nm, Xps = 0, x
        while (Xps > np.pi): Xps -= 2 * np.pi
        for k in Xpi:
            if (abs(k - Xps) < E): return Ys[Nm]
            Nm += 1

    # Синк функция
    def S(k, x, n=100):
        return (((-1) ** k) * np.sin(n * x)) / (n * x - k * np.pi)

    # Функция Уиткера (4.1)
    # Принимает функцию, которую иследуют, его значение по X и постоянную n
    def Ln(f, x, n=100):
        LN = 0
        for k in range(1, n): LN += ((((-1) ** k) * np.sin(n * x)) / (n * x - k * np.pi)) * f((k * np.pi) / n)
        return LN

    # Функцию разделил на условные блоки (чтобы не запутаться)
    def DF1(k):
        return ((F(Xpi[k + 1]) + F(Xpi[k])) / 2)

    def DF2():
        return ((F(np.pi) - F(0)) / np.pi)

    def DF3(k):
        return ((Xpi[k + 1] + Xpi[k]) / 2)

    # Функция модификатор (5.36)
    def ATh(F, x):
        AT = 0
        for k in range(0, len(Xpi) - 1): AT += (DF1(k) - (DF2() * DF3(k)) - F(0)) * S(k, x)
        return AT + (DF2() * x) + F(0)

    # Возращаем данные
    if (PW):    return {"X": Xs, "Y": [Ln(F, x) for x in Xpi]}
    else:       return {"X": Xs, "Y": [ATh(F, x) for x in Xpi]}

def Main():

    # Считываем данные с сервера YAHOO
    ARR = Data_YAHOO('FB', '1/1/2019', '1/1/2020')

    # Проверка, что данные плучены (не обязательно!!!)
    plt.subplot(3, 1, 1); plt.title('Low');     plt.plot(np.array(ARR['Low']),      color='green')
    plt.subplot(3, 1, 2); plt.title('High');    plt.plot(np.array(ARR['High']),     color='green')
    plt.subplot(3, 1, 3); plt.title('Volume');  plt.plot(np.array(ARR['Volume']),   color='green')
    plt.show()

    BM = BM_MFI(ARR)
    X = [I for I in range(len(BM))]

    # Сама задача
    plt.subplot(3, 1, 1); plt.title("BM MFI");  plt.plot(BM, color='green')
    DATA = Operator(X,BM,PW=False)
    plt.subplot(3, 1, 2); plt.title("BM MFI + Модификатор 4.1");    plt.plot(DATA['X'], DATA['Y'], color='green')
    DATA = Operator(X,BM,PW=True)
    plt.subplot(3, 1, 3); plt.title("BM MFI + Модификатор 5.36");   plt.plot(DATA['X'], DATA['Y'], color='green')
    plt.show()

# Главный метод
if __name__ == "__main__": Main()