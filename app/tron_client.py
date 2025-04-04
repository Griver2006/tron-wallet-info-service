from os import getenv
from dotenv import load_dotenv

from tronpy import Tron
from tronpy.providers import HTTPProvider

load_dotenv()

# Получаем API ключ из переменных окружения
API = getenv('API')

# Инициализация клиента Tron для взаимодействия с сетью через TronGrid
client = Tron(provider=HTTPProvider('https://api.trongrid.io', api_key=API))


def get_wallet_info(address: str) -> dict:
    # Получаем баланс, bandwidth и ресурсы (energy) кошелька
    balance = client.get_account_balance(address)
    bandwidth = client.get_bandwidth(address)
    resource = client.get_account_resource(address)

    # Вычисляем энергию, если данные доступны
    energy = 0
    energy_limit = resource.get('EnergyLimit', False)
    energy_used = resource.get('EnergyUsed', False)
    if energy_limit and energy_used:
        energy = energy_limit - energy_used

    return {
        'address': address,
        'balance': balance,
        'bandwidth': bandwidth,
        'energy': energy
    }
