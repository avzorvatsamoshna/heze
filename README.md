# OSINT PROJECT. DOCUMENTATION FOR DEVELOPERS. 3301





## Работа с БД. Создание ревизии. Обновление бд. Создание миграции.
В данном разделе будет показано как правильно создавать ревизию, обновлять бд, а также создание миграции.

В проекте уже есть созданая миграция, так что вот что нужно сделать в стандартном случае. 

1. В файлах database.py а также alembic.ini есть строки примерно такого содержания:
lf   ![img](templates/без имени.png)         
   их надо заменить в таком порядке:"postgresql+asyncpg://имя_админа_бд:пароль@хост./имя бд". Но в alembic.ini  надо писать без asyncpg.

2. после этого, рекомендуеться удалить файлы в папке migrations/versions, так как это помешает созданию новой ревизии.

3. прописать "alembic revision --autogenerate "имя_ревизии " ".         
  ![img2](templates/1.png)  

4. проверить правильность файла, который создался в выше указаной папке. В первый раз файл должен содержать все строки, которые указаны в файле database.py.
    ![img3](templates/2.png)  
5. после всего выше описаного, надо прописать "alembic upgrade head". Это обновит БД до последней версии ревизии.
    
И если вы сделали все правильно, то ваша БД заработает, и будет отвечать на попытку регистрации, авторизации и т.д.
    ![img4](templates/3.png)  