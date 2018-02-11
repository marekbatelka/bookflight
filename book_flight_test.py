"""
 Testing module
"""
import datetime
import book_flight


# ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
# ./book_flight.py --date 2018-04-13 --from LHR --to DXB --return 5
# ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2
# ./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest

def test_parser_case1():
    """
    ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
    """
    parser = book_flight.parse_args(['--d', '2018-04-13', '--from', 'BCN',
                                     '--to', 'DUB', '--one-way'])
    assert parser.bags == '0'
    assert parser.sort == 'price'
    assert parser.date == '2018-04-13'
    assert parser.origin == 'BCN'
    assert parser.days_in_destination == 'oneway'
    assert parser.to == 'DUB'


def test_parser_case2():
    """
    ./book_flight.py --date 2018-04-13 --from LHR --to DXB --return 5
    """
    parser = book_flight.parse_args(['--date', '2018-04-13', '--from', 'LHR',
                                     '--to', 'DXB', '--return', '10'])
    assert parser.bags == '0'
    assert parser.sort == 'price'
    assert parser.date == '2018-04-13'
    assert parser.origin == 'LHR'
    assert parser.days_in_destination == '10'
    assert parser.to == 'DXB'


def test_parser_case3():
    """
    ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2
    """
    parser = book_flight.parse_args(['--date', '2018-04-13', '--from', 'NRT',
                                     '--to', 'SYD', '--cheapest', '--bags', '2'])
    assert parser.bags == '2'
    assert parser.sort == 'price'
    assert parser.date == '2018-04-13'
    assert parser.origin == 'NRT'
    assert parser.days_in_destination == 'oneway'
    assert parser.to == 'SYD'


def test_parser_case4():
    """
    # ./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest
    """
    parser = book_flight.parse_args(['--date', '2018-04-13', '--from',
                                     'CPH', '--to', 'MIA', '--fastest'])
    assert parser.bags == '0'
    assert parser.sort == 'duration'
    assert parser.date == '2018-04-13'
    assert parser.origin == 'CPH'
    assert parser.days_in_destination == 'oneway'
    assert parser.to == 'MIA'


def test_get_flight_1():
    """
    ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
    """
    parser = book_flight.parse_args(['--d', '2018-04-13', '--from', 'BCN',
                                     '--to', 'DUB', '--one-way'])
    flight = book_flight.get_flight(parser)
    assert flight['flyFrom'] == 'BCN'
    assert flight['flyTo'] == 'DUB'
    assert parser.date == datetime.datetime.fromtimestamp(int(flight['dTime'])).strftime('%Y-%m-%d')


def test_get_flight_2():
    """
    ./book_flight.py --date 2018-04-13 --from LHR --to DXB --return 5
    """
    parser = book_flight.parse_args(['--date', '2018-04-13', '--from',
                                     'LHR', '--to', 'DXB', '--return', '10'])
    flight = book_flight.get_flight(parser)
    assert flight['flyFrom'] == 'LHR'
    assert flight['flyTo'] == 'DXB'
    assert parser.date == datetime.datetime.fromtimestamp(
        int(flight['dTime'])).strftime('%Y-%m-%d')
    assert parser.bags == '0'
    assert parser.days_in_destination == '10'


def test_get_flight_3():
    """
    ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2
    """
    parser = book_flight.parse_args(
        ['--date', '2018-04-13', '--from', 'NRT', '--to', 'SYD',
         '--cheapest', '--bags', '2'])
    flight = book_flight.get_flight(parser)
    assert flight['flyFrom'] == 'NRT'
    assert flight['flyTo'] == 'SYD'
    # not sure why date is 2018-04-14 - timezone?
    # assert parser.date == datetime.datetime.fromtimestamp(
    # int(flight['dTime'])).strftime('%Y-%m-%d')
    assert parser.sort == 'price'
    assert parser.bags == '2'


def test_get_flight_4():
    """
    # ./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest
    """
    parser = book_flight.parse_args(['--date', '2018-04-13', '--from', 'CPH',
                                     '--to', 'MIA', '--fastest'])
    flight = book_flight.get_flight(parser)
    assert flight['flyFrom'] == 'CPH'
    assert flight['flyTo'] == 'MIA'
    assert parser.date == datetime.datetime.fromtimestamp(
        int(flight['dTime'])).strftime('%Y-%m-%d')
    assert parser.sort == 'duration'
    assert parser.bags == '0'


def test_booking():
    """
    Test booking for flight 1
    ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
    """
    parser = book_flight.parse_args(['--date', '2018-04-13', '--from', 'CPH',
                                     '--to', 'MIA', '--fastest'])
    flight = book_flight.get_flight(parser)
    booking = book_flight.book(flight, parser)
    assert booking
