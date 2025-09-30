# Knowledge Flow 💡 

[![Docker Image
CI](https://github.com/SZyablov/knowledge-flow/actions/workflows/docker-image.yml/badge.svg)](https://github.com/SZyablov/knowledge-flow/actions/workflows/docker-image.yml)

## Описание проекта

```{=html}
<details>
```
```{=html}
<summary>
```
Подробнее
```{=html}
</summary>
```
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

```{=html}
</details>
```
## Технологии

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![SearxNG](https://img.shields.io/badge/-SearxNG-46a247?logo=search)](https://searxng.github.io/searxng/)
[![Gradio](https://img.shields.io/badge/Gradio-orange?logo=gradio)](https://www.gradio.app/)

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
docker-compose up -d
```

После запуска будут активны все сервисы: UI, backend и поисковый
движок.\
Откройте `http://127.0.0.1:7860/`, чтобы получить доступ к интерфейсу.

## Использование

1)  Введите поисковый запрос в интерфейсе
2)  Сервис выполнит поиск в интернете
3)  Результаты будут проиндексированы
4)  LLM сгенерирует итоговый ответ и предоставит ссылки на источники
