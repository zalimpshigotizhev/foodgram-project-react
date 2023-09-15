# recipes
MIN_TIME_COOK = 1
MAX_TIME_COOK = 500
MIN_COUNT_INGR = 1
MIN_COUNT_INGR = 32000
DEFAULT_INGR = 1
MAX_SIZE_IMAGE = (1000, 1000)


def id_and_amount_pull_out_from_dict(classes, data_ingr):
    """ Вытаскивает id и amount из
        request.context['ingredients'] в виде кортежа """
    id_list = []
    amounts = []

    for ingredient in data_ingr:
        for name, value in ingredient.items():
            if name == 'id':
                id_list.append(value)
            elif name == 'amount':
                amounts.append(value)

    ingredients = classes.objects.filter(id__in=id_list)
    return list(zip(ingredients, amounts))
