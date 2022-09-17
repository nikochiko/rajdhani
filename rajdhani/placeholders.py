"""This module contain mock data for various parts of this app
as a placeholder until the real implementation is added.
"""

AUTOCOMPLETE_STATIONS = [
    {"code": "ADI", "name": "AHMEDABAD JN"},
    {"code": "BCT", "name": "Mumbai Central"},
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

SCHEDULE = [
    {"station_code": "BCT", "station_name": "Mumbai Central", "day": "1.0", "arrival": "None", "departure": "23:25:00"},
    {"station_code": "MX", "station_name": "Mumbai Mahalakshmi", "day": "1.0", "arrival": "23:26:00", "departure": "23:26:00"},
    {"station_code": "PL", "station_name": "Mumbai Lower Parel", "day": "1.0", "arrival": "23:27:00", "departure": "23:27:00"},
    {"station_code": "ADI", "station_name": "AHMEDABAD JN", "day": "2.0", "arrival": "06:00:00", "departure": "None"},
]

TRIPS = [
    {
        "train_number": "12608",
        "train_name": "Lalbagh Exp",
        "from_station_code": "SBC",
        "from_station_name": "Bangalore",
        "to_station_code": "MAS",
        "to_station_name": "Chennai",
        "ticket_class": "3A",
        "date": "2022-09-22",
        "passenger_name": "Tourist",
        "passenger_email": "tourist@example.com",
    },
]
