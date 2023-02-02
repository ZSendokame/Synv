import random

import lilidb
from flask import Flask, render_template, redirect, request, jsonify

app = Flask(__name__, static_folder='templates')


@app.get('/')
def root():
    with lilidb.Database('database/rooms.json') as db:
        return render_template('index.html', rooms=db.database)


@app.get('/room/<id>')
def room(id):
    with lilidb.Database('database/rooms.json') as db:
        if not db.exists(id):
            return render_template('404.html', id=id)

        room = db.get(id)

    return render_template('room.html', video=room['embed'], title=room['title'])


@app.post('/api/create')
def api_create():
    with lilidb.Database('database/rooms.json') as db:
        embed = request.form.get('embed')
        title = request.form.get('title')
        room_id = '0'

        if all([embed, title]):
            while db.exists(room_id):
                room_id = str(random.randint(0, 900000000))

            db.set(room_id, {'embed': embed, 'title': title})

        else:
            return redirect('/')

    return redirect('/room/' + room_id)


@app.get('/api/list')
def api_list():
    with lilidb.Database('database/rooms.json') as db:
        return jsonify(db.database)


app.run()
