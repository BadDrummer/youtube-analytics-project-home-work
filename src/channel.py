import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')

    def __init__(self, channel_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        self.__init_from_api()

    def __init_from_api(self):
        service = self.get_service()
        channel_info = service.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        self.title = channel_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/channel/{self._channel_id}"
        self.description = channel_info['items'][0]['snippet']['description']
        self.subscribers = int(channel_info['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(channel_info['items'][0]['statistics']['videoCount'])
        self.views_count = int(channel_info['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        return self.subscribers - other.subscribers

    def __gt__(self, other):
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        return self.subscribers >= other.subscribers

    def __lt__(self, other):
        return self.subscribers < other.subscribers

    def __le__(self, other):
        return self.subscribers <= other.subscribers

    def __eq__(self, other):
        return self.subscribers == other.subscribers

    @property
    def channel_id(self):
        return self._channel_id

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self._channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, filename):
        channel_data = {
            'id': self._channel_id,
            'title': self.title,
            'url': self.url,
            'description': self.description,
            'subscribers': self.subscribers,
            'video_count': self.video_count,
            'views_count': self.views_count
        }
        with open(filename, 'w', encoding='utf-8') as output_file:
            json.dump(channel_data, output_file, ensure_ascii=False, indent=2)
