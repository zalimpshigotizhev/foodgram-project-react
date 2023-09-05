from recipes.models import Cart


def get_cart_data_for_user(user):
    cart_item = Cart.objects.filter(user=user)
    cart_data = []
    for cart_item in cart_item:
        cart_data.append({
            'name': cart_item.recipe.name,
            'amount': cart_item.amount,
            'unit': cart_item.unit,
        })

    return cart_data