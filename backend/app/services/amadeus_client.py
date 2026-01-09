from amadeus import Client, ResponseError
import os
from dotenv import load_dotenv

load_dotenv()

class AmadeusService:
    def __init__(self):
        self.amadeus = Client(
            client_id=os.getenv('AMADEUS_API_KEY'),
            client_secret=os.getenv('AMADEUS_API_SECRET')
        )

    def search_flights(self, origin, destination, date):
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=date,
                adults=1
            )
            return response.data
        except ResponseError as error:
            print(error)
            return []