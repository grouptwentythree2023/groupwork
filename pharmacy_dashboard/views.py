from collections import Counter
import json

from django.shortcuts import render
from django.conf import settings
 

import requests
from polygon import RESTClient
from datetime import datetime, date

from django.shortcuts import render
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
from io import BytesIO
import base64

from alpha_vantage.foreignexchange import ForeignExchange


# Create your views here.
def dashboard(request):

    # image_base64 = Stock_Data()
    competitor_plot = Stock_of_Competitors()
    # exchange_rate_text = Exchange_Rate()
    
    retail_sale = gdp_core_markets()
    # trending_scks = trending_sickness()
    # vaccination_data = vaccination()

    
    context = {
                # 'image_base64': image_base64,
                # 'exchange_rate_text':exchange_rate_text,
                'competitor_plot':competitor_plot,
                'retail_sale':retail_sale,
                # 'trending_scks':trending_scks,
                # 'vaccination_data': vaccination_data,
               }

    
    return render(request, 'dashboard/home.html', context)




def dict_data(data_list):
    converted_data = []
    for item in data_list:
        data_dict = {
            "open": item.open,
            "high": item.high,
            "low": item.low,
            "close": item.close,
            "volume": item.volume,
            "vwap": item.vwap,
            "timestamp": item.timestamp,
            "transactions": item.transactions,
            "otc": item.otc
        }
        converted_data.append(data_dict)
    return converted_data





def Stock_Data():

    client = RESTClient(settings.POLYGONE_API_KEY)

    aggs = client.get_aggs(
        "AAPL",
        1,
        "day",
        "2022-01-01",
        "2023-02-03",
    )
    # print(aggs)
    stock_data = dict_data(aggs)
    
    # print(stock_data)
    #   stock market data
    
    
    
    # stock_data = [
    #     {"open": 177.83, "high": 182.88, "low": 177.71, "close": 182.01, "volume": 104677470.0, "vwap": 181.4156, "timestamp": 1641186000000, "transactions": 772691, "otc": None},
    #     {"open": 182.63, "high": 182.94, "low": 179.12, "close": 179.7, "volume": 99110438.0, "vwap": 180.5574, "timestamp": 1641272400000, "transactions": 831890, "otc": None},
    #     {"open": 179.61, "high": 180.17, "low": 174.64, "close": 174.92, "volume": 94535602.0, "vwap": 177.2884, "timestamp": 1641358800000, "transactions": 848513, "otc": None}
    # ]


    # stock data
    ohlc_data = [
        [pd.to_datetime(d['timestamp'], unit='ms').toordinal(), d['open'], d['high'], d['low'], d['close']]
        for d in stock_data
    ]
    stock_df = pd.DataFrame(ohlc_data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
    
    # print(stock_df)

    # Plotting the chart
    fig, ax = plt.subplots()
    candlestick_ohlc(ax, stock_df.values, width=0.6, colorup='g', colordown='r')

    # Customizing the stock plot
    plt.title('Stock Market')
    plt.xlabel('Date')
    plt.ylabel('Price')


    # Converting plot to a base64 image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    image_base64 =  f'data:image/png;base64,{image_base64}'
    
    return image_base64






def Stock_of_Competitors():
    

    # api_key = settings.POLYGONE_API_KEY
    

    # competitors = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

    # base_url = 'https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/2023-01-01/2023-12-31?unadjusted=true&apiKey={}'
    
    # competitor_data = {}

    # for symbol in competitors:
    #     url = base_url.format(symbol, api_key)
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         competitor_data[symbol] = response.json()['results']

    
    # plt.figure(figsize=(10, 6))

    # print(competitor_data)
    
    # f = open(settings.BASE_DIR/'pharmacy_dashboard/stock_competitor.json')
    
    # data = json.load(f)
    
    data = {
        "AAPL": [
            {"v": 112117471.0, "vw": 125.725, "o": 130.28, "c": 125.07, "h": 130.9, "l": 124.17, "t": 1672722000000, "n": 1021065}
        ],
        "GOOGL": [
            {"v": 28131224.0, "vw": 89.3218, "o": 89.585, "c": 89.12, "h": 91.05, "l": 88.52, "t": 1672722000000, "n": 282704}
        ],
        "MSFT": [
            {"v": 25740036.0, "vw": 239.8394, "o": 243.08, "c": 239.58, "h": 245.75, "l": 237.4, "t": 1672722000000, "n": 314904}
        ],
        "AMZN": [
            {"v": 76706040.0, "vw": 85.5452, "o": 85.46, "c": 85.82, "h": 86.96, "l": 84.205, "t": 1672722000000, "n": 575321}
        ]
    }


    data_list = []

    for symbol, values in data.items():
        for entry in values:
            entry['symbol'] = symbol  # Add a 'symbol' key for each entry
            data_list.append(entry)

    df = pd.DataFrame(data_list)
    df['t'] = pd.to_datetime(df['t'], unit='ms')  # Convert timestamp to datetime
    df = df.set_index('t')  # Set datetime as index
    df = df[['symbol', 'o', 'h', 'l', 'c', 'v']]  # Reorder columns
    df = df.rename(columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'v': 'Volume'})  
    

    return df.to_html(classes='table table-stripped')





def Exchange_Rate():

    # exchange_rates = {
    #     "CHF/EUR": 0.92,
    #     "CHF/USD": 1.10
    # }
    api_key = settings.ALPHA_API_KEY
    
    av_fx = ForeignExchange(key=api_key)

    # Get exchange rates for CHF/EUR and CHF/USD
    exchange_rates, _ = av_fx.get_currency_exchange_rate(from_currency='CHF', to_currency='EUR')
    chf_eur_exchange_rate = exchange_rates['5. Exchange Rate']
    exchange_rates, _ = av_fx.get_currency_exchange_rate(from_currency='CHF', to_currency='USD')
    chf_usd_exchange_rate = exchange_rates['5. Exchange Rate']

    
    exchange_rate_text = f"Exchange Rates:\nCHF/EUR: {chf_eur_exchange_rate}\nCHF/USD: {chf_usd_exchange_rate}"
    
    return exchange_rate_text




def gdp_core_markets():

    core_markets = ['USA', 'Switzerland', 'Germany', 'United Kingdom']

    #  API DATA
    # url = f'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey={settings.ALPHA_API_KEY}'
    # r = requests.get(url)
    # data = r.json()
    
    

    f = open(settings.BASE_DIR/'pharmacy_dashboard/retail_sales.json')
    
    data = json.load(f)


    # Extracting dates and values from the data
    dates = [entry['date'] for entry in data['data']]
    values = [float(entry['value']) for entry in data['data']]
    
    # Creating a line plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Value (millions of dollars)')
    plt.title(data['name'])

    # Converting plot to base64 image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Passing the base64 image to the Django template
    image_base64 = f'data:image/png;base64,{image_base64}'
    
    
    return image_base64
    
    
    

def trending_sickness():
    
    # API 
    # import http.client

    # conn = http.client.HTTPSConnection("health-conditions-file.p.rapidapi.com")

    # headers = {
    #     'X-RapidAPI-Key': "75f8daffabmsh70e1b797d2c71cbp117a94jsncbcdee2513a8",
    #     'X-RapidAPI-Host': "health-conditions-file.p.rapidapi.com"
    # }

    # conn.request("GET", "/records?limit=500&orderBy=dataListIndex_asc", headers=headers)
    
    # res = conn.getresponse()
   
    # data = res.read()

    # print(data.decode("utf-8"))
    
    
    # API json Data
    
    # getting json data
    json_data = open(settings.BASE_DIR/'pharmacy_dashboard/trending_sickness.json')
    
    # loading json data to dict
    json_data = json.load(json_data)
    
    # 
    list_data = []
    
    for entry in json_data['data']:
        dataListIndex = entry.get('dataListIndex')
        panel = entry.get('panel')
        year = entry.get('year')
        estimate = entry.get('estimate')
        dict_data = [panel, year, estimate]
        list_data.append(dict_data)

    
    sickness_panels = [entry[0] for entry in list_data if entry[0]]  # Filter out empty values if needed

    # Counting occurrences of each sickness panel
    sickness_panel_counts = Counter(sickness_panels)

    # Geting the top four most common sicknesses
    top_three_sicknesses = sickness_panel_counts.most_common(4)

    trending_scks = []
    for index, (sickness, count) in enumerate(top_three_sicknesses, start=1):
        trending_scks.append(f"{index}. {sickness}")
    
    return trending_scks
    
 
 
 
 
 
 
 
 
 
 
def vaccination():
    # Read the generated dummy vaccination data from the JSON file
    with open(settings.BASE_DIR/'pharmacy_dashboard/vaccination_data.json', 'r') as file:
        vaccination_data = json.load(file)
    

    # Counting the number of vaccinations for each vaccine name
    vaccine_counts = Counter(entry['vaccine_name'] for entry in vaccination_data)

    # Calculating the total dosages administered
    total_dosages = sum(entry['dosage'] for entry in vaccination_data)

    # Analyzing vaccination trends over time
    dates = [datetime.strptime(entry['vaccination_date'], '%Y-%m-%d') for entry in vaccination_data]
    dates.sort()  # Sort dates
    earliest_date = dates[0]
    latest_date = dates[-1]

    # Determine the range of vaccination dates
    vaccination_range = (latest_date - earliest_date).days

    vaccination_data = []
    
    # print("Vaccine Counts:")
    for vaccine, count in vaccine_counts.items():
        # print(f"{vaccine}: {count} vaccinations")
        vaccination_data.append(f"{vaccine}: {count} vaccinations")

    # print("\nVaccination Trend Over Time:\n")
    # for i, date in enumerate(dates):
    #     print(f"{i + 1}. {date.strftime('%Y-%m-%d')}")
    # print("\n")
    # daily_trend = [(365 / vaccination_range) * (i+1) for i in range(vaccination_range)]
    
    vaccination_data.append(f"Total Dosages Administered: {total_dosages}")
    vaccination_data.append(f"Vaccination Period: {earliest_date.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')} ({vaccination_range} days)")

    return vaccination_data