# Generated by Django 5.0.6 on 2024-06-25 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_commneted_by_comment_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdf_files'),
        ),
    ]
