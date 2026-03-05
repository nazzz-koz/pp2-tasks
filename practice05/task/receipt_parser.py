import re
import json

with open("raw.txt", "w", encoding="utf-8") as file:
    text = """
ДУБЛИКАТ
Филиал ТОО EUROPHARMA Астана
БИН 080841000762
НДС Серия 58002
 № 0014371
Касса 300-190
Смена 10
Порядковый номер чека №61
Чек №2331180266
Кассир Аптека 17-1
ПРОДАЖА
1.
Натрия хлорид 0,9%, 200 мл, фл
2,000 x 154,00
308,00
Стоимость
308,00
2.
Борный спирт 3%, 20 мл, фл.
1,000 x 51,00
51,00
Стоимость
51,00
3.
Шприц 2 мл, 3-х комп. (Bioject)
2,000 x 16,00
32,00
Стоимость
32,00
4.
Система для инфузии Vogt Medical
2,000 x 60,00
120,00
Стоимость
120,00
5.
Шприц 5 мл, 3-х комп. 
1,000 x 310,00
310,00
Стоимость
310,00
6.
AURA Ватные диски №150
1,000 x 461,00
461,00
Стоимость
461,00
7.
Чистая линия скраб мягкий 50 мл
1,000 x 381,00
381,00
Стоимость
381,00
8.
Чистая линия  скраб очищающийабрикос 50 мл
1,000 x 386,00
386,00
Стоимость
386,00
9.
Чистая линия скраб мягкий 50 мл
1,000 x 381,00
381,00
Стоимость
381,00
10.
Nivea шампунь 3в1мужской  400 мл
1,000 x 414,00
414,00
Стоимость
414,00
11.
Pro Series Шампунь яркий цвет 500мл
1,000 x 841,00
841,00
Стоимость
841,00
12.
Pro Series бальзам-ополаскивательдля длител ухода за окрашеннымиволосами Яркий цвет 500мл
1,000 x 841,00
841,00
Стоимость
841,00
13.
Clear шампунь Актив спорт 2в1мужской  400 мл
1,000 x 1 200,00
1 200,00
Стоимость
1 200,00
14.
Bio World (HYDRO THERAPY)Мицеллярная вода 5в1, 445мл
1,000 x 1 152,00
1 152,00
Стоимость
1 152,00
15.
Bio World (HYDRO THERAPY) Гель-муссдля умывания с гиалуроновойкислотой, 250мл
1,000 x 1 152,00
1 152,00
Стоимость
1 152,00
16.
[RX]-Натрия хлорид 0,9%, 100 мл, фл.
1,000 x 168,00
168,00
Стоимость
168,00
17.
[RX]-Дисоль р-р 400 мл, фл.
1,000 x 163,00
163,00
Стоимость
163,00
18.
Тагансорбент с иономи серебра №30,пор.
1,000 x 1 526,00
1 526,00
Стоимость
1 526,00
19.
[RX]-Церукал 2%, 2 мл, №10, амп.
2,000 x 396,00
792,00
Стоимость
792,00
20.
[RX]-Андазол 200 мг, №40, табл.
1,000 x 7 330,00
7 330,00
Стоимость
7 330,00
Банковская карта:
18 009,00
ИТОГО:
18 009,00
в т.ч. НДС 12%:
0,00
Фискальный признак:
2331180266
Время: 18.04.2019 11:13:58
г. Нур-султан,Казахстан, Мангилик Ел,19, нп-5
Оператор фискальных данных: АО"Казахтелеком"Для проверки чека зайдите на сайт:consumer.oofd.kz
ФИСКАЛЬНЫЙ ЧЕК
ФП
ИНК ОФД: 311559
Код ККМ КГД (РНМ): 620300145311
ЗНМ: SWK00034965
WEBKASSA.KZ
    """
    file.write(text)

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

#1 Extract all prices from the receipt
price_pattern = r"\d[\d ]*,\d{2}"
prices = re.findall(price_pattern, text)
clean_prices = [
    float(p.replace(" ", "").replace(",", ".").replace("\n", ""))
    for p in prices
]

#2 Find all product names
product_pattern = r"\d+\.\n(.+)"
products = re.findall(product_pattern, text)

#3 Calculate total amount
total_amount = sum(clean_prices)

#4 Extract date and time information
datetime_pattern = r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}"
datetime_match = re.search(datetime_pattern, text)
datetime_value = datetime_match.group() if datetime_match else None

#5 Find payment method
payment_method = None
if "Банковская карта" in text:
    payment_method = "Bank Card"

#6 Create a structured output (JSON or formatted text)
data = {
    "products": products,
    "prices": clean_prices,
    "total_calculated": total_amount,
    "datetime": datetime_value,
    "payment_method": payment_method
}

print(json.dumps(data, indent=4, ensure_ascii=False))