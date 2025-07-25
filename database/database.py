from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CartItem:
    item_id: int = None
    name: str = None
    price_per_unit: int = None
    quantity: int = None

    @property
    def total_price(self) -> float:
        return self.price_per_unit * self.quantity


@dataclass
class Cart:
    items: Dict[int, CartItem] = field(default_factory=dict)

    def add_item(self, item: CartItem) -> None:
        if item.item_id in self.items:
            self.items[item.item_id].quantity += item.quantity
        else:
            self.items[item.item_id] = item

    def remove_item(self, item_id: int, quantity: int = 1) -> None:
        if item_id not in self.items:
            return
        if self.items[item_id].quantity <= quantity:
            del self.items[item_id]
        else:
            self.items[item_id] -= quantity

    def get_item(self, item_id: int) -> CartItem:
        if item_id in self.items:
            return self.items.get(item_id)

    def has_item(self, item_id: int) -> bool:
        return item_id in self.items

    def total_uniq_items(self) -> int:
        return len(self.items)

    def total_items(self) -> int:
        return sum(item.quantity for item in self.items.values())

    def clear(self) -> None:
        self.items.clear()


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
    cart: Cart = field(default_factory=Cart)


user_dict_template = UserData(
    referral=Referral(),
    profile=Profile(),
    cart=Cart(
        items=
        {
            5: CartItem(
                item_id=5,
                name='ANIRACETAM',
                price_per_unit=1400,
                quantity=2
            ),
            1: CartItem(
                item_id=1,
                name='7-OXO (7-KETO-DHEA)',
                price_per_unit=3400,
                quantity=1
            ),
            34: CartItem(
                item_id=34,
                name='TROPOFLAVIN (7,8-DHF)',
                price_per_unit=1300,
                quantity=5
            )
        }
    )
)
user_db: Dict[int, UserData] = {}
