
from dotenv import load_dotenv
from datetime import datetime
from googleapiclient.discovery import build
import pandas as pd
import os

load_dotenv()

youTubeApiKey = os.getenv('API_KEY')

youtube = build('youtube', 'v3', developerKey=youTubeApiKey)

playListId = os.getenv('PLAY_LIST_ID')
playListName = 'NAME_PLAYLIST'
nextPage_token = None

playList_videos = []

while True:
    res = youtube.playlistItems().list(part='snippet', playlistId=playListId,
                                       maxResults=15, pageToken=nextPage_token).execute()
    playList_videos = res['items']
    nextPage_token = res.get('nextPageToken')

    if nextPage_token is None:
        break

print('Número total de vídeos na Playlist', len(playList_videos))

videos_ids = list(map(lambda x: x['snippet']
                      ['resourceId']['videoId'], playList_videos))

stats = []

for video_id in videos_ids:
    res = youtube.videos().list(part='statistics', id=video_id).execute()
    stats += res['items']


videos_title = list(map(lambda x: x['snippet']['title'], playList_videos))
url_thumbnails = list(
    map(lambda x: x['snippet']['thumbnails']['high']['url'], playList_videos))
published_date = list(
    map(lambda x: x['snippet']['publishedAt'], playList_videos))
video_description = list(
    map(lambda x: x['snippet']['description'], playList_videos))
videoid = list(map(lambda x: x['snippet']
               ['resourceId']['videoId'], playList_videos))

liked = list(map(lambda x: x['statistics']['likeCount'], stats))
disliked = list(map(lambda x: x['statistics']['dislikeCount'], stats))
views = list(map(lambda x: x['statistics']['viewCount'], stats))
comment = list(map(lambda x: x['statistics']['commentCount'], stats))


extraction_date = [str(datetime.now())]*len(videos_ids)


playlist_df = pd.DataFrame({
    'title': videos_title,
    'video_id': videoid,
    'video_description': video_description,
    'published_date': published_date,
    'extraction_date': extraction_date,
    'likes': liked,
    'dislikes': disliked,
    'views': views,
    'comment': comment,
    'thumbnail': url_thumbnails
})

playlist_df.to_csv('./data.csv')
