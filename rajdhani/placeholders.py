"""This module contain mock data for various parts of this app
as a placeholder until the real implementation is added.
"""

AUTOCOMPLETE_STATIONS = [
    {"code": "ADI", "name": "AHMEDABAD JN"},
    {"code": "SBC", "name": "BANGALORE CITY JN"},
    {"code": "MAS", "name": "CHENNAI CENTRAL"},
    {"code": "HWH", "name": "HOWRAH JN"},
    {"code": "CSTM", "name": "MUMBAI CST"},
    {"code": "NDLS", "name": "NEW DELHI"},
    {"code": "DLI", "name": "OLD DELHI"},
    {"code": "PUNE", "name": "PUNE JN"},
]

SEARCH_TRAINS = [
    {
        "number": "12028",
        "name": "Shatabdi Exp",
        "from_station_code": "SBC",
        "from_station_name": "Bangalore",
        "to_station_code": "MAS",
        "to_station_name": "Chennai",
        "departure": "06:00",
        "arrival": "11:00",
        "duration_h": 5,
        "duration_m": 0
    },
    {
        "number": "12608",
        "name": "Lalbagh Exp",
        "from_station_code": "SBC",
        "from_station_name": "Bangalore",
        "to_station_code": "MAS",
        "to_station_name": "Chennai",
        "departure": "06:20",
        "arrival": "12:15",
        "duration_h": 5,
        "duration_m": 55
    },
]
