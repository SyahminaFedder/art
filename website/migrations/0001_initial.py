# Generated by Django 5.1 on 2024-10-20 09:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('tid', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('tname', models.TextField()),
                ('tpass', models.CharField(max_length=10)),
                ('role', models.TextField()),
                ('tphno', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('eid', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('ename', models.TextField()),
                ('sdate', models.DateField()),
                ('edate', models.DateField()),
                ('venue', models.TextField(default=None)),
                ('tid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sid', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('sname', models.TextField()),
                ('spass', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=8)),
                ('sphno', models.CharField(max_length=20)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.course')),
            ],
        ),
        migrations.CreateModel(
            name='Attendace',
            fields=[
                ('aid', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('eid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.event')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.student')),
            ],
        ),
    ]
