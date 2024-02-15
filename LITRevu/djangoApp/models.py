from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(
                                    blank=True,
                                    max_length=2048
                                )
    user = models.ForeignKey(
                            to=settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE
                            )
    time_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='tickets/', null=True, blank=True)

    def get_fields(self):
        return {
            'title': self.title,
            'description': self.description,
            'user': self.user,
            'time_created': self.time_created,
            'image': self.image.url if self.image else None,
            'type': 'ticket'
        }

    def get_related_reviews(self):
        return self.reviews.all()


class Review(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
                                to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE
                            )
    time_created = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(
                                Ticket,
                                related_name='reviews',
                                on_delete=models.PROTECT,
                                null=True
                            )

    def get_fields(self):
        return {
            'rating': self.rating,
            'headline': self.headline,
            'body': self.body,
            'user': self.user,
            'time_created': self.time_created,
            'type': 'review'
        }


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
    )

    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'followed_user', )
