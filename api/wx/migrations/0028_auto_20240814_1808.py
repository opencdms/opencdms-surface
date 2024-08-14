# Generated by Django 3.2.13 on 2024-08-14 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wx', '0027_auto_20230725_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='is_synoptic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='station',
            name='synop_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='WMOCodeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=8)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('code_table', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wx.codetable')),
            ],
            options={
                'unique_together': {('code_table', 'value')},
            },
        ),
    ]
