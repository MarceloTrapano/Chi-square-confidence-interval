#Do prawidłowego działania programu niezbędne będzie zainstalowanie bibliotek matplotlib, scipy oraz numpy
#Próbowałem stworzyć plik wykonywalny .exe, aby nie było trzeba instalować pythona i bibliotek, ale niestety jedna z bibliotek nie była kompatybilna z kompilatorem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np
from scipy.stats import chi2

def find_interval(n,alpha):                                                                     #Funkcja znajdująca przedział
    spr1 = 0                                           
    spr2 = 0
    for i in np.arange(1,99.9,0.1):                     
        a = chi2.ppf(i*alpha/100,df=(n-1))                                                      #Dane kwantyle rozkładu chi kwadrat
        b = chi2.ppf(1-((100-i)*alpha)/100,df=(n-1))
        if abs((a**2)*chi2.pdf(a,df=(n-1)) - (b**2)*chi2.pdf(b,df=(n-1))) < 0.001:              #Warunek sprawdzający warunki najmniejszego przedziału ufności dla dokładności 0.001 co do abs
            return a, b                                                                         #Przerywanie funkcji gdy dana dokładność zostanie osiągnięta
        if abs((a**2)*chi2.pdf(a,df=(n-1)) - (b**2)*chi2.pdf(b,df=(n-1))) < 0.01:               #Warunek sprawdzający warunki najmniejszego przedziału ufności dla dokładności 0.01 co do abs
            a1 = a                                                                              #Zapamiętywanie wartości o tej dokładności
            b1 = b
            spr1 = 1                                                                            #Nadpisanie wartości logicznej
        if abs((a**2)*chi2.pdf(a,df=(n-1)) - (b**2)*chi2.pdf(b,df=(n-1))) < 0.1:                #Warunek sprawdzający warunki najmniejszego przedziału ufności dla dokładności 0.01 co do abs
            a2 = a                                                                              #Zapamiętywanie wartości o tej dokładności
            b2 = b
            spr2 = 1                                                                            #Nadpisanie wartości logicznej
    if spr1:                                                                                    #Warunek sprawdzający czy trochę gorsza dokładność została osiągnięta
        a = a1
        b = b1
        return a, b
    if spr2:                                                                                    #Warunek sprawdzający czy jeszcze gorsza dokładność została osiągnięta
        a = a2
        b = b2
        return a, b
    a = chi2.ppf(alpha/2,df=(n-1))                                                              #W razie niepowodzenia przyznane zostaną wartości domyślne z tabel
    b = chi2.ppf(1-alpha/2,df=(n-1))
    print("nie udalo sie")
    return a, b


def click_action():                                                                             #Funkcja obsługująca działanie przycisku
    alpha = float(alpha_entry.get())                                                            #Zbieranie danych z pól wejściowych
    n = float(n_entry.get())
    n_entry.delete(0, 'end')                                                                    #Resetowanie pola wejściowego
    alpha_entry.delete(0, 'end')                                                            

    a,b = find_interval(n,alpha)                                                                #Wykonywanie funkcji odpowiedzialnej za znalezienie najlepszego przedziału ufności

    fig, ax = plt.subplots()                                                                    #Obsługa wykresu
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(column=0,row=4,sticky=tk.EW,padx=5,pady=5)

    x = np.arange(0,5*n,0.001)
    ax.grid()
    ax.plot(x, chi2.pdf(x, df=(n-1)), color="red")

    str_var.set('b - a = '+str(b-a))                                                                                #Obsługa wyświetlania wyniku
    str_var2.set('a^2 *f(a) - b^2 * f(b) = '+str((a**2)*chi2.pdf(a,df=(n-1)) - (b**2)*chi2.pdf(b,df=(n-1))))
    str_var3.set('a = '+ str(a) + ', b = ' + str(b))
    
    ylim = ax.get_ylim()                                                                        #Tworzenie pionowych linii wskazujących przedział ufności
    ax.vlines(a,ylim[0],ylim[1],linestyle='--')
    ax.vlines(b,ylim[0],ylim[1],linestyle='--')
    return

root = tk.Tk()                                                                                  #Obsługa okienka i konfiguracja z biblioteki tkinter
root.geometry("800x700")
root.title('chi_kwadrat')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

str_var = tk.StringVar()                                                                        #Tworzenie zmiennych typu string
str_var2 = tk.StringVar()
str_var3 = tk.StringVar()

str_var.set('')                                                                                 #Resetowanie zmiennych str
str_var2.set('')
str_var3.set('')

interval_label = tk.Label(root, textvariable=str_var)                                           #Tworzenie napisu pokazującego długość przedziału
interval_label.grid(column=0,row=6,sticky=tk.S,padx=5,pady=5)

interval_label2 = tk.Label(root, textvariable=str_var2)                                         #Tworzenie napisu pokazującego wartość warunku najdłuższego przedziału ufności
interval_label2.grid(column=0,row=7,sticky=tk.S,padx=5,pady=5)

a_label = tk.Label(root, textvariable=str_var3)                                                 #Tworzenie napisu pokazującego punkty a i b
a_label.grid(column=0,row=5,sticky=tk.S,padx=5,pady=5)

alpha_label = tk.Label(root, text="Alpha:")                                                     #Tworzenie napisu wskazującego w którym polu należy podać wartość alpha
alpha_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

alpha_entry = tk.Entry(root)                                                                    #Tworzenie wejścia dla alphy
alpha_entry.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

n_label = tk.Label(root, text="n:")                                                             #Tworzenie napisu wskazującego w którym polu należy podać wartość n
n_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

n_entry = tk.Entry(root)                                                                        #Tworzenie wejścia dla n'a
n_entry.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

click_button = tk.Button(root, text="Akceptuj", width=8, command=click_action)                  #Tworzenie przycisku tworzącego wykres
click_button.grid(column=1,row=2, sticky=tk.W, padx=5, pady=5)

exitb = tk.Button(root, text="Zamknij",background="red", width=8, command=root.destroy)         #Tworzenie przycisku wyjścia
exitb.grid(column=1,row=5, sticky=tk.E, padx=5, pady=5)

root.mainloop()

