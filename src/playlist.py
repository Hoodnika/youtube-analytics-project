import json
from googleapiclient.discovery import build
from src.channel import Channel
from src.video import Video
import isodate
import datetime


class PlayList:
    """
    Класс для плейлиста из ютуба
    """

    @classmethod
    def get_service(cls):
        youtube = build("youtube", "v3", developerKey=Channel.api_key)
        return youtube

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.__json_dict = PlayList.get_service().playlists().list(id=self.__playlist_id,
                                                                   part='snippet',
                                                                   maxResults=50,
                                                                   ).execute()
        self.__title = self.__json_dict['items'][0]['snippet']['title']
        self.__url = "https://www.youtube.com/playlist?list=" + self.__playlist_id

    @property
    def play_list_items(self):
        play_list_items = PlayList.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                      part='contentDetails,snippet',
                                                                      maxResults=50,
                                                                      ).execute()
        return play_list_items

    @property
    def total_duration(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.play_list_items['items']]
        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)
                                                              ).execute()
        total_duration = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = str(isodate.parse_duration(iso_8601_duration))
            (h, m, s) = duration.split(':')
            d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            total_duration += d
        return total_duration

    def show_best_video(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.play_list_items['items']]
        video_lists = []
        for id in video_ids:
            video_lists.append(Video(id))
        best_video = video_lists[0]
        for video in video_lists:
            if video.like_count > best_video.like_count:
                best_video = video
        return best_video.url

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    def print_info(self):
        user_choice = int(input("Получить информацию по самому плейлисту(1) или по всем видео из плейлиста(2)?\n"
              "Введите 1 или 2\n"))
        if user_choice == 1:
            print(json.dumps(self.__json_dict, indent=2, ensure_ascii=False))
        if user_choice == 2:
            print(json.dumps(self.play_list_items, indent=2, ensure_ascii=False))
        if user_choice != 1 or 2:
            print("Try again, hommy")

