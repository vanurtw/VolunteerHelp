from django.db import models
from tasks.models import Task
from users.models import MyUser

class Review(models.Model):
    CHOICES_RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    # кто оставил
    from_user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    # на кого оставил
    to_user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(
        choices=CHOICES_RATING
    )
    comment = models.TextField(blank=True, null=True)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.from_user} на {self.to_user}"

    class Meta:
        unique_together = ('task', 'from_user')
        ordering = ['-date_creation']

