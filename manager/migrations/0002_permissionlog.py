# Generated by Django 4.1.1 on 2022-09-23 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_property_options'),
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_change', models.CharField(choices=[('Role', 'Role'), ('Property', 'Property'), ('Both', 'Both')], max_length=300)),
                ('initiated_by', models.CharField(choices=[('Update', 'Update'), ('Create', 'Create'), ('Delete', 'Delete')], max_length=300)),
                ('account_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permission_logs', to='manager.accountuser')),
                ('added_properties', models.ManyToManyField(related_name='+', to='core.property')),
                ('deleted_properties', models.ManyToManyField(related_name='+', to='core.property')),
                ('new_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.role')),
                ('old_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.role')),
            ],
        ),
    ]
