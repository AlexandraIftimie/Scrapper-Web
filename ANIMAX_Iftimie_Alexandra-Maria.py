# Instalam request si beautifulsoup cu pip install in terminal
import requests


# Definim URL-ul paginii pe care dorim sa o analizam
url = "https://animax.ro/collections/pasari"
base_url=url
#Preluam html-ul si folosim dictionar headers pt a nu ni se bloca accesul de catre server
Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;  Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
response = requests.get(url, headers=Headers)
html = response.content

#Verificam daca solicitarea a fost realizata cu succes
if response.status_code == 200:
    print("Solicitarea a fost realizata cu succes")
else:
   print("Solicitarea are buba")

from bs4 import BeautifulSoup

#Cream liste in care vom stoca datele obtinute pentru scrierea in fisier
BRAND=[]
NUME=[]
CODARTICOL=[]
PRET=[]
PRET_Redus=[]

#definim variabila pentru parcurgerea paginilor
page_num=2



while requests.get(url, headers=Headers).status_code==200  :
    
    
    soup = BeautifulSoup(html, 'html.parser')
    #Gasim toate elementele de tip div cu clasa necesara
    products = soup.find_all('div', class_='col-6 col-sm-6 col-md-4 col-lg-4 col-xl-3')


    #cream noul url pt pagina urmatoare
    url=f'{base_url}?page={page_num}'
    page_num=page_num+1
    
     

    #html pentru noua pagina
    html = requests.get(url, headers=Headers).content
    
    #extrasem din pagina informatiile referitoare la butonul de "Urmatoarea pagina"
    next_page_link = soup.find("a", {"class": "pagination__item pagination__item--prev pagination__item-arrow btn"}) 

    
    #Pentru fiecare produs gasim anterior, luam brandul, numele, id-ul, pretul si pretul redus(daca exista)
    #Preturile vor fi transformate prin cast in date de tip float


    for product in products:
        #Luam brandul, numele, id-ul si pretul produsului
        brand = product.find('div', class_='product-collection__more-info mb-3').text.strip()
        BRAND.append(brand)
        nume= product.find('h4', class_='m-0').text.strip()
        NUME.append(nume)
        codArticol=product.find('p', class_='m-0').text.strip().replace('Cod articol: ','')
        CODARTICOL.append(codArticol)
        pret = product.find('span', class_ = 'price' ).text.strip().replace(' lei',' ')
        Pret=[]
        for x in pret:
            if x!=" ":
                Pret.append(x)
            else:
                break
        pret="".join(Pret)

        # pret_redus=product.find('span', class_ = 'price price--sale')
        # Daca exista, luam si pretul redus
            
        if product.find('span', class_ = 'price price--sale') is None:
            pret_redus = 'NaN'
            #pret = product.find('span', class_ = 'price').text.strip().replace(' lei','')
        else:
            pret_redus=product.find('span', class_= 'price price--sale').text.strip().replace(' lei','').replace(pret, "")
            pret_redus=pret_redus.replace(",",".")
            pret_redus=float(pret_redus)
            #print("s a facut strip", pret_redus)

        #cast la float
        #tratam cazul in care pretul este mai mare de 999.99 si vor aparea 2 puncte in float-> va produce eroare
        if len(pret)<7:
            pret=pret.replace(",",".")
        else:
            pret=pret.replace(",","", 1).replace(",",".")
        pret=float(pret)

        PRET.append(pret)
        PRET_Redus.append(pret_redus)

        #afisam si pe ecran    
        print(brand, nume, codArticol, pret, pret_redus) 
    
    #daca nu avem butonul de "Urmatoarea pagina "  in pagina curenta, inseamna ca este ultima pagina si iesim din while/
    # am terminat de extras produse din categoria respectiva
    if  next_page_link is None:
       break
   



#importam csv pentru scrierea datelor in fisier csv
import csv

CapTabel=["Cod_Articol","Brand","Nume","Pret", "Pret_Redus"]

#Cu fisierul deschis, scriem capul de tabel si informatiile obtinute, pe fiecare rand
with open('Produse_Animax.csv', 'w',encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    #scriem capul de tabel
    writer.writerow(CapTabel)

    #scriem datele in fisier
    for i in range(len(BRAND)):
        
        writer.writerow([CODARTICOL[i],BRAND[i],NUME[i],PRET[i],PRET_Redus[i]])


