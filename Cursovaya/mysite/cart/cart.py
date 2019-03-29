from decimal import Decimal
from django.conf import settings
from catalog.models import Tour


class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Добавление товара в корзину пользователя или обновление количества товара
    def add(self, tour, quantity=1, update_quantity=False):
        tour_id = str(tour.id)
        if tour_id not in self.cart:
            self.cart[tour_id] = {'quantity': 0,
                                         'price': str(tour.PriceAdult)}
        if update_quantity:
            self.cart[tour_id]['quantity'] = quantity
        else:
            self.cart[tour_id]['quantity'] += quantity
        self.save()

    # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

    def remove(self, tour):
        tour_id = str(tour.id)
        if tour_id in self.cart:
            del self.cart[tour_id]
            self.save()

    # Итерация по товарам
    def __iter__(self):
        tour_ids = self.cart.keys()
        tours = Tour.objects.filter(id__in=tour_ids)
        for tour in tours:
            self.cart[str(tour.id)]['tour'] = tour

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # Количество товаров
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True