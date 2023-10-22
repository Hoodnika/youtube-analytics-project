import json
from googleapiclient.discovery import build
from src.channel import Channel


class Video:
    """
    Класс для видео из ютуба
    """

    @classmethod
    def get_service(cls):
        youtube = build("youtube", "v3", developerKey=Channel.api_key)
        return youtube

    def __init__(self, video_id: str) -> None:
        try:
            self.__video_id = video_id
            self.__json_dict = Video.get_service().videos().list(id=self.__video_id, part='snippet,statistics,contentDetails').execute()
            self.__title = self.__json_dict['items'][0]['snippet']['title']
            self.__url = 'https://youtu.be/' + self.__video_id
            self.__view_count = int(self.__json_dict['items'][0]['statistics']['viewCount'])
            self.__like_count = int(self.__json_dict['items'][0]['statistics']['likeCount'])
        except:
            self.__video_id = video_id
            self.__title = None
            self.__url = None
            self.__view_count = None
            self.__like_count = None

    def __str__(self):
        return self.__title

    @property
    def video_id(self):
        return self.__video_id

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def view_count(self):
        return self.__view_count

    @property
    def like_count(self):
        return self.__like_count

    def print_info(self):
        print(json.dumps(self.__json_dict, indent=2, ensure_ascii=False))


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
