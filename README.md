# Vacation application service


## About

Это моё тестовое задание в profi.ru.

Проект представляет из себя веб-интерфейс подачи заявки сотрудником на отпуск.
В интерфейсе реализованы следующие возможности:

* логин/регистрация пользователя
* подача заявки на отпуск
* отмену заявки, причём отмена заявки возможна не позднее 3-х дней до начала отпуск
* проверку на то, что у сотрудника есть запрашиваемое им количество дней
* раздел статистики (доступный только для абминов), в котором будет выводятся:
	* количество дней отпуска за каждый год
	* данные по месяцам, где больше/меньше всего люди ходили в отпуск (для упрощения, я считаю, что в момент начала отпуска из его свободных дней вычитается вся длительность отпуска)


## Features

### Логин/регистрация пользователя

Когда неавторизовнный пользователь заходит на сайт, он попадает на страничку логина/регистрации. 

![Login page](/images/login.jpg)

В случае несовпадения пароля, пользователь видит предупреждение.

![warning](/images/warning.jpg)

При регистрации пользователь видит сообщение об ошибке, если первый и второй пароли не совпадают или если пользователь с таким имеьем уже существует.

### Подача заявки на отпуск

Вот так выглядит домашняя страница пользователя.

![home](/images/personal_page.jpg)

Вверху выводится, сколько свободных дней есть у пользователя в этом году, ниже -- таблица со всеми активными заявками (то есть заявками на будущее время).
Ниже находится кнопка "Apply for vacation!".

При её нажатии появляется такая форма:

![application](/images/application.jpg)

Если пользователь запросил больше дней, чем у него есть, он видит предупреждение, и заявку оставить не получается.

![another worning](/images/another_warning.jpg)

### Отмена заявки

Пользователь нажимает на кнопку revert рядом с заявкой, которую он хочет отменить.
После этого он видит модальное окно, оповещающее его, удалось ли отменить заявку (заявка не отменяется, если до отпуска менее 3 дней).

# Статистика

Так выглядит раздел статистики.

![stats](/images/demo_stats.jpg)

Вверху таблица с суммарным количеством дней по месяцам разных лет, сколько дней работники были в отпуске в этом месяце.
Тёмно-синий цвет значит месяц с максимальным количеством дней, фиолетовый — с минимальным.
Ниже можно ввести имя или юзернэйм пользователя и узнать данные о его отпусках по годам.

## Implementation

Бэк-энд написан на Python3, Flask с использованием базы данных на SQLite.

Код, обрабатывающий общение клиента с сервером, находится в файле `interface.py`, класс, отвечающий за общение с базой данных -- в `db.py`.

На стороне клиента в нескольких случаях использован JavaScript с применением jQuery (см. ./templates/home.html). Так, при отмене заявки на отпуск данные передаются на сервер с помощью $.ajax.

## Demo

[Здесь](http://maryszmary.pythonanywhere.com/).

В базе данной демо-версии существуют такие пользователи:
* username: administer, пароль 111; может просматривать статистику
* username: alexham, пароль: nonstop
* username: maryszmary, пароль: aaa
