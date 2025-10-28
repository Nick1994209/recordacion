from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RecordImage(models.Model):
    """Model to store individual images for records"""
    image = models.ImageField(upload_to='record_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class RecordEntry(models.Model):
    """Main model for record entries"""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview_image = models.ImageField(
        upload_to='preview_images/', 
        verbose_name="Картинка для preview",
        blank=True,
        null=True
    )
    images = models.ManyToManyField(
        RecordImage, 
        related_name='records',
        verbose_name="Картинки",
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Дата обновления"
    )
    is_approved = models.BooleanField(
        default=False, 
        verbose_name="Принято администратором"
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_records',
        verbose_name="Кто принял рекорд"
    )

    class Meta:
        verbose_name = "Запись рекорда"
        verbose_name_plural = "Записи рекордов"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
