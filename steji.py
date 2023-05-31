#Functia 1:
import csv

def sb_append(date, name, score):
    nume_fisier = 'score.csv'
    rand_nou = [date, name, score]
    
    with open(nume_fisier, 'a', newline='') as fisier_csv:
        scriitor_csv = csv.writer(fisier_csv)
        scriitor_csv.writerow(rand_nou)
    
    #print("Informațiile au fost adăugate cu succes în fișierul CSV.")

# Exemplu de utilizare
date = '1111'
name = 'laj'
score = '2225'

sb_append(date, name, score)

  
#Functia 2:

def leaderb():
    nume_fisier = 'score.csv'
    
    with open(nume_fisier, 'r') as fisier_csv:
        cititor_csv = csv.reader(fisier_csv)
        urmatorul = cititor_csv  # Ignorăm antetul
        
        clasament = sorted(cititor_csv, key=lambda x: int(x[2]), reverse=True)
        primii_zece = clasament[:10]
        
        return primii_zece

# Exemplu de utilizare
clasament = leaderb()
for pozitie, jucator in enumerate(clasament, start=1):
    print(f"Locul {pozitie}: {jucator}")


