# Generated by Django 4.2.7 on 2023-12-03 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0026_color_name_alter_color_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='additional_attributes',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='color',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliate.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='affiliate.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliate.size')),
            ],
        ),
    ]
