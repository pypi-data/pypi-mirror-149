# Формули {#formula}

Довідкова інформація стосовно синатксису LaTeX доступна за [посиланням](http://fkn.ktu10.com/?q=node/2906)

## В тексті абзаца {#section-form}
Формула: $f(k) = {n \choose k} p^{k} (1-p)^{n-k}$

```
Формула: $f(k) = {n \choose k} p^{k} (1-p)^{n-k}$
```

## Окремий блок {#block-form}

$$\begin{array}{ccc}
x_{11} & x_{12} & x_{13}\\
x_{21} & x_{22} & x_{23}
\end{array}$$

```
$$\begin{array}{ccc}
x_{11} & x_{12} & x_{13}\\
x_{21} & x_{22} & x_{23}
\end{array}$$
```

## Автоматична нумерація {#autonumb-form}

Блок з автоматичною нумерацією за допомоги `\begin{equation}` та `\end{equation}`. Формулі необхідно надати унікальний ідентифікатор, в прикладі нижче це `binom`.

Дивись формулу \@ref(eq:binom).  

\begin{equation} 
  f\left(k\right) = \binom{n}{k} p^k\left(1-p\right)^{n-k}
  (\#eq:binom)
\end{equation}

```
Дивись формулу \@ref(eq:binom)

\begin{equation} 
  f\left(k\right) = \binom{n}{k} p^k\left(1-p\right)^{n-k}
  (\#eq:binom)
\end{equation}
```

## Формула без номера {#nonumb-form}

\begin{equation*} 
\frac{d}{dx}\left( \int_{a}^{x} f(u)\,du\right)=f(x)
\end{equation*} 

```
\begin{equation*} 
\frac{d}{dx}\left( \int_{a}^{x} f(u)\,du\right)=f(x)
\end{equation*} 
```
