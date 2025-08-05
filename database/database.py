import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class CartItem:
    item_id: int = None
    name: str = None
    unit_price: float = None
    quantity: int = None
    category_id: int = None
    image_url: str = None

    @property
    def total_price(self) -> float:
        return self.unit_price * self.quantity


@dataclass
class Cart:
    items: Dict[int, CartItem] = field(default_factory=dict)
    is_active: bool = True

    def validate_items(self) -> bool:
        # метод для проверки наличия товара на складе
        return

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
            self.items[item_id].quantity -= quantity

    def get_item(self, item_id: int) -> CartItem:
        if item_id in self.items:
            return self.items.get(item_id)

    def has_item(self, item_id: int) -> bool:
        return item_id in self.items

    def total_uniq_items(self) -> int:
        return len(self.items)

    def total_items(self) -> int:
        return sum(item.quantity for item in self.items.values())

    def increase_item_quantity(self, item_id: int, val: int) -> None:
        if item_id not in self.items:
            return
        self.items[item_id].quantity += val

    def decrease_item_quantity(self, item_id: int, val: int) -> None:
        if item_id not in self.items:
            return
        self.items[item_id].quantity -= val

    def clear(self) -> None:
        self.items.clear()

    def calculate_total(self) -> float:
        return sum(item.total_price for item in self.items.values())


@dataclass
class Profile:
    full_name: str = None
    phone: str = None
    address: str = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def is_complete(self) -> bool:
        return all([self.full_name, self.phone, self.address])


@dataclass
class Referral:
    referral_key: str = None
    referred_by: str = None
    referral_count: int = 3
    referral_income: int = 10010
    created_at: datetime = field(default_factory=datetime.now)
    balance: int = 1000

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def generate_key(self, user_id: int) -> None:
        self.referral_key = f"{user_id}_{hash(self.created_at)}"


@dataclass
class Order:
    order_id: int = None
    items: List[CartItem] = field(default_factory=list)
    created_at: datetime = None
    subtotal: float = None
    delivery_address: str = None
    contact_name: str = None
    contact_phone: str = None
    delivery_cost: float = None
    discount: float = None
    notes: str = None
    tracking_number: str = None
    user_id: int = None
    referral_key: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    @property
    def final_price(self) -> float:
        return self.subtotal + self.delivery_cost - self.discount


@dataclass
class UserData:
    user_id: int = None
    is_active: bool = True
    referral: Referral = None
    profile: Profile = None
    cart: Cart = field(default_factory=Cart)
    orders: List[Order] = field(default_factory=list)

    def get_user_id(self) -> int:
        return self.user_id

    def create_order_from_cart(self) -> Order:
        order = Order(
            order_id=int(uuid.uuid4().int & (1<<31)-1),
            items=list(self.cart.items.values()),
            created_at=datetime.now(),
            subtotal=self.cart.calculate_total(),
            delivery_address=self.profile.address,
            contact_name=self.profile.full_name,
            contact_phone=self.profile.phone,
            delivery_cost=800,
            discount=0,
            user_id=self.get_user_id(),
        )
        self.orders.append(order)
        self.cart.clear()
        return order

    def apply_referral_balance(self, order: Order) -> None:
        if self.referral.balance > 0:
            order.discount += self.referral.balance
            self.referral.balance = 0

    def get_order_history(self) -> List[Order]:
        return sorted(self.orders, key=lambda x: x.created_at, reverse=True)


user_dict_template = UserData(
    referral=Referral(),
    profile=Profile(),
    cart=Cart(),
    orders=[]
)
user_db: Dict[int, UserData] = {}
