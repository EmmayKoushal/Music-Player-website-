from main import db, songs, recently_played
import pandas
import random

data = pandas.read_csv('songs.csv')
data2 = data[['mood', 'language', 'artist_name', 'URI']]

dictlist = data2.to_dict('records')

random_samples = random.sample(dictlist, 40)
for song in random_samples:
    sid = songs.query.filter_by(uri=song['URI']).first()
    rp = recently_played(
        song_id = sid.id,
        song_mood = song['mood'],
        song_languages = song['language'],
        song_artist = song['artist_name'],
        frequency = 1
    )
    db.session.add(rp)
    db.session.commit()

