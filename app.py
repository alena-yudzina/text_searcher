from datetime import datetime

from elasticsearch import Elasticsearch
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
es = Elasticsearch('http://localhost:9200')
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    rubrics = relationship('Rubric', back_populates='posts')

    def __repr__(self):
        return self.text


class Rubric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    posts = relationship('Post', back_populates='rubrics')

    def __repr__(self):
        return self.name


class Search(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text')
        params = parser.parse_args()
        result = es.search(
            index='posts_search',
            body={
                "query": {
                    "match": {
                        "text": params['text']
                    }
                },
                "sort": [
                    {
                        "created_date": {
                            "order": "asc"
                        }
                    }
                ]
            },
            size=20,
        )
        matches = []
        for item in result['hits']['hits']:
            matches.append(
                {
                    'id': item['_source']['id'],
                    'text': item['_source']['text'],
                    'created_date': item['_source']['created_date'],
                    'rubrics': item['_source']['rubrics']
                }
            )
        if not matches:
            return {'answer': 'No matches found'}, 404
        return matches, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        params = parser.parse_args()
        id = params['id']
        post = es.search(
            index='posts_search',
            body={'query': {'match': {'id': id}}}
        )
        try:
            elastic_post_id = post['hits']['hits'][0]['_id']
        except IndexError:
            return {'answer': f"Can't find post with id {id}."}, 400

        es.delete(index='posts_search', doc_type='_doc', id=elastic_post_id)
        post_in_db = db.session.get(Post, id)
        db.session.delete(post_in_db)
        db.session.commit()
        return {'answer': f'Post with id {id} was deleted.'}, 200


api.add_resource(Search, '/search', '/delete')
if __name__ == '__main__':
    app.run(debug=True)
