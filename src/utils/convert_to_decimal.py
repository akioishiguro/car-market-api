from decimal import Decimal


def convert_to_decimal(data):
    for key, value in data.items():
        if isinstance(value, float):
            data[key] = Decimal(str(value))
        elif isinstance(value, dict):
            convert_to_decimal(value)
    return data
