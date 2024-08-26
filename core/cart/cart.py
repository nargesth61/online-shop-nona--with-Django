from shop.models import ProductStatusType,ProductModel

class CartSession:
    def __init__(self,session) :
        self.session = session
        self._cart = self.session.setdefault('_cart',
                                            {
                                            'items':[],
                                            'total_price':0,
                                            'tatal_item':0
                                            })
    def add_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] += 1
                break
        else:
            new_item = {"product_id": product_id, "quantity": 1}
            self._cart["items"].append(new_item)
        self.save()
    
    def decrease_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] -= 1
                break
        else:
            new_item = {"product_id": product_id, "quantity": 1}
            self._cart["items"].append(new_item)
        self.save()
    
    def count_of_product(self, product_id):
        for item in self._cart["items"]:
            if int(product_id) == int(item["product_id"]):
                return item["quantity"]
        return 0  # Product not found in the cart
            
    def update_product(self, product_id,quantity):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = int(quantity)
                break
        else:
            return
        self.save()
    
    def remove_product(self,product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                break
        else:
            return
        self.save() 
   
    def clear(self):
        self._cart = self.session['_cart']={
            'items':[],
            'total_price':0,
            'tatal_item':0
        }
        self.save()
    
    def save(self):
        self.session.modified = True
    
    def get_cart_dict(self):
        return self._cart

    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self._cart["items"])

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self._cart["items"])
   
    def get_cart_items(self):
        for item in self._cart["items"]:
            product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            item.update({"product_obj": product_obj, "total_price": item["quantity"] * product_obj.get_price()})
        return self._cart["items"]

