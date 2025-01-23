import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd
from io import StringIO
from datetime import date

# Function to fetch data from the web
def fetch_exchange_data():
    try:
        # Replace this URL with your actual data source
        time_today = date.today().strftime("%Y-%m-%d")
        url = f'https://data.norges-bank.no/api/data/EXR/B.USD.NOK.SP?format=csv&startPeriod={time_today}&endPeriod={time_today}&locale=no'  # Example CSV URL
        response = requests.get(url)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text), delimiter=';')
            return data.iloc[0]
        else:
            messagebox.showerror("Error", f"Failed to fetch data: {response.status_code}")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

# Function to perform the calculation
def calculate():
    try:
        amount = float(amount_entry.get().strip())
        rate = float(exchange_data['OBS_VALUE'].replace(',', '.'))
        result = amount * rate
        result_label.config(text=f"Converted Amount: {result:.2f} NOK @ {exchange_data['TIME_PERIOD']}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for the amount.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("Currency Exchange Calculator")

# Fetch exchange data at the start
exchange_data = fetch_exchange_data()
if exchange_data is None:
    exit()  # Exit the program if data cannot be loaded

# Labels and entries
tk.Label(root, text="FRA USD:").grid(row=0, column=0, pady=5, padx=5)
tk.Label(root, text="TIL NOK:").grid(row=1, column=0, pady=5, padx=5)

tk.Label(root, text="mengde:").grid(row=2, column=0, pady=5, padx=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, pady=5, padx=5)

# Button to calculate
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result label
result_label = tk.Label(root, text="Converted Amount: ", fg="blue")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()