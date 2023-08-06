# Таблиці {#table}

## Проста таблиця {#simple-table}

Таблиці необхідно надати унікальний ідентифікатор, в прикладі нижче це `tab1`.

В цьому абзаці посилання на табл. \@ref(tab:tab1)

:::{.table}
Table: (\#tab:tab1) Назва таблиці

 #                          | First Name (по центру) | Last Name (по правому)
----------------------------|:----------------------:|----------------------:
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::

```
В цьому абзаці посилання на табл. \@ref(tab:tab1)

:::{.table}
Table: (\#tab:tab1) Назва таблиці
 
 #                          | First Name (по центру) | Last Name (по правому)
----------------------------|:----------------------:|----------------------:
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::
```

## Таблиця з чередуванням фону рядків {#table-striped}

Посилання на табл. \@ref(tab:tab2)

:::{.table .table-striped}
Table: (\#tab:tab2) Назва таблиці

 #                          | First Name             | Last Name
----------------------------|------------------------|-----------------------
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::

```
Посилання на табл. \@ref(tab:tab2)

:::{.table .table-striped}
Table: (\#tab:tab2) Назва таблиці
 
 #                          | First Name             | Last Name
----------------------------|------------------------|-----------------------
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::
```

## Таблиця з границями {#table-bordered}

Посилання на табл. \@ref(tab:tab3)

:::{.table .table-bordered}
Table: (\#tab:tab3) Назва таблиці

 #                          | First Name             | Last Name
----------------------------|------------------------|-----------------------
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::

```
Посилання на табл. \@ref(tab:tab3)

:::{.table .table-bordered}
Table: (\#tab:tab3) Назва таблиці
 
 #                          | First Name             | Last Name
----------------------------|------------------------|-----------------------
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::
```

## Таблиця з ефектами наведення {#table-hover}

Посилання на табл. \@ref(tab:tab4)

:::{.table .table-hover}
Table: (\#tab:tab4) Назва таблиці

 #                          | First Name             | Last Name
----------------------------|------------------------|-----------------------
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::

```
Посилання на табл. \@ref(tab:tab4)

:::{.table .table-hover}
Table: (\#tab:tab4) Назва таблиці
 
 #                          | First Name             | Last Name
----------------------------|------------------------|-----------------------
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::
```

## Таблиця стисла {#table-condensed}

Посилання на табл. \@ref(tab:tab5)

:::{.table .table-condensed}
Table: (\#tab:tab5) Назва таблиці

 #                          | First Name             | Last Name
----------------------------|------------------------|-----------------------
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::

```
Посилання на табл. \@ref(tab:tab5)

:::{.table .table-condensed}
Table: (\#tab:tab5) Назва таблиці
 
 #                          | First Name             | Last Name
----------------------------|------------------------|-----------------------
1                           |Otto                    |Mark
2                           |Thornton                |Jacob 
3                           |Larry                   |the Bird
:::
```
## Таблиці з прокруткою {#scroll-table}

В цьому абзаці посилання на табл. \@ref(tab:tab20)

:::{.table}
Table: (\#tab:tab20) Назва таблиці

 #                          | First Name (по центру) | Last Name (по правому)|Column1|Column2|Column3|Column4|Column5|  
----------------------------|:----------------------:|----------------------:|-------|-------|-------|-------|-------| 
1                           |Otto                    |Mark                   |1      |1      |1      |1      |1      | 
2                           |Thornton                |Jacob                  |2      |1      |1      | 1      |1      |
3                           |Larry                   |the Bird               |3      |1      |1      | 1      |1      |
:::

<details>
<summary>Проста таблиця у блоці</summary>
В цьому абзаці посилання на табл. \@ref(tab:tab21)

:::{.table}
Table: (\#tab:tab21) Назва таблиці

 #                          | First Name (по центру) | Last Name (по правому)|Column1|Column2|Column3|Column4|Column5|  
----------------------------|:----------------------:|----------------------:|-------|-------|-------|-------|-------| 
1                           |Otto                    |Mark                   |1      |1      |1      |1      |1      | 
2                           |Thornton                |Jacob                  |2      |1      |1      | 1      |1      |
3                           |Larry                   |the Bird               |3      |1      |1      | 1      |1      |
:::
</details>

<details>
<summary>Таблиця з чередуванням</summary>

:::{.table .table-striped}
Table: (\#tab:tab22) Назва таблиці

 #                          | First Name (по центру) | Last Name (по правому)|Column1|Column2|Column3|Column4|Column5|  
----------------------------|:----------------------:|----------------------:|-------|-------|-------|-------|-------| 
1                           |Otto                    |Mark                   |1      |1      |1      |1      |1      | 
2                           |Thornton                |Jacob                  |2      |1      |1      | 1      |1      |
3                           |Larry                   |the Bird               |3      |1      |1      | 1      |1      |
:::
</details>

<details>
<summary>Таблиця з границями</summary>

:::{.table .table-bordered}
Table: (\#tab:tab23) Назва таблиці

 #                          | First Name (по центру) | Last Name (по правому)|Column1|Column2|Column3|Column4|Column5|  
----------------------------|:----------------------:|----------------------:|-------|-------|-------|-------|-------| 
1                           |Otto                    |Mark                   |1      |1      |1      |1      |1      | 
2                           |Thornton                |Jacob                  |2      |1      |1      | 1      |1      |
3                           |Larry                   |the Bird               |3      |1      |1      | 1      |1      |
:::
</details>

<details>
<summary>Таблиця з наведенням</summary>

:::{.table .table-hover}
Table: (\#tab:tab24) Назва таблиці

 #                          | First Name (по центру) | Last Name (по правому)|Column1|Column2|Column3|Column4|Column5|  
----------------------------|:----------------------:|----------------------:|-------|-------|-------|-------|-------| 
1                           |Otto                    |Mark                   |1      |1      |1      |1      |1      | 
2                           |Thornton                |Jacob                  |2      |1      |1      | 1      |1      |
3                           |Larry                   |the Bird               |3      |1      |1      | 1      |1      |
:::
</details>

<details>
<summary>Таблиця стисла</summary>

:::{.table .table-condensed}
Table: (\#tab:tab25) Назва таблиці

 #                          | First Name (по центру) | Last Name (по правому)|Column1|Column2|Column3|Column4|Column5|  
----------------------------|:----------------------:|----------------------:|-------|-------|-------|-------|-------| 
1                           |Otto                    |Mark                   |1      |1      |1      |1      |1      | 
2                           |Thornton                |Jacob                  |2      |1      |1      | 1      |1      |
3                           |Larry                   |the Bird               |3      |1      |1      | 1      |1      |
:::
</details>
