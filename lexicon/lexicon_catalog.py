from typing import Callable

LEXICON_CATALOG: dict[str, str | Callable] = {
    'welcome_text': '<b>Ассортимент магазина PREMIONCE</b>\n\n'
                    'Сильному человеку требуется многокомпонентный арсенал для преобразования жизненной энергии в '
                    'материальные и духовные блага.\n\n'
                    'PREMIONCE STORE - это инструментарий с помощью которого Вы быстрее и качественнее '
                    'получаете результаты во всех сферах.\n\n'
                    '✨ Выбирайте из каталога то, что резонирует с Вами.\n\n'
                    'Посмотрите наш ассортимент по '
                    '<a href="https://telegra.ph/Assortiment-magazina-PREMIONCE-07-06">ссылке</a>',
    'back_to_catalog': '🔙 Назад',
    'item_info': lambda description, dosage, quantity, price: (
        f'<b>Описание</b>: {description}\n\n'
        f'<b>Дозировка</b>: {dosage}\n\n'
        f'<b>Кол-во</b>: {quantity}\n\n'
        f'<b>Стоимость</b>: {price}₽\n\n'
    ),
}

LEXICON_CATALOG_CATEGORIES: dict[str, str] = {
    "racetami": "🧠 Рацетамы",
    "holinergetiki": "⚡ Холинергики",
    "stimulators": "🚀 Стимуляторы / Дофаминергические",
    "neiroprotectors": "🛡️ Нейропротекторы",
    "adaptogeni": "⚖️ Адаптогены / Эндокринные модуляторы",
    "antidepressanti": "😌 Антидепрессанты / Анксиолитики",
    "metabolicheskie": "🔬 Метаболические / Другие",
}

LEXICON_RACETAMI_ITEMS: dict[str, str] = {
    'aniracetam': "Анирацетам (Aniracetam)",
    'phenylpiracetam_hydrazide': "Фенотропил-гидразид (Phenylpiracetam Hydrazide)",
    'pramiracetam': "Прамирацетам (Pramiracetam)",
    'fasoracetam': "Фасорацетам (Fasoracetam)",
    'coluracetam': "Колурацетам (Coluracetam)",
    'noopept': "Омберацетам (Noopept)",
    'back_to_catalog': "🔙 Назад"
}

LEXICON_HOLINERGETIKI_ITEMS: dict[str, str] = {
    'citicoline': "CDP-Холин (Citicoline)",
    'centrophenoxine': "Мефеноксат (Centrophenoxine)",
    'encephabol': "Пиритинол (Encephabol)",
    'back_to_catalog': "🔙 Назад"
}

LEXICON_STIMULATORES_ITEMS: dict[str, str] = {
    'ladasten': "Бромантан (Ladasten)",
    'enerion': "Сульбутиамин (Enerion)",
    'wakix': "Питолизант (Wakix)",
    'tesofensine': "Тесофензин (Tesofensine)",
    'back_to_catalog': "🔙 Назад"
}

LEXICON_NEIROPROTECTORS_ITEMS: dict[str, str] = {
    'dihexa': "Дигекса (Dihexa, спрей)",
    'osavampator': "TAK-653 (Osavampator, спрей)",
    'j-147': "J-147",
    'l-thp': "L-THP (левотетрагидропальматин)",
    'prl-8-53': "PRL-8-53",
    'unifiram': "Унифирам (Unifiram)",
    'back_to_catalog': "🔙 Назад"
}

LEXICON_ADAPTOGENI_ITEMS: dict[str, str] = {
    '7-oho': "7-OXO (7-KETO-DHEA)",
    'cycloastragenol': "Циклоастрагенол (Cycloastragenol)",
    'androxal': "Энкломифен (Androxal)",
    'aromasin': "Экземестан (Aromasin)",
    'mk-677': "Ибутаморен (MK-677)",
    'fareston': "Торемифен (Fareston)",
    'back_to_catalog': "🔙 Назад"
}

LEXICON_ANTIDEPRESSANTI_ITEMS: dict[str, str] = {
    '9-me-bc': "9-ME-BC",
    'd-phenylalanine': "D-Фенилаланин (D-Phenylalanine)",
    'nor-bni': "NOR-BNI (спрей)",
    'back_to_catalog': "🔙 Назад"
}

LEXICON_METABOLICHESKIE_ITEMS: dict[str, str] = {
    'aicar': "AICAR",
    'ketas': "Ибудиласт (Ketas)",
    'magnesium_l-threonate': "Магний L-треонат (Magnesium L-Threonate)",
    'nnmti': "NNMTI (5-AMINO-1MQ)",
    '4-dma-78-dhf': "Эутропофлавин (4'-DMA-7,8-DHF)",
    '78-dhf': "Тропофлавин (7,8-DHF)",
    'amino-tadalafil': "AMINO-TADALAFIL (WITH BIOPERINE)",
    'back_to_catalog': "🔙 Назад"
}

LEXICON_CATEGORIES_INFO = {
    'racetami': {
        'category_id': 1,
        'category_name': 'racetami',
        'description': "Рацетамы — класс ноотропов, улучшающих когнитивные функции, память и концентрацию за счёт модуляции нейротрансмиттеров, особенно ацетилхолина и глутамата.",
        'items': LEXICON_RACETAMI_ITEMS
    },
    'holinergetiki': {
        'category_id': 2,
        'category_name': 'holinergetiki',
        'description': "Холинергики — группа веществ, усиливающих синтез, высвобождение или активность ацетилхолина — ключевого нейромедиатора для памяти, обучения и когнитивных функций. Они улучшают нейропластичность и могут снижать возрастное ухудшение когнитивных способностей.",
        'items': LEXICON_HOLINERGETIKI_ITEMS
    },
    'stimulators': {
        'category_id': 3,
        'category_name': 'stimulators',
        'description': "Стимуляторы и дофаминергические вещества повышают энергию, мотивацию и концентрацию за счёт усиления активности дофамина, норадреналина и других возбуждающих нейротрансмиттеров. Они улучшают работоспособность, но требуют осторожности из-за возможного привыкания и побочных эффектов.",
        'items': LEXICON_STIMULATORES_ITEMS
    },
    'neiroprotectors': {
        'category_id': 4,
        'category_name': 'neiroprotectors',
        'description': "Нейропротекторы — соединения, защищающие нервные клетки от повреждений, окислительного стресса и нейродегенерации. Они способствуют долгосрочному здоровью мозга, улучшают устойчивость к нагрузкам и могут замедлять возрастные когнитивные изменения.",
        'items': LEXICON_NEIROPROTECTORS_ITEMS
    },
    'adaptogeni': {
        'category_id': 5,
        'category_name': 'adaptogeni',
        'description': "Адаптогены и эндокринные модуляторы помогают организму адаптироваться к стрессу, нормализуя работу гормональной системы (кортизол, серотонин, мелатонин). Они улучшают устойчивость к нагрузкам, снижают усталость и способствуют балансу нервной системы.",
        'items': LEXICON_ADAPTOGENI_ITEMS
    },
    'antidepressanti': {
        'category_id': 6,
        'category_name': 'antidepressanti',
        'description': "Антидепрессанты и анксиолитики влияют на серотонин, ГАМК и другие нейромедиаторы, снижая тревожность, улучшая настроение и стабилизируя эмоциональный фон. Некоторые из них обладают ноотропными свойствами, улучшая когнитивные функции при стрессе.",
        'items': LEXICON_ANTIDEPRESSANTI_ITEMS
    },
    'metabolicheskie': {
        'category_id': 7,
        'category_name': 'metabolicheskie',
        'description': "Метаболические ноотропы и другие вещества улучшают энергообмен в мозге, усиливают кровообращение или оказывают комплексное воздействие на когнитивные функции. Они могут включать витаминоподобные соединения, пептиды и другие вспомогательные компоненты для поддержки работы мозга.",
        'items': LEXICON_METABOLICHESKIE_ITEMS
    }
}

LEXICON_ITEMS: dict[str, dict[str, int | str]] = {
    "7-oho": {
        "item_id": 1,
        "category_id": 5,
        "category_name": "adaptogeni",
        "name": "7-OXO (7-KETO-DHEA)",
        "price": 3400,
        "quantity": "30 капсул",
        "dosage": "100 мг",
        "description": "7-OXO (7-KETO-DHEA) - Ускоряет метаболизм, повышает энергию. Не влияет на гормоны напрямую."
    },
    "9-me-bc": {
        "item_id": 2,
        "category_id": 6,
        "category_name": "antidepressanti",
        "name": "9-ME-BC",
        "price": 1500,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "9-ME-BC - Восстанавливает дофаминовые нейроны. Улучшает мотивацию и когнитивные функции."
    },
    "aicar": {
        "item_id": 3,
        "category_id": 7,
        "category_name": "metabolicheskie",
        "name": "AICAR",
        "price": 1500,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "AICAR - Активирует AMPK, улучшает выносливость и метаболизм глюкозы."
    },
    "amino-tadalafil": {
        "item_id": 4,
        "category_id": 7,
        "category_name": "metabolicheskie",
        "name": "AMINO-TADALAFIL (WITH BIOPERINE)",
        "price": 1600,
        "quantity": "60 капсул",
        "dosage": "5+5 мг",
        "description": "AMINO-TADALAFIL (WITH BIOPERINE) - Комбинация тадалафила и биоперина. Улучшает кровообращение и либидо."
    },
    "aniracetam": {
        "item_id": 5,
        "category_id": 1,
        "category_name": "aniracetam",
        "name": "ANIRACETAM",
        "price": 1400,
        "quantity": "30 капсул",
        "dosage": "300 мг",
        "description": "ANIRACETAM - Улучшает память и настроение, снижает тревожность. Действует через AMPA-рецепторы."
    },
    "ladasten": {
        "item_id": 6,
        "category_id": 3,
        "category_name": "stimulators",
        "name": "BROMANTANE (LADASTEN)",
        "price": 2500,
        "quantity": "30 капсул",
        "dosage": "50 мг",
        "description": "BROMANTANE (LADASTEN) - Повышает выносливость и адаптацию к стрессу. Без перевозбуждения."
    },
    "citicoline": {
        "item_id": 7,
        "category_id": 2,
        "category_name": "holinergetiki",
        "name": "CDP-CHOLINE (CITICOLINE)",
        "price": 1600,
        "quantity": "30 капсул",
        "dosage": "250 мг",
        "description": "CDP-CHOLINE (CITICOLINE) - Восстанавливает мембраны нейронов, улучшает фокус и ясность ума."
    },
    "coluracetam": {
        "item_id": 8,
        "category_id": 1,
        "category_name": "racetami",
        "name": "COLURACETAM",
        "price": 2600,
        "quantity": "30 капсул",
        "dosage": "50 мг",
        "description": "COLURACETAM - Улучшает зрительное восприятие и память. Потенциальный антидепрессант."
    },
    "cycloastragenol": {
        "item_id": 9,
        "category_id": 5,
        "category_name": "adaptogeni",
        "name": "CYCLOASTRAGENOL",
        "price": 3200,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "CYCLOASTRAGENOL - Активирует теломеразу, замедляет старение. Улучшает иммунитет."
    },
    "d-phenylalanine": {
        "item_id": 10,
        "category_id": 6,
        "category_name": "antidepressanti",
        "name": "D-PHENYLALANINE",
        "price": 1400,
        "quantity": "30 капсул",
        "dosage": "700 мг",
        "description": "D-PHENYLALANINE - Повышает уровень эндорфинов. Эффективен при депрессии и боли."
    },
    "dihexa": {
        "item_id": 11,
        "category_id": 4,
        "category_name": "neiroprotectors",
        "name": "DIHEXA (SPRAY)",
        "price": 5500,
        "quantity": "100 мг в 5 мл",
        "dosage": "1 мг/пшик (100 доз)",
        "description": "DIHEXA (SPRAY) - Мощный нейрорегенератор, улучшает память и обучаемость."
    },
    "androxal": {
        "item_id": 12,
        "category_id": 5,
        "category_name": "adaptogeni",
        "name": "ENCLOMIPHENE (ANDROXAL)",
        "price": 2800,
        "quantity": "30 капсул",
        "dosage": "20 мг",
        "description": "ENCLOMIPHENE (ANDROXAL) - Повышает тестостерон, улучшает либидо и энергию."
    },
    "4-dma-78-dhf": {
        "item_id": 13,
        "category_id": 7,
        "category_name": "metabolicheskie",
        "name": "EUTROPOFLAVIN (4'-DMA-7,8-DHF)",
        "price": 2200,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "EUTROPOFLAVIN (4'-DMA-7,8-DHF) - Аналог BDNF, улучшает нейропластичность и память."
    },
    "aromasin": {
        "item_id": 14,
        "category_id": 5,
        "category_name": "adaptogeni",
        "name": "EXEMESTANE (AROMASIN)",
        "price": 1800,
        "quantity": "30 капсул",
        "dosage": "25 мг",
        "description": "EXEMESTANE (AROMASIN) - Ингибитор ароматазы. Снижает эстроген, повышает тестостерон."
    },
    "fasoracetam": {
        "item_id": 15,
        "category_id": 1,
        "category_name": "racetami",
        "name": "FASORACETAM",
        "price": 2600,
        "quantity": "30 капсул",
        "dosage": "100 мг",
        "description": "FASORACETAM - Улучшает внимание и обучаемость, особенно при СДВГ."
    },
    "ketas": {
        "item_id": 16,
        "category_id": 7,
        "category_name": "metabolicheskie",
        "name": "IBUDILAST (KETAS)",
        "price": 2000,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "IBUDILAST (KETAS) - нейропротектор, снижает нейровоспаление."
    },
    "mk-677": {
        "item_id": 17,
        "category_id": 5,
        "category_name": "adaptogeni",
        "name": "IBUTAMOREN (MK-677)",
        "price": 2000,
        "quantity": "30 капсул",
        "dosage": "15 мг",
        "description": "IBUTAMOREN (MK-677) - Стимулятор гормона роста. Увеличивает мышечную массу."
    },
    "j-147": {
        "item_id": 18,
        "category_id": 4,
        "category_name": "neiroprotectors",
        "name": "J-147",
        "price": 1600,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "J-147 - Антиоксидант и нейропротектор, замедляет старение мозга."
    },
    "l-thp": {
        "item_id": 19,
        "category_id": 4,
        "category_name": "neiroprotectors",
        "name": "L-THP",
        "price": 1200,
        "quantity": "30 капсул",
        "dosage": "30 мг",
        "description": "L-THP - Анксиолитик и мягкий стимулятор. Снижает тревожность."
    },
    "magnesium_l-threonate": {
        "item_id": 20,
        "category_id": 7,
        "category_name": "metabolicheskie",
        "name": "MAGNESIUM L-THREONATE",
        "price": 1000,
        "quantity": "30 капсул",
        "dosage": "500 мг",
        "description": "MAGNESIUM L-THREONATE - Лучшая форма магния для мозга. Улучшает память и сон."
    },
    "centrophenoxine": {
        "item_id": 21,
        "category_id": 2,
        "category_name": "holinergetiki",
        "name": "MECLOFENOXATE (CENTROPHENOXINE)",
        "price": 3500,
        "quantity": "30 капсул",
        "dosage": "300 мг",
        "description": "MECLOFENOXATE (CENTROPHENOXINE) - Улучшает энергетический обмен в мозге, замедляет старение."
    },
    "nnmti": {
        "item_id": 22,
        "category_id": 7,
        "category_name": "metabolicheskie",
        "name": "NNMTI (5-AMINO-1MQ)",
        "price": 5700,
        "quantity": "30 капсул",
        "dosage": "50 мг",
        "description": "NNMTI (5-AMINO-1MQ) - Блокирует NNMT, повышает NAD+. Замедляет старение."
    },
    "nor-bni": {
        "item_id": 23,
        "category_id": 6,
        "category_name": "antidepressanti",
        "name": "NOR-BNI",
        "price": 3800,
        "quantity": "50 мг в 10 мл",
        "dosage": "750 мкг/пшик (65 доз)",
        "description": "NOR-BNI - Блокирует каппа-опиоидные рецепторы, снижает тревожность."
    },
    "noopept": {
        "item_id": 24,
        "category_id": 1,
        "category_name": "racetami",
        "name": "OMBERACETAM (NOOPEPT)",
        "price": 1200,
        "quantity": "30 капсул",
        "dosage": "30 мг",
        "description": "OMBERACETAM (NOOPEPT) - Нейропротектор с анксиолитическим эффектом."
    },
    "phenylpiracetam_hydrazide": {
        "item_id": 25,
        "category_id": 1,
        "category_name": "racetami",
        "name": "PHENYLPIRACETAM HYDRAZIDE",
        "price": 2500,
        "quantity": "30 капсул",
        "dosage": "100 мг",
        "description": "PHENYLPIRACETAM HYDRAZIDE - Аналог фенотропила с пролонгированным действием."
    },
    "wakix": {
        "item_id": 26,
        "category_id": 3,
        "category_name": "stimulators",
        "name": "PITOLISANT (WAKIX)",
        "price": 3500,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "PITOLISANT (WAKIX) - Блокирует гистаминовые рецепторы, повышает бодрость."
    },
    "pramiracetam": {
        "item_id": 27,
        "category_id": 1,
        "category_name": "racetami",
        "name": "PRAMIRACETAM",
        "price": 2500,
        "quantity": "30 капсул",
        "dosage": "300 мг",
        "description": "PRAMIRACETAM - Сильный стимулятор памяти и аналитического мышления."
    },
    "prl-8-53": {
        "item_id": 28,
        "category_id": 4,
        "category_name": "neiroprotectors",
        "name": "PRL-8-53",
        "price": 1400,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "PRL-8-53 - Улучшает краткосрочную память. Эффект после однократного приема."
    },
    "encephabol": {
        "item_id": 29,
        "category_id": 2,
        "category_name": "holinergetiki",
        "name": "PYRITINOL (ENCEFABOL)",
        "price": 2000,
        "quantity": "30 капсул",
        "dosage": "100 мг",
        "description": "PYRITINOL (ENCEFABOL) - Стимулирует метаболизм глюкозы в мозге. Повышает бодрость."
    },
    "enerion": {
        "item_id": 30,
        "category_id": 3,
        "category_name": "stimulators",
        "name": "SULBUTIAMINE (ENERION)",
        "price": 1800,
        "quantity": "30 капсул",
        "dosage": "200 мг",
        "description": "SULBUTIAMINE (ENERION) - Улучшает энергетический обмен, снижает усталость."
    },
    "osavampator": {
        "item_id": 31,
        "category_id": 4,
        "category_name": "neiroprotectors",
        "name": "TAK-653 (OSAVAMPATOR)",
        "price": 3000,
        "quantity": "100 мг в 5 мл DMSO",
        "dosage": "1 мг/пшик (100 доз)",
        "description": "TAK-653 (OSAVAMPATOR) - Усиливает синаптическую пластичность через AMPA-рецепторы."
    },
    "tesofensine": {
        "item_id": 32,
        "category_id": 3,
        "category_name": "stimulators",
        "name": "TESOFENSINE",
        "price": 3000,
        "quantity": "30 мг в 3 мл DMSO",
        "dosage": "500 мкг/пшик (60 доз)",
        "description": "TESOFENSINE - Сильный ингибитор обратного захвата дофамина и норадреналина."
    },
    "fareston": {
        "item_id": 33,
        "category_id": 5,
        "category_name": "adaptogeni",
        "name": "TOREMIFEN (FARESTON)",
        "price": 3500,
        "quantity": "30 капсул",
        "dosage": "20 мг",
        "description": "TOREMIFEN (FARESTON) - Антиэстроген, используется в терапии рака груди."
    },
    "78-dhf": {
        "item_id": 34,
        "category_id": 7,
        "category_name": "metabolicheskie",
        "name": "TROPOFLAVIN (7,8-DHF)",
        "price": 1300,
        "quantity": "30 капсул",
        "dosage": "25 мг",
        "description": "TROPOFLAVIN (7,8-DHF) - Усиливает когнитивные функции, защищает нейроны."
    },
    "unifiram": {
        "item_id": 35,
        "category_id": 7,
        "category_name": "metabolicheskie",
        "name": "UNIFIRAM",
        "price": 2800,
        "quantity": "30 капсул",
        "dosage": "10 мг",
        "description": "UNIFIRAM - Усиливает когнитивные функции, может улучшать долговременную память."
    }
}
