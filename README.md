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
```
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
