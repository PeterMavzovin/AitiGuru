## Даталогическая схема данных (реляционная модель)

Таблицы:

### 1.1. Категории (`category`)

| Поле      | Тип    | Описание                                 |
|-----------|--------|------------------------------------------|
| id        | PK     | Первичный ключ                           |
| name      | TEXT | Название категории                       |
| parent_id | FK     | Внешний ключ на category.id, NULL для корневых |

### 1.2. Номенклатура (`product`)

| Поле        | Тип    | Описание                                 |
|-------------|--------|------------------------------------------|
| id          | PK     | Первичный ключ                           |
| name        | TEXT | Название товара                            |
| quantity    | INTEGER    | Количество                           |
| price       | NUMERIC(10, 2)  | Цена                            |
| category_id | FK     | Внешний ключ на category.id              |

### 1.3. Клиенты (`client`)

| Поле    | Тип    | Описание         |
|---------|--------|------------------|
| id      | PK     | Первичный ключ   |
| name    | TEXT | Имя клиента      |
| address | TEXT | Адрес клиента    |

### 1.4. Заказы (`order`)

| Поле      | Тип    | Описание                        |
|-----------|--------|---------------------------------|
| id        | PK     | Первичный ключ                  |
| client_id | FK     | Внешний ключ на client.id       |
| order_date| DATE   | Дата заказа                     |

### 1.5. Позиции заказа (`order_item`)

| Поле       | Тип    | Описание                        |
|------------|--------|---------------------------------|
| id         | PK     | Первичный ключ                  |
| order_id   | FK     | Внешний ключ на order.id        |
| product_id | FK     | Внешний ключ на product.id      |
| quantity   | INTEGER    | Количество                      |
| price      | NUMERIC(10, 2)  | Цена                            |



## SQL запросы

### 2.1
```sql
SELECT
    c.name AS client_name,
    SUM(oi.quantity * oi.price) AS total_sum
FROM
    client c
JOIN
    "order" o ON o.client_id = c.id
JOIN
    order_item oi ON oi.order_id = o.id
GROUP BY
    c.id, c.name;
```

### 2.2
```sql
SELECT
    parent.id AS category_id,
    parent.name AS category_name,
    COUNT(child.id) AS children_count
FROM
    category parent
LEFT JOIN
    category child ON child.parent_id = parent.id
GROUP BY
    parent.id, parent.name;
```

### 2.3
### 2.3.1
```sql
CREATE OR REPLACE VIEW top5_products_last_month AS
SELECT
    p.name AS product_name,
    c1.name AS category_lvl1,
    SUM(oi.quantity) AS total_quantity
FROM
    order_item oi
JOIN
    product p ON p.id = oi.product_id
JOIN
    category c ON c.id = p.category_id
LEFT JOIN
    category c1 ON (
        c1.id = c.id AND c1.parent_id IS NULL
    )
LEFT JOIN
    category c2 ON c2.id = c.parent_id
WHERE
    oi.order_id IN (
        SELECT id FROM "order"
        WHERE order_date >= (CURRENT_DATE - INTERVAL '1 month')
    )
GROUP BY
    p.id, p.name, c1.name
ORDER BY
    total_quantity DESC
LIMIT 5;
```

### 2.3.2
1. Использовать индексы на:
 - order.order_date
 - order_item.product_id
 - product.category_id
 - category.parent_id
2. Для ускорения поиска корневой категории — материализовать путь (например, добавить поле root_category_id в product или category).
3. Для больших данных — денормализовать часто используемые отчеты (например, хранить агрегаты продаж по дням/товарам).
4. Использовать партиционирование таблиц заказов по дате.
