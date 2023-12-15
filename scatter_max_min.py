def get_data(avtal):
    #Hämta data av lägenhets priser
    lgh_data = read_file('lghpriser.csv')
    lgh_header = lgh_data[0]
    lgh_data_lista = []

    #Hämta data av villa priser
    villa_data = read_file('villapriser.csv')
    villa_header = villa_data[0]
    villa_data_lista = []

    if avtal == 'rörligt':
        avtal = "Rorligt pris"
    elif avtal == 'fast 1 år':
        avtal = 'Fast pris 1 ar'   
    else:
        avtal = 'Fast pris 3 ar'
        
    for i in range(1, 5): # range(1,5) motsvarar SE1-SE4
        for kolumn in [f'SE{i}-{avtal}']:
            lgh_index = lgh_header.index(kolumn)
            lgh_områden = [row[lgh_index] for row in lgh_data]
            lgh_data_lista.append(lgh_områden)
            
            villa_index = villa_header.index(kolumn)
            villa_områden = [row[villa_index] for row in villa_data]
            villa_data_lista.append(villa_områden)
                   

    return lgh_data_lista, villa_data_lista #Returnerar två listor med alla priser för lägenhets- samt villakunder 



def get_year(index):
    year = 0

    if index <= 12:
        year = 2018
    elif index <= 24:
        year = 2019
    elif index <= 36:
        year = 2020
    elif index <= 48:
        year = 2021
    elif index <= 60:
        year = 2022
    elif index <= 72:
        year = 2023

    return year

def minsta(data):
    #Initerar med att skapa 4 listor som ska populeras med minsta priser från varje prisområde och bostads kategori samt dess månad
    min_priser = []    
    min_mån = []
    min_år = []
    
    # Iterar över varje prisområde
    for i in range(4):
        min_värde = None
        område = data[i]
        minsta_pris = [float(pris) if len(pris) > 3 else int(pris) for pris in område[1:]] #För att man ska kunna ta fram lägsta värdet måste 'string' omvandlas till float

        for tal in minsta_pris:
            if(min_värde is None or tal < min_värde):
                min_värde = tal
        min_priser.append(min_värde)
        
        månad_minsta_index = område.index(str(min_värde))
        if månad_minsta_index > 12:
            månad_minsta_index -= 24
        min_mån.append(int(månad_minsta_index))
        
        minsta_år = get_year(månad_minsta_index)
        min_år.append(minsta_år)

    return min_priser, min_mån, min_år


def högsta(data):
    #Initerar med att skapa 4 listor som ska populeras med minsta priser från varje prisområde och bostads kategori samt dess månad
    max_priser = []    
    max_mån = []
    max_år = []
    
    # Iterar över varje prisområde
    for i in range(4):
        max_värde = None
        område = data[i]
        
        högsta_pris = [float(pris) if len(pris) > 3 else int(pris) for pris in område[1:]]

        for tal in högsta_pris:
            if(max_värde is None or tal > max_värde):
                max_värde = tal
        max_priser.append(max_värde)

        månad_högsta_index = område.index(str(max_värde))
        if månad_högsta_index > 12:
            månad_högsta_index -= 48
        max_mån.append(int(månad_högsta_index))

        
        högsta_år = get_year(månad_högsta_index)
        max_år.append(högsta_år)


    return max_priser, max_mån, max_år


# Medelvärdet = summan / antal värden
def medel(data):
    medel_lista = []

    for i in range(4):
        område = data[i]
        priser = [float(x) for x in område[1:]] #Omvandlar priser från 'string' till float samt börjar på index 1 då första strängen är rubriken
        summa_av_tal = 0
        for pris in range(len(priser)):
            summa_av_tal += priser[pris]
        
        medel_värde =  summa_av_tal / len(priser)
        medel_lista.append(round(medel_värde, 2))
    
    return medel_lista 
        
    
#Funktionen presentar data i en enkel tabell
def presentera_tabell(avtal, lgh_minsta, villa_minsta, lgh_högsta, villa_högsta, lgh_medel, villa_medel, lgh_minsta_månader, villa_minsta_månader, lgh_högsta_månad, villa_högsta_månad, lgh_minsta_år, villa_minsta_år, lgh_högsta_år, villa_högsta_år):
    print()
    print("Kategori lägenhetskund")
    print(100*"-")
    print(f"Prisomr{'':7}[lägsta - år - mån]{'':20}[högsta - år - mån]{'':23}medel")
    print()
    for område in range(4): 
        print(f"SE{område+1} {lgh_minsta[område]:15} - {lgh_minsta_år[område]} - {lgh_minsta_månader[område]:15}{lgh_högsta[område]:15} - {lgh_högsta_år[område]} - {lgh_högsta_månad[område]:15}{lgh_medel[område]:15}")
    print()
    
    print("Kategori villakund")
    print(100*"-")
    for område in range(4): 
        print(f"SE{område+1}{villa_minsta[område]:15} - {villa_minsta_år[område]} - {villa_minsta_månader[område]:15}{villa_högsta[område]:15} - {villa_högsta_år[område]} - {villa_högsta_månad[område]:15}{villa_medel[område]:15}")
    print()

def presentera_diagram(avtal, lgh_minsta, villa_minsta, lgh_högsta, villa_högsta, lgh_medel, villa_medel):
    x = [
        'SE1',
        'SE2',
        'SE3',
        'SE4'
    ]
    

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)  
    plt.xticks(rotation=45)
    plt.title(f"Elpris-, högsta och medelvärde under 2018-2023.\nKategori lägenhetskund - {avtal} avtal.")
    plt.xlabel("Prisområden")
    plt.ylabel("Pris [öre/kWh]")
    plt.scatter(x, lgh_minsta, label='lägsta elpris', color='blue')
    plt.scatter(x, lgh_högsta, label='högsta elpris', color='orange')
    plt.scatter(x, lgh_medel, label='medelvärde', color='green')
    plt.grid()
    plt.legend()


    plt.subplot(1, 2, 2) 
    plt.xticks(rotation=45)
    plt.title(f"Elpris-, högsta och medelvärde under 2018-2023.\nKategori villakund - {avtal} avtal.")
    plt.xlabel("Prisområden")
    plt.ylabel("Pris [öre/kWh]")
    plt.scatter(x, villa_minsta, label='lägsta elpris', color='blue')
    plt.scatter(x, villa_högsta, label='högsta elpris', color='orange')
    plt.scatter(x, villa_medel, label='medelvärde', color='green')
    plt.grid()
    plt.legend()

    plt.tight_layout() 
    plt.show()
    

def uppgift_5():
    #Hämta avtal
    avtal = get_avtal()
    #Hämta data
    lgh_data, villa_data = get_data(avtal)
    

    #Hämta lägsta priser
    lgh_minsta, lgh_minsta_månader, lgh_minsta_år = minsta(lgh_data)
    villa_minsta, villa_minsta_månader, villa_minsta_år = minsta(villa_data)
    #Hämta högsta priser
    lgh_högsta, lgh_högsta_månader, lgh_högsta_år = högsta(lgh_data)
    villa_högsta, villa_högsta_månader, villa_högsta_år = högsta(villa_data)
    #Hämta medel
    lgh_medel = medel(lgh_data)
    villa_medel = medel(villa_data)
    
    
    #Hämta månader för lgh
    lgh_minsta_månader = get_månad(lgh_minsta_månader)
    lgh_högsta_månader = get_månad(lgh_högsta_månader)
    
    #Hämta månader för villa
    villa_minsta_månader = get_månad(villa_minsta_månader)
    villa_högsta_månader = get_månad(villa_högsta_månader)
    
    #Presentera data
    presentera_tabell(avtal, lgh_minsta, villa_minsta, lgh_högsta, villa_högsta, lgh_medel, villa_medel, lgh_minsta_månader, villa_minsta_månader, lgh_högsta_månader, villa_högsta_månader, lgh_minsta_år, villa_minsta_år, lgh_högsta_år, villa_högsta_år)
    presentera_diagram(avtal, lgh_minsta, villa_minsta, lgh_högsta, villa_högsta, lgh_medel, villa_medel)
    
    
    
    
uppgift_5() #Anroppar huvudfunktionen
