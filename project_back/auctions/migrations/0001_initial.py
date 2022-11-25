from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paintings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_bid', models.PositiveIntegerField(default=10000, verbose_name='시작 입찰가')),
                ('now_bid', models.PositiveIntegerField(blank=True, null=True, verbose_name='현재 입찰가')),
                ('last_bid', models.PositiveIntegerField(blank=True, null=True, verbose_name='최종 입찰가')),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='경매 시작')),
                ('end_date', models.DateTimeField(null=True, verbose_name='경매 마감')),
                ('auction_like', models.ManyToManyField(blank=True, related_name='like_auction', to=settings.AUTH_USER_MODEL, verbose_name='경매 좋아요')),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auction_bidder', to=settings.AUTH_USER_MODEL, verbose_name='입찰자')),
                ('painting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paintings.painting', verbose_name='유화')),
            ],
            options={
                'db_table': 'auction',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=100, verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='auctions.auction', verbose_name='경매 작품')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'db_table': 'comment',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AuctionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('now_bid', models.PositiveIntegerField(blank=True, null=True, verbose_name='입찰가')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
                ('auction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction', verbose_name='경매 작품')),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auction_history_bidder', to=settings.AUTH_USER_MODEL, verbose_name='입찰자')),
            ],
            options={
                'db_table': 'auction_history',
                'ordering': ['id'],
            },
        ),
    ]
