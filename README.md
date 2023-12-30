NOT MAINTAINED

# book_flight.py
Python 3 CLI program for booking flight tickets using api.skypicker.com

Program is built mainly for Kiwi.com Python weekend and shall be used with special care.

## Warning
This program is without warranty and is created as exercise case.

Author is not programmer and takes no responsibility for re-use of this program.

Kitties can die when using without caution. 

 
## Install
Install following packages if not already available
> pip install argparse requests 

alternativelly

> pip install -r requirements.txt
 
## Testing
py.test is used as test framework
> pytest

## documentation
* docstring
* sphinx compatible (no config made)

## Formatting, Syntax
* PEP8 syntax
* pylint 10/10 

## Known issues
* Exceptions handling
* Not complete tests
* several stuff could be moved to configuration
* all in one file - could be separate modules
* No exception handling
* Tested on Windows only
 
 # Usage
  
 except
 > ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
 
 run
 > c:\python36\python.exe book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way
 
## Examples
> ./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way

> ./book_flight.py --date 2018-04-13 --from LHR --to DXB --return 5

> ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2

> ./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest

All above examples will make booking using kiwi api. Returns reservation code. No payment is necessary.

> --one-way

default option, indicates one way flight only (no return)
 
> --return 5 

make booking for return flight which returns after 5 nights. 

> --cheapest

default option - books zabookuje nejlevnější let a --fastest bude fungovat stejně

> --bags 2

Ticket will be booked with 2 checked in baggages

> --from 

Departure airport (uses IATA codes)

> --to 

Destination airport (uses IATA codes)
