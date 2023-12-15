# Ber användaren ange ett kundområde genom en while loop och därmed körs programet tills ett korrekt värde har angivits
def get_kundområde():
    while True:
        kategori = input("Lägenhetskund ange (L)\nVillakund ange (V)\n") #Sparar användarens val i variablen kategori
        
        if kategori == '': #Om användarens input är tom avsluta med nreak
            break
        
        try:
            kategori = kategori.strip()
            
            #if else för att verifiera användarens val
            if kategori.lower() == 'l' or kategori.lower() == 'v': # lower() gör användarens input till litebokstav så att både l/L för lgh samt v/V för villa blir giltigt vid validering
                return kategori  # returnerar om ett korrekt alternativ angavs
            else:
                print("Var vänlig och ange (L) eller (V)")  # Skriver ut ett felmedelande om inget korrekt val har angivits och kör nästa vara i while loopen
                continue
            
        except:
            print("Testa igen!")
            continue
            
            
        
#Be om årtal till presentation av data. Här används en extra "error handling" genom try/execpt för att fånga möjliga fel som inkorrekt data typ
def get_årtal():
    while True:
        årtal = input("Ange årtalet som ska presenteras (2018-2023): ") #Användarens val spara som en sträng men omvandlas till integer vid validering för att förebygga felmedelanden
        
        if årtal == '':
            break
        
        try:
            årtal = årtal.strip()
            årtal = int(årtal)
            if 2018 <= årtal <= 2023: # Validerar om användarens val är inom interval 2018 till 2023   
                return årtal
            else:
                print("Var vänlig och ange ett av de angivna årtalen (2018-2023).")
                
        except ValueError:  #Except ValueError ser till att programet inte krashar om användaren anger annat tecken än int
            print("Ogiltigt årtal. Var vänlig ange en siffra mellan 2018 och 2023.")



def get_data(årtal, kategori):
    #Hämta användarens val för uträkning
    start, end = get_årtalIndex(årtal)
    
    #Anropa read_file funktionen och spara sedan värdet i lgh_data respektive villa_data
    if kategori == 'l': #Om användaren valde läghenhet anropa readfile med lghpriser.cscv
        data = read_file('lghpriser.csv') 
        header = data[0] # Tar fram rubrikerna på rad 0 av filen över lgh prisert
        list_analys = [] # initierarar en tom lista som ska fyllas på med elpris data 

    else: #Annars valde de villa
        data = read_file('villapriser.csv')
        header = data[0] # Tar fram rad 0 av filen över lgh priser
        list_analys = [] # initierarar en tom lista som ska fyllas på med elpris data 
        
        

    #Här används en for loop med interval 1-4 (1,2,3,4) för att hämta kolumnerna för alla områden fast pris 3år och rörligt
    for i in range(1,5):
        for kolumn in [f"SE{i}-Fast pris 3 ar", f"SE{i}-Rorligt pris"]:  
            index = header.index(kolumn)
            x_områden = [float(row[index]) for row in data[start:end]] #start och end avgör årtalet som skrivs ut (ex 1:13 motsavara 2018)
            list_analys.append(x_områden) # append() för att lägga till i listan
             
    return list_analys


def hitta_minsta(elpris_data):
    # Defienera två listor som ska tilldelas värden nedan. 
    minsta_lista = [] #Lista med de lägsta priserna för valt år samt kategori
    min_månader = [] # Månad för motsvarande lägsta priset

    # Iterera över alla priser och områden (område 1 till 4)
    for priser in elpris_data:
        min_pris = priser[0]
        min_månad = 1  
        
        #enumerate används här för att räkna varje iteration av loopen, därmed prisets månad av 12
        for månad, pris in enumerate(priser[1:], start=2): 
            if pris < min_pris:
                min_pris = pris # Om nuvarande är priset är lägst sparas värdet i variabeln min_pris
                min_månad = månad #Spara värdet på antal varv i loopen som prisets månad
                
        #Lägg till de hittade värdena i listorna ovan
        minsta_lista.append(min_pris) 
        min_månader.append(min_månad)

    return minsta_lista, min_månader #returnera en lista med priser för diagram och en lista med månader till tabell

                
# Hitta högsta följer samma steg som minsta men söker hösta värdet i listan
def hitta_högsta(elpris_data):
    högsta_lista = []
    högsta_månader = []

    # Iterera över alla priser och områden (område 1 till 4)
    for priser in elpris_data:
        max_pris = priser[0]  # Initialisera det högsta priset med det första priset inom området
        högsta_månad = 1  # Initialisera månaden med 1 (första månaden)

        # Använd enumerate() för att loopa igenom priser tillsammans med månadsräknaren
        for månad, pris in enumerate(priser[1:], start=2):
            if pris > max_pris:
                max_pris = pris
                högsta_månad = månad
        
        högsta_månader.append(högsta_månad)
        högsta_lista.append(max_pris)  # Bifoga ny lista med månad, högsta pris och område

    return högsta_lista, högsta_månader



def hitta_medelVärde(elpris_data):
    medelvärde_lista = []

    for område in range(8):
        priser = elpris_data[område]
        summan_priser = 0
        for pris in priser:
            summan_priser += pris
        
        medel_värde = summan_priser / len(priser)
        medelvärde_lista.append(round(medel_värde,2))

        
    return medelvärde_lista

def hitta_medianen(elpris_data):
    median_lista = []

    for i in range(8): # Börja iterera för varje elpris_område (8st)
        område = elpris_data[i] # Ta fram varje elpris_område för sig genom indexering
        
        sorterad_lista = sorted(område) # Använd sorted() för att sortera listorna i stigande ordning
        listans_längd = len(område)
        mitten = (listans_längd - 1) // 2
        
        #Om jämn (12månader)
        if(listans_längd % 2):
            median_lista.append(round(sorterad_lista[mitten], 2))
        
        #Annars räkna ut om udda (år 2023)
        else:
            udda_median = (sorterad_lista[mitten] + sorterad_lista[mitten + 1]) / 2.0
            median_lista.append(round(udda_median, 2))
            

    return median_lista


    
def get_statistics(elpris_data, årtal, kategori):
    #Hämtar data för tabell och diagram
    minsta, min_månader  = hitta_minsta(elpris_data)
    högsta, högsta_månader = hitta_högsta(elpris_data)
    medel = hitta_medelVärde(elpris_data)
    median = hitta_medianen(elpris_data)
    min_mån = get_månad(min_månader) 
    max_mån = get_månad(högsta_månader)

    #Presenterar data som en tabell och diagram
    presentera_tabell(minsta, min_mån, högsta, max_mån, median, medel, årtal)
    presentera_diagram(minsta, högsta, medel, median, årtal, kategori)

    
def presentera_tabell(minsta, min_mån, högsta, max_mån, median, medel, årtal):
    print()
    print(100*"-")
    print(f"Analys av elpriser för år {årtal}")


    print(f"fast pris 3 år (öre/kWh){'':30} Rörliga (öre/kWh)")
    print(f"min-(mån)    max-(mån)     medel     median{'':12}min-(mån)    max-(mån)    medel     median")
    print()
    områden = ["SE1", "SE2", "SE3", "SE4"]
        
    for i in range(8):
        område = ""
        if i < 4:
            område = områden[i]
        if i % 2 == 0: #Använder en Modulo för att kolla om i är jämnt delbar med 2 
            print(f"{minsta[i]}-{min_mån[i]}{'':5}{högsta[i]}-{max_mån[i]}{'':5}{median[i]}{'':5}{medel[i]}{'':5}", end='  -     ') 
            
        elif i % 2 != 0:
            print(f"{minsta[i]}-{min_mån[i]}{'':5}{högsta[i]}-{max_mån[i]}{'':5}{median[i]}{'':5}{medel[i]}") #annars rörliga

    print(100*"-")
     
def sortera_rörliga(data):    
    # initierar programet med 2 tomma listor
    rörliga = [] #
    y_rörliga = []

    #Hämtar alla rörliga priser och appendar dem i första listan. 
    #Resultatet är en nestald lista [[]]
    for data_typ in data:
        rörliga.append([data_typ[i] for i in range(len(data_typ)) if i % 2 != 0])
        
    #Därför itererar programet över den första listan för att ta fram en []
    for priser in rörliga:
        for pris in priser:
            y_rörliga.append(pris)

    return y_rörliga


def sortera_fast(data):
    fast = []
                    
    #Hämtar alla fast priser
    for data_typ in data:
        fast.append([data_typ[i] for i in range(len(data_typ)) if i % 2 == 0])    
    y_fast = []
    for priser in fast:
        for pris in priser:
            y_fast.append(pris)  
    return y_fast


# Sorterar genom y_rörliga listan och returnera 4 nya listor för varje resultat av uträkningarna ovan
def get_rörliga(y_rörliga):
    # y_rörliga
    y_rörliga_min = []
    y_rörliga_max = []
    y_rörliga_medel = []
    y_rörliga_median = []
    
    # Här används range() med listans längd till intervallet av 16 då det finns totalt 16 svar 4*4 från varje kategori
    for i in range(min(len(y_rörliga), 16)):
        
        # Vilkorssats används för att kolla vilken iteration programet är på och då lägger till talet i rätt kategori.
        # Annars uppstor ett ValueError i presentation av tabellen
        
        # 0,    1,   2,   3
        # 4,    5,   6,   7,
        #  8,   9,  10,  11,
        # 12,  13,  14,  15    
        
        if i < 4:
            y_rörliga_min.append(y_rörliga[i])
        elif i < 8:
            y_rörliga_max.append(y_rörliga[i])
        elif i < 12:
            y_rörliga_medel.append(y_rörliga[i])
        else:
            y_rörliga_median.append(y_rörliga[i])
            
    return y_rörliga_min, y_rörliga_max, y_rörliga_medel, y_rörliga_median

#Följer sammar algorithm som get_rörliga
#TODO
# Bör kunna skriva en ända funktion för både rörliga och fast?
def get_fast(y_fast):
    # y_fast
    y_fast_min = []
    y_fast_max = []
    y_fast_medel = []
    y_fast_median = []

    for i in range(min(len(y_fast), 16)):
        if i < 4:
            y_fast_min.append(y_fast[i])
        elif i < 8:
            y_fast_max.append(y_fast[i])
        elif i < 12:
            y_fast_medel.append(y_fast[i])
        else:
            y_fast_median.append(y_fast[i])
    
    return y_fast_min, y_fast_max, y_fast_medel, y_fast_median
    
    
def presentera_diagram(minsta, högsta, medel, median, årtal, kategori):
    områden = ["SE1", "SE2", "SE3", "SE4"]
    data = [minsta, högsta, medel, median] #Börja med att samla all data i en ända lista
    
    y_rörliga = sortera_rörliga(data) #Kallar på funktionen som sortera alla rörliga priser i en lista och användas för att presentera y-axelns data
    y_fast = sortera_fast(data) # Sortera alla fast 3år priser i en lista
    
    y_rörliga_min, y_rörliga_max, y_rörliga_medel, y_rörliga_median = get_rörliga(y_rörliga) # funktionen returnerar 4 listor, rörliga priser för varjer katerori
    y_fast_min, y_fast_max, y_fast_medel, y_fast_median = get_fast(y_fast) # Likadant som ovan
    
    x = range(len(områden))
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    

    # Färg och etikett för staplarna så att de blir mer enklare att urskilja
    #Flytta stapelrnas x för att kunna skapa ett grupperat stapeldiagram
    axes[0].bar([x - 1.5 * 0.2 for x in x], y_rörliga_min, 0.2, label='Rörlig - min', color='b')
    axes[0].bar([x - 0.5 * 0.2 for x in x], y_rörliga_max, 0.2, label='Rörlig - max', color='orange')
    axes[0].bar([x + 0.5 * 0.2 for x in x], y_rörliga_medel, 0.2, label='Rörlig - medel', color='g')
    axes[0].bar([x + 1.5 * 0.2 for x in x], y_rörliga_median, 0.2, label='Rörligt - median', color='r')
    # Lägga till informativ text i diagrammet
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(områden)
    axes[0].set_xlabel("prisområden")
    axes[0].set_ylabel("Pris [öre/kWh]")
    axes[0].set_title(f'Elpriser rörligt för {kategori} i prisområderna SE1-SE4 år {årtal}')
    axes[0].legend()

    # plot fast 3 år data
    # Färg och etikett för staplarna så att de blir mer enklare att urskilja
    axes[1].bar([x - 1.5 * 0.2 for x in x], y_fast_min, 0.2, label='Fast 3 år - min', color='b')
    axes[1].bar([x - 0.5 * 0.2 for x in x], y_fast_max, 0.2, label='Fast 3 år - max', color='orange')
    axes[1].bar([x + 0.5 * 0.2 for x in x], y_fast_medel, 0.2, label='Fast 3 år - medel', color='g')
    axes[1].bar([x + 1.5 * 0.2 for x in x], y_fast_median, 0.2, label='Fast 3 år - median', color='r')
    # Lägga till informativ text i diagrammet
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(områden)
    axes[1].set_xlabel("prisområden")
    axes[1].set_ylabel("Pris [öre/kWh]")
    axes[1].set_title(f'Elpriser fast 3 år för {kategori} i prisområderna SE1-SE4 år {årtal}')
    axes[1].legend()

    #Skriv ut diagramen
    plt.tight_layout()
    plt.show()
            
def main_elpris_analys():
    kategori =  get_kundområde() #Spara användarens val av område i variablen katogori för att användas vid uträkning
    årtal = get_årtal() #Spara användarens val av årtal i variablen år för att användas i samband med område vid uträkning
    elpris_data = get_data(årtal,kategori) 
    get_statistics(elpris_data, årtal, kategori) 
    


main_elpris_analys()
