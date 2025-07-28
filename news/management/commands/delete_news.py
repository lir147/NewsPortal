from django.core.management.base import BaseCommand, CommandError
from news.models import Category, News  # предположим, что модель категории - Category, новости - News

class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории (с подтверждением)'

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str, help='Имя категории, из которой надо удалить новости')

    def handle(self, *args, **options):
        category_name = options['category_name']

        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise CommandError(f'Категория с именем "{category_name}" не найдена.')

        news_qs = News.objects.filter(category=category)

        count = news_qs.count()
        if count == 0:
            self.stdout.write(self.style.WARNING(f'В категории "{category_name}" нет новостей для удаления.'))
            return

        self.stdout.write(f'В категории "{category_name}" найдено {count} новостей.')
        self.stdout.write('Вы уверены, что хотите удалить их все? (yes/no): ')

        confirm = input().strip().lower()
        if confirm != 'yes':
            self.stdout.write(self.style.WARNING('Операция удаления отменена.'))
            return

        deleted_count, _ = news_qs.delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено {deleted_count} новостей из категории "{category_name}".'))