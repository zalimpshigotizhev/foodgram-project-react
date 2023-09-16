# recipes
MIN_TIME_COOK = 1
MAX_TIME_COOK = 500
MIN_COUNT_INGR = 1
MAX_COUNT_INGR = 32000
DEFAULT_INGR = 1
MAX_SIZE_IMAGE = (1000, 1000)
MAX_LENGTH_NAME_TAG = 56
MAX_LENGTH_NAME_INGR = 56
MAX_LENGTH_NAME_RECIPE = 56
MAX_LENGTH_NAME_COLOR = 56
MAX_LENGTH_MEASUR_UNIT = 56


def id_and_amount_pull_out_from_dict(classes, data_ingr):
    """ Вытаскивает id и amount из
        request.context['ingredients'] в виде кортежа
    """
    id_list = []
    amounts = []

    for ingredient in data_ingr:
        for name, value in ingredient.items():
            if name == "id":
                id_list.append(value)
            elif name == "amount":
                amounts.append(value)

    ingredients = classes.objects.filter(id__in=id_list)
    return list(zip(ingredients, amounts))


def make_new_count_ingr(classes, recipe, ingredients):
    """ Создает связку Ingredient:CountIngredient
        с помощью метода мгновенного добавление в базу данных .bulk_create()
    """
    amount_list = []
    for ingredient, amount in ingredients:
        amount_ingr = classes(ingredient=ingredient,
                              amount=amount,
                              recipe=recipe)
        amount_list.append(amount_ingr)
    classes.objects.bulk_create(amount_list)
