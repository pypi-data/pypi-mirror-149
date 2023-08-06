# Зображення {#image}

## Рисунки без автоматичної нумерації {#noautonumb-img}

### Завантаження зображення з Інтернету {#inet-img}

![Рис. 1. Логотип Moodle](https://moodle.org/logo/moodle-logo.png "Лого"){width=70%}

```
![Рис. 1. Логотип Moodle](https://moodle.org/logo/moodle-logo.png "Лого"){width=70%}
```

Ширина задається значенням атрибуту `width` в процентах від ширини області тексту.

### Завантаження зображення з комп'ютера {#device-img}

![Рис. 2. Логотип Moodle](content/img/moodle-logo-100.png "Лого-100")

```
![Рис. 2. Логотип Moodle](content/img/moodle-logo-100.png "Лого-100")
```

## З автоматичною нумерацією та вирівнюванням {#autonumb-img}

Зображенню необхідно надати унікальний ідентифікатор, в прикладі це `ris1`.

В цьому абзаці знаходиться посилання на рис. \@ref(fig:ris1)

```{r ris1, echo=FALSE, fig.cap = 'Название рисунка.', out.width='70%', fig.align = 'center' }
knitr::include_graphics("http://lazvm-comp.ucoz.ru/_pu/0/35475892.gif")
```

---

В цьому абзаці знаходиться посилання на рис. `\@ref(fig:ris1)`

    `r ''````{r ris1, echo=FALSE, fig.cap = 'Название рисунка.', out.width='70%', fig.align = 'center' }
    knitr::include_graphics("http://lazvm-comp.ucoz.ru/_pu/0/35475892.gif")
    ```

Параметри блоку:

- fig.align - вирівнювання `left, right and center`
- fig.cap - заголовок рисунка
- out.width - ширина в % до області тексту
- out.extra - додаткові параметри та клас, приклад: out.extra='style="border:1px solid black;" class="img-rounded"'

## Обтікання рисунків {#wrapp-img}

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aliquid corporis, praesentium. Dolorum ut, placeat mollitia delectus optio sit autem voluptas alias molestiae nobis totam asperiores excepturi fugiat dignissimos tempore quibusdam debitis modi ducimus architecto, quaerat error inventore dolores rem veritatis earum? Accusantium qui, commodi. Sed earum et non iusto. Ipsam.

:::{.pull-left}
![Рис. 2. Логотип Moodle](content/img/moodle-logo-100.png "Лого-100"){width=300px}
:::

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aliquid corporis, praesentium. Dolorum ut, placeat mollitia delectus optio sit autem voluptas alias molestiae nobis totam asperiores excepturi fugiat dignissimos tempore quibusdam debitis modi ducimus architecto, quaerat error inventore dolores rem veritatis earum? Accusantium qui, commodi. Sed earum et non iusto. Ipsam.

:::{.pull-right}
![Рис. 2. Логотип Moodle](content/img/moodle-logo-100.png "Лого-100"){width=30%}
:::

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aliquid corporis, praesentium. Dolorum ut, placeat mollitia delectus optio sit autem voluptas alias molestiae nobis totam asperiores excepturi fugiat dignissimos tempore quibusdam debitis modi ducimus architecto, quaerat error inventore dolores rem veritatis earum? Accusantium qui, commodi. Sed earum et non iusto. Ipsam.

:::{.pull-left}
![](content/img/moodle-logo-100.png "Лого-100"){width=100%}
:::

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aliquid corporis, praesentium. Dolorum ut, placeat mollitia delectus optio sit autem voluptas alias molestiae nobis totam asperiores excepturi fugiat dignissimos tempore quibusdam debitis modi ducimus architecto, quaerat error inventore dolores rem veritatis earum? Accusantium qui, commodi. Sed earum et non iusto. Ipsam.

---

Обтікання ліворуч:

```
:::{.pull-left}
![Рис. 2. Логотип Moodle](content/img/moodle-logo-100.png "Лого-100"){width=300px}
:::
```

Обтікання праворуч:

```
:::{.pull-right}
![Рис. 2. Логотип Moodle](content/img/moodle-logo-100.png "Лого-100"){width=30%}
:::
```

Обтекание ліворуч без підпису зображення:

```
:::{.pull-left}
![](content/img/moodle-logo-100.png "Лого-100"){width=100%}
:::
```

## Зображения по тексту {#inline-img}

Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quis nobis optio nihil dignissimos voluptates culpa, quas quidem commodi cupiditate repellendus sint aliquam amet ducimus? Sunt repellat animi sint est laboriosam aliquam incidunt ratione ![](inc/img/close.png) temporibus, praesentium consequuntur? Assumenda labore, fugiat suscipit quae porro provident, explicabo magni libero doloribus repellat, ex magnam nostrum ullam beatae odio, numquam eos? Mollitia aliquam, accusantium illum hic earum. 

```
Зображення ![](inc/img/close.png) по тексту
```

## Емоджі

Для вставки емоджі в тексті потрібно записати його shortcode між двокрапками `:smile:`

:smile: :pencil: :book:

[EMOJI CHEAT SHEET](https://www.webpagefx.com/tools/emoji-cheat-sheet/)

## Іконки Font Awesome {#fontawesome}

### Використання іконок в тексті {#text-fontawesom}

Використання іконок можливо в любомі місці у тексті, списку або іншому місці. Для того щоб вставити необхідну Вам іконку необхідно звернутись на сайт [FontAwesome](https://fontawesome.com/v4.7.0/) та обрати із запропонованих там потрібну та вставити в тексті її назву з префіксом `fa-` як у прикладі нижче. Клас `fa` є опціональним.

```
:fa fa-quora: Lorem ipsum dolor :fa-circle-o-notch fa-spin fa-3x fa-fw: sit amet, consectetur adipisicing elit.
```

:fa fa-quora: Lorem ipsum dolor :fa-circle-o-notch fa-spin fa-3x fa-fw: sit amet, consectetur adipisicing elit.

### Додаткові можливості

Для ознайомлення з розширеними можливостями використання іконок звернітся на сайт FontAwesome у розділ [прикладів](https://fontawesome.com/v4.7.0/examples/)

#### Розмір іконок {-}

:fa fa-camera-retro fa-lg: fa-lg

:fa fa-camera-retro fa-2x: fa-2x

:fa fa-camera-retro fa-3x: fa-3x

:fa fa-camera-retro fa-4x: fa-4x

:fa fa-camera-retro fa-5x: fa-5x

---

```
:fa-camera-retro fa-lg: fa-lg
:fa-camera-retro fa-2x: fa-2x
:fa-camera-retro fa-3x: fa-3x
:fa-camera-retro fa-4x: fa-4x
:fa-camera-retro fa-5x: fa-5x
```

#### Іконки фіксованої ширини {-}

:fa-home fa-fw: Home

:fa-book fa-fw: Library

:fa-pencil fa-fw: Applications

:fa-cog fa-fw: Settings

---

```
:fa-home fa-fw: Home
:fa-book fa-fw: Library
:fa-pencil fa-fw: Applications
:fa-cog fa-fw: Settings
```

#### Обрамлення та обтікання іконок {-}

:fa fa-quote-left fa-3x fa-pull-right fa-border: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque commodo ipsum ac ligula congue, sit amet feugiat dolor ornare. Vivamus sagittis elit ac bibendum maximus. Vestibulum sem velit, condimentum scelerisque volutpat sed, tempus at lectus. Maecenas ac ultrices enim. 
:fa fa-quote-left fa-3x fa-pull-left fa-border: Donec metus quam, luctus eu nunc sit amet, gravida accumsan dui. Proin dapibus fringilla risus vitae ornare. Proin in orci lacinia, sagittis lorem imperdiet, ultrices nulla. Proin eleifend id purus non fermentum. Suspendisse ut nisl sit amet odio sagittis suscipit in non quam. Sed lacinia facilisis nibh, lobortis accumsan massa semper id. Sed pharetra lobortis congue. Pellentesque felis turpis, porta quis viverra quis, euismod quis arcu.

---

```
:fa fa-quote-left fa-3x fa-pull-right fa-border: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque commodo ipsum ac ligula congue, sit amet feugiat dolor ornare. Vivamus sagittis elit ac bibendum maximus. Vestibulum sem velit, condimentum scelerisque volutpat sed, tempus at lectus. Maecenas ac ultrices enim. 
:fa fa-quote-left fa-3x fa-pull-left fa-border: Donec metus quam, luctus eu nunc sit amet, gravida accumsan dui. Proin dapibus fringilla risus vitae ornare. Proin in orci lacinia, sagittis lorem imperdiet, ultrices nulla. Proin eleifend id purus non fermentum. Suspendisse ut nisl sit amet odio sagittis suscipit in non quam. Sed lacinia facilisis nibh, lobortis accumsan massa semper id. Sed pharetra lobortis congue. Pellentesque felis turpis, porta quis viverra quis, euismod quis arcu.
```

#### Анімація  {-}


:fa-spinner fa-spin fa-3x fa-fw:

:fa-circle-o-notch fa-spin fa-3x fa-fw:

:fa-refresh fa-spin fa-3x fa-fw:

:fa-cog fa-spin fa-3x fa-fw:

:fa-spinner fa-pulse fa-3x fa-fw:

---

```
:fa-spinner fa-spin fa-3x fa-fw:
:fa-circle-o-notch fa-spin fa-3x fa-fw:
:fa-refresh fa-spin fa-3x fa-fw:
:fa-cog fa-spin fa-3x fa-fw:
:fa-spinner fa-pulse fa-3x fa-fw:
```

#### Повернуті та віддзеркалені іконки {-}

:fa-shield:

:fa-shield fa-rotate-90:

:fa-shield fa-rotate-180:

:fa-shield fa-rotate-270:

:fa-shield fa-flip-horizontal:

:fa-shield fa-flip-vertical:

---

```
:fa-shield:
:fa-shield fa-rotate-90:
:fa-shield fa-rotate-180:
:fa-shield fa-rotate-270:
:fa-shield fa-flip-horizontal:
:fa-shield fa-flip-vertical:
```

#### Комбінування іконок {-}


[:fa-square-o fa-stack-2x: :fa-twitter fa-stack-1x:]{.fa-stack .fa-lg}

[:fa-circle fa-stack-2x: :fa-flag fa-stack-1x fa-inverse:]{.fa-stack .fa-lg}

[:fa-square fa-stack-2x: :fa-terminal fa-stack-1x fa-inverse:]{.fa-stack .fa-lg}

[:fa-camera fa-stack-1x: [:fa-ban fa-stack-2x:]{.text-danger}]{.fa-stack .fa-lg}

---

```
[:fa-square-o fa-stack-2x: :fa-twitter fa-stack-1x:]{.fa-stack .fa-lg}
[:fa-circle fa-stack-2x: :fa-flag fa-stack-1x fa-inverse:]{.fa-stack .fa-lg}
[:fa-square fa-stack-2x: :fa-terminal fa-stack-1x fa-inverse:]{.fa-stack .fa-lg}
[:fa-camera fa-stack-1x: [:fa-ban fa-stack-2x:]{.text-danger}]{.fa-stack .fa-lg}
```

### Список з маркерами іконками FontAwesome {#list-fontawesome}

- :fa-li fa fa-check-square: List icons
- :fa-li fa fa-check-square: can be used
- :fa-li fa fa-spinner fa-spin: as bullets 
- :fa-li fa fa-square: in lists

---

```
- :fa-li fa fa-check-square: List icons
- :fa-li fa fa-check-square: can be used
- :fa-li fa fa-spinner fa-spin: as bullets 
- :fa-li fa fa-square: in lists
```

## Схеми та діаграми {#drawio}

**Інструкція експорту діаграм з редактору draw.io**

 #. Після створення діаграми у меню перейти: `Файл(File)` > `Вставити(Embed)` > `HTML...`
 #. У вспливаючому вікні прибрати галку навпроти пункту `Редагувати` та натиснути `Створити`
 #. У наступному вспливаючому вікні натиснути `Скачати`
 #. Змінити назву файла накшталт `ris1-1.html` та `Скачати`
 #. Відкрити файл за допомогою текстового редактору (не Microsoft Word !!!), наприклад блокноті (Открыть с помощью...)
 #. Видалити останній рядок `<script>..</script>` та зберегти файл
 #. Скопіювати файл у папку проекту видання `content\img\drawio\`
 
Демонстрація вставки схеми, підготовленої за допомогою редактора draw.io, на рис.\ \@ref(fig:ris11) 

`r htmltools::includeHTML('./content/img/drawio/img1.html')`

```{r ris11, echo=FALSE, fig.cap = 'Рисунок draw.io', fig.align = 'center' }
knitr::include_graphics("inc/img/pix.png")
```

---

`Демонстрація вставки схеми, підготовленої за допомогою редактора draw.io, на рис.\ \@ref(fig:ris11)` 

```{r, eval=FALSE}     
`r htmltools::includeHTML('./content/img/drawio/img1.html')`
```

    `r ''````{r ris11, echo=FALSE, fig.cap = 'Рисунок draw.io', fig.align = 'center' }
    knitr::include_graphics("inc/img/pix.png")
    ```

---

`r htmltools::includeHTML('content/img/drawio/img2.html')`

```{r ris12, echo=FALSE, fig.cap = 'Рисунок draw.io', fig.align = 'center' }
knitr::include_graphics("inc/img/pix.png")
```

---

```{r, eval=FALSE}  
`r htmltools::includeHTML('content/img/drawio/img2.html')`
```

    `r ''````{r ris12, echo=FALSE, fig.cap = 'Рисунок draw.io', fig.align = 'center' }
    knitr::include_graphics("inc/img/pix.png")
    ```
