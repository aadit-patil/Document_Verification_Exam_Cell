from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    
    path('payment/',views.payment,name="payment"),
    path('upload/',views.upload,name="upload"),
    path('uploaded/<str:id>',views.uploaded,name="uploaded"),
    # path('pendingusers/', views.pendingusers, name="pendingusers"),
    path('form/',views.InsertRecord, name="form"),
    path('login/',views.login,name="login"),
    path('login/dashboard/',views.dashboard,name="dashboard"),
    path('login/dashboard/viewDocs/<str:id>',views.viewDocs,name="viewDocs"),
    path('login/dashboard/viewDocs/verify/<str:id>',views.verify,name="verify"),

    #url(r'^simpleemail/(?P<emailto>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/','sendSimpleEmail' , name = 'sendSimpleEmail'),
    #  path('admin/', admin.site.urls),  
    # path('emp', views.emp),  
    # path('show',views.show),  
    # path('edit/<int:id>', views.edit),  
    # path('update/<int:id>', views.update),  
    # path('delete/<int:id>', views.destroy),
    
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    

    