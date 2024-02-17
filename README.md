# Добро пожаловать на Foodgram!
![](https://github.com/zalimpshigotizhev/foodgram-project-react/blob/master/pic/1-100.jpg)

На нашем сайте "Foodgram" вы сможете окунуться в мир кулинарных удовольствий и поделиться своими рецептами с другими гурманами. Наш сайт предоставляет широкий спектр функциональных возможностей для истинных ценителей еды.

## СТЕК:
django-filter==21.1
djangorestframework==3.14.0
djoser==2.1.0
python-decouple==3.5
drf-extra-fields==3.2.1
gunicorn==20.1.0
Pillow==9.3.0
psycopg2-binary==2.9.3

## Основные функции Foodgram:

### Регистрация и Авторизация

Присоединяйтесь к нашему кулинарному сообществу, создавайте свои аккаунты и наслаждайтесь всеми возможностями Foodgram. Мы предоставляем удобную систему регистрации и авторизации.

### Публикация Рецептов

У вас есть любимый рецепт, который вы хотели бы поделиться с миром? На Foodgram вы можете опубликовать свой рецепт с фотографиями, подробными инструкциями по приготовлению и списком необходимых ингредиентов.

### Создание Своих Рецептов

Вы можете создавать собственные уникальные рецепты и делиться ими с сообществом. Добавляйте новые блюда, придумывайте интересные сочетания ингредиентов и получайте отзывы и оценки от других пользователей.

### Фильтрация по Тегам

На сайте доступен удобный фильтр по тегам, который поможет вам находить рецепты по вашим предпочтениям. Выбирайте теги, которые вам интересны, и наслаждайтесь кулинарными открытиями.

### Список Покупок

Составьте список покупок для выбранных рецептов и скачайте его в удобном формате. Теперь вы никогда не забудете необходимые ингредиенты перед походом в магазин.

### Подписка на Пользователей

Следите за активностью других участников и подписывайтесь на тех, чьи рецепты и идеи вас вдохновляют. Будьте в курсе всех обновлений и новых блюд ваших любимых авторов.

## Присоединяйтесь к Foodgram уже сегодня и откройте для себя бескрайний мир вкусов и кулинарных открытий!


## Как развернуть проект
1) Форкнуть этот репозиторий на свой ГитХаб
2) Развернуть на локалке, далее:
  Изменить паайплай под свой сервер.
3) Запушить после изменений workflows. Изменить в настройках репозитория, выбрать Action - там подставить свои key для workflows.
4) Скопировать свой .env и docker-compose.production.yml на сервер.
5) Ввести изменение в локальной части проекта, запушить проект далее проект развернется на сервере автоматически, благодаря GitHub Actions.
   # OR
   Запустить оркестрацию через docker compose up

## В .env нужно написать:
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432


