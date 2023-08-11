# -*-coding:utf-8-*-
# @Author: XuCheng
# @Time:2023-7-21

import random
import time
from flask import Flask, render_template, request, url_for
import json

app = Flask(__name__)

with open('data/jx.json', mode='r', encoding="utf-8") as f:
    data = json.loads(f.read())

with open('data/data.json', mode='r', encoding="utf-8") as f:
    database = json.loads(f.read())


def append_data(id_name, num):
    if id_name in database:
        database[id_name] += num
    else:
        database[id_name] = num


def choice_ans(name_id):
    num = random.random()
    strs = "恭喜" + name_id + "用户获得"
    if num <= 0.01 and data['一等奖'] > 0:
        strs += '一等奖'
        data['一等奖'] -= 1
    elif 0.1 >= num > 0.01 and data['二等奖'] > 0:
        strs += '二等奖'
        data['二等奖'] -= 1
    elif 0.3 >= num > 0.1 and data['三等奖'] > 0:
        strs += '三等奖'
        data['三等奖'] -= 1
    else:
        strs += '特殊奖'
    return strs


def get_log(strs):
    tm = str(time.localtime()[3]) + '-' + str(time.localtime()[4]) + '-' + str(time.localtime()[5])
    with open('get.log', mode='a', encoding='utf-8') as f:
        f.write(tm + ' ' + strs + '\n')


def log(strs):
    tm = str(time.localtime()[3]) + '-' + str(time.localtime()[4]) + '-' + str(time.localtime()[5])
    with open('log.log', mode='a', encoding='utf-8') as f:
        f.write(tm + ' ' + strs + '\n')


@app.route('/')
def index():
    url_for('static', filename='style.css')
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        if request.form['username'] == 'admin' and request.form['password'] == '2580':
            return append()
        else:
            return render_template('login.html')


@app.route('/contact')
def contact():
    url_for('static', filename='style.css')
    return render_template('contact.html')


@app.route('/choice', methods=['GET', 'POST'])
def choice():
    url_for('static', filename='back_for_choice.png')
    if request.method == 'POST':
        if request.form['id'] not in database:
            error = "该账号不存在"
            return render_template('answer.html', ans=error)
        else:
            if database[request.form['id']] >= 3:
                database[request.form['id']] -= 3
                with open('data/jx.json', mode='w', encoding="utf-8") as f:
                    f.write(json.dumps(data))
                ans = choice_ans(request.form['id'])
                log(strs=ans)
                return render_template('answer.html', ans=ans)
            else:
                error = "积分不足"
                return render_template('answer.html', ans=error)
    return render_template('choice.html')


@app.route('/append', methods=['GET', 'POST'])
def append():
    if request.method == 'POST':
        try:
            num = int(request.form['num'])
            append_data(request.form['id'], num)
            strs = request.form['id'] + "获得了" + request.form['num'] + "积分"
            get_log(strs)
            with open('data/data.json', mode='w', encoding="utf-8") as f:
                f.write(json.dumps(database))
            return render_template('answer.html', ans="添加成功")
        except:
            return render_template('answer.html', ans="添加失败，请重试")
    return render_template('append.html')


@app.route('/show')
def show():
    url_for('static', filename='style_for_show.css')
    url_for('static', filename='script_for_show.js')
    return render_template('show.html')


@app.route('/about')
def about():
    url_for('static', filename='style.css')
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
