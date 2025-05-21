
# Анализ данных о фондах и инвестициях (PostgreSQL)

**Цель:** проанализировать данные о фондах и инвестициях, написав запросы к базе данных.

## Выполненные задачи:



### 1. Закрытие компании
```sql
SELECT *
FROM public.company
WHERE status='closed'
```

### 2. Привлечённые средства новостных компаний США
```sql
SELECT funding_total
FROM company
WHERE category_code = 'news'
   AND country_code = 'USA'
ORDER BY funding_total DESC;
```

### 3. Сумма сделок по покупке компаний за наличные (2011-2013)
```sql
SELECT SUM(price_amount)
FROM acquisition
WHERE term_code  = 'cash'
  AND EXTRACT('year' FROM acquired_at) BETWEEN 2011 AND 2013;
```

### 4. Люди с аккаунтами, начинающимися на 'Silver'
```sql
SELECT first_name, last_name, network_username
FROM people
WHERE network_username LIKE 'Silver%';
```

### 5. Люди с 'money' в username и фамилией на 'K'
```sql
SELECT *
FROM people
WHERE network_username LIKE '%money%'
  AND last_name LIKE 'K%';
```

### 6. Сумма инвестиций по странам
```sql
SELECT country_code,
       SUM(funding_total)
FROM company
GROUP BY country_code
ORDER BY SUM(funding_total) DESC;
```

### 7. Минимальные и максимальные инвестиции по датам
```sql
SELECT funded_at,
       MIN(raised_amount),
       MAX(raised_amount)
FROM funding_round
GROUP BY funded_at
HAVING MIN(raised_amount) <> 0
   AND MIN(raised_amount) <> MAX(raised_amount);
```

### 8. Категоризация фондов по активности
```sql
SELECT *,
       CASE
           WHEN invested_companies < 20 THEN 'low_activity'
           WHEN invested_companies >= 20 AND invested_companies < 100 THEN 'middle_activity'
           WHEN invested_companies >= 100 THEN 'high_activity'
       END
FROM fund;
```

### 9. Среднее количество раундов по категориям
```sql
SELECT CASE
           WHEN invested_companies>=100 THEN 'high_activity'
           WHEN invested_companies>=20 THEN 'middle_activity'
           ELSE 'low_activity'
       END AS activity,
       ROUND(AVG(investment_rounds))
FROM fund
GROUP BY activity
ORDER BY ROUND(AVG(investment_rounds));
```

### 10. Топ-10 активных стран-инвесторов (2010-2012)
```sql
SELECT 
    f.country_code,
    MIN(f.invested_companies) AS min_invested_companies,
    MAX(f.invested_companies) AS max_invested_companies,
    AVG(f.invested_companies) AS avg_invested_companies
FROM fund f
WHERE EXTRACT(YEAR FROM f.founded_at) BETWEEN 2010 AND 2012
GROUP BY f.country_code
HAVING MIN(f.invested_companies) > 0
ORDER BY avg_invested_companies DESC, f.country_code ASC
LIMIT 10;
```

### 11. Сотрудники и их учебные заведения
```sql
SELECT p.first_name,
       p.last_name,
       ed.instituition
FROM people AS p
LEFT JOIN education AS ed ON p.id = ed.person_id;
```

### 12. Топ-5 компаний по количеству уникальных вузов сотрудников
```sql
SELECT comp.name,
       COUNT(DISTINCT ed.instituition)
FROM people AS p
JOIN education AS ed ON p.id = ed.person_id
JOIN company AS comp ON p.company_id = comp.id
GROUP BY comp.name
ORDER BY COUNT(ed.instituition) DESC
LIMIT 5;
```

### 13. Закрытые компании с единственным раундом финансирования
```sql
SELECT name
FROM company
WHERE status = 'closed'
  AND id IN (SELECT company_id
             FROM funding_round
             WHERE is_first_round = 1
               AND is_last_round = 1);
```

### 14. Сотрудники таких компаний
```sql
SELECT DISTINCT p.id AS employee_id
FROM people p
JOIN company c ON p.company_id = c.id
WHERE c.status = 'closed'
  AND c.id IN (
      SELECT company_id
      FROM funding_round
      WHERE is_first_round = 1
        AND is_last_round = 1
  );
```

### 15. Сотрудники и их учебные заведения
```sql
SELECT DISTINCT p.id,
       ed.instituition
FROM people AS p
INNER JOIN education AS ed ON p.id = ed.person_id
WHERE company_id IN (SELECT id
                     FROM company
                     WHERE status = 'closed'
                           AND id IN (SELECT company_id
                                      FROM funding_round
                                      WHERE is_first_round = 1
                                        AND is_last_round = 1));
```

### 16. Количество учебных заведений на сотрудника
```sql
SELECT p.id,
       COUNT(ed.instituition)
FROM people AS p
INNER JOIN education AS ed ON p.id = ed.person_id
WHERE company_id IN (SELECT id
                     FROM company
                     WHERE status = 'closed'
                           AND id IN (SELECT company_id
                                      FROM funding_round
                                      WHERE is_first_round = 1
                                        AND is_last_round = 1))
GROUP BY p.id;
```

### 17. Среднее число учебных заведений (всех сотрудников)
```sql
WITH people_instituition AS (
    SELECT p.id,
           COUNT(ed.instituition) AS count_instituition
    FROM people AS p
    INNER JOIN education AS ed ON p.id = ed.person_id
    WHERE company_id IN (SELECT id
                         FROM company
                         WHERE status = 'closed'
                           AND id IN (SELECT company_id
                                      FROM funding_round
                                      WHERE is_first_round = 1
                                        AND is_last_round = 1))
GROUP BY p.id)

SELECT AVG(count_instituition)
FROM people_instituition;
```

### 18. Среднее число учебных заведений (сотрудники Socialnet)
```sql
WITH people_institution AS (
    SELECT p.id,
           COUNT(ed.instituition) AS count_institution
    FROM people AS p
    INNER JOIN education AS ed ON p.id = ed.person_id
    WHERE p.company_id IN (SELECT id
                           FROM company
                           WHERE name = 'Socialnet')
    GROUP BY p.id
)

SELECT AVG(count_institution) AS average_institutions
FROM people_institution;
```

### 19. Инвестиции в компании с >6 этапами (2012-2013)
```sql
SELECT fund.name AS name_of_fund,
       comp.name AS name_of_company,
       fr.raised_amount AS amount
FROM investment AS invest
JOIN fund ON invest.fund_id = fund.id
JOIN funding_round AS fr ON invest.funding_round_id = fr.id
JOIN company AS comp ON invest.company_id = comp.id
WHERE comp.milestones > 6
  AND EXTRACT('year' FROM fr.funded_at) BETWEEN 2012 AND 2013;
```

### 20. Топ-10 сделок с соотношением цена/инвестиции
```sql
SELECT buy_comp.name AS name_acquiring_company,
       ac.price_amount,
       sell_comp.name AS name_acquired_company,
       sell_comp.funding_total,
       ROUND(ac.price_amount / sell_comp.funding_total) AS price_to_funding_rate
FROM acquisition AS ac
LEFT JOIN company AS buy_comp ON ac.acquiring_company_id = buy_comp.id
LEFT JOIN company AS sell_comp ON ac.acquired_company_id = sell_comp.id
WHERE ac.price_amount > 0
  AND sell_comp.funding_total > 0
ORDER BY ac.price_amount DESC, name_acquired_company
LIMIT 10;
```

### 21. Социальные компании с финансированием (2010-2013)
```sql
SELECT comp.name,
       EXTRACT('month' from fr.funded_at)
FROM company AS comp
JOIN funding_round AS fr ON fr.company_id = comp.id
WHERE comp.category_code = 'social'
  AND fr.raised_amount <> 0
  AND EXTRACT('year' from fr.funded_at) BETWEEN 2010 AND 2013;
```

### 22. Статистика по месяцам (2010-2013)
```sql
WITH
fund_count_monthly AS
   (SELECT EXTRACT('month' from fr.funded_at) AS month,
           COUNT(DISTINCT invest.fund_id) AS fund_count
    FROM funding_round AS fr
    INNER JOIN investment AS invest ON fr.id = invest.funding_round_id
    WHERE EXTRACT('year' from fr.funded_at) BETWEEN 2010 AND 2013
      AND invest.fund_id IN (SELECT id
                             FROM fund
                             WHERE country_code = 'USA')
    GROUP BY month),

acquired_company_monthly AS
   (SELECT EXTRACT('month' from acquired_at) AS month,
           COUNT(acquired_company_id) AS company_count,
           SUM(price_amount) AS total_price
    FROM acquisition
    WHERE EXTRACT('year' from acquired_at) BETWEEN 2010 AND 2013
    GROUP BY month)
    
SELECT fcm.month,
       fcm.fund_count,
       acm.company_count,
       acm.total_price
FROM fund_count_monthly AS fcm
JOIN acquired_company_monthly AS acm ON fcm.month = acm.month;
```

### 23. Средние инвестиции по странам и годам
```sql
WITH 
funding_2011 as
   (SELECT country_code AS country, 
           AVG(funding_total) AS avg_invest_2011
    FROM company AS comp
    WHERE EXTRACT('year' from founded_at) = 2011
    GROUP BY country_code),

funding_2012 as
   (SELECT country_code AS country, 
           AVG(funding_total) AS avg_invest_2012
    FROM company AS comp
    WHERE EXTRACT('year' from founded_at) = 2012
    GROUP BY country_code),

funding_2013 as
   (SELECT country_code AS country, 
           AVG(funding_total) AS avg_invest_2013
    FROM company AS comp
    WHERE EXTRACT('year' from founded_at) = 2013
    GROUP BY country_code)

SELECT f11.country,
       f11.avg_invest_2011,
       f12.avg_invest_2012,
       f13.avg_invest_2013 
FROM funding_2011 AS f11
INNER JOIN funding_2012 AS f12 ON f11.country = f12.country
INNER JOIN funding_2013 AS f13 ON f11.country = f13.country
ORDER BY f11.avg_invest_2011 DESC;
```



