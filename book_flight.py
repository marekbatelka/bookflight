"""
Book flight on kiwi using CLI

Examples:
# ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
# ./book_flight.py --date 2018-04-13 --from LHR --to DXB --return 5
# ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2
# ./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest

"""

import datetime
import json
import argparse
import sys
import requests


def get_flight(arguments):
    """
    connects to skypicker servive and get most optimal flight base on search criteria
    :param arguments: inputs arguments from parse_arg
    :return dict: flight
    """
    api_url = 'https://api.skypicker.com/flights?v=3&'
    adults = '1'

    # convert time format 2018-04-13 -> 13/04/2018
    date = datetime.datetime.strptime(arguments.date, "%Y-%m-%d").strftime("%d/%m/%Y")
    fly_from = arguments.origin
    fly_to = arguments.to
    sort = arguments.sort

    if arguments.days_in_destination == 'oneway':
        # constructing search query for ONEWAY flight
        type_flight = 'oneway'
        query_string = '&flyFrom=' + fly_from + \
                       '&to=' + fly_to + \
                       '&dateFrom=' + date + \
                       '&dateTo=' + date + \
                       '&typeFlight=' + type_flight + \
                       '&adults=' + adults + \
                       '&sort=' + sort + \
                       '&asc=1'
    else:
        # constructing search query for RETURN flight
        days_in_destination = arguments.days_in_destination
        type_flight = 'round'
        query_string = 'daysInDestinationFrom=' + days_in_destination + \
                       '&daysInDestinationTo=' + days_in_destination + \
                       '&flyFrom=' + fly_from + \
                       '&to=' + fly_to + \
                       '&dateFrom=' + date + \
                       '&dateTo=' + date + \
                       '&typeFlight=' + type_flight + \
                       '&adults=' + adults + \
                       '&sort=' + sort + \
                       '&asc=1'
    if arguments.verbose:
        print(query_string)
    get_data = requests.get(api_url + query_string)
    json_data = json.loads(get_data.content)
    flights = json_data['data']
    # return first flight in the sorted list
    if arguments.verbose:
        print(flights[0])
    return flights[0]


def parse_args(args):
    """
    function parse_args takes arguments from CLI and return them parsed for later use.
    :param list args : pass arguments from sys cmd line or directly
    :return dict: parsed arguments
    """
    parser = argparse.ArgumentParser()

    required = parser.add_argument_group()
    required.add_argument("-d", "--date", help="Date of Flight", required=True)
    # name origin used because of conflicting name "from" in tests etc. cannot use parser.from
    required.add_argument("-fr", "--from", help="IATA code of Departure",
                          dest="origin", required=True)
    required.add_argument("-t", "--to", help="IATA code of Destination",
                          required=True)

    days_in_destination = parser.add_mutually_exclusive_group()
    days_in_destination.add_argument("-o", "--one-way", action="store_const",
                                     help="Oneway ticket", dest="days_in_destination",
                                     const="oneway")
    days_in_destination.add_argument("-r", "--return", action="store",
                                     help="Round ticket followed by number of days in destination",
                                     dest="days_in_destination")
    days_in_destination.set_defaults(days_in_destination='oneway')

    sort = parser.add_mutually_exclusive_group()
    sort.add_argument("-c", "--cheapest", action="store_const",
                      help="Book cheapest flight", dest="sort", const="price")
    sort.add_argument("-fa", "--fastest", action="store_const",
                      help="Book fastest flight", dest="sort",
                      const="duration")
    sort.set_defaults(sort='price')

    parser.add_argument("-b", "--bags", help="Number of checked-in baggages", default='0')
    parser.add_argument("-v", "--verbose", help="sets verbose output", action='store_true')
    return parser.parse_args(args)


def book(flight_selected, arguments):
    """
    function makes booking to kiwi api
    :param flight_selected: best option flight
    found in get_flight() using flight_selected['booking_token'] only
    :param arguments: arguments from command line using arguments.bags only
    :return string: returns booking ID
    """

    json_data = {
        "bags": arguments.bags,
        # could be in config
        "passengers": {
            "email": "john.doe@gmail.com",
            "title": "Mr",
            "firstName": "John",
            "lastName": "Doe",
            "documentID": "1234567",
            "birthday": "1987-10-10"
        },
        "currency": "EUR",
        "booking_token": flight_selected['booking_token']
    }

    if arguments.verbose:
        print(json_data)
    res = requests.post('http://128.199.48.38:8080/booking', json=json_data)
    confirmation = json.loads(res.content.decode())
    if arguments.verbose:
        print(confirmation)
    return confirmation['pnr']


if __name__ == "__main__":
    # get valid arguments from CLI
    PARSED_ARGS = parse_args(sys.argv[1:])
    # find best flight
    FLIGHT = get_flight(PARSED_ARGS)
    # make booking
    CONFIRMATION_NUMBER = book(FLIGHT, PARSED_ARGS)
    # return to CLI
    print(CONFIRMATION_NUMBER)
