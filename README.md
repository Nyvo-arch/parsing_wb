# WB Analytics

Сервис аналитики товаров Wildberries: парсинг, фильтрация, визуализация.

# 📦 Функционал

- 🔍 Парсинг товаров по запросу (название, цена, скидка, рейтинг, отзывы)
- 💾 Сохранение в базу данных (SQLite)
- ⚙️ API-эндпоинт: `/api/products/`  
  Поддерживает фильтры: `min_price`, `max_price`, `min_rating`, `min_reviews`, `ordering`
- 🌐 Фронтенд:
  - Таблица товаров с фильтрами и сортировкой
  - Гистограмма цен
  - Гистограмма: скидка (%) vs рейтинг

# 🛠️ Стек

- Python + Django + Django REST Framework
- SQLite
- TailwindCSS + Chart.js + noUiSlider + JS

# 🚀 Запуск

```bash
git clone https://github.com/Nyvo-arch/parsing_wb.git
cd parsing_wb
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# (по желанию) создать суперюзера
python manage.py createsuperuser
Готовый юзер: admin:1wax2qsZ

# Запустить парсинг (пример)
python manage.py parse_wb "носки" --pages 3 (кол-во страниц)

# Запустить сервер
python manage.py runserver
