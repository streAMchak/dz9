import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

class CurrencyConverter:
    def __init__(self, exchange_rate):
        self.exchange_rate = exchange_rate 

    def convert_to_usd(self, amount):
        return amount / self.exchange_rate

def get_exchange_rate():
    url = "https://bank.gov.ua/ua/markets/exchangerates"  
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Помилка при завантаженні сайту!")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        table = soup.find('table', class_='table')
        rows = table.find_all('tr')

        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 0 and columns[0].text.strip() == "Долар США":
                exchange_rate = float(columns[1].text.strip().replace(',', '.'))
                return exchange_rate
    except Exception as e:
        print(f"Помилка при парсингу даних: {e}")
        return None

def on_convert_button_click():
    exchange_rate = get_exchange_rate()
    
    if exchange_rate is None:
        messagebox.showerror("Помилка", "Не вдалося отримати курс валют.")
        return

    try:
        amount_in_local_currency = float(entry_amount.get())

        converter = CurrencyConverter(exchange_rate)

        amount_in_usd = converter.convert_to_usd(amount_in_local_currency)

        label_result.config(text=f"Це еквівалентно {amount_in_usd:.2f} доларів США.")
    
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть правильне число.")

root = tk.Tk()
root.title("Конвертер валют")
root.geometry("400x200")

label_prompt = tk.Label(root, text="Введіть кількість валюти вашої країни:")
label_prompt.pack(pady=10)

entry_amount = tk.Entry(root, width=20)
entry_amount.pack(pady=5)

convert_button = tk.Button(root, text="Конвертувати", command=on_convert_button_click)
convert_button.pack(pady=10)

label_result = tk.Label(root, text="", font=("Helvetica", 12))
label_result.pack(pady=10)

root.mainloop()
