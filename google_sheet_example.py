import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# Конфигурация
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'creds.json'  # путь к скачанному JSON
SPREADSHEET_NAME = 'premionce'  # название вашей таблицы


# Инициализация клиента
def get_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
    client = gspread.authorize(creds)
    return client


# Создание новой таблицы с двумя листами
def create_spreadsheet():
    client = get_client()
    spreadsheet = client.create(SPREADSHEET_NAME)

    # Добавляем лист категорий
    categories_sheet = spreadsheet.add_worksheet(title="Категории", rows=100, cols=10)
    categories_sheet.append_row(["ID категории", "Название категории"])

    # Добавляем лист товаров
    items_sheet = spreadsheet.add_worksheet(title="Товары", rows=1000, cols=10)
    items_sheet.append_row([
        "ID товара", "ID категории", "Цена", "Количество",
        "Дозировка", "Описание"
    ])

    # Удаляем дефолтный лист
    default_sheet = spreadsheet.get_worksheet(0)
    spreadsheet.del_worksheet(default_sheet)

    return spreadsheet


# Получение существующей таблицы
def get_spreadsheet():
    client = get_client()
    spreadsheet = client.open(SPREADSHEET_NAME)
    return spreadsheet


# Заполнение начальными данными
def fill_initial_data(spreadsheet):
    # Категории
    LEXICON_CATALOG_CATEGORIES = {
        "racetami": "🧠 Рацетамы",
        "holinergetiki": "⚡ Холинергики",
        "stimulators": "🚀 Стимуляторы / Дофаминергические",
        "neiroprotectors": "🛡️ Нейропротекторы",
        "adaptogeni": "⚖️ Адаптогены / Эндокринные модуляторы",
        "antidepressanti": "😌 Антидепрессанты / Анксиолитики",
        "metabolicheskie": "🔬 Метаболические / Другие",
    }

    categories_sheet = spreadsheet.worksheet("Категории")
    for cat_id, cat_name in LEXICON_CATALOG_CATEGORIES.items():
        categories_sheet.append_row([cat_id, cat_name])

    # Товары
    LEXICON_ITEMS = {
        "7-oho": {
            "price": 3400,
            "quantity": "30 капсул",
            "dosage": "100 мг",
            "description": "7-OXO (7-KETO-DHEA) - Ускоряет метаболизм, повышает энергию. Не влияет на гормоны напрямую.",
            "category": "adaptogeni"
        },
        # ... остальные товары (добавьте category для каждого)
    }

    items_sheet = spreadsheet.worksheet("Товары")
    for item_id, item_data in LEXICON_ITEMS.items():
        items_sheet.append_row([
            item_id,
            item_data.get("category", ""),
            item_data.get("price", ""),
            item_data.get("quantity", ""),
            item_data.get("dosage", ""),
            item_data.get("description", "")
        ])


# Примеры использования
def examples():
    # Получаем таблицу
    spreadsheet = get_spreadsheet()

    # 1. Получение всех категорий
    categories_sheet = spreadsheet.worksheet("Категории")
    all_categories = categories_sheet.get_all_records()
    print("Все категории:")
    pprint(all_categories)

    # 2. Получение всех товаров
    items_sheet = spreadsheet.worksheet("Товары")
    all_items = items_sheet.get_all_records()
    print("\nВсе товары:")
    pprint(all_items[:3])  # выводим первые 3 для примера

    # 3. Получение товаров по категории
    category_id = "adaptogeni"
    items_in_category = [item for item in all_items if item["ID категории"] == category_id]
    print(f"\nТовары в категории {category_id}:")
    pprint(items_in_category)

    # 4. Получение конкретного товара
    item_id = "7-oho"
    specific_item = next((item for item in all_items if item["ID товара"] == item_id), None)
    print(f"\nТовар с ID {item_id}:")
    pprint(specific_item)

    # 5. Добавление новой категории
    new_category = ["new_category", "🆕 Новая категория"]
    categories_sheet.append_row(new_category)
    print("\nДобавлена новая категория")

    # 6. Добавление нового товара
    new_item = [
        "new_item",
        "new_category",
        9999,
        "10 таблеток",
        "50 мг",
        "Новый товар для тестирования"
    ]
    items_sheet.append_row(new_item)
    print("\nДобавлен новый товар")


# Основная функция
def main():
    # Создаем новую таблицу (выполнить один раз)
    spreadsheet = get_spreadsheet()
    fill_initial_data(spreadsheet)

    # Работа с существующей таблицей
    examples()


if __name__ == "__main__":
    main()