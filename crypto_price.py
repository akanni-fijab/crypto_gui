#Name :Al Hassan Oluwatobi Fijabi 242030010
#       Maduka Chidera Joachim 242030090
#      Adoga Salamatu Lorna 241080002
#      Dzungu Kumasughun Faith 242030078


import os

import dotenv
import requests

# never make api calls across files
dotenv.load_dotenv()  # Load envars

api = os.getenv("api_key")  # store api key form .env file
curr_api_key = os.getenv("curr_api_key")  # get currency conversion api



try:

    def other_cur(denomination):
        url = f"https://api.currencyapi.com/v3/latest?apikey={curr_api_key}&currencies=EUR%2CGBP%2CNGN"
        req = requests.get(url=url)
        json_obj = req.json() # formatting
       

        if denomination == "NGN":
            return int(json_obj["data"]["NGN"]["value"])  # incase is returned as str
        elif denomination == "EUR":
            return json_obj["data"]["EUR"]["value"]
        elif denomination == "GBP":
            return json_obj["data"]["GBP"]["value"]

    def get_price(choice, n, denomination=None):
        if denomination is None:  # assume currency is dollars
            url = f"https://rest.coincap.io/v3/assets/{choice}?apiKey={api}"
            req = requests.get(url=url)
            json_obj = req.json()  # store req as a json object for easy indexing

            crypto_price = float(json_obj["data"]["priceUsd"])
            return f"{crypto_price * n:,.2f} "
        else:
            url = f"https://rest.coincap.io/v3/assets/{choice}?apiKey={api}"
            req = requests.get(url=url)
            json_obj = req.json()  # store req as a json object for easy indexing

            crypto_price = float(json_obj["data"]["priceUsd"])
            result = crypto_price * n * other_cur(denomination)

        return f"{result:,.2f}"

except requests.exceptions.RequestException:
    print("A network issue occured")



