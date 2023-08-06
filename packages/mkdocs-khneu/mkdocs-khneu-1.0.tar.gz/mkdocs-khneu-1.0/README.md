# Mkdocs Template

Шаблон електронного видання для Material for MkDocs з прикладами оформлення контенту 

Приклади оформлення контенту проекту Bookdown розташовані у папці `old-content`.

## Як користуватись

Для роботи з Material for MkDocs нам потрібно виконати наступну команду з встановлення ПЗ: 

```shell
pip install mkdocs-material pymdown-extensions mkdocs-enumerate-headings-plugin
```

Далі виконуєио команду `mkdocs new {project's name}` та створюємо папку нашого проекту. Отримуємо папку `docs` та файл `.yml`. У `docs` знаходитимуться наші `.md` файли, а в `.yml` більшість налаштувань. Введіть у ваш `.yml` таку конфігурацію:
 
     theme:
        name: material

Надалі в кореневій директорії проекту виконуємо наступні команди:

- `mkdocs serve` - для старту live-сервера
- `mkdocs build` - для збірки сайту з метою подальшого розповсюдження

## Корисні посилання

### Власні ресурси

- [Електронні видання ХНЕУ](https://pns.hneu.edu.ua/course/index.php?categoryid=1047) (для перегляду потрібно авторизуватися на сайті ПНС, найбільш функціональне видання - Економетрика)
- [Кузня контенту](https://content.hneu.edu.ua/) (для онлайн-роботи з markdown)
- [Приклади оформлення контенту для електронних видань](https://cdn.hneu.edu.ua/bookdown/content/index.html)
    
### MkDocs

- [MkDocs](https://www.mkdocs.org/)
- [MkDocs Plugins](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
