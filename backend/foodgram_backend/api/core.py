

class Defs:
    def id_and_amount_pull_out_from_dict(list_dicts_):
        ''' Вытаскивает id и amount из
            request.context['ingredients'] в виде кортежа'''
        lst_id = []

        for dict_ in list_dicts_:
            ids = dict_['id']
            amount = dict_['amount']
            tuple_ = (ids, amount)
            lst_id.append(tuple_)
        return lst_id