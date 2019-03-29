#Импорт необходимых модулей
import csv,sys,os

#Указываем путь до папки проекта Django в котором находится файл settings.py
project_dir ='Users\DNS\PycharmProjects\Cursovaya\mysite'

#Добавляем в переменную sys.path путь до проекта Django
sys.path.append(project_dir)

#Определяем переменную с настройками Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

#Импортируем модуль Django
import django

#Загружаем настройки Django
django.setup()

#Импортируем модель Post
from orders.models import Transaction

#Считываем CSV-файл
data = csv.reader(open("datasetid.csv"))

for row in data:
	#Пропускаем заголовки
	tr =  Transaction()
	tr.col = row
	tr.save()