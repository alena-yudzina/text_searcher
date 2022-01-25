from elasticsearch import Elasticsearch
from app import Post
import tqdm
from elasticsearch.helpers import streaming_bulk


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
    create_index(client)

    print("Indexing documents...")
    number_of_docs = 1500
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=client, index="posts_search", actions=get_query(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))


if __name__ == "__main__":
    main()
