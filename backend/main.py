import json
import os
import shutil
import jwt
import bcrypt
import uuid
import requests

from flask import Flask, current_app, request, jsonify, Response, g, send_file
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup


from werkzeug.utils import secure_filename
import feedparser


# Default JSON encoder는 set를 JSON으로 변환할 수 없다.
# 그러므로 커스텀 엔코더를 작성해서 set을 list로 변환하여 JSON으로 변환 가능하게 해주어야 한다.

# sys.setrecursionlimit(10**7)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)


app = Flask(__name__)
CORS(app, resources={r'*': {'origins': '*'}})
app.json_encoder = CustomJSONEncoder

app.config.from_pyfile('config.py')
database = create_engine(app.config['DB_URL'], encoding="utf-8")
app.database = database


def insert_user(user):
    return app.database.execute(text("""
        INSERT INTO users (
            name,
            email,
            hashed_pwd
        ) VALUES (
            :name,
            :email,
            :password
        )
    """), user).lastrowid


def get_user(user_id):
    user = app.database.execute(text(f"""
        SELECT
            *
        FROM users
        WHERE user_id = {user_id}
    """)).fetchone()

    return {
        'id': user_id,
        'name': user['name'],
        'email': user['email'],
        'bio': user['bio'],
        'location': user['location'],
        'website': user['website'],
        'birth': str(user['birth']),
        'bg_image': user['bg_image'],
        'profile_image': user['profile_image'],
        'created_at': str(user['created_at']),
        'updated_at': str(user['updated_at'])
    } if user else None


def update_user(user):
    return app.database.execute(text(f"""
        UPDATE users
        SET
        name='{user['name']}',
        bio = CASE WHEN '{user['bio']}' = '' THEN NULL ELSE '{user['bio']}' END,
        location = CASE WHEN '{user['location']}' = '' THEN NULL ELSE '{user['location']}' END,
        website = CASE WHEN '{user['website']}' = '' THEN NULL ELSE '{user['website']}' END,
        birth = CASE WHEN '{user['birth']}' = '' THEN NULL ELSE '{user['birth']}' END,
        bg_image = CASE WHEN '{user['bg_image']}' = '' THEN NULL ELSE '{user['bg_image']}' END,
        profile_image = CASE WHEN '{user['profile_image']}' = '' THEN NULL ELSE '{user['profile_image']}' END
        WHERE user_id = {int(user['user_id'])}
    """))


def get_user_id_and_password(email):
    row = app.database.execute(text(f"""
        SELECT
            user_id, hashed_pwd
        FROM users WHERE email = '{email}'
    """)).fetchone()

    return {
        'id': row['user_id'],
        'hashed_password': row['hashed_pwd']
    } if row else None


def insert_tweet(user_id, u_tweet, filenames):
    return app.database.execute(text(f"""
        INSERT INTO tweets (
            user_id,
            tweet,
            uploads
        ) VALUES (
            {user_id},
            '{u_tweet}',
            '{filenames}'
        )
    """)).rowcount


def get_tweet(tweet_id, user_id):
    tweet = app.database.execute(text(f"""
        SELECT 
            t.id,
            t.user_id,
            t.tweet,
            t.created_at,
            t.likes,
            t.uploads,
            u.name,
            u.email,
            u.profile_image,
            l.tweet_id
        FROM tweets t
        LEFT JOIN likes l
        ON l.user_id = {user_id} AND l.tweet_id = t.id
        LEFT JOIN users u
        ON t.user_id = u.user_id
        WHERE t.id = {tweet_id};
    """)).fetchone()

    return {
        'id': tweet['id'],
        'user_id': tweet['user_id'],
        'tweet': tweet['tweet'],
        'created_at': str(tweet['created_at']),
        'like_count': tweet['likes'],
        'uploads': tweet['uploads'],
        'name': tweet['name'],
        'email': tweet['email'],
        'profile_image': tweet['profile_image'],
        'like': True if tweet['tweet_id'] else False
    } if tweet else None



def delete_tweet(tweet_id):
    return app.database.execute(text(f"""
        delete from tweets where id={tweet_id};
    """))


def insert_follow(user_follow):
    return app.database.execute(text("""
        INSERT INTO users_follow_list (
            user_id,
            follow_user_id
        ) VALUES (
            :id,
            :follow
        )
    """), user_follow).rowcount


def insert_unfollow(user_unfollow):
    return app.database.execute(text("""
        DELETE FROM users_follow_list
        WHERE user_id = :id
        AND follow_user_id = :unfollow
    """), user_unfollow).rowcount


def get_follow(user_id):
    followings = app.database.execute(text(f"""
            SELECT follow_user_id
            FROM users_follow_list
            WHERE user_id = {user_id}
        """)).fetchall()

    followers = app.database.execute(text(f"""
                SELECT user_id
                FROM users_follow_list
                WHERE follow_user_id = {user_id}
            """)).fetchall()

    followings_arr = [following['follow_user_id'] for following in followings]
    followers_arr = [follower['user_id'] for follower in followers]

    return {
        'followings': followings_arr,
        'followers': followers_arr
    }


def get_random_users(user_id):
    users = app.database.execute(text(f"""
        SELECT DISTINCT * FROM users u
        WHERE user_id NOT IN (select follow_user_id from users_follow_list where user_id = {user_id})
        AND user_id != {user_id}
        ORDER BY rand() LIMIT 5
    """))

    return [{
        'id': user['user_id'],
        'name': user['name'],
        'email': user['email'],
        'profile_image': user['profile_image']
    } for user in users]


def get_timeline(user_id, keyword):
    print('user_id', user_id)
    print('keyword', keyword)
    if keyword and user_id is not None:
        print('search')
        timeline = app.database.execute(text(f"""
                SELECT DISTINCT
                    t.id,
                    t.user_id,
                    t.tweet,
                    t.likes,
                    t.uploads,
                    t.created_at,
                    u.name,
                    u.email,
                    u.profile_image,
                    l.tweet_id
                FROM tweets t
                LEFT JOIN users_follow_list ufl
                ON ufl.user_id = {user_id}
                LEFT JOIN likes l
                ON l.user_id = {user_id} AND l.tweet_id = t.id
                LEFT JOIN users u
                ON u.user_id = t.user_id
                WHERE t.tweet LIKE '%{keyword}%'
                OR t.user_id = ufl.follow_user_id
            """)).fetchall()

    else:
        print('post')
        timeline = app.database.execute(text(f"""
        SELECT DISTINCT
            t.id,
            t.user_id,
            t.tweet,
            t.likes,
            t.uploads,
            t.created_at,
            u.name,
            u.email,
            u.profile_image,
            l.tweet_id
        FROM tweets t
        LEFT JOIN users_follow_list ufl
        ON ufl.user_id = {user_id}
        LEFT JOIN likes l
        ON l.user_id = {user_id} AND l.tweet_id = t.id
        LEFT JOIN users u
        ON u.user_id = t.user_id
        WHERE t.user_id = {user_id}
        OR t.user_id = ufl.follow_user_id
    """)).fetchall()

    return [{
        'id': tweet['id'],
        'user_id': tweet['user_id'],
        'tweet': tweet['tweet'],
        'like_count': tweet['likes'],
        'uploads': tweet['uploads'],
        'created_at': str(tweet['created_at']),
        'name': tweet['name'],
        'email': tweet['email'],
        'profile_image': tweet['profile_image'],
        'like': True if tweet['tweet_id'] else False
        } for tweet in timeline]


def get_my_timeline(user_id):
    timeline = app.database.execute(text(f"""
        SELECT DISTINCT
            t.id,
            t.user_id,
            t.tweet,
            t.likes,
            t.uploads,
            t.created_at,
            u.name,
            u.email,
            l.tweet_id
        FROM tweets t
        LEFT JOIN users u
        ON u.user_id = t.user_id
        LEFT JOIN likes l
        ON l.tweet_id = t.id
        WHERE t.user_id = {user_id}
    """)).fetchall()

    return [{
        'id': tweet['id'],
        'user_id': tweet['user_id'],
        'tweet': tweet['tweet'],
        'like_count': tweet['likes'],
        'uploads': tweet['uploads'],
        'created_at': str(tweet['created_at']),
        'name': tweet['name'],
        'email': tweet['email'],
        'like': True if tweet['tweet_id'] else False
        } for tweet in timeline]


def get_search_user(key):
    search_users = app.database.execute(text(f"""
        SELECT * FROM users
        WHERE name LIKE '%{key}%'
    """))

    return [{
        'id': user['user_id'],
        'name': user['name'],
        'email': user['email'],
        'bio': user['bio'],
        'profile_image': user['profile_image']
    } for user in search_users]


def likes(payload):
    like_row = app.database.execute(text("""
        SELECT id FROM likes WHERE user_id=:user_id AND tweet_id=:tweet_id  
    """), payload).fetchone()


    if like_row is None:
        app.database.execute(text("""
            INSERT INTO likes (tweet_id, user_id)
            VALUES (:tweet_id, :user_id)
        """), payload)
        app.database.execute(text(f"""
            UPDATE tweets SET likes = likes + 1
            WHERE id = :tweet_id
        """), payload)

        return '좋아요'


    else:
        app.database.execute(text("""
            DELETE FROM likes WHERE tweet_id=:tweet_id AND user_id=:user_id
        """), payload)
        app.database.execute(text(f"""
            UPDATE tweets SET likes = likes - 1
            WHERE id = :tweet_id
        """), payload)

    return '좋아요 취소'


def get_trend():
    # feed = feedparser.parse('https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR')
    # print(feed.keys())
    # print(feed.entries[0])

    # url = 'https://trends.google.com/trends/trendingsearches/daily?geo=KR'

    url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR'
    response = requests.get(url)


    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        channel = soup.select_one('channel')
        titles = channel.select('item > title')
        list = []

        for title in titles:
            list.append(title.get_text())

        return jsonify({'body': list}), 200

    else:
        print(response.status_code)
        return '데이터를 가져올 수 없습니다.', 200


def create_room():
    return app.database.execute(text("""
        INSERT INTO rooms () VALUES ()
    """)).lastrowid


def create_participants(new_room_id, user_id):
    return app.database.execute(text(f"""
        INSERT INTO participants (
            room_id,
            user_id
        ) VALUES (
            {new_room_id},
            {user_id}
        )
    """))


def validation_single_chat(payload):
    return app.database.execute(text("""
        SELECT sc_id FROM single_chat
        WHERE (user_one=:myId and user_two=:userId)
        OR (user_one=:userId and user_two=:myId);
    """), payload).fetchone()


def create_single_chat(payload):
    return app.database.execute(text("""
        INSERT INTO single_chat (user_one, user_two) VALUE (:myId, :userId)
    """), payload).lastrowid


def get_single_chat(user_id):
    chats = app.database.execute(text(f"""
        SELECT u.user_id, sc.sc_id, u.name, u.email, u.profile_image, sc.created_at
        FROM users u, single_chat sc
        WHERE 
        CASE
            WHEN sc.user_one = {user_id}
            THEN sc.user_two = u.user_id
            WHEN sc.user_two = {user_id}
            THEN sc.user_one = u.user_id
        END
        AND ( sc.user_one = {user_id} OR sc.user_two = {user_id} )
        ORDER BY sc.sc_id DESC
    """)).fetchall()

    return [{
        'sc_id': chat['sc_id'],
        'user_id': chat['user_id'],
        'name': chat['name'],
        'email': chat['email'],
        'profile_image': chat['profile_image'],
        'created_at': (chat['created_at']).strftime('%B %Y')
        } for chat in chats]















# Decorators



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], 'HS256')
            except jwt.InvalidTokenError:
                payload = None

            if payload is None:
                return Response(status=401)

            user_id = payload['user_id']
            g.user_id = user_id
            g.user = get_user(user_id) if user_id else None
        else:
            return Response(status=401)

        return f(*args, **kwargs)
    return decorated_function


# token을 decode하여 반환함, decode에 실패하는 경우 payload = None으로 반환
def check_access_token(access_token):
    try:
        payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], "HS256")
        if payload['exp'] < datetime.utcnow():  # 토큰이 만료된 경우
            payload = None
    except jwt.InvalidTokenError:
        payload = None

    return payload


@app.route("/ping")
def ping():
    return 'pong'


@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user['password'] = bcrypt.hashpw(
        new_user['password'].encode('UTF_8'), bcrypt.gensalt()
    )
    new_user_id = insert_user(new_user)
    new_user = get_user(new_user_id)['name']

    if new_user:
        return f'{new_user}님, 가입을 환영합니다.', 200


@app.route('/login', methods=['POST'])
def login():
    credential = request.json
    email = credential['email']
    password = credential['password']
    user_credential = get_user_id_and_password(email)

    if user_credential and bcrypt.checkpw(password.encode('UTF-8'), user_credential['hashed_password'].encode('UTF-8')):
        user_id = user_credential['id']
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=60*60*24)
        }
        token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], 'HS256')

        user = get_user(user_id)

        return jsonify({
            'access_token': token,
            'user': {
                'id': user['id'],
                'email': user['email']
            }
        })

    else:
        return '', 401


@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def user(user_id):

    return jsonify(get_user(user_id))


@app.route('/user', methods=['POST'])
@login_required
def edit_user():
    user_info = request.form.to_dict()
    user_id = user_info['user_id']

    if request.files.get('bgFile'):
        bg_uploads_dir = f'../frontend/public/bgImgs/{user_id}'

        if os.path.exists(bg_uploads_dir):
            shutil.rmtree(bg_uploads_dir)

        os.makedirs(bg_uploads_dir, exist_ok=True)

        file = request.files.get('bgFile')
        name = file.filename
        file_ext = name.split('.')[1]
        auto_gen_name = uuid.uuid4()
        new_name = str(auto_gen_name) + '.' + file_ext

        file.save(os.path.join(bg_uploads_dir, new_name))
        user_info['bg_image'] = new_name

    if request.files.get('profileFile'):
        profile_uploads_dir = f'../frontend/public/profileImgs/{user_id}'

        if os.path.exists(profile_uploads_dir):
            shutil.rmtree(profile_uploads_dir)

        os.makedirs(profile_uploads_dir, exist_ok=True)

        file = request.files.get('profileFile')
        name = file.filename
        file_ext = name.split('.')[1]
        auto_gen_name = uuid.uuid4()
        new_name = str(auto_gen_name) + '.' + file_ext

        file.save(os.path.join(profile_uploads_dir, new_name))
        user_info['profile_image'] = new_name

    update_user(user_info)

    return '', 200


@app.route('/tweet', methods=['POST'])
@login_required
def post_tweet():
    user_tweet = request.form
    user_id = user_tweet['id']
    u_tweet = user_tweet['tweet']
    filenames = ""

    if request.files.get('file'):
        uploads_dir = '../frontend/public/uploads'
        os.makedirs(uploads_dir, exist_ok=True)

        for file in request.files.getlist('file'):

            name = file.filename
            file_ext = name.split('.')[1]
            auto_gen_name = uuid.uuid4()
            new_name = str(auto_gen_name) + '.' + file_ext

            file.save(os.path.join(uploads_dir, new_name))
            filenames += new_name + ' '

    if u_tweet:
        if len(u_tweet) > 300:
            return '300자를 초과했습니다.', 400

    insert_tweet(user_id, u_tweet, filenames)
    return '', 200


@app.route('/tweet/<int:tweet_id>/<int:user_id>', methods=['GET', 'DELETE'])
@login_required
def tweet(tweet_id, user_id):
    if request.method == 'GET':
        return jsonify(get_tweet(tweet_id, user_id))

    if request.method == 'DELETE':
        path = '../frontend/public/uploads/'
        files = get_tweet(tweet_id, user_id)

        # if files['uploads']:
        #     files['uploads'] = files['uploads'].split(" ")[0:-1]
        #     for file in files['uploads']:
        #         os.remove(path + format(file))

        # TODO : like foreign key CASCADE 옵션 추가하기
        delete_tweet(tweet_id)
        return '', 200


@app.route('/follow', methods=['POST'])
@login_required
def follow():
    payload = request.json
    insert_follow(payload)

    return '', 200


@app.route('/follow/<int:user_id>', methods=['GET'])
@login_required
def following(user_id):

    return jsonify(get_follow(user_id))


@app.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
    payload = request.json
    insert_unfollow(payload)

    return '', 200


@app.route('/random-users/<int:user_id>', methods=['GET'])
@login_required
def random_users(user_id):
    return jsonify(get_random_users(user_id))


@app.route('/timeline', methods=['GET'])
@login_required
def timeline():
    search_data = request.args
    user_id = search_data.get('user_id')
    keyword = search_data.get('keyword')

    return jsonify({'timeline': get_timeline(user_id, keyword)})


@app.route('/my-timeline/<int:user_id>', methods=['GET'])
@login_required
def my_timeline(user_id):
    return jsonify({
        'timeline': get_my_timeline(user_id)
    })


@app.route('/user/<key>', methods=['GET'])
@login_required
def user_key(key):

    return jsonify(get_search_user(key))


@app.route('/like', methods=['POST'])
@login_required
def like():
    payload = request.json

    return jsonify(likes(payload))


@app.route('/trend', methods=['GET'])
def trend():
    return get_trend()


@app.route('/single-chat', methods=['POST'])
@login_required
def post_single_chat():
    payload = request.json
    validation_chat = validation_single_chat(payload)

    if validation_chat:
        return '이미 생성된 채팅입니다.', 200
    else:
        return jsonify({'sc_id': create_single_chat(payload)})



@app.route('/single-chat/<int:user_id>', methods=['GET'])
@login_required
def single_chat(user_id):

    return jsonify({'chats': get_single_chat(user_id)})


@app.route('/message', methods=['POST', 'GET', 'DELETE'])
@login_required
def message():
    if request.method == 'POST':
        payload = request.json
        app.database.execute(text("""
            INSERT INTO single_chat_msg (user_id, message, sc_id)
            VALUE (:user_id, :message, :sc_id)
        """), payload)

        return '', 200

    if request.method == 'GET':
        sc_id = request.args.get('sc_id')

        messages = app.database.execute(text(f"""
            SELECT scm.m_id, scm.created_at, scm.message, u.user_id, u.name, u.profile_image
            FROM users u, single_chat_msg scm
            WHERE scm.user_id = u.user_id AND scm.sc_id = {sc_id}
            ORDER BY scm.m_id ASC
        """)).fetchall()

        if len(messages) == 0:
            return 'no messages', 200

        else:
            return jsonify([{
                'm_id': msg['m_id'],
                'created_at': (msg['created_at']).strftime('%Y/%m/%dT%p %I:%M'),
                'message': msg['message'],
                'user_id': msg['user_id'],
                'name': msg['name'],
                'profile_img': msg['profile_image']
                } for msg in messages])

    if request.method == 'DELETE':
        m_id = request.args.get('m_id')
        app.database.execute(text(f"""
            DELETE FROM single_chat_msg WHERE m_id={m_id}
        """))

        return '', 200


#
# @app.route('/message', methods=['GET'])
# @login_required
# def get_message():
#


@app.route('/room/<int:user_id>', methods=['GET'])
def get_room(user_id):
    room = get_room(user_id)

    return jsonify({
        ''
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)