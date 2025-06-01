import requests
import random
import uuid
from datetime import datetime


# Função para gerar dados de teste
def generate_car_data():
    brand_model = random.choice(brands_models)
    brand = brand_model["brand"]
    model = random.choice(brand_model["models"])
    year = random.randint(2000, 2023)
    color = random.choice(colors)
    price = round(random.uniform(5000, 50000), 2)
    status = random.choice(statuses)
    return {
        "brand": brand,
        "model": model,
        "year": year,
        "color": color,
        "price": price,
        "status": status,
    }


if __name__ == '__main__':

    # URL da API
    url = "http://localhost:8080/cars/create_car"

    # Dados reais de exemplo
    brands_models = [
        {"brand": "Toyota", "models": ["Corolla", "Camry", "RAV4"]},
        {"brand": "Honda", "models": ["Civic", "Accord", "CR-V"]},
        {"brand": "Ford", "models": ["Focus", "Mustang", "Explorer"]},
        {"brand": "Chevrolet", "models": ["Malibu", "Impala", "Equinox"]},
        {"brand": "BMW", "models": ["3 Series", "5 Series", "X5"]},
        {"brand": "Mercedes-Benz", "models": ["C-Class", "E-Class", "GLC"]},
        {"brand": "Audi", "models": ["A3", "A4", "Q5"]},
        {"brand": "Volkswagen", "models": ["Golf", "Passat", "Tiguan"]},
        {"brand": "Hyundai", "models": ["Elantra", "Sonata", "Tucson"]},
        {"brand": "Nissan", "models": ["Altima", "Sentra", "Rogue"]},
    ]

    colors = ["Red", "Blue", "Black", "White", "Silver", "Gray", "Green", "Yellow"]
    statuses = ["available", "sold"]

    # Enviar 500 dados de teste
    for _ in range(500):
        car_data = generate_car_data()
        response = requests.post(url, json=car_data)
        if response.status_code == 201:
            print(f"Carro criado com sucesso: {car_data}")
        else:
            print(f"Erro ao criar carro: {response.status_code}, {response.text}")