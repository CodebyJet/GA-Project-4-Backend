from django.db import models


class Description(models.Model):
    text = models.TextField(max_length=500)
    owner = models.ForeignKey(
        "jwt_auth.User", related_name="descriptions", on_delete=models.CASCADE)
    def __str__(self):
        return f" {self.owner} - {self.text} "
