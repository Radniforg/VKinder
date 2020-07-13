**Описание приложения Vinder.**

Назначение: поиск знакомств (как романтических, так и дружеских).

Входные данные: TOKEN пользователя (получается через модуль VK_TOKEN.py, см дальше), ID пользователя.

Результат работы приложения: JSON-файл partners.json, содержащий 10 лучших совпадений по поиску знакомств.

**ПОДГОТОВКА ПЕРЕД ИСПОЛЬЗОВАНИЕМ ПРИЛОЖЕНИЯ**
- Установите postgre sql
- Создайте базу данных
- _при необходимости - создайте отдельного пользователя для базы данных_
- Внесите имя базы данных, имя пользователя и пароль в файл _settings.py_ 
в области database, username и password соответственно. 
- Пример: sql = {'database': 'Имя базы данных', 'username': 'Имя пользователя', 'password': 'Пароль'}


- В том же файле _settings.py_ введите id пользователя в графе user
- Пример: user = id098754567890098765678
- При необходимости можно изменить значимость параметров по умолчанию: для этого замените
 цифры в области standart_matrix на другие (от 0 до 9). Перевод обозначений можно прочитать в ReadMe ниже 
 или в словаре translator в том же файле.
 
 - **Не заменяйте APP_ID и не удаляйте строки в файле settings.py - без них программа перестанет работать**



**ВАЖНОЕ ПРИМЕЧАНИЕ ПО ТЕСТАМ**

Файл _test-data.py_ содержит ID друзей автора программы. 
Их профили могут быть закрыты для сторонних пользователей.
При использовании автоматических тестов автор рекомендует
заменить ID в файле _test-data.py_ на ID профилей, доступных
тестеру.

**Описание содержащихся файлов и их функций**

**_VKinder.py_**

Основной модуль файла. Объединяет четыре модуля для работы приложения.
Не разбит на отдельные функции.

На данный момент имеет дублирующий вывод результатов в PyCharm (строка 52)

**_User_decomposition_**

Модуль, предназначенный для получения данных со страниц пользователей для дальнейшего сравнения. Содержит в себе 3 функции.

- **_user_interests(id,token)_**

Функция, разбивающия профиль (как пользователя, так и партнера) на элементы для дальнейшего сравнения

- **_user_element_weight()_**

Функция, позволяющая пользователю самостоятельно ввести значимость тех или иных параметров для поиска партнеров. 
Есть значения по умолчанию (основанные на предпочтениях автора программы). 

Функция интересуется допустимым диапозоном возраста партнера относительно возраста пользователя
 (асиммитричный ввод пока недоступен)

Функция интересуется целью пользователя (романтическое знакомство или нет)

**Д** - запрашивается предпочетаемый пол партнера, блокируются все пользователи, состоящие в тех или иных отношениях.

**Н** - пол идет по умолчанию _0_ (любой), отношения - любые.

Функция запрашивает, хочет ли пользователь изменить матрицу используемых весов.

**Д** - идет череда запросов, в которых пользователю нужно указать значимость параметров по шкале 
от 0 (_совсем не имеет значения_) до 9 (_максимальное значение_).

**Н** - используется стандартная матрица.

- **_user_comparison(user_elements, partner_elements, standart_matrix)_**

Функция сравнивает интересы пользователя и потенциального партенра, используя матрицу весов как модификатор

В самом начале функция сравнивает совместимость пользователя и партнера по отношения к алкоголю и курению,
блокируя партнеров с противоположным отношением к вредным привычкам

Далее функция высчитывает "общий вес" партнера по следующему принципу:

- _Возраст_ = (Допустимая разница в возрасте(пользовательский ввод в предыдущей функции) - 
модуль(возраст пользователя - возраст партнера) + 0.1) * значимость разницы возраста(стандарт)
- _Общие друзья_ = Количество общих друзей / (10 - значимость общих друзей)
- _Интересы (книги, музыка, фильмы)_ - при каждом совпадении +значимость данной категории
- _Базовые и персональные данные (место рождения, политические взгляды)_ - при совпадении 
+значимость данной категории данных 

В качесте результата функция выдает суммарный "вес" партнера, который суммируется в **VKinder.py**

**_VK_TOKEN.py_**

Универсальный модуль, предназначенный для проверки и корректировки доступа к данным и информации по пользователю
- token_confirmation(app_id, TOKEN='')

Функция проверяет вложенный токен и, при ошибке, выдает ссылку, позволяющую получить токен.

Формат вставки: url без https:\\

Функция возвращает token (на данном этапе - для ручной записи для текущей сессии)
- user_confirmed(user1, TOKEN)

Функция проверяет существование пользователя. При ошибке просит снова ввести id.

**_data_procession.py_**

Модуль, занимающийся поиском подходящих пользователей и обработкой данных фотографий профиля

- profile_pictures(user_id, token)

Функция, позволяющая получить три наиболее оцененные фотографии из профиля потенциального партнера
- user_search(search_queue, token, giant_id_list)

Функция поиска в ВК потенциальных пользователей. Для расширения выборки (более 1000) используется два цикла:

_Поиск по статусу отношений_ - 3 значения для романтического поиска, 8 для общения.

_Поиск по возрасту_ - от 1 значения (при 0) до большого. **Важно**: в данной версии программы минимальный
 возраст партнера - 18 лет
 
 Итого суммарно для наименьшей выборки (поиск романтических знакомств одного возраста с пользователем) рассматриваются 
 три группы максимум по 1000 человек
 
- partner_photo(potential_partner_list, token)

Собирает по три фотографии потенциальных партнеров в финальный словарь (в дальнейшем в **_VKinder_** 
переводится в итоговый json)

**_vkinder_sql.py_**

Модуль для работы с sql

- partner_add_block(conn, id_user, block_string):

Функция, добавляющая id уже показанных партнеров, чтобы не повторять результаты

- block_check(conn, user_id):

Функция получает список id уже показанных партнеров, чтобы в дальнейшем их не использовать.

- sql_result(conn, id_user, result):

Функция, записывающая id пользователя и текст json файла в SQL. 

- restart(conn):
   
Внутренняя функция очистки БД от данных (не используется в основном приложении)

**_requirements.json_**

Файл с заготовкой для выполнения простого запуска. В нём можно вручную отредактировать id пользователя
 и используемую матрицу (см. Дополнительную информацию ниже)

**Дополнительная информация**

_Базовая таблица весов_

- Значимость разницы в возрасте ('age_difference') = 2
- Предпочитаемый пол партнера ('sex_preference') = 0 - настраивается отдельно
- Значимость совпадения должностей ('activities') = 1
- Значимость совпадения вкуса в книгах ('books') = 9
- Значимость проживания в одном городе ('city') = 0
- Значимость количества общих друзей ('common_count') = 2
- Значимость обучения на одном факультете ('faculty_name') = 1
- Значимость совпадения вкуса в играх ('games') = 9
- Значимость совпадения места рождения ('home_town') = 2
- Значимость совпадения интересов ('interests') = 9
- Значимость совпадения взглядов на жизнь ('life_main') = 6
- Значимость совпадения вкуса в фильмах ('movies') = 0
- Значимость совпадения вкуса в музыке ('music') = 0
- Значимость совпадения общего места работы ('occupation') = 1
- Значимость совпадения взглядов на людские черты ('people_main') =  8
- Значимость совпадения политических взглядов ('political') = 2
- Параметр значимости отношений партнера ('relation_ban') = 0 - настраивается отдельно
- Значимость совпадения религиозных взглядов ('religion') = 3
- Значимость совпадения вкусов в сериалах и мультипликации ('tv') = 8,
- Значимость несовпадения взглядов на алкоголь ('alcohol') = 0 - не настраивается
- Значимость несовпадения взглядов на курение ('smoking') = 0 - не настраивается