import requests
import pandas as pd
from io import StringIO
from tkinter import *
from datetime import date

time_today = date.today().strftime("%Y-%m-%d")
url = f"https://data.norges-bank.no/api/data/EXR/B.USD+GBP+RUB+EUR.NOK.SP?format=csv&startPeriod={time_today}&endPeriod={time_today}&locale=no"

#Get request til Api'et
response = requests.get(url)


if response.status_code == 200:
    data = response.text
    df = pd.read_csv(StringIO(data), delimiter=';')
    #df = df.iloc[0]
    print(df)

else:
    print("Failed to retrieve data:", response.status_code)


def main():
    filtered_df=df[(df["BASE_CUR"]==ent_options.get())]
    basisvaluta.set(ent_options.get())
    filtered_df=filtered_df.iloc[0]
    #filtered_df=df[(df["BASE_CUR"]=="USD")]
    valutakurs=float(filtered_df["OBS_VALUE"].replace(",","."))
    total=0.0
    
    
    nok=float(ent1.get().strip())
    usd=float(ent2.get().strip())
    
    if nok:
        result=f"{nok} {filtered_df["QUOTE_CUR"]} blir til {round((nok / valutakurs),2)} i {filtered_df["BASE_CUR"]}."
    
    elif usd:
        result=f"{usd} {filtered_df["BASE_CUR"]} blir til {round((usd * valutakurs),2)} i {filtered_df["QUOTE_CUR"]}"
        
    else:
        result=("Ugyldig verdi!")
    
    ent1.set(0)    
    ent2.set(0)    
        
        


    #total=(kurs1 * kurs2)

    lbl_answer.config(text=result)
    lbl_update_time.config(text=f"Hentet fra Norgesbank {filtered_df["TIME_PERIOD"]}.")

myWindow=Tk()
myWindow.title("Valutakalkulator")

kvoteringsvaluta=StringVar()
kvoteringsvaluta.set(str(df["Kvoteringsvaluta"].iloc[0]))
lbl_1=Label(myWindow, textvariable= kvoteringsvaluta)
lbl_1.grid(row=0, column=0, padx=5, pady=5, sticky=W)

ent1=StringVar(value=0)
ent_1=Entry(myWindow,width=10,textvariable=ent1)
ent_1.grid(row=0,column=1,padx=5,pady=5)


basisvaluta=StringVar()
basisvaluta.set(df["Basisvaluta"].iloc[0])
lbl_2=Label(myWindow, textvariable=basisvaluta)
lbl_2.grid(row=1, column=0, padx=5, pady=5, sticky=W)

ent2=StringVar(value=0)
ent_2=Entry(myWindow,width=10,textvariable=ent2)
ent_2.grid(row=1,column=1,padx=5,pady=5)

lbl_answer=Label(myWindow, text="")
lbl_answer.grid(row=5,column=0,padx=5,sticky=W)

lbl_update_time=Label(myWindow,text="")
lbl_update_time.grid(row=6,column=0,padx=5,sticky=W)

btn=Button(myWindow,text="Beregn",command=main)
btn.grid(row=4,column=1,padx=5,pady=10,sticky=SE)


ent_options=StringVar(value=df["BASE_CUR"][0])
options=df["BASE_CUR"].tolist()
dropdown=OptionMenu(myWindow, ent_options,*options)
dropdown.grid(row=8,column=0,padx=5,pady=10,sticky=W)


myWindow.mainloop()