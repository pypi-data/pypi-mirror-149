import django
import os

__title__ = 'Django Moo'
__version__ = '0.0.0'
__author__ = 'Xiaomo Lee'
__doc__ = "write less, do more..."

VERSION = __version__
DIR_PATH = __file__.split("__init__.py")[0]






   





from django_moo.delay_threading import delay_conduct
from django.db.models.signals import post_init
from django.dispatch import receiver
import threading

# @receiver(post_init)
# def my_callback(sender, **kwargs):
t = threading.Thread(target=delay_conduct)
t.start()
# delay_conduct()


from django.test.signals import setting_changed
from django.dispatch import receiver

@receiver(setting_changed)
def hello(sender, *args, **kwargs):
    print('='*20)
    print(args)
    print(kwargs)


# setting_changed.send('1',2,3)





# class FileOperator:
#     def get_file_data(self, filename):
#         f= open(f'{DIR_PATH}/{filename}', 'r', encoding='utf-8')
#         content = f.read()
#         f.close()
#         return content
    
#     def write_file_data(self, filename, content):
#         f= open(f'{DIR_PATH}/{filename}', 'w', encoding='utf-8')
#         f.write(content)
#         f.close()

# fo = FileOperator() 
# content = fo.get_file_data('delay_threading.py')

# s = '''
#     from {} import views as {}_views
#     for m in dir({}_views):
#         try:
#             getattr({}_views, m)(request) 
#         except (NameError, TypeError, AttributeError):
#             pass
# ''' 
   
# ss = '' 

# apps_name = get_user_all_apps_name() 
# for app_name in apps_name:
#     ss += s.format(app_name, app_name, app_name, app_name,app_name, app_name, app_name, app_name, app_name)

# content = content.replace("#{1}#", ss) 
# fo.write_file_data("delay_threading_.py", content)

# import django_moo.delay_threading_ 