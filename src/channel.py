import json
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    api_key = "AIzaSyC4O9lc-eaALlbHYi-NTAk-AgAuMDYoCAg"

    @classmethod
    def get_service(cls):
        youtube = build("youtube", 'v3', developerKey=Channel.api_key)
        return youtube

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__json_dict = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.__title = self.__json_dict['items'][0]['snippet']['title']
        self.__video_count = self.__json_dict['items'][0]['statistics']['videoCount']
        self.__url = 'https://www.youtube.com/' + self.__json_dict['items'][0]['snippet']['customUrl']
        self.__description = self.__json_dict['items'][0]['snippet']['description']
        self.__subs_count = self.__json_dict['items'][0]['statistics']['subscriberCount']
        self.__view_count = self.__json_dict['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def video_count(self):
        return self.__video_count

    @property
    def url(self):
        return self.__url

    @property
    def description(self):
        return self.__description

    @property
    def subs_count(self):
        return self.__subs_count

    @property
    def view_count(self):
        return self.__view_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__json_dict, indent=2, ensure_ascii=False))

    def to_json(self, title_json):
        new_file = open(title_json, 'w+')
        new_file.write(json.dumps(self.__json_dict, indent=2, ensure_ascii=False))
        new_file.close()
