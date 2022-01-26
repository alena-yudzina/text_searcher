# Текстовый поисковик

Проект предназначен для поиска по текстам документов.

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

Для наполнения базы данными из файла `posts.csv` выполните команду:
```
python3 load_data.py
```

Для запуска `ElasticSearch` выполните команды:
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.16.3
```
```
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.3
```

Далее в отдельном окне терминала выполните команду для создания поискового индекса:
```
python3 elastic.py
```

Для запуска приложения выполните команду:
```
python3 app.py
```