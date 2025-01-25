import requests
import pandas as pd
from io import StringIO
from tkinter import *
from datetime import date

def get_norges_bank_api(dato_to_ret):
    if dato_to_ret is not None:
        next
    else: 
        dato_to_ret = date.today().strftime("%Y-%m-%d")
      
    response = requests.get(f"https://data.norges-bank.no/api/data/EXR/B.USD+GBP+RUB+EUR.NOK.SP?format=csv&startPeriod={dato_to_ret}&endPeriod={dato_to_ret}&locale=no")
                
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text), delimiter=';')        
    else:
        print(f"Failed to retrieve data {dato_to_ret}:", response.status_code)

def main():
    global df
    text_widget_answer.delete("1.0", END)
    
    filtered_df=df[(df["Basisvaluta"]==ent_options.get())].iloc[0]
    valutakurs=float(filtered_df["OBS_VALUE"].replace(",","."))
    
    nok=ent1.get()
    usd=ent2.get()
    
    if nok:
        result=f"{nok} {filtered_df['QUOTE_CUR']} blir til {round((nok / valutakurs),2)} i {filtered_df['BASE_CUR']}."
    elif usd:
        result=f"{usd} {filtered_df['BASE_CUR']} blir til {round((usd * valutakurs),2)} i {filtered_df['QUOTE_CUR']}"
    else:
        result=("Ugyldig verdi!")  
      
    text_widget_answer.insert("1.0", result + "\n\n", "black")
    text_widget_answer.insert("3.0", f"Data fra Norgesbank API: \n", "black")
    text_widget_answer.insert("end", "- " +filtered_df['TIME_PERIOD'], "black")
    
    ent1.set(0)
    ent2.set(0)
    
df = get_norges_bank_api("2025-01-23")

# TK INTER STUFF
myWindow = Tk()
myWindow.title("Valutakalkulator")
myWindow.geometry("350x220")

# Add Button
btn = Button(myWindow, text="Beregn", command=main)
btn.grid(row=3, column=1, padx=5, pady=10, sticky=E)

# Add Kvoteringsvaluta Label
kvoteringsvaluta = StringVar()
kvoteringsvaluta.set(str(df["Kvoteringsvaluta"].iloc[0]))
lbl_1 = Label(myWindow, textvariable=kvoteringsvaluta)
lbl_1.grid(row=0, column=0, padx=5, pady=5, sticky=W)

# Add Entry 1
ent1 = DoubleVar(value=0)
ent_1 = Entry(myWindow, width=10, textvariable=ent1)
ent_1.grid(row=0, column=1, padx=5, pady=5, sticky=E)

# Add Dropdown Menu
ent_options = StringVar(value=df["Basisvaluta"][0])
options = df["Basisvaluta"].tolist()
dropdown = OptionMenu(myWindow, ent_options, *options)
dropdown.grid(row=1, column=0, padx=5, pady=10, sticky=W)

# Add Entry 2
ent2 = DoubleVar(value=0)
ent_2 = Entry(myWindow, width=10, textvariable=ent2)
ent_2.grid(row=1, column=1, padx=5, pady=5, sticky=E)

# Add Text Widget
text_widget_answer = Text(myWindow, width=40, height=5, wrap="word")
text_widget_answer.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Configure grid rows and columns for resizing
myWindow.grid_rowconfigure(4, weight=1)  # Make row 4 expandable vertically
myWindow.grid_columnconfigure(0, weight=1)  # Make column 0 expandable horizontally
myWindow.grid_columnconfigure(1, weight=1)  # Make column 1 expandable horizontally

myWindow.mainloop()