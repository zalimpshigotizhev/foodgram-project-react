class Const:
    # Параметр для поиска ингридиентов по вхождению значения в название
    SEARCH_ING_NAME = "name"
    # Параметр для поиска объектов в списке "избранное"
    FAVORITE = "is_favorited"
    # Параметр для поиска объектов в списке "покупки"
    SHOP_CART = "is_in_shopping_cart"
    # Параметр для поиска объектов по автору
    AUTHOR = "author"
    # Параметр для поиска объектов по тэгам
    TAGS = "tags"
    RECIPE_IMAGE_SIZE = 500, 500
    # Поиск объектов только с переданным параметром.
    # Например только в избранном: `is_favorited=1`
    SYMBOL_TRUE_SEARCH = "1", "true"
    # Поиск объектов не содержащих переданный параметр.
    # Например только не избранное: `is_favorited=0`
    SYMBOL_FALSE_SEARCH = "0", "false"
