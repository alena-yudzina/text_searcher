from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from app import Post


def create_index(client):
    client.indices.create(
        index='posts_search',
        body={
            'settings': {'number_of_shards': 1},
            'mappings': {
                'properties': {
                    'id': {'type': 'integer'},
                    'text': {'type': 'text'},
                    'created_date': {'type': 'date'},
                    'rubrics': {'type': 'text'}
                }
            },
        },
        ignore=400,
    )


def get_query():
    posts = Post.query.all()
    for post in posts:
        doc = {
            'id': post.id,
            'text': post.text,
            'created_date': post.created_date,
            'rubrics': str(post.rubrics)
        }
        yield doc


def main():

    client = Elasticsearch('http://localhost:9200')
    client.indices.delete(index='posts_search', ignore=[400, 404])
    create_index(client)
    for ok, action in streaming_bulk(
        client=client, index="posts_search", actions=get_query(),
    ):
        pass


if __name__ == "__main__":
    main()
