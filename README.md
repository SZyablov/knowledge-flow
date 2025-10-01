# Knowledge Flow 💡 

## Описание проекта

<details><summary>Подробнее</summary>
    
### Основная информация

Сервис позволяет выполнять
интеллектуальный поиск информации в интернете. Система скраппит результаты поиска, индексирует
полученные тексты и предоставляет итоговый ответ пользователю с помощью
LLM, сопровождая его ссылками на источники.

### Функциональные части сервиса

-   Веб-интерфейс для пользователя (Gradio)
-   Бэкенд-сервис с API
-   Сервис поиска (через SearxNG)

### Возможности

-   Поиск информации в интернете и локальных источниках
-   Индексация текста
-   Формирование итогового ответа с указанием ссылок

</details>

## Технологии

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![SearxNG](https://img.shields.io/badge/-SearxNG-46a247)](https://searxng.github.io/searxng/)
[![Gradio](https://img.shields.io/badge/Gradio-orange)](https://www.gradio.app/)
[![Faiss](https://img.shields.io/badge/Faiss-lightgrey)](https://github.com/facebookresearch/faiss)

## Установка

### Необходимые условия

-   [Docker](https://www.docker.com/products/docker-desktop/) установлен
    в вашей системе
-   Git установлен

### Шаг 1: Клонирование репозитория

``` bash
git clone https://github.com/SZyablov/knowledge-flow.git
cd knowledge-flow
```

### Шаг 2: Настройка окружения

1)  Скопируйте шаблон файла `docker-compose.override.template.yml` в
    `docker-compose.override.yml`
2)  Задайте ключи для Groq/TogetherAI, выберите нужного провайдера

### Шаг 3: Сборка и запуск контейнеров

``` bash
docker-compose build

# Стандарнтый запуск
docker-compose up
# Detached режим
docker-compose up -d
```

После запуска будут активны все сервисы: UI, backend и поисковый
движок.\
Откройте `http://127.0.0.1:7860/`, чтобы получить доступ к интерфейсу.

## Использование

Откройте `http://127.0.0.1:7860/` и затем:
1)  Введите поисковый запрос в интерфейсе
2)  Сервис выполнит поиск в интернете
3)  Результаты будут проиндексированы
4)  LLM сгенерирует итоговый ответ и предоставит ссылки на источники

## TODO

* Добавить настройку для выбора Open AI Compatiple endpoint
* Добавить возможность задать модель на выбор
