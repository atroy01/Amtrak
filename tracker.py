import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_prices(departure_date):
    url = f"https://www.amtrak.com/booking/fare-options?fromStation=CHI&toStation=TRU&departureDate={departure_date}&fareProductCode=ARP&fareProductCode=BRP&fareProductCode=FRP"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    prices = {}

    room_types = ["roomette", "bedroom", "family-room"]
    for room_type in room_types:
        price_element = soup.find('span', {'class': f'price-{room_type}'})
        if price_element:
            price = price_element.get_text()
            prices[room_type] = float(price.replace('$', '').replace(',', ''))

    return prices

def main():
    start_date = datetime(2024, 5, 1)
    end_date = datetime(2024, 9, 1)
    delta = timedelta(days=1)

    dates = []
    roomette_prices = []
    bedroom_prices = []
    family_room_prices = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        prices = get_prices(date_str)
        
        dates.append(date_str)
        roomette_prices.append(prices.get('roomette', None))
        bedroom_prices.append(prices.get('bedroom', None))
        family_room_prices.append(prices.get('family-room', None))
        
        current_date += delta

    plt.figure(figsize=(10, 6))
    plt.plot(dates, roomette_prices, label='Roomette')
    plt.plot(dates, bedroom_prices, label='Bedroom')
    plt.plot(dates, family_room_prices, label='Family Room')
    plt.xlabel('Departure Date')
    plt.ylabel('Price ($)')
    plt.title('Amtrak Room Prices from CHI to TRU')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()