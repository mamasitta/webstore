from store_api.models import Product, OrderItem


def check_order_items(item):
    """ Function to check if ordered product exist and have required amount """
    product_id = item['product_id']
    item_amount = item['amount']
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return False
    if product.amount >= item_amount:
        return True
    else:
        return False


def save_order_items(item, order_id):
    product = Product.objects.filter(id=item['product_id']).first()
    try:
        new_product_amount = product.amount - int(item['amount'])
    except ValueError:
        return False
    Product.objects.filter(id=item['product_id']).update(amount=new_product_amount)
    new_order_item = OrderItem(order_id=order_id, product_id=item['product_id'], amount=item['amount'])
    new_order_item.save()
    return True
