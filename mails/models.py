from django.db import models

# Create your models here.


class Mail(models.Model):
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        "jwt_auth.User", related_name="mail_owner", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        "jwt_auth.User", related_name="mail_reciever", on_delete=models.CASCADE)
    def __str__(self):
        return f" {self.owner} - {self.text} "
