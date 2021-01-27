from django.db  import models
import uuid
from datetime import date
# now=datetime.datetime.now()
# date=now.strftime("%y-%m-%d")
# class UserInsert(models.Model) :
#     name=models.CharField(max_length=100)
#     PRN=models.CharField( max_length=15)
#     email=models.CharField(max_length=100)
#     ID=models.DateTimeField(auto_now_add=True)
#     date_of_application=models.DateField(default=date.today)
#     ACK_NO=models.CharField(max_length=10, unique=True, default=uuid.uuid4)
#     class Meta:
#             db_table="users"