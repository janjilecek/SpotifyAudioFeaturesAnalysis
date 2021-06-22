import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import plotly.express as px


class SpotifyFeaturesAnalysis:
    def __init__(self):
        client_id = "provide_your_own_id" # generate on https://developer.spotify.com/dashboard/applications
        client_secret = "provide_your_own_secret"
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        self.data = []
        self.username = None

        # spotify features
        self.danceability = 0
        self.energy = 0
        self.speechiness = 0
        self.acousticness = 0
        self.instrumentalness = 0
        self.liveness = 0
        self.valence = 0

    def get_all_track_features(self, tracks):
        isolated_ids = []
        for i, item in enumerate(tracks['items']):
            track = item['track']
            if track['id'] is not None:
                isolated_ids.append(track['id'])
            result = '{} : {}'.format(track['name'], track['id'])
            print(result)
            for item in self.sp.audio_features(isolated_ids):
                self.data.append(item)

    def load_playlists(self, username):
        playlists = self.sp.user_playlists(username)
        self.username = username
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                results = self.sp.playlist(playlist['id'], fields="tracks,next")
                print(playlist['name'])
                tracks = results['tracks']

                self.get_all_track_features(tracks)
                #break  # optional: only first playlist, then stop
                while tracks['next']:
                    tracks = self.sp.next(tracks)
                    self.get_all_track_features(tracks)

            if playlists['next']:
                playlists = self.sp.next(playlists)
            else:
                playlists = None

    def factor_average(self, factor):
        return float(sum(d[factor] for d in self.data)) / len(self.data)

    def calculate_average_features(self):
        self.energy = self.factor_average('energy')
        self.acousticness = self.factor_average('acousticness')
        self.liveness = self.factor_average('liveness')
        self.valence = self.factor_average('valence')
        self.danceability = self.factor_average('danceability')
        self.speechiness = self.factor_average('speechiness')
        self.instrumentalness = self.factor_average('instrumentalness')

    def plot_graph(self):
        data = {"energy": [self.energy],
                "valence": [self.valence],
                "acousticness": [self.acousticness],
                "liveness": [self.liveness],
                "danceability": [self.danceability],
                "speechiness": [self.speechiness],
                "instrumentalness": [self.instrumentalness]
                }

        fig = px.line_polar(data, r=[item[0] for item in data.values()], theta=data.keys(),
                            range_r=[0.0, 1.0], line_close=True,
                            title='Audio features of {}\'s playlists'.format(self.username),
                            width=600, height=500)
        fig.show()


if __name__ == '__main__':
    sfa = SpotifyFeaturesAnalysis()
    sfa.load_playlists("provide_your_username_here") # provide your own username - copy your account link and you will see it in the url
    sfa.calculate_average_features()
    sfa.plot_graph()
