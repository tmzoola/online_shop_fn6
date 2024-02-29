from store.models import Product
class Cart:

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product,quantity):
        product_id = str(product.id)
        product_qyt = str(quantity)

        if product_id in self.cart:
            pass
        else:
           # self.cart[product_id] = {"price":str(product.price)}
            self.cart[product_id] = int(product_qyt)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)


    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantity(self):
        quantity = self.cart
        return quantity

    def update(self, product, quantity):
        product_id = str(product)
        product_qyt = int(quantity)

        cart_update = self.cart
        cart_update[product_id] = product_qyt

        self.session.modified = True
        thing = self.cart

        return thing

    def delete(self, product_id):
        product = str(product_id)

        if product in self.cart:
            del self.cart[product]

        self.session.modified = True


    def get_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        total = 0

        for key,value in self.cart.items():
            key = int(key)
            for product in products:
                    if product.id == key:
                        total = total + (product.price * value)
        return total


    def get_all_info(self):
        prods = self.get_products()
        quantity = self.get_quantity()

        result = []

        for prod in prods:
            if str(prod.id) in quantity:
                data = {
                    'id': prod.id,
                    'name': str(prod.name),
                    'price': prod.price,
                    'quantity': quantity[str(prod.id)]
                }
                result.append(data)
        return result


    def cart_clear(self):
        self.cart.clear()
        self.session.modified = True
        return self.cart
