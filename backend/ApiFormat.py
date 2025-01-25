import requests #retreive data from Api
import pandas as pd #manipulation of data
from io import StringIO #Data conversion/ respons conversion (stores values in ram, easier to load data with pd)
from tkinter import *
from datetime import date 

def get_norges_bank_api(date_to_retreive):
    df = pd.DataFrame() #Initialize the dataframe 
    if date_to_retreive is None: #sjekker om vi har oppgitt en dato vi vil hente data fra
        date_to_retreive = date.today().strftime("%Y-%m-%d") #Hvis If'en ikke går gjennom, så bruker funskjonen dagens dato og fjerner unødig info
        
    response = requests.get(f"https://data.norges-bank.no/api/data/EXR/B.targeted_value+USD+GBP+DKK+SEK+HKD+EUR.NOK.SP?format=csv&startPeriod={date_to_retreive}&endPeriod={date_to_retreive}&locale=no")
                
    if response.status_code == 200: #Sjekker om vi har contact med Api
        df = pd.read_csv(StringIO(response.text), delimiter=';') #populerer df med data fra apiet. StringIO lurer systemet til å tro at csv er lagret i hdd, delimiter skiller mellom objektene i fila
        return df.sort_values(by="Basisvaluta") #Sorterer df alfabetisk
    else:
        print(f"Failed to retrieve data {date_to_retreive}:", response.status_code) #Dersom vi får feilmelding fra Api
    
df = get_norges_bank_api("2025-01-23") #Hardcoder dato fra sist fredag

def main():
    global df # henter inn df fra global
    filtered_df=df[(df["Basisvaluta"]==ent_options.get())] #filtrerer df'en i henhold til dropdown menyen (beholder kun valutanavn)
    filtered_df=filtered_df.iloc[0] #selecterer den første raden i dataframen
    valutakurs=float(filtered_df["OBS_VALUE"].replace(",",".")) #gjør om til float og erstatter komma med punktum i desimalene
    
    if filtered_df["Multiplikator"] == "Hundre": #likestiller basisenheten i f.eks. (sek, dkk) 
        valutakurs=valutakurs/100

    value_nok=ent1.get() #henter inn verdiene vi har tasta inn i inputene
    targeted_value=ent2.get()
    
    if value_nok:
        result=f"{value_nok} {filtered_df['QUOTE_CUR']} blir til {round((value_nok / valutakurs),2)} i {filtered_df['BASE_CUR']}."
    elif targeted_value:
        result=f"{targeted_value} {filtered_df['BASE_CUR']} blir til {round((targeted_value * valutakurs),2)} i {filtered_df['QUOTE_CUR']}"
    else:
        result=("Ugyldig verdi!")
    #her sjekker vi om det er nok eller annen valuta som er tastet inn og gjennomfører konvertering av valutaene.
    
    ent1.set(0)    
    ent2.set(0)    
    #Nullstiller entriene
      
    lbl_answer.config(text=f"{result} \n Hentet fra Norgesbank {filtered_df['TIME_PERIOD']}.")
    #skriver svaret med konvertert valuta
        

#fjerner placeholder når du trykker inn i entrien
def clear_ent(event):
    if event.widget.get() == "0":
        event.widget.delete(0, END)

#TkInter vinduet
root=Tk()
root.title("Valutakalkulator")
root.geometry("260x200")

kvoteringsvaluta=StringVar()
kvoteringsvaluta.set(str(df["Kvoteringsvaluta"].iloc[0]))
lbl_1=Label(root, textvariable= kvoteringsvaluta)
lbl_1.grid(row=0, column=0, padx=5, pady=5, sticky=W)

ent1=DoubleVar(value=0)
ent_1=Entry(root,width=10,textvariable=ent1)
ent_1.grid(row=0,column=1,padx=5,pady=5,sticky=E)
ent_1.bind("<FocusIn>",clear_ent) #nullstiller entriene

ent_options=StringVar(value=df["Basisvaluta"].iloc[0])
options=df["Basisvaluta"].tolist()
dropdown=OptionMenu(root, ent_options,*options)
dropdown.grid(row=1,column=0,padx=5,pady=10,sticky=W)

ent2=DoubleVar(value=0)
ent_2=Entry(root,width=10,textvariable=ent2)
ent_2.grid(row=1,column=1,padx=5,pady=5,sticky=E)
ent_2.bind("<FocusIn>",clear_ent)

root.grid_columnconfigure(0, weight=1)  # Make column 0 expandable horizontally
root.grid_columnconfigure(1, weight=1)  # Make column 1 expandable horizontally

lbl_answer=Label(root, width=25,text="")
lbl_answer.grid(row=5,column=0,columnspan=2,padx=5,sticky=NSEW)

btn=Button(root, text="Beregn", command=main)
btn.grid(row=4,column=1,padx=5,pady=10,sticky=E)

root.mainloop()