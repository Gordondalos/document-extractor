Для корректной работы в корне проекта положите

.env

с таким содержимым

    API_KEY="Ваш Апи ключ от гемини в консоли гугла


можно через докер


соберите

        docker build -t my-flask-app .

запустите

        docker run -d -p 5000:5000 my-flask-app

и заходим на http://localhost:5000

Для остановки 

        docker ps
        docker stop ИМЯ_КОНТЕЙНЕРА

Почистить от мусора докера не забываем

        docker container prune -f



или на прямую
Установите genai апи

pip install -U google-generativeai

Остальные зависимости, обычно входят в дефолтную библиотеку или легко гуглятся и ставятся

все что нужно указано в файле requirments.txt