import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

# Your provided data
LEXICON_CATALOG_CATEGORIES = {
    "racetami": "🧠 Рацетамы",
    "holinergetiki": "⚡ Холинергики",
    "stimulators": "🚀 Стимуляторы / Дофаминергические",
    "neiroprotectors": "🛡️ Нейропротекторы",
    "adaptogeni": "⚖️ Адаптогены / Эндокринные модуляторы",
    "antidepressanti": "😌 Антидепрессанты / Анксиолитики",
    "metabolicheskie": "🔬 Метаболические / Другие",
}

LEXICON_ITEMS = {
    "7-oho": {
        "price": 3400,
        "quantity": "30 капсул",
        "dosage": "100 мг",
        "description": "7-OXO (7-KETO-DHEA) - Ускоряет метаболизм, повышает энергию. Не влияет на гормоны напрямую.",
        "category": "metabolicheskie"
    },
    "9-me-bc": {
        "price": 1500,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "9-ME-BC - Восстанавливает дофаминовые нейроны. Улучшает мотивацию и когнитивные функции.",
        "category": "stimulators"
    },
    "aicar": {
        "price": 1500,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "AICAR - Активирует AMPK, улучшает выносливость и метаболизм глюкозы.",
        "category": "metabolicheskie"
    },
    "amino-tadalafil": {
        "price": 1600,
        "quantity": "60 капсул",
        "dosage": "5+5 мг",
        "description": "AMINO-TADALAFIL (WITH BIOPERINE) - Комбинация тадалафила и биоперина. Улучшает кровообращение и либидо.",
        "category": "adaptogeni"
    },
    "aniracetam": {
        "price": 1400,
        "quantity": "30 капсул",
        "dosage": "300 мг",
        "description": "ANIRACETAM - Улучшает память и настроение, снижает тревожность. Действует через AMPA-рецепторы.",
        "category": "racetami"
    },
    # Add other items similarly with appropriate category assignments
}

# Initialize Google Sheets client
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'creds.json'  # Replace with your JSON credentials file path
SPREADSHEET_ID = '1gWctti68rVN7yDrQYH75Cx7ziDYOx13OKAZftEJ2lQQ'  # Replace with your Google Sheet ID


def initialize_sheets_client():
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client


def setup_sheets(spreadsheet):
    # Get or create Categories worksheet
    try:
        categories_sheet = spreadsheet.worksheet('Categories')
        # Clear existing data to avoid duplicates
        categories_sheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        categories_sheet = spreadsheet.add_worksheet(title='Categories', rows=100, cols=10)

    # Setup Categories headers
    categories_sheet.update('A1:B1', [['Category ID', 'Category Name']])

    # Populate categories
    category_data = [[k, v] for k, v in LEXICON_CATALOG_CATEGORIES.items()]
    categories_sheet.append_rows(category_data)

    # Get or create Items worksheet
    try:
        items_sheet = spreadsheet.worksheet('Items')
        # Clear existing data to avoid duplicates
        items_sheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        items_sheet = spreadsheet.add_worksheet(title='Items', rows=100, cols=10)

    # Setup Items headers
    items_sheet.update('A1:F1', [['Item ID', 'Category ID', 'Price', 'Quantity', 'Dosage', 'Description']])

    # Populate items
    item_data = [
        [item_id, item_info['category'], item_info['price'], item_info['quantity'],
         item_info['dosage'], item_info['description']]
        for item_id, item_info in LEXICON_ITEMS.items()
    ]
    items_sheet.append_rows(item_data)

    return categories_sheet, items_sheet


def get_all_items(spreadsheet):
    items_sheet = spreadsheet.worksheet('Items')
    return items_sheet.get_all_records()


def get_items_by_category(spreadsheet, category_id):
    items_sheet = spreadsheet.worksheet('Items')
    records = items_sheet.get_all_records()
    return [record for record in records if record['Category ID'] == category_id]


def get_item_by_id(spreadsheet, item_id):
    items_sheet = spreadsheet.worksheet('Items')
    records = items_sheet.get_all_records()
    for record in records:
        if record['Item ID'] == item_id:
            return record
    return None


def add_category(spreadsheet, category_id, category_name):
    categories_sheet = spreadsheet.worksheet('Categories')
    categories_sheet.append_row([category_id, category_name])
    print(f"Added category: {category_name}")


def add_item(spreadsheet, item_id, category_id, price, quantity, dosage, description):
    items_sheet = spreadsheet.worksheet('Items')
    items_sheet.append_row([item_id, category_id, price, quantity, dosage, description])
    print(f"Added item: {item_id}")


def main():
    # Initialize client and open existing spreadsheet
    client = initialize_sheets_client()
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # Setup sheets with initial data
    categories_sheet, items_sheet = setup_sheets(spreadsheet)

    # Example operations
    print("All Items:")
    pprint(get_all_items(spreadsheet))

    print("\nItems in 'racetami' category:")
    pprint(get_items_by_category(spreadsheet, 'racetami'))

    print("\nItem with ID 'aniracetam':")
    pprint(get_item_by_id(spreadsheet, 'aniracetam'))

    # Add a new category
    add_category(spreadsheet, 'new_category', '🆕 Новая Категория')

    # Add a new item
    add_item(
        spreadsheet,
        item_id='new_item',
        category_id='racetami',
        price=2000,
        quantity='30 капсул',
        dosage='50 мг',
        description='New item description'
    )


if __name__ == '__main__':
    main()