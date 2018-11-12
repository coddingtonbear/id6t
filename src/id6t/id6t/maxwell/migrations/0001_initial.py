# Generated by Django 2.1.3 on 2018-11-11 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('string', 'String'), ('float', 'Float'), ('int', 'Integer'), ('bool', 'Boolean'), ('pipe_delimited_float', 'Pipe-delimited Float')], max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='data',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maxwell.DataSet'),
        ),
        migrations.AddField(
            model_name='data',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maxwell.DataType'),
        ),
    ]
