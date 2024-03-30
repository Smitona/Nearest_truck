# Сервис поиска ближайших машин для перевозки грузов
API сервис, который позволяет найти машины для перевозки грузов. Разаботан на основе Django REST API.

## Запуск проекта:
1. Клонировать репозиторий:
   ```
   git clone git@github.com:Smitona/Nearest_truck.git
   ```
2. Создать .env файл с переменными.
3. Запустить контейнры:
   ```
   docker compose up -d
   ```
4. Открыть сервис по локальному адресу:
   ```
   http://127.0.0.1:8000/api/
   ```
***При запуске БД заполняется локациями, создаётся 20 грузовиков со случайными валидными данными.***

## Примеры запросов

```GET``` ```http://127.0.0.1:8000/api/trucks/2/``` → получение информации по грузовику.
```
{
    "id": 2,
    "plate_number": "3486V",
    "location": {
        "zip": "00638",
        "city": "Ciales",
        "state": "Puerto Rico",
        "latitude": 18.28462,
        "longitude": -66.5137
    },
    "cargo_capacity": "776"
}
```

```GET``` ```http://127.0.0.1:8000/api/cargos/``` → получение списка грузов.
```
[
    {
        "id": 2,
        "description": "Olas",
        "weight": 90,
        "pickup_loc": {
            "zip": "00617",
            "city": "Barceloneta",
            "state": "Puerto Rico",
            "latitude": 18.44598,
            "longitude": -66.56006
        },
        "delivery_loc": {
            "zip": "00636",
            "city": "Rosario",
            "state": "Puerto Rico",
            "latitude": 18.16354,
            "longitude": -67.08014
        },
        "trucks_count": 1
    }
]
```

```POST``` ```http://127.0.0.1:8000/api/cargos/``` → создание груза.
```
{
    "description": "Olas",
    "weight": 90,
    "pickup_loc": "Barceloneta, Puerto Rico at 18.44598 latitude and -66.56006 longitude.",
    "delivery_loc": "Rosario, Puerto Rico at 18.16354 latitude and -67.08014 longitude.",
    "trucks": [
        {
            "plate": "1091D",
            "distance": 1640.800763769878
        },
        {
            "plate": "1303P",
            "distance": 1606.0174407493307
        },
        {
            "plate": "1459R",
            "distance": 2255.1639573084394
        },
        {
            "plate": "1934J",
            "distance": 1687.0767343291714
        },
        {
            "plate": "2531F",
            "distance": 1485.4029300613856
        },
        {
            "plate": "2604A",
            "distance": 2220.7002944873466
        },
        {
            "plate": "3486V",
            "distance": 11.507745673480168
        },
        {
            "plate": "3572G",
            "distance": 1971.4931590334065
        },
        {
            "plate": "3791I",
            "distance": 2334.7523467633123
        },
        {
            "plate": "4557J",
            "distance": 2561.813683163634
        },
        {
            "plate": "6342B",
            "distance": 1663.5899637748407
        },
        {
            "plate": "6682Y",
            "distance": 1825.0974050838868
        },
        {
            "plate": "6740J",
            "distance": 1916.7910061826053
        },
        {
            "plate": "7531K",
            "distance": 1529.8435675075173
        },
        {
            "plate": "7826I",
            "distance": 1669.1027162850216
        },
        {
            "plate": "8333Y",
            "distance": 1690.5807397564404
        },
        {
            "plate": "8549S",
            "distance": 1786.4644819118605
        },
        {
            "plate": "8755S",
            "distance": 3018.276477952838
        },
        {
            "plate": "9160C",
            "distance": 1613.248959364049
        },
        {
            "plate": "9250O",
            "distance": 2243.3960444952804
        }
    ]
}
```
---
### Стек ⚡
<img src="https://img.shields.io/badge/Python-black?style=for-the-badge&logo=Python&logoColor=DodgerBlue"/> <img src="https://img.shields.io/badge/Django-black?style=for-the-badge&logo=Django&logoColor=darkturquoise"/> <img src="https://img.shields.io/badge/Docker-black?style=for-the-badge&logo=Docker&logoColor=dodgerblue"/> <img src="https://img.shields.io/badge/Postman-black?style=for-the-badge&logo=Postman&logoColor=Tomato"/> <img src="https://img.shields.io/badge/postgresql-black?style=for-the-badge&logo=postgresql&logoColor=Cyan"/>


