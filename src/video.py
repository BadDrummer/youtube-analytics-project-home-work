import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('API_KEY')

    def __init__(self, video_id):
        video = \
            self.get_service().videos().list(part='snippet,statistics,contentDetails, topicDetails',
                                             id=video_id).execute()['items'][0]
        self.video_id = video_id
        self.title = video['snippet']['title']
        self.link = 'https://www.youtube.com/watch?v=' + video_id
        self.view_count = video['statistics']['viewCount']
        self.like_count = video['statistics']['likeCount']


    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
