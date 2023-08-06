import threading
import time
# from django_moo import moost

def delay_conduct():
    time.sleep(1)
    print("[django_moo] the url_pattern is ready...")
    from django.http import HttpRequest
    request = HttpRequest()
    
    from myapp import views as myapp_views
    for m in dir(myapp_views):
        getattr(myapp_views, m)(request)

    from study_record import views as study_record_views
    for m in dir(study_record_views):
        try:
            getattr(study_record_views, m)(request)
        except:
            pass

    from django_moo.moost import main
    
    main(__file__)

t = threading.Thread(target=delay_conduct)
t.start()