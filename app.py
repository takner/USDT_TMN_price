from flask import Flask, jsonify
import requests

app = Flask(__name__)

TETHER_API_URL = "https://api.wallex.ir/v1/coin-price-list?keys=USDT&fields=quotes.USDT.price,quotes.TMN.price"
BITCOIN_API_URL = "https://api.wallex.ir/v1/coin-price-list?keys=BTC&fields=quotes.USDT.price"
BNB_API_URL = "https://api.wallex.ir/v1/coin-price-list?keys=BNB&fields=quotes.USDT.price"
PAXG_API_URL = "https://api.wallex.ir/v1/coin-price-list?keys=PAXG&fields=quotes.USDT.price"
TON_API_URL = "https://api.wallex.ir/v1/coin-price-list?keys=TON&fields=quotes.USDT.price"


def get_prices():
    """
     API get api for usd price from wallex

    Returns:
        dict: if we have error.
    """
    try:
        tether_response = requests.get(TETHER_API_URL)
        tether_response.raise_for_status()
        tether_data = tether_response.json()
        bitcoin_response = requests.get(BITCOIN_API_URL)
        bitcoin_response.raise_for_status()
        bitcoin_data = bitcoin_response.json()
        bnb_response = requests.get(BNB_API_URL)
        bnb_response.raise_for_status()
        bnb_data = bnb_response.json()
        paxg_response = requests.get(PAXG_API_URL)
        paxg_response.raise_for_status()
        paxg_data = paxg_response.json()
        ton_response = requests.get(TON_API_URL)
        ton_response.raise_for_status()
        ton_data = ton_response.json()

        if (
            tether_data
            and tether_data["success"]
            and tether_data["result"]
            and tether_data["result"]["markets"]
            and bitcoin_data
            and bitcoin_data["success"]
            and bitcoin_data["result"]
            and bitcoin_data["result"]["markets"]
            and bnb_data
            and bnb_data["success"]
            and bnb_data["result"]
            and bnb_data["result"]["markets"]
            and paxg_data
            and paxg_data["success"]
            and paxg_data["result"]
            and paxg_data["result"]["markets"]
            and ton_data
            and ton_data["success"]
            and ton_data["result"]
            and ton_data["result"]["markets"]
        ):
            usdt_price = tether_data["result"]["markets"][0]["quotes"]["USDT"]["price"]
            tmn_price = tether_data["result"]["markets"][0]["quotes"]["TMN"]["price"]
            btc_price_usdt = bitcoin_data["result"]["markets"][0]["quotes"]["USDT"]["price"]
            bnb_price_usdt = bnb_data["result"]["markets"][0]["quotes"]["USDT"]["price"]
            paxg_price_usdt = paxg_data["result"]["markets"][0]["quotes"]["USDT"]["price"]
            ton_price_usdt = ton_data["result"]["markets"][0]["quotes"]["USDT"]["price"]

            dollar_price = float(tmn_price) / float(usdt_price)
            dollar_price_rounded = round(dollar_price, 1)  

            tether_price_rounded = round(float(tmn_price), 1)

            btc_price_usdt_rounded = round(float(btc_price_usdt), 1)
            bnb_price_usdt_rounded = round(float(bnb_price_usdt), 1)
            paxg_price_usdt_rounded = round(float(paxg_price_usdt), 1)
            ton_price_usdt_rounded = round(float(ton_price_usdt), 1)


            return {
                "tether_price": tether_price_rounded,
                "dollar_price": dollar_price_rounded,
                "bitcoin_price": btc_price_usdt_rounded,
                "bnb_price": bnb_price_usdt_rounded,
                "gold_price": paxg_price_usdt_rounded,
                "ton_price": ton_price_usdt_rounded,
            }
        else:
            print(" API no data for.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"error in API: {e}")
        return None
    except (KeyError, TypeError, ValueError) as e:
        print(f"error in data process API: {e}")
        return None


@app.route('/prices')
def get_current_prices():
    """
    Endpoint for chenge to price JSON.
    """
    prices = get_prices()
    if prices:
        return jsonify(
            {
                "tether": prices["tether_price"],
                "dollar": prices["dollar_price"],
                "bitcoin": prices["bitcoin_price"],
                "bnb": prices["bnb_price"],
                "gold": prices["gold_price"],
                "ton": prices["ton_price"],
            }
        )
    else:
        return jsonify({"error": "Could not retrieve prices"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 