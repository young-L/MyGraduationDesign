from django.db import models

# Create your models here.
class UserManage(models.Manager):
    def create(self,user,password):
        use = self.model()
        use.userName = user
        use.password = password
        return use

class Users(models.Model):
    userName = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    man = UserManage()


    class Meta:
        db_table = 'users'

