# Блоки {#blocks}

## Списки {#list}

### Нумерований список {#ul}

1. Перший пункт нумерованого списку 
2. Другий пункт нумерованого списку
3. Третій пункт нумерованого списку

```
1. Перший пункт нумерованого списку 
2. Другий пункт нумерованого списку
3. Третій пункт нумерованого списку
```

### Маркований список {#ol}

* пункт один
* пункт два
* пункт три

```
* пункт один
* пункт два
* пункт три
```

### Змішаний список {#ul-ol}

1. Перший пункт списку
2. Другий пункт списку:
    * пункт 2.1
    * пункт 2.2
3. Третій пункт списку
    * пункт 3.1
    * пункт 3.2
   
```
1. Перший пункт списку
2. Другий пункт списку:
    * пункт 2.1
    * пункт 2.2
3. Третій пункт списку
    * пункт 3.1
    * пункт 3.2
``` 

### Нумерований список (широкий) {#list-wide}

1. Перший пункт нумерованого списку

2. Другий пункт нумерованого списку

3. Третій пункт нумерованого списку

4. Четвертий пункт нумерованого списку

5. П'ятий пункт нумерованного списку

```
1. Перший пункт нумерованого списку

2. Другий пункт нумерованого списку

3. Третій пункт нумерованого списку

4. Четвертий пункт нумерованого списку

5. П'ятий пункт нумерованного списку

```

### Автоматична нумерація списку {#auto-numeric}

 #. Один.
 #. Два.
 #. Три.

```
 #.  Один.
 #.  Два.
 #.  Три.
```

### Список без стилів {#list-unstyled}

:::{.list-unstyled}
* Перший елемент
* Другий елемент
* Третій елемент
:::

```
:::{.list-unstyled}
* Перший елемент
* Другий елемент
* Третій елемент
:::
```

### Список без точки після номеру пункту {#list-with-dot}

:::{.list-decimal}
1. Перший елемент
2. Другий елемент
3. Третій елемент
:::

```
:::{.list-decimal}
1. Перший елемент
2. Другий елемент
3. Третій елемент
:::
```

### Нумерований список з дужкою {#list-with-bracket}

:::{.list-bracket}
1. Перший елемент
2. Другий елемент
3. Третій елемент
:::

```
:::{.list-bracket}
1. Перший елемент
2. Другий елемент
3. Третій елемент
:::
```

## Цитати {#quote}

### Звичайна цитата {#simple-quote}
> Приклад використання розмітки для цитування. Можна використовувати для виділення важливих моментів!
 
```
> Приклад використання розмітки для цитування. Можна використовувати для виділення важливих моментів! 
```

### Цитата в іншу сторону {#quote-reverse}

:::{.blockquote-reverse}
Текст в блокноті
:::

```
:::{.blockquote-reverse}
Текст в блокноті
:::
```
    
### Цитата із зазначенням джерела {#autor-quote}

> "I thoroughly disapprove of duels. If a man should challenge me,
  I would take him kindly and forgivingly by the hand and lead him
  to a quiet place and kill him."
>
> --- Mark Twain

```
> "I thoroughly disapprove of duels. If a man should challenge me,
  I would take him kindly and forgivingly by the hand and lead him
  to a quiet place and kill him."
>
> --- Mark Twain
```

## Текстові блоки {#block}

### Преформатований блок {#pre-block}

```
Цей текст відображаться преформатованим
```

<pre>
```
Цей текст відображаться преформатованим
```</pre>

### Інформаційні панелі {#panels}

Інформаційні панелі застосовуються для зручного подання інформації, що напряму не відноситься до викладу основної інформації. Панель є опціональною та складається з декількох елементів, таких як: основний контент панелі (обов'язковий елемент), зображення, назва та посилання. Додавання елемнтів виконується за допомогою атрибутів блоку.

- `data-panel-name` - назва панелі.
- `data-panel-img` - посилання на зображення.
- `data-panel-link` - посилання для переходу на джерело або ж додаткову інформацію.

У прикладі, що надано нижче, відображена  панель, що  має усі елементи. 

:::{.mh-panel data-panel-name="Назва Панелі" data-panel-img="https://www.elegantthemes.com/blog/wp-content/uploads/2016/01/WordPress-eBooks-FT-shutterstock_298676606-adichrisworo.png" data-panel-link="http://www.google.com"}
Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.
:::

```
:::{.mh-panel data-panel-name="Назва Панелі" data-panel-img="..." data-panel-link="..."}
Текст...
:::
```

### Вирівнювання тексту {#text-aligment}

:::{.tl}
Вирівнювання по лівому краю
:::
:::{.tr}
Вирівнювання по правому краю
:::
:::{.tc}
Вирівнювання по центру
:::
:::{.tj}
Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa hic, adipisci eaque nobis corrupti repellendus. Minus, eius vitae repellat optio temporibus quibusdam atque, ipsa modi quos.
:::

```
:::{.tl}
Текст вирівняний по лівому краю.
:::

:::{.tr}
Текст вирівняний по правому краю.
:::

:::{.tc}
Текст вирівняний по центру.
:::

:::{.tj}
Текст вирівняний по ширині.
:::
```

### Основний колір тексту {#block-text-color}

:::{.text-muted}
Кольорове виділення тексту усього абзацу  за допомогою класу text-muted.
:::

```
:::{.text-muted}
Текст певного кольору.
:::
```

<details class="more">
<summary>Додаткове кольорове забарвлення</summary>

```{block, type = 'text-muted'}
Кольорове виділення за допомогою класу text-muted
```
```{block, type = 'text-primary'}
Кольорове виділення за допомогою класу text-primary
```
```{block, type = 'text-success'}
Кольорове виділення за допомогою класу text-success
```
```{block, type = 'text-info'}
Кольорове виділення за допомогою класу text-text-info
```
```{block, type = 'text-warning'}
Кольорове виділення за допомогою класу text-warning
```
```{block, type = 'text-danger'}
Кольорове виділення за допомогою класу text-danger
```
```{block, type = 'text-aqua'}
Кольорове виділення за допомогою класу text-aqua
```
```{block, type = 'text-black'}
Кольорове виділення за допомогою класу text-black
```
```{block, type = 'text-blue'}
Кольорове виділення за допомогою класу text-blue
```
```{block, type = 'text-fuchsia'}
Кольорове виділення за допомогою класу text-fuchsia
```
```{block, type = 'text-gray'}
Кольорове виділення за допомогою класу text-gray
```
```{block, type = 'text-green'}
Кольорове виділення за допомогою класу text-green
```
```{block, type = 'text-lime'}
Кольорове виділення за допомогою класу text-lime
```
```{block, type = 'text-maroon'}
Кольорове виділення за допомогою класу text-maroon
```
```{block, type = 'text-navy'}
Кольорове виділення за допомогою класу text-navy
```
```{block, type = 'text-olive'}
Кольорове виділення за допомогою класу text-olive
```
```{block, type = 'text-purple'}
Кольорове виділення за допомогою класу text-purple
```
```{block, type = 'text-red'}
Кольорове виділення за допомогою класу text-red
```
```{block, type = 'text-silver'}
Кольорове виділення за допомогою класу text-silver
```
```{block, type = 'text-teal'}
Кольорове виділення за допомогою класу text-teal
```
```{block, type = 'text-white bg-silver'}
Кольорове виділення за допомогою класу text-white
```
```{block, type = 'text-yellow'}
Кольорове виділення за допомогою класу text-yellow
```

</details>

### Колір фону блоку {#block-bg-color}

:::{.bg-silver}
Кольорове виділення за допомогою класу bg-silver
:::

```
:::{.bg-silver}
Кольорове виділення за допомогою класу bg-silver
:::
```

<details class="more">
<summary>Додаткове кольорове забарвлення</summary>

```{block, type = 'bg-primary'}
Кольорове виділення фону за допомогою класу bg-primary
```
```{block, type = 'bg-success'}
Кольорове виділення фону за допомогою класу bg-success
```
```{block, type = 'bg-info'}
Кольорове виділення фону за допомогою класу bg-info
```
```{block, type = 'bg-warning'}
Кольорове виділення фону за допомогою класу bg-warning
```
```{block, type = 'bg-danger'}
Кольорове виділення фону за допомогою класу bg-danger
```
```{block, type = 'bg-aqua'}
Кольорове виділення фону за допомогою класу bg-aqua
```
```{block, type = 'bg-black'}
Кольорове виділення фону за допомогою класу bg-black
```
```{block, type = 'bg-blue'}
Кольорове виділення фону за допомогою класу bg-blue
```
```{block, type = 'bg-fuchsia'}
Кольорове виділення фону за допомогою класу bg-fuchsia
```
```{block, type = 'bg-gray'}
Кольорове виділення фону за допомогою класу bg-gray
```
```{block, type = 'bg-green'}
Кольорове виділення фону за допомогою класу bg-green
```
```{block, type = 'bg-lime'}
Кольорове виділення фону за допомогою класу bg-lime
```
```{block, type = 'bg-maroon'}
Кольорове виділення фону за допомогою класу bg-maroon
```
```{block, type = 'bg-navy'}
Кольорове виділення фону за допомогою класу bg-navy
```
```{block, type = 'bg-olive'}
Кольорове виділення фону за допомогою класу bg-olive
```
```{block, type = 'bg-purple'}
Кольорове виділення фону за допомогою класу bg-purple
```
```{block, type = 'bg-red'}
Кольорове виділення фону за допомогою класу bg-red
```
```{block, type = 'bg-silver'}
Кольорове виділення фону за допомогою класу bg-silver
```
```{block, type = 'bg-teal'}
Кольорове виділення фону за допомогою класу bg-teal
```
```{block, type = 'bg-white '}
Кольорове виділення фону за допомогою класу bg-white
```
```{block, type = 'bg-yellow'}
Кольорове виділення фону за допомогою класу bg-yellow
```

</details>

### Сповіщення {#alert}

:::{.alert .alert-success}
**Успішно!** Сповіщення про успішну чи позитивну дію.
:::

:::{.alert .alert-info}
**Інформація!** Сповіщення про додаткову інформацію чи дію.
:::

:::{.alert .alert-warning}
**Попередження!** Сповіщення про попередження, яке може потребувати вашої уваги.
:::

:::{.alert .alert-danger}
**Увага!** Сповіщення про небезпечну чи потенційно негативну дію.
:::

```
:::{.alert .alert-success}
**Успішно!** Сповіщення про успішну чи позитивну дію.
:::

:::{.alert .alert-info}
**Інформація!** Сповіщення про додаткову інформацію чи дію.
:::

:::{.alert .alert-warning}
**Попередження!** Сповіщення про попередження, яке може потребувати вашої уваги.
:::

:::{.alert .alert-danger}
**Увага!** Сповіщення про небезпечну чи потенційно негативну дію.
:::
```

### Комбінування використання кастомних класів {#comd-custom-class}

:::{.tr .text-primary .bg-yellow}
Вирівнювання по правому краю та голубий колір тексту на жовтому фоні
:::

```
:::{.tr .text-primary .bg-yellow}
Вирівнювання по правому краю та голубий колір тексту на жовтому фоні
:::
```

### Вкладки {#tabs}

:::{.tab-list}
1. Вкладка 1
2. Вкладка 2
3. Вкладка 3
4.  
    * Lorem ipsum dolor sit amet, consectetur adipisicing elit. Harum dolore, sequi ex quam sunt delectus veniam aut tempore illum, dolor nemo quae nulla nam perferendis enim quisquam, culpa. Amet corporis explicabo soluta magni similique alias earum porro et enim itaque. Quidem cupiditate aspernatur doloremque rerum quo facere sint ratione labore.
    ![Рис. 1. Логотип Moodle](https://moodle.org/logo/moodle-logo.png "Лого"){width=70%}
    * <iframe src="https://h5p.org/h5p/embed/707" width="688" height="448" frameborder="0" allowfullscreen="allowfullscreen">Завантаження...</iframe>
    * ![Рис. 1. Логотип Moodle](https://moodle.org/logo/moodle-logo.png "Лого"){width=70%}
:::

```
:::{.tab-list}
1. Вкладка 1
2. Вкладка 2
3. Вкладка 3
4.  
    * Контент для 1 вкладки
    * Контент для 2 вкладки
    * Конетнт для 3 вкладки
:::
```

### Анімація блоків {#animate-css}

Для того, щоб добавити анімацію не блочного елементу (зображенню, абзацу, заголовку і т.д.) потрібно добавити відповідний "клас" до нього. Умовно він складається з двох частин `anim_` - є обов'язковим, та власне назвою потрібної вам анімації. Наприклад `anim_bounce`, де `fadeIn` є назвою анімації. Елемент, що має такий клас при прогортанні сторіки матиме таку анімацію:

:::{.alert .alert-success .anim_fadeInUp}
**Успішно!** Сповіщення про успішну чи позитивну дію.
:::

```
:::{.alert .alert-success .anim_fadeIn}
**Успішно!** Сповіщення про успішну чи позитивну дію.
:::
```

Для того, щоб анімація програвалась постійно, Ви можете добавити клас `infinite`

:::{.alert .alert-success .infinite .anim_fadeIn}
**Успішно!** Сповіщення про успішну чи позитивну дію.
:::

```
:::{.alert .alert-success .infinite .anim_fadeIn'}
**Успішно!** Сповіщення про успішну чи позитивну дію.
:::
```

Приклади анімації та назви відповідних класів ми зможете знайти за [посиланням](https://daneden.github.io/animate.css/)  

## Лістинг програми {#listing}

Лістинг програми можуть бути не тільки виведені з підсвіткою синтаксису, але і виконані з відобраденням результату. Виконання можливе тільки для програм на наступних мовах прорамування: r, python, C++, SQL.

### З підсвіткою синтаксису та відображенням результату виконання  (eval=TRUE, echo=TRUE) {#listing-color-eval-echo}

```{r, eval=TRUE, echo=TRUE}
a = 5
b = 2
print(a+b)
```

---

    `r ''````{r, eval=TRUE, echo=TRUE}
    a = 5
    b = 2
    print(a+b)
    ```

### З відображенням тільки результату {#listing-eval}

```{r, echo=FALSE, eval=TRUE}
a = 5
b = 2
print(a+b)
```

---

    `r ''````{r, echo=FALSE, eval=TRUE}
    a = 5
    b = 2
    print(a+b)
    ```

### Без виконання {#listing-none}

```{r, eval=FALSE}
a = 5
b = 2
print(a+b)
```

---

    `r ''````{r, eval=FALSE}
    a = 5
    b = 2
    print(a+b)
    ```

## Визначення та приклади {#def-exam}

### Визначення {#definitions}

Moodle
:   це система управління курсами (електронним навчанням), також відома як система управління навчанням або віртуалье навчальне середовище (англ.). Являє собою абревіатуру від англ. Modular Object-Oriented Dynamic Learning Environment (модульне об'єктно-орієнтоване динамічне навчальне середовище).

```
Moodle
:   це система управління курсами (електронного навчання), також відома як система управління навчання або віртуалье навчальне середовище (англ.). Являє собою абревіатуру від англ. Modular Object-Oriented Dynamic Learning Environment (модульне об'єктно-орієнтоване динамічне навчальне середовище).
```

### Горизонтальне визначення {#def-hor}

:::{.dl-horizontal}
Moodle
:   це система управління курсами (електронного навчання), також відома як система управління навчання або віртуалье навчальне середовище (англ.). Являє собою абревіатуру від англ. Modular Object-Oriented Dynamic Learning Environment (модульне об'єктно-орієнтоване динамічне навчальне середовище).
:::

```
:::{.dl-horizontal}
Moodle
:   це система управління курсами (електронного навчання), також відома як система управління навчання або віртуалье навчальне середовище (англ.). Являє собою абревіатуру від англ. Modular Object-Oriented Dynamic Learning Environment (модульне об'єктно-орієнтоване динамічне навчальне середовище).
:::
```

### Автоматична нумерація прикладів {#autonumb-exm}

(@)  Приклад один (1).
(@)  Приклад два (2).
(@)  Приклад три (3).

```
(@)  Приклад один (1).
(@)  Приклад два (2).
(@)  Приклад три (3).

```

## Поділ сторінки суцільною лінією {#hr}

---

```
---
```