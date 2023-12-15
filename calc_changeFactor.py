def get_data(kategori, avtal, prisområde, årtal):
    # Hämta användarens val för uträkning
    # start = januari på givet årtal
    # end = december på givet årtal
    start, end = get_årtalIndex(årtal)
    
    # Förändringsfaktorn för januari 2018 kan ej beräknas eftersom data för dec 2017 saknas.
    # Därför kollar programmet om årtalet INTE är 2018 innan de tar fram december från förra året
    if årtal != 2018:
        start = start - 1 # start = december året innan angivet årtal

    # Anropa read_file funktionen och spara sedan värdet i lgh_data respektive villa_data
    if kategori == 'l':
        data = read_file('lghpriser.csv')
        header = data[0]
        list_analys = []
    else:
        data = read_file('villapriser.csv')
        header = data[0]
        list_analys = []

    if avtal == 'rörligt':
        for kolumn in [f"SE{prisområde}-Rorligt pris"]:
            index = header.index(kolumn)
            x_områden = [float(row[index]) for row in data[start:end]]
            list_analys.append(x_områden)
    elif avtal == 'fast 1 år':
        for kolumn in [f"SE{prisområde}-Fast pris 1 ar"]:
            index = header.index(kolumn)
            x_områden = [float(row[index]) for row in data[start:end]]
            list_analys.append(x_områden)
    else:
        for kolumn in [f"SE{prisområde}-Fast pris 3 ar"]:
            index = header.index(kolumn)
            x_områden = [float(row[index]) for row in data[start:end]]
            list_analys.append(x_områden)

    # List comprehension skapar en ny lista baserad på värdena i en befintlig lista.
    # I detta programet omvandlas 2D lista till 1D så att värdena kan beräknas
    data = [pris for lista in list_analys for pris in lista]
    return data

    

def beräkna_förändringsfaktor(årtal, data):
    FF_list = [] # Funktionen initieras med en tom lista som tilldelas med förändringsfaktor per månad nedan 


    if årtal == 2018:
        for index, pris in enumerate(data, start = 1):
            if index != 12: #Beräkna fram till index 11
                ff = ((data[index] - pris) / pris) * 100
                FF_list.append(round(ff))

    elif årtal == 2023:
        for index, pris in enumerate(data, start = 1): #Start ett steg i förväg genom start = 1 så att funktionen kan beräkna Mån+1 - Mån
            if index != 8: #Räkna fram till index 12 
                ff = ((data[index] - pris) / pris) * 100
                FF_list.append(round(ff))

    else:
        for index, pris in enumerate(data, start = 1): #Start ett steg i förväg genom start = 1 så att funktionen kan beräkna Mån+1 - Mån
            if index != 13: #Räkna fram till index 12 
                ff = ((data[index] - pris) / pris) * 100
                FF_list.append(round(ff))
    return FF_list

def presentera_stapeldiagram(kategori, avtal, prisområde, årtal, FF_list):

    x = [
        "jan", 
        "feb", 
        "mar", 
        "apr", 
        "maj", 
        "jun", 
        "jul", 
        "aug", 
        "sep", 
        "okt", 
        "nov",
        "dec"
    ]
    
    # Kolla om 2018 har angivits 
    if årtal == 2018:
        x = x[1:12] # Då räknar programet inte med Jan-Dec
    elif årtal == 2023:
        x = x[:7] # 
    
    #Kolla katerori inför presentation av data
    if kategori == 'v':
        kategori = "villa"
    else:
        kategori = "lägenhets"
    
    #Skapa stapeldiagram
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.bar(x, FF_list, width=0.5, color="r")
    plt.grid()
    plt.xticks(rotation=45)  
    plt.title(f"Förändringsfaktor per månad för {kategori}kund i SE{prisområde} år {årtal}")
    plt.xlabel("Månad")
    plt.ylabel("förändring [%]")
    plt.legend([avtal]) 
    plt.show()
    


#Programmets huvudfunktion anropar funktionererna som hämtar data och skriver ut resultat
def uppgift_4():
    kategori =  get_kundområde() # Villa eller lgh
    avtal = get_avtal() #Rörligt, fast 1 år eller fast 3år
    prisområde = pris_område() # SE1-4
    årtal = get_årtal() # 2018-2023
    data = get_data(kategori, avtal, prisområde, årtal) #Spara data som en varaibel data baserat på användarens givna värden
    FF_list = beräkna_förändringsfaktor(årtal, data) #Skicka data till metod för berkänning av förändringsfaktorn
    presentera_stapeldiagram(kategori, avtal, prisområde, årtal, FF_list) #Slutligen presentera data i ett stapeldiagram

        
    
uppgift_4() #Anroppa huvudfunktionen
