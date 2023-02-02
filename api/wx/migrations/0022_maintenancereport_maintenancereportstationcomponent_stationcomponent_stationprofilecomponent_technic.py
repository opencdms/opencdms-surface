# Generated by Django 3.2.13 on 2023-02-02 11:20

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import wx.models


class Migration(migrations.Migration):

    dependencies = [
        ('wx', '0021_hfsummarytask'),
    ]

    operations = [
        migrations.CreateModel(
            name='StationComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('report_template', ckeditor.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'station component',
                'verbose_name_plural': 'station components',
            },
        ),
        migrations.CreateModel(
            name='Technician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VisitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MaintenanceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('visit_date', models.DateField(help_text='Enter the date of the visist', validators=[wx.models.no_future])),
                ('initial_time', models.TimeField()),
                ('status', models.CharField(choices=[('A', 'Approved'), ('D', 'Draft'), ('P', 'Published')], default='D', max_length=1)),
                ('station_on_arrival_conditions', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('contacts', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('next_visit_date', models.DateField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('current_visit_summary', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('next_visit_summary', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('data_logger_file', models.TextField(blank=True, null=True)),
                ('other_technician_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='other_technician_1', to='wx.technician')),
                ('other_technician_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='other_technician_2', to='wx.technician')),
                ('other_technician_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='other_technician_3', to='wx.technician')),
                ('responsible_technician', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='responsible_technician', to='wx.technician')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wx.station')),
                ('visit_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wx.visittype')),
            ],
            options={
                'unique_together': {('station', 'visit_date')},
            },
        ),
        migrations.CreateModel(
            name='StationProfileComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('presentation_order', models.IntegerField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wx.stationprofile')),
                ('station_component', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wx.stationcomponent')),
            ],
            options={
                'unique_together': {('profile', 'presentation_order')},
            },
        ),
        migrations.CreateModel(
            name='MaintenanceReportStationComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('condition', ckeditor.fields.RichTextField()),
                ('component_classification', models.CharField(choices=[('F', 'Fully Functional'), ('P', 'Partially Functional'), ('N', 'Not Functional')], default='F', max_length=1)),
                ('maintenance_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wx.maintenancereport')),
                ('station_component', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='wx.stationcomponent')),
            ],
            options={
                'unique_together': {('maintenance_report', 'station_component')},
            },
        ),
    ]
