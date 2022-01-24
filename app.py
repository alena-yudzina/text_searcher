from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
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


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        new_post = Post(text=text)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your post'

    else:
        posts = Post.query.order_by(Post.created_date).all()
        return render_template('index.html', posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
