import csv
import os
from django.core.management.base import BaseCommand
from board.models import Facility

class Command(BaseCommand):
    help = 'Load data from CSV file into Facility model'

    def handle(self, *args, **kwargs):
        # 파일 경로를 프로젝트 루트 디렉토리로 설정
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        file_path = os.path.join(base_dir, 'data.csv')
        
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Facility.objects.create(
                    name=row['시설명'],
                    region=row['지역'],
                    location=row['위치'],
                    sport=row['종목'],
                    target=row['대상'],
                    period=row['기간'],
                    day=row['요일'],
                    time=row['진행시간(1회)'],
                    fee=int(row['수강료(원)']),
                    capacity=int(row['전체정원수'])
                )
        self.stdout.write(self.style.SUCCESS('Data successfully loaded'))
