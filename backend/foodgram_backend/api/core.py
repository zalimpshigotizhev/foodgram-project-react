
def id_and_amount_pull_out_from_dict(self, list_dicts_):
    ''' Вытаскивает id и amount из
        request.context['ingredients'] в виде кортежа'''
    lst_id = []

    for dict_ in list_dicts_:
        ids = dict_['id']
        amount = dict_['amount']
        tuple_ = (ids, amount)
        lst_id.append(tuple_)

    return lst_id


MIN_TIME_COOK = 1
MAX_TIME_COOK = 500
MIN_COUNT_INGR = 1
MIN_COUNT_INGR = 32000
DEFAULT_INGR = 1


MAX_SIZE_IMAGE = (1000, 1000)
