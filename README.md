# Парсер [топ 1000 фильмов и сериалов](https://www.kinopoisk.ru/lists/movies/popular/) с кинопоиска

## Задача
Получить с [этой](https://www.kinopoisk.ru/lists/movies/popular/) страницы:
- Номер в рейтинге
- Название на русском
- Название на английском
- Год выпуска
- Рейтинг кинопоиска

Для выполнения задачи я использовал Python фреймворк [Scrapy](https://scrapy.org/).

## Установка и запуск
---
Для запуска в Dockerfile необходимо указать API ключ [прокси агрегатора](https://scrapeops.io/). После регистрации вы найдёте ключ в личном кабинете.

### Создание образа
```bash
docker build --tag kinopoiskspider .
```

### Запуск контейнера
```bash
docker run --rm -v $PWD/kinopoiskspider/:/kinopoiskspider kinopoiskspider:latest
```