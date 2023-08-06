# Мультимедіа та інтерактив {#multimedia}

<audio id="chapter-audio" controls preload="metadata" src="content/audio/narration.mp3"></audio>

## Аудіосупроводження розділу книги {#audio-page}

Щоб додати аудіосупроводження до окремого (під)розділу книги потрібно у вихідному rmd-файлі після першого заголовку 1-го або 2-го рівня додати наступний тег '<audio>' з посиланням на файл аудіосупроводження між пустими рядками:

```html
<audio id="chapter-audio" controls preload="metadata" src="content/audio/lesson.mp3"></audio>
```

## Аудіо {#audio}

<audio controls="1" controlsList="nodownload">
<source src="content/audio/gimn_ua.mp3" data-external="1" type="audio/mpeg">
</source>
</audio>

```html
<audio controls="1" controlsList="nodownload">
<source src="content/audio/gimn_ua.mp3" data-external="1" type="audio/mpeg">
</source>
</audio>
```

## Відео {#video}

### Локальний файл {#local-video}

<video src="content/video/flag.mp4" width="100%" controls="controls" poster="content/img/plenka.png">
Елемент video не підтримується вашим браузером 
<a href="content/video/flag.mp4">Скачайте відео</a>
</video>

```html
<video src="content/video/flag.mp4" width="100%" controls="controls" poster="content/img/plenka.png">
Елемент video не підтримується вашим браузером 
<a href="content/video/flag.mp4">Скачайте відео</a>
</video>
```

### Із сервису YouTube {#youtube-video}

<iframe width="100%" src="https://www.youtube.com/embed/wop3FMhoLGs" frameborder="0" allowfullscreen style="min-height:315px;"></iframe>

```html
<iframe width="100%" src="https://www.youtube.com/embed/.." frameborder="0" allowfullscreen style="min-height:315px;"></iframe>
```

## Інтерактивні завдання

<iframe src="https://h5p.org/h5p/embed/707" width="688" height="448" frameborder="0" allowfullscreen="allowfullscreen">Завантаження...</iframe>

    `r ''`<iframe src="https://h5p.org/h5p/embed/707" width="688" height="412" frameborder="0" allowfullscreen="allowfullscreen">Завантаження...</iframe>
    