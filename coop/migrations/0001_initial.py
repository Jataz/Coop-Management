# Generated by Django 5.0.6 on 2024-07-23 16:07

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.IntegerField(choices=[(30, '1 Month'), (90, '3 Months'), (180, '6 Months')], unique=True)),
                ('interest_rate', models.DecimalField(decimal_places=2, help_text='Interest rate as a percentage', max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('id_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('physical_address', models.TextField(blank=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_no', models.CharField(blank=True, max_length=30, unique=True)),
                ('mobile_account', models.CharField(max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('term_months', models.PositiveIntegerField()),
                ('interest_rate', models.DecimalField(decimal_places=2, default=Decimal('5.00'), max_digits=5)),
                ('service_fee', models.DecimalField(decimal_places=2, default=Decimal('2.00'), max_digits=10)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('repayment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('disbursed_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('application_date', models.DateField(auto_now_add=True)),
                ('application_time', models.TimeField(auto_now_add=True)),
                ('agreed_to_terms', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Outstanding', 'Outstanding'), ('Cleared', 'Cleared')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outstanding_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField()),
                ('total_to_be_repaid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('summary_interest', models.DecimalField(decimal_places=2, max_digits=10)),
                ('overdue_mgt_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('late_interest', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('partial_payment', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('repayment_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('loan_application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Loan_application_status', to='coop.loanapplication')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_fee_paid', models.BooleanField(default=False)),
                ('is_member', models.BooleanField(default=False)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OtpToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(default='4e3e5f', max_length=6)),
                ('tp_created_at', models.DateTimeField(auto_now_add=True)),
                ('otp_expires_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShareCapital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payement_date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShareCapitalPartialPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partial_payment', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('share_capital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.sharecapital')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionPartialPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partial_payment', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.subscription')),
            ],
        ),
    ]
