# Создаем корневую папку проекта и переходим в нее
#mkdir fire_detection_api && cd fire_detection_api

# Создаем основную структуру папок
mkdir -p app/api/v1/endpoints app/core app/db app/schemas app/services app/tests

# Создаем пустые файлы, чтобы Python считал папки модулями
touch app/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/endpoints/__init__.py
touch app/core/__init__.py
touch app/db/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/tests/__init__.py

# Создаем основные файлы, с которыми будем работать
touch main.py
touch app/api/v1/api.py
touch app/core/config.py
touch requirements.txt
touch .gitignore