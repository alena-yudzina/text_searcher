from ast import literal_eval

import pandas

from app import Post, Rubric, db

db.create_all()

df = pandas.read_csv('posts.csv', parse_dates=['created_date'], converters={'rubrics': literal_eval})
for _, row in df.iterrows():
    new_post = Post(
        text=row['text'],
        created_date=row['created_date'])
    db.session.add(new_post)
    db.session.commit()

    for rubric in row['rubrics']:
        new_rubric = Rubric(name=rubric, post_id=new_post.id)
        db.session.add(new_rubric)
        db.session.commit()
