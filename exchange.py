from flask import Flask, render_template, request
import requests
import json
import apikey as apikey

app = Flask(__name__)

_myKey = apikey.myKey


def getExchange(toCurrency, fromCurrency) -> float:
    # toCurrency: str, fromCurrency: str
    # both must be "XXX", an abbreviation of a currency
    #   i.e. USD or CNY
    url = "https://openexchangerates.org/api/latest.json?app_id=" + _myKey + "&base=USD"
    response = json.loads(requests.request("GET", url).text)

    if fromCurrency == "USD":
        # USD to other
        return response["rates"][toCurrency]
    elif toCurrency == "USD":
        # other to USD
        return (1 / response["rates"][fromCurrency])
    else:
        """ 
        other to other
        eg: euro to gbp = 1EUR = 0.86 GBP
        - usd to euro = 1USD = 0.93 EUR
        - usd to gbp = 1USD = .8 GBP
        - calculate euro to gbp: .8 / .93 = .86
        """
        return response["rates"][toCurrency] / response["rates"][fromCurrency]
    

    # EURO TO POUND 
    # 

def checkRequestLimit() -> bool:
    url = "https://openexchangerates.org/api/usage.json?app_id=" + _myKey
    response = json.loads(requests.request("GET", url).text)
    return response["data"]["usage"]["requests_remaining"] > 5

def dropdown():
    currency = [
        "USD",	
        "EUR",	
        "JPY",	
        "GBP",	
        "AUD",	
        "CAD",	
        "CHF",	
        "CNY",	
        "HKD",	
        "NZD",	
        "AED", 
        "AMD",	
        "ANG",	
        "ARS",	
        "AZN",	
        "BBD",	
        "BDT",	
        "BGN",	
        "BHD",	
        "BMD",	
        "BOB",	
        "BRL",	
        "BTN",	
        "BYN",	
        "BZD",	
        "CLP",	
        "COP",	
        "CRC",	
        "CUP",	
        "CZK",	
        "DKK",	
        "DOP",	
        "DZD",	
        "EEK",	
        "EGP",	
        "ETB",	
        "GHS", 
        "GTQ",	
        "HNL",	
        "HRK",	
        "HTG",	
        "HUF",	
        "IDR",	
        "ILS",	
        "INR",	
        "IQD",	
        "IRR",	
        "ISK",	 
        "JMD", 
        "KES", 
        "KHR",	 
        "KPW",	 
        "KRW",	 
        "KWD",	 
        "LAK",	 
        "LBP",	 
        "LKR",	 
        "LRD", 
        "LYD",	 
        "MAD",	 
        "MDL",	 
        "MKD",	 
        "MNT",	 
        "MXN",	 
        "MYR",	 
        "NGN",	 
        "NIO",	
        "NOK", 
        "NPR",	
        "PAB",	
        "PEN",	
        "PGK",	
        "PHP",	
        "PKR",	
        "PLN",	
        "PYG",	
        "QAR",	
        "RON",	
        "RSD",	
        "RUB",	
        "RWF",	
        "SAR",	
        "SDG",	
        "SEK",	
        "SGD",	
        "SOS",	
        "SSP",	
        "SVC",	
        "SYP",	
        "THB",	
        "TND",	
        "TRY",	
        "TWD",	
        "TZS",	
        "UAH",	
        "UGX",	
        "UYU",	
        "VES",	
        "VND",	
        "WST",
        "YER",	
        "ZAR",	
        "ZMW"]
    return currency

@app.route('/')
def index():
    return render_template("index.html", currency = dropdown(), returnString = "Select currencies from above.")

@app.route('/select', methods=["POST"])
def getInfo():
    if checkRequestLimit():
        quant = float(request.form["quantity"])
        if quant == "":
            return render_template("index.html", currency = dropdown(), returnString = "Select a number.")
        baseC = request.form["base"]
        targetC = request.form["target"]
        converted = getExchange(targetC, baseC)
        rStr = f"{quant:.0f} {baseC} is equivalent to {round((converted * quant), 2)} {targetC}"
        return render_template("index.html", currency = dropdown(), returnString = rStr)
    else:
        return render_template("index.html", currency = dropdown(), returnString = "We have run out of API requests. Try again soon!")


if __name__ == "__main__":
    #getExchange()
    app.run(host="0.0.0.0", port=80, debug=True)