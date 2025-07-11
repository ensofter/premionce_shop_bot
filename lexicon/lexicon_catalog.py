from typing import Callable
from database.catalog_ds import nootropics_dict
from database.catalog_gk import nootropics


LEXICON_CATALOG: dict[str, str] = {
    'welcome_text': '<b>Ассортимент магазина PREMIONCE</b>\n\n'
                    'Сильному человеку требуется многокомпонентный арсенал для преобразования жизненной энергии в '
                    'материальные и духовные блага.\n\n'
                    'PREMIONCE STORE - это инструментарий с помощью которого Вы быстрее и качественнее '
                    'получаете результаты во всех сферах.\n\n'
                    '✨ Выбирайте из каталога то, что резонирует с Вами.\n\n'
                    'Посмотрите наш ассортимент по '
                    '<a href="https://telegra.ph/Assortiment-magazina-PREMIONCE-07-06">ссылке</a>',
    'back_to_catalog': '🔙 Назад'
}

LEXICON_CATALOG_CATEGORIES: dict[str, str] = {
    "racetami": "🧠 Рацетамы",
    "holinergetiki": "⚡ Холинергики",
    "stimulators": "🚀 Стимуляторы / Дофаминергические",
    "neiroprotectors": "🛡️ Нейропротекторы",
    "adaptogeni": "⚖️ Адаптогены / Эндокринные модуляторы",
    "antidepressanti": "😌 Антидепрессанты / Анксиолитики",
    "metabolicheskie": "🔬 Метаболические / Другие"
}


