# Особливі блоки {#special-block}

## Стан блока {#state-block}

Особливий блок може бути в двох станах - відкритий та закритий (по замовчуванню). Щоб блок був відкритим (розгорнутим) необхідно добавити атрибут `open` відкриваючому тегу `details` особливого блока (див. приклади далі).

## Лістинг {#listing-block}

<details open>
<summary>Лістинг</summary>

```cs
using System;
using System.Data;
using System.Text;
using System.Windows.Forms;
using System.Data.OleDb;
print 2+2;
```

<button title="Копіювати у буфер обміну" class="btn btn-default btn-r" data-clipboard-text="
using System;
using System.Data;
using System.Text;
using System.Windows.Forms;
using System.Data.OleDb;
print 2+2;"> <span class="glyphicon glyphicon-file" aria-hidden="true"></span>
</button>
</details>

    `r ''`<details open>
    <summary>Лістинг</summary>
     
    ```cs
    using System;
    using System.Data;
    using System.Text;
    using System.Windows.Forms;
    using System.Data.OleDb;
    print 2+2;
    ```
     
    <button title="Копіювати у буфер обміну" class="btn btn-default btn-r" data-clipboard-text="
    using System;
    using System.Data;
    using System.Text;
    using System.Windows.Forms;
    using System.Data.OleDb;
    print 2+2;"> 
    <span class="glyphicon glyphicon-file" aria-hidden="true"></span>
    </button>
    </details>

Для реалізації кнопки копіювання в буфер обміну лістинга, значення атрибута `data-clipboard-text` повинно містити  в подвійних лапках той самий текст програми, що і лістинг (див. приклад вище починаючи з рядку `using System;` та закінчуючи `print 2+2;`)

## Додаткова інформація {#add-info-block}

<details class="more">
<summary>Додаткова інформація</summary>

Блок з додатковою інформацією

</details>

```html
<details class="more">
<summary>Додаткова інформація</summary>

Блок з додатковою інформацією

</details>
```

## Цікаво знати {#intresting-block}

<details class="idea">
<summary>Цікаво знати</summary>

Блок з цікавою інформаією

</details>

```html
<details class="idea">
<summary>Цікаво знати</summary>

Блок з цікавою інформаією

</details>
```

## Визначення {#definition-block}

<details class="def" open>
<summary>Визначення</summary>

Текст визначення

</details>

```html
<details class="def" open>
<summary>Визначення</summary>

Текст визначення

</details>
```

## Приклад {#example-block}

<details class="example">
<summary>Приклад</summary>

Текст приклада

</details>

```html
<details class="example">
<summary>Приклад</summary>

Текст приклада

</details>
```

## Відео {#video-block}

<details class="video">
<summary>Відео</summary>

<video src="content/video/flag.mp4" width="100%" controls="controls" poster="content/img/plenka.png">
Елемент video не підтримується вашим браузером 
<a href="content/video/flag.mp4">Скачайте відео</a>
</video>

</details>

```html
<details class="video">
<summary>Відео</summary>

<video src="content/video/flag.mp4" width="100%" controls="controls" poster="content/img/plenka.png">
Елемент video не підтримується вашим браузером 
<a href="content/video/flag.mp4">Скачайте відео</a>
</video>

</details>
```

---

<details class="video">
<summary>Відео з YouTube</summary>

<iframe width="100%" src="https://www.youtube.com/embed/q5FRNY1ZW1g" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen style="min-height:315px;"></iframe>

</details>

```html
<details class="video">
<summary>Відео з YouTube</summary>

<iframe width="100%" src="https://www.youtube.com/embed/.." frameborder="0" allow="autoplay; encrypted-media" allowfullscreen style="min-height:315px;"></iframe>

</details>
```

## Аудіо {#audio-block}

<details class="audio">
<summary>Аудіо</summary>

<audio controls="1">
  <source src="content/audio/gimn_ua.mp3"
          data-external="1" type="audio/mpeg">
  </source>
</audio>

</details>

```html
<details class="audio">
<summary>Аудіо</summary>

<audio controls="1">
  <source src="content/audio/gimn_ua.mp3"
          data-external="1" type="audio/mpeg">
  </source>
</audio>

</details>
```

## Тренувальна вправа {#training-block}

<details class="exercise">
<summary>Тренувальна вправа (Adobe Captivate)</summary>

<iframe src="./content/interact/oprint1/index.html" frameborder="0" allowfullscreen="allowfullscreen" class="responsive-iframe">Завантаження...</iframe>

</details>

```html
<details class="exercise">
<summary>Тренувальна вправа (Adobe Captivate)</summary>

<iframe src="./content/interact/oprint1/index.html" frameborder="0" allowfullscreen="allowfullscreen" class="responsive-iframe">Завантаження...</iframe>

</details>
```

---

<details class="exercise">
<summary>Тренувальна вправа (H5P)</summary>

<iframe src="https://h5p.org/h5p/embed/707" frameborder="0" allowfullscreen="allowfullscreen"></iframe>

</details>

```html
<details class="exercise">
<summary>Тренувальна вправа (H5P)</summary>

<iframe src="https://h5p.org/h5p/embed/707" frameborder="0" allowfullscreen="allowfullscreen"></iframe>

</details>
```

---

<details class="exercise">
<summary>Тести (Google Forms)</summary>

<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSdxSJe89lBk7oNCZ001EsZUWlxXumIfW7DFwJWBCRUWMz2T0g/viewform?embedded=true" width="100%" style="min-height: 450px;" frameborder="0" marginheight="0" marginwidth="0">Загрузка...</iframe>

</details>

```html
<details class="exercise">
<summary>Тести (Google Forms)</summary>

<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSdxSJe89lBk7oNCZ001EsZUWlxXumIfW7DFwJWBCRUWMz2T0g/viewform?embedded=true" width="100%" style="min-height: 450px;" frameborder="0" marginheight="0" marginwidth="0">Загрузка...</iframe>

</details>
```
## Зображення {#image-block}

<details class="image">
<summary>Зображення</summary>

![](content/img/plenka.png "Підказка"){width=100%}

</details>

```html
<details class="image">
<summary>Зображення</summary>

![](content/img/plenka.png "Підказка"){width=100%}

</details>
```

-----

<details class="image">
<summary>Схема draw.io</summary>
<iframe frameborder="0" style="width:100%;height:843px;" src="https://www.draw.io/?lightbox=1&highlight=0000ff&nav=1&title=%D0%94%D1%96%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%B0%20%D0%B1%D0%B5%D0%B7%20%D0%BD%D0%B0%D0%B7%D0%B2%D0%B8.xml#R7VzZdts4Ev0aPbYPF1GyH2M76e5zMn16xpnJM0RCEjokQWOxlfn6QRXAFZCXjmXZE%2BkhEkAQKNS9uCwUEc%2FSq2r3qyDN9h%2B8oOUsiYrdLL2eJUmcxpH5gprvtuY8urAVG8EK16ivuGH%2Fpa7S3bfRrKBy1FBxXirWjCtzXtc0V6M6IgS%2FHzdb83I8akM21Ku4yUnp135lhdq62jiK%2Bgu%2FUbbZuqHPM3dhRfJvG8F17cabJekaP%2FZyRdq%2BXHu5JQW%2FH1SlH2fpleBc2V%2FV7oqW4NvWbfa%2BT3uudnYLWqun3LCMkkW2jC%2ByeZEvsiT6xfVwR0pN2ymgoep76xypBP%2FW%2BSWepZfdLCJTKIjc0sIVSMk2tfmdG3uoMBVbVZX9XQ10We02wKKziuffdHNmMFWE1VTIsxUgScVXVmP3l8IxBXpes7K84iUXaFTrZdMrWje4ssCPuVKZXr%2FQnfXLFXRHcy0ku6P%2ForLvGNHrJlCSFS0vO1TbfmteUzDC2PqJVKwEnv%2BHioLUxFU7U%2BPElQcWRfgx9T5arfupUHQ3qHLo%2FUp5RZX4bpq4q6kjkltoLa%2FuB6yNWnJuh4xtWxK3VDZd1z1dzA%2FHmCeyJ%2FHY8yestCSKj8giUudbcP0IlqUPS0eUdriSrlUQpb2r5smwLcawxYkPWxxALVkcALTUA22rFAjtB%2Bgz%2BXR%2Ff39W0DXRpTJurd4CkiMheDuoxpPVuPBXYxJajAeBde7B%2BpWuJFOwHP8gFfVwVKiNQ0QazmqFNmWXs%2BzadyK4hpnH5gdXrXgDQDYkZ%2FXmCxSujR0jjNLoYd18mk7%2BOFYTqOK5j1U6D2CVHUI3Fx5WNyasYbwOSufrABVnbwOobP44UvEygFR6CKSWPlIc1lLkFBIiVYAHAlaIPBl2J20b8DeF2MMYZSLEZEEqgKFeyQadtyiVRcXgvtjgbzB5azCC4JEL7AT6VVuKBSb7C3Zc24eZ17CbY1EoeT6F7rdGom7QUen1vXkQvBatlgGxDgnA%2FBC0On9AAPwI%2FOcWgG5hH0UALk4C8P8pAMFo7dUEoI32TyFAAKrz6C2FALGfIzlJwLuUAI9XR40B2iTASAKIyLen1f%2BGnv%2Bxv6%2Feg9KB8yJrLip5JnHsS74LpT4v8DNJfT4pdZq0uJ7neGlfUmWafJmwzvHrM5au09nzsquvQqbQUz95NTJlHpk8GrUr9zP46k8uGQYF6fWKK8Wrv82qPYIQ4myIfRUR8FUyRGo%2F856VTd%2FDyxfPsv8AjRxtujdcjybaD5Jnj%2F2E0RemynCm%2Fed6WiTj9Z0e92Hhp4s%2Bm0CtgnsaqeG7QL8YwBgEjMSMaYPDnNfSbACo0nCVFKxhkuU2CqQlc62kWVrQB1QyLSteYBBYNdgnq3NWsELX0LWGf8wCtIEiDGPHhlJFNgYoM0zJbjU5M7%2F%2BDddpzSocHJowW7gzlaSyo99qjD1rbta%2FhkZ0R0XOFHH7Fl2WpMp5O65tbKbRWoPDsQZvhH8Izrsys%2BCtB4w5Cuy5tkMRjflrJjTa3TqPwWiCNoJuqZEbgb7Eyjte6sYYRNF09FtEpYRibuSmhwCdoiFc1xtGoFkN5lt%2BmgotwIyPu5w2imqLGPqV5zmhOd6R64YVRNm70QON4KwAdlu0LBJoWK7LhlgfQifrtQGX4B5CUmHbVby0BhPreoYulh2OujImGSUAMUovb5AK6NeGCtlAfwqdBgoMY1Q1FplEb9RmTlCkQgwI2PkLgc9zLUmt2MBN1a2maIAu2iswNcUVsCKy5DaPDNGxhBJ7i2G8nTCBEllBVVlydIhhlbIY3AF6znAkqWmPjIE4x2wLctxTrahxMzZn9rtguSK9i%2BmuKY2ArTiA9geteM9mMKOaztSgQPo62a9HaWYCnhKWfODGwl7BApBltBRdR467xhi8E9YX61yIU%2BOyA1%2FgeqFTm6ADuFxTmTPTk52K9aVZ34K7FWgcVLXEuOo6dWgNlMaZ9iTBueo0J2f9yvGmaUle66q1gWm7GS3gLqtDZOaE6IkyVLXCQCrHFkHGzNyvT4jhPoFCAwcChc5BicLZi8YplNRm0g3r7GRctv354mVVbzYSLzYbiJfxZvrJVPyzFzAroyUKDgJkxWyqXxZHFAtKZg9KmXNWzbastMJh2MBwYQwNwTnYkVvtm5LFWtRp4K3m42UxFUWcXDjgGIcL2QMBXmi%2FPwhXJsHJg8mF32h5RyF2mQznQsxxoOoqxzFqF07HR9mgTOOXQEoiC8UvB8pJ%2BC8mLrXZd4Szkgfe8a5wZOm%2BQ9uO0b40FHGON8K2oxs3AXdsK3igoG0zPXnkiBAi8LF3usuLCZMCO9344tUiYf%2B9SUckf897ItIbJtI8yo5IpFYfT9n3955993iVHTP7nvhvdU6puPeQisvOj5qKa2ny%2FniDBZbLM8mqpqS%2F5%2BFHYceffZw46oHpFzi0mY1UaBHI7CZRkE2HoFPqy1Cb2fV59ZNlds%2BjR5F6vdRu6q%2F7Fqj0Jwdq%2BbaA8s%2B3tzFawe5GOC1uNfzHm0uA6xeHxwfT4i8tFVt%2F7xv0UZ0fML54NOpFkgcMUrtqdM249sW8tRU9Xm0byCsN73hpVE6Q%2Fx3In9X4BOs7h%2FUE4AlA8DFGIAEHT4KaR7L2e7Lqj%2B8RvB1IF6z4W5sD7VO9XVc4GnuV4Clw1rU7tDQMnrqI6mWjp8Bxt1O67T2m25LlhFiBdNs8FJUfJN2W%2BieYTidjTidjXvRkDArDSnTRwOmATO%2Fp4QGZqSqfXuf%2FwJ9jGIvsMvCubB56VxYn2bNV1hT7vxSC1wZ%2FjiX9%2BD8%3D"></iframe>
</details>

```html
<details class="image">
<summary>Схема draw.io</summary>
<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="..."></div>
</details>
```

:::{.alert .alert-info}
**Зверніть увагу!** Для коректного відображення діаграм, між ними не повинно бути пустих рядків. 
:::

**Інструкції експорту діаграм з редактору draw.io в особливий блок**

 #. Після створення діаграми уменю перейти: `Файл(File)` > `Вставити(Embed)` > `Iframe...`
 #. У вспливаючому вікні прибрати галку навпроти пункту `Редагуати` та натиснути `Створити`
 #. Вставити скопійований код у потрібне місце в електронному видані

## Динамічна схема {#dinamic-scheme-block}

<details class="diagram">
<summary>Динамічна схема</summary>

Код для вбудови динамічної схеми (як для тренувальної вправи)

</details>

```html
<details class="diagram">
<summary>Динамічна схема</summary>

Код для вбудови динамічної схеми (як для тренувальної вправи)

</details>
```
