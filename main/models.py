import re
from django.db import models
from django.utils import timezone


class User(models.Model):
    UserName = models.CharField("UserName", max_length=100, default="")
    Email = models.CharField("Email", max_length=100, default="")
    FirstName = models.CharField("FirstName", max_length=100, default="")
    SecondName = models.CharField("SecondName", max_length=100, default="")
    Birthday = models.DateField("Birthday", default=timezone.now)
    RegisterDate = models.DateTimeField("RegisterDate", default=timezone.now)
    Age = models.IntegerField("Age", default=0)
    Password = models.CharField("Password", max_length=100, default="")
    Smoking_ch = (
        ("Neut", "Neutral"),
        ("Neg", "Negative"),
        ("Pos", "Positive"),
    )
    Smoking = models.CharField(
        choices=Smoking_ch, null=True, blank=True, max_length=256
    )

    def __str__(self):
        return self.FirstName + " " + self.SecondName

    @staticmethod
    def calculate_age(birthday):
        today = timezone.now()
        return (
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day))
        )

    @staticmethod
    def is_valid_name(name: str):
        if not name:
            return False
        if not re.match(r"^[a-zA-Z]+$", name):
            return False
        return True

    @staticmethod
    def is_valid_username(username: str):
        if not username:
            return False
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            return False
        if re.match(r"^[\d_-]", username):
            return False
        if username.endswith("-"):
            return False
        return True

    @staticmethod
    def username_rules_description():
        return "The username can contain only Latin letters, numbers, '_', and '-', must not start with a number, '_', or '-', and must not end with a '-'"


class Message(models.Model):
    Sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    Recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    Text = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["CreatedAt"]
