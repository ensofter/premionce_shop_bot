from dataclasses import dataclass
from typing import Dict


@dataclass
class Profile:
    fio: str = None
    phone: str = None
    address: str = None


@dataclass
class Referral:
    url: str = None
    total_referral: int = 3
    total_income: int = 10010
    balance: int = 1000


@dataclass
class UserData:
    referral: Referral = None
    profile: Profile = None


user_dict_template = UserData(
    referral=Referral(),
    profile=Profile()
)
user_db: Dict[int, UserData] = {}
