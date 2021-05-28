from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_marshmallow import Marshmallow
import os


#Application and database setup
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
POSTGRES = {
    'user': 'ubuntu',
    'pw': 'ubuntu',
    'db': 'postgres',
    'host': 'ip',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

@app.route('/')
def hello():
    return {"hello": "world"}

# @app.route('/verify')
# def verify():
#     return '<p>' + app.config['SECRET_KEY'] + '</p>'


db = SQLAlchemy(app)
ma = Marshmallow(app)

#Database creation flask commands
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    quote1 = Quote(quote_desc='It always seem impossible until it is done.',
                     quote_type='Motivation',
                     author='Nelson Mandela')

    quote2 = Quote(quote_desc='With the new day comes new strength and new thoughts.',
                         quote_type='Motivation',
                         author='Eleanor Roosevelt')

    quote3 = Quote(quote_desc='The secret of getting ahead is getting started.',
                     quote_type='Motivation',
                     author='Mark Twain')

    quote4 = Quote(quote_desc='With self-discipline most anything is possible.',
                     quote_type='Inspiration',
                     author='Theodore Roosevelt')

    quote5 = Quote(quote_desc='It is during our darkest moments that we must focus to see the light.',
                     quote_type='Inspiration',
                     author='Aristotle')


    db.session.add(quote1)
    db.session.add(quote2)
    db.session.add(quote3)
    db.session.add(quote4)
    db.session.add(quote5)
    db.session.commit()
    print('Database seeded!')


# database model
class Quote(db.Model):
    __tablename__ = 'quotes'
    quote_id = Column(Integer, primary_key = True)
    quote_desc = Column(String)
    quote_type = Column(String)
    author = Column(String)


# Quote model added to the Marshmallow library for JSON serialization
class QuoteSchema(ma.Schema):
    class Meta:
        fields = ('quote_id', 'quote_desc', 'quote_type', 'author')


quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)


@app.route('/quotes', methods=['GET'])
def quotes():
    quotes_list = Quote.query.all()
    result = quotes_schema.dump(quotes_list)
    return jsonify(result)


@app.route('/quote_details/<int:quote_id>', methods=['GET'])   
def quote_details(quote_id: int):
    quote = Quote.query.filter_by(quote_id=quote_id).first()
    if quote:
        result = quote_schema.dump(quote)
        return jsonify(result)
    else:
        return jsonify(message="That quote does not exist."), 404

@app.route('/add_quote', methods=['POST'])   
def add_quote():
    quote_desc = request.form['quote_desc']
    test = Quote.query.filter_by(quote_desc=quote_desc).first()
    if test:
        return jsonify(message="There is already a quote by that description."), 409
    else:
        quote_type= request.form['quote_type']
        author= request.form['author']
        quote =  Quote(quote_desc=quote_desc,
                         quote_type= quote_type,
                         author= author)  
        db.session.add(quote)
        db.session.commit()                 
        return jsonify(message="Quote added successfully!"), 201     

@app.route('/update_quote/<int:quote_id>', methods=['PUT'])   
def update_quote(quote_id : int):
    quote = Quote.query.filter_by(quote_id=quote_id).first()
    if quote:
        quote.quote_desc = request.form['quote_desc']
        quote.quote_type = request.form['quote_type']
        quote.author= request.form['author']
        db.session.commit()                 
        return jsonify(message="Quote successfully updated!")
    else:
        return jsonify(message="That quote does not exist"), 404

@app.route('/remove_quote/<int:quote_id>', methods=['DELETE'])   
def remove_quote(quote_id : int):
    quote = Quote.query.filter_by(quote_id=quote_id).first()
    if quote:
        db.session.delete(quote)
        db.session.commit()                 
        return jsonify(message="Quote successfully deleted!"), 200
    else:
        return jsonify(message="That quote does not exist"), 404


if __name__ == '__main__':
    app.run()
