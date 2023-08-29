import isodate
from datetime import timedelta
import os
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('API_KEY')

    def __init__(self, playlist_id):

        self.playlist = self.get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails, snippet', maxResults= 50).execute()
        self.title = self.playlist["items"][0]["snippet"]["title"].split(".")[0]
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',id=','.join(self.video_ids)).execute()

        # video_response = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def total_duration(self):
        duration = timedelta()
        for video in self.video_response['items']:
            iso_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_duration)
        return duration

    def show_best_video(self):
        likes = 0
        best_video = None
        for video in self.video_ids:
            video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video).execute()
            video_likes = video_response['items'][0]['statistics']['likeCount']
            if int(video_likes) > likes:
                likes = int(video_likes)
                best_video = f"https://youtu.be/{video}"
        return best_video
