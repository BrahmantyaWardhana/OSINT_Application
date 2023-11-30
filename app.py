import os
from tkinter import Tk, Frame, Button, Entry, Label

import requests
import ttkbootstrap as ttk
from dotenvy import load_env, read_file
from ttkbootstrap.constants import *

from modules.exchangeRate import ExchangeRateApi


class Login(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.parent = parent

        # form header
        hdr_txt = "Select the API you would like to use"
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=10)

        # data frame
        self.data_frame = Frame(self)
        self.data_frame.pack(pady=10)

        # button frame
        self.btn_frame = Frame(self)
        self.btn_frame.pack()

        # Coin Market Cap Button
        (ttk.Button(self.btn_frame,
                    text='Coin Market Cap',  # Button name
                    # Function that button executes on press - only use function name without ending '()'
                    command=self.coin_market_cap_btn_press)
         .pack(side='left', padx=10, pady=10))

        # Exchange Rate Converter Button
        (ttk.Button(self.btn_frame,
                    text='Exchange Rate Converter',
                    command=self.exchange_rate_converter_btn_press)
         .pack(side='left', padx=10, pady=10))

        # Country Data Button
        (ttk.Button(self.btn_frame,
                    text='Country Data',
                    command=self.country_data_btn_press)
         .pack(side='left', padx=10, pady=10))

        # API 4 Button
        (ttk.Button(self.btn_frame,
                    text='Sunrise Sunset',
                    command=self.sunrise_sunset_btn_press)
         .pack(side='left', padx=10, pady=10))

    # Functions that execute when user clicks any of the API selectors on the main menu
    def coin_market_cap_btn_press(self):
        self.destroy()  # This will 'destroy' the current frame, in this case, the API selection page on API press
        CoinMarketCapFormPage(root).pack()  # This will call the respective API frame to create a new page

    def exchange_rate_converter_btn_press(self):
        self.destroy()
        ExchangeRateConverterFormPage(root).pack()

    def country_data_btn_press(self):
        self.destroy()
        CountryDataFormPage(root).pack()

    def sunrise_sunset_btn_press(self):
        self.destroy()
        SunriseSunset(root).pack()


class CoinMarketCapFormPage(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        super().__init__()
        self.parent = parent

        # Form Variables
        # Will use 'Bitcoin / BTC / 1' as default values unless changes by user in the
        # '# form entries' section
        self.coin_full_name = ttk.StringVar(value="Bitcoin")
        self.coin_abbreviation = ttk.StringVar(value="BTC")
        self.coin_number_ranking = ttk.IntVar(value=1)

        # form header
        hdr_txt = "Get Coin Data using either it's full name, abbreviation, or ranking"
        hdr = ttk.Label(master=self, text=hdr_txt)
        hdr.pack(fill=X, pady=10)

        # form entries
        self.create_form_entry("Crypto Coin Full Name", self.coin_full_name)
        self.create_form_entry("Crypto Coin Abbreviation", self.coin_abbreviation)
        self.create_form_entry("Crypto Coin Ranking", self.coin_number_ranking)

        # data frame
        self.data_frame = Frame(self)
        self.data_frame.pack(pady=10)

        # button frame
        self.btn_frame = Frame(self)
        self.btn_frame.pack()

        # Back Button
        ttk.Button(self.btn_frame, text='Back',
                   command=self.back).pack(side='left', padx=10, pady=10)

        # Submit button
        ttk.Button(self.btn_frame, text='Submit',
                   command=self.submit).pack(side='left', padx=10, pady=10)

    # Form entry styling
    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title())
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    # INSERT ANY API ACTIONS WITHIN THE FOLLOWING 'submit' FUNCTION
    def submit(self):
        print("Crypto Coin Full Name:", self.coin_full_name.get())
        print("Crypto Coin Abbreviation:", self.coin_abbreviation.get())
        print("Crypto Coin Ranking:", self.coin_number_ranking.get())

        self.destroy()
        Login(root).pack()

    # Return to the API selector page
    def back(self):
        self.destroy()
        Login(root).pack()


class ExchangeRateConverterFormPage(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        super().__init__()
        self.parent = parent

        # Form Variables
        # Will use 'USD' as the base currency and 'CAD' as the 'USD -> CAD' conversion
        self.base_currency_abbreviation = ttk.StringVar(value="USD")
        self.converted_currency_abbreviation = ttk.StringVar(value="CAD")

        # form header
        hdr_txt = "Currency Converter"
        hdr = ttk.Label(master=self, text=hdr_txt)
        hdr.pack(fill=X, pady=10)

        # form entries
        self.create_form_entry("Base Currency Abbreviation", self.base_currency_abbreviation)
        self.create_form_entry("Converted Currency Abbreviation", self.converted_currency_abbreviation)

        # data frame
        self.data_frame = Frame(self)
        self.data_frame.pack(pady=10)

        # button frame
        self.btn_frame = Frame(self)
        self.btn_frame.pack()

        # Back Button
        ttk.Button(self.btn_frame, text='Back',
                   command=self.back).pack(side='left', padx=10, pady=10)

        # Submit button
        ttk.Button(self.btn_frame, text='Submit',
                   command=self.submit).pack(side='left', padx=10, pady=10)

    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title())
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    # INSERT ANY API ACTIONS WITHIN THE FOLLOWING 'submit' FUNCTION
    def submit(self, ):
        load_env(read_file('.env'))
        exchange_rate_api_secret = os.environ.get('EXCHANGE_RATE_API_SECRET')
        exchange_rate_api = ExchangeRateApi(exchange_rate_api_secret)

        print("Base Currency Abbreviation:", self.base_currency_abbreviation.get().upper())
        print("Converted Currency Abbreviation:", self.converted_currency_abbreviation.get().upper())

        exchange_rate = (exchange_rate_api.get_exchange_rates
                         (self.base_currency_abbreviation.get().upper(),
                          self.converted_currency_abbreviation.get().upper()))

        if exchange_rate is not None:
            print(f'Exchange rate from {self.base_currency_abbreviation.get().upper()} to '
                  f'{self.converted_currency_abbreviation.get().upper()}: {exchange_rate}')
        else:
            print(f'Unable to fetch exchange rate for {self.base_currency_abbreviation.get().upper()} to '
                  f'{self.converted_currency_abbreviation.get().upper()}')

        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container,
                        text=f"1 {self.base_currency_abbreviation.get().upper()} "
                             f"= {exchange_rate} {self.converted_currency_abbreviation.get().upper()}")
        lbl.pack(side=LEFT, padx=5)

    # Return to the API selector page
    def back(self):
        self.destroy()
        Login(root).pack()


class CountryDataFormPage(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        super().__init__()
        self.parent = parent

        # Form Variables
        # Will use 'USD' as the base currency and 'CAD' as the 'USD -> CAD' conversion
        self.country_name = ttk.StringVar(value="Canada")
        self.country_capital = ttk.StringVar

        # form header
        hdr_txt = "Enter a Name of a Country to get its Information"
        hdr = ttk.Label(master=self, text=hdr_txt)
        hdr.pack(fill=X, pady=10)

        # form entries
        self.create_form_entry("Country Name", self.country_name)

        # data frame
        self.data_frame = Frame(self)
        self.data_frame.pack(pady=10)

        # button frame
        self.btn_frame = Frame(self)
        self.btn_frame.pack()

        # Back Button
        ttk.Button(self.btn_frame, text='Back',
                   command=self.back).pack(side='left', padx=10, pady=10)

        # Submit button
        ttk.Button(self.btn_frame, text='Submit',
                   command=self.submit).pack(side='left', padx=10, pady=10)

    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title())
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    # INSERT ANY API ACTIONS WITHIN THE FOLLOWING 'submit' FUNCTION
    def submit(self):
        print("Country:", self.country_name.get())

        self.country_capital = ttk.StringVar(value="")

        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text="Capital", textvariable=self.country_capital)
        lbl.pack(side=LEFT, padx=5)

        # self.destroy()
        # Login(root).pack()

    # Return to the API selector page
    def back(self):
        self.destroy()
        Login(root).pack()


class SunriseSunset(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        super().__init__()
        self.parent = parent

        # Form Variables
        # Will 'America/New_York' has the coordinate location
        self.longitude = ttk.StringVar(value='40.71427')
        self.latitude = ttk.StringVar(value='-74.00597')

        # form header
        hdr_txt = "Enter a Longitude and Latitude to get Sunrise and Sunset Info - Powered by SunriseSunset.io"
        hdr = ttk.Label(master=self, text=hdr_txt)
        hdr.pack(fill=X, pady=10)

        # form entries
        self.create_form_entry("Longitude", self.longitude)
        self.create_form_entry("Latitude", self.latitude)

        # data frame
        self.data_frame = Frame(self)
        self.data_frame.pack(pady=10)

        # button frame
        self.btn_frame = Frame(self)
        self.btn_frame.pack()

        # Back Button
        ttk.Button(self.btn_frame, text='Back',
                   command=self.back).pack(side='left', padx=10, pady=10)

        # Submit button
        ttk.Button(self.btn_frame, text='Submit',
                   command=self.submit).pack(side='left', padx=10, pady=10)

    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title())
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    # INSERT ANY API ACTIONS WITHIN THE FOLLOWING 'submit' FUNCTION
    def submit(self):
        api_url = f'https://api.sunrisesunset.io/json?lat={self.latitude.get()}&lng={self.longitude.get()}'

        try:
            response = requests.get(api_url)
            data = response.json()
            print(data)
        except Exception as e:
            print(f'An error occurred: {str(e)}')

        print("Longitude:", self.longitude.get())
        print("Latitude:", self.latitude.get())



    # Return to the API selector page
    def back(self):
        self.destroy()
        Login(root).pack()


if __name__ == "__main__":
    root = ttk.Window("OSINT Application", "superhero", resizable=(False, False))
    Login(root).pack()
    root.mainloop()
