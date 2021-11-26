import pprint

import pandas as pd

from elasticsearch import Elasticsearch

# Instantiate a client instance
client = Elasticsearch("http://3.101.85.85:9200")


def clean_data(x):
    return str.lower(x.replace(" ", ""))


def create_soup(x):
    return x['original_title'] + ' ' + x['authors'] + ' ' + x['average_rating']

def search_multiple_songs(listOfSongIds):
    build_query = {
        "query": {
            "terms": {
                "song_id": listOfSongIds,
                "boost": 1.0
            }
                }
            }
    print(build_query)
    result = client.search(index="msd", body=build_query)
    print(result)
    return  [d["_source"] for d in result["hits"]["hits"]]
    # song_id = result["hits"]["hits"][0]['_source']['song_id']

def get_song_by_name(title):
    query_body = {
        "query": {"query_string": {"default_field": "title", "query": title}}}
    print(query_body)
    result = client.search(index="msd", body=query_body)
    print(result)
    song_id = result["hits"]["hits"][0]['_source']['song_id']
    print("query hits:", result["hits"]["hits"][0]['_source']['song_id'])

    return get_recommendations_new(song_id)


def get_song_list():
    result = client.search(index="msd", body={"query": {"match_all": {}}})
    print("query hits:", result["hits"]["hits"])
    return result["hits"]["hits"][0]['_source']['song_name']


def get_recommendations_new(id):
    resp = client.info()
    query_body = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "song_id": id
                    }
                }
            }
        }
    }
    print(query_body)
    result = client.search(index="result", body=query_body)
    print("query hits:", result["hits"]["hits"][0]['_source']['recommendations'])
    recs = result["hits"]["hits"][0]['_source']['recommendations']
    song_ids = [d['song_id'] for d in recs]
    print(song_ids)
    list1 = search_multiple_songs(song_ids)
    list2 = result["hits"]["hits"][0]['_source']['recommendations']
    pprint.pprint(list2)
    pprint.pprint(list1)
    print(len(list2), len(list1))
    for x in list2:
        x['title'] = [i for i in list1 if i['song_id'] == str(x['song_id'])][0]['song_name']
    return list2



books = pd.read_csv(r'books.csv', error_bad_lines=False)
books = books.dropna()

features = ['original_title', 'authors', 'average_rating']
fbooks = books[features]
fbooks = fbooks.astype(str)
# print(list(fbooks['original_title']))
for feature in features:
    fbooks[feature] = fbooks[feature].apply(clean_data)

# fbooks.head(2)

fbooks['soup'] = fbooks.apply(create_soup, axis=1)

fbooks = fbooks.reset_index()
indices = pd.Series(fbooks.index, index=fbooks['original_title'])

if __name__ == '__main__':
    da = {'took': 2, 'timed_out': False, '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 10, 'relation': 'eq'}, 'max_score': 1.0, 'hits': [{'_index': 'msd', '_type': 'msd', '_id': 'w9KGVn0BKZ1IbgXbZhBA', '_score': 1.0, '_source': {'song_id_category': 'SOWEHOM12A6BD4E09E', 'song_id': '332743', 'artist_name': 'The Crests', 'song_name': '16 Candles'}}, {'_index': 'msd', '_type': 'msd', '_id': '2dKGVn0BKZ1IbgXbZhBA', '_score': 1.0, '_source': {'song_id_category': 'SOEGIYH12A6D4FC0E3', 'song_id': '67917', 'artist_name': 'Barry Tuckwell/Academy of St Martin-in-the-Fields/Sir Neville Marriner', 'song_name': 'Horn Concerto No. 4 in E flat K495: II. Romance (Andante cantabile)'}}, {'_index': 'msd', '_type': 'msd', '_id': '59KGVn0BKZ1IbgXbZhBA', '_score': 1.0, '_source': {'song_id_category': 'SOLFXKT12AB017E3E0', 'song_id': '176425', 'artist_name': 'Charttraxx Karaoke', 'song_name': 'Fireflies'}}, {'_index': 'msd', '_type': 'msd', '_id': '99KGVn0BKZ1IbgXbZhBA', '_score': 1.0, '_source': {'song_id_category': 'SOUVTSM12AC468F6A7', 'song_id': '314455', 'artist_name': 'Lil Wayne / Eminem', 'song_name': 'Drop The World'}}, {'_index': 'msd', '_type': 'msd', '_id': '29KGVn0BKZ1IbgXbZhJB', '_score': 1.0, '_source': {'song_id_category': 'SOEQJBS12A8AE475A4', 'song_id': '74235', 'artist_name': 'Band Of Horses', 'song_name': 'The Funeral (Album Version)'}}, {'_index': 'msd', '_type': 'msd', '_id': 'h9KGVn0BKZ1IbgXbaC8X', '_score': 1.0, '_source': {'song_id_category': 'SOFLJQZ12A6D4FADA6', 'song_id': '87066', 'artist_name': 'Cartola', 'song_name': 'Tive Sim'}}, {'_index': 'msd', '_type': 'msd', '_id': 'RdKGVn0BKZ1IbgXbaU4B', '_score': 1.0, '_source': {'song_id_category': 'SOOFYTN12A6D4F9B35', 'song_id': '220787', 'artist_name': 'Alliance Ethnik', 'song_name': 'ReprÃ©sente'}}, {'_index': 'msd', '_type': 'msd', '_id': 'v9KGVn0BKZ1IbgXbanOK', '_score': 1.0, '_source': {'song_id_category': 'SOHFJAQ12AB017E4AF', 'song_id': '114672', 'artist_name': 'The Ruts', 'song_name': 'West One (Shine On Me)'}}, {'_index': 'msd', '_type': 'msd', '_id': 'ptKGVn0BKZ1IbgXba4cD', '_score': 1.0, '_source': {'song_id_category': 'SOTNHIP12AB0183131', 'song_id': '295905', 'artist_name': 'Kid Cudi / Kanye West / Common', 'song_name': 'Make Her Say'}}, {'_index': 'msd', '_type': 'msd', '_id': 'HNKGVn0BKZ1IbgXba56O', '_score': 1.0, '_source': {'song_id_category': 'SOOGNOZ12AAF3B2936', 'song_id': '221144', 'artist_name': 'White Denim', 'song_name': 'Transparency'}}]}}
    song_ids = [d["_source"] for d in da["hits"]["hits"]]
    pprint.pprint(song_ids)
