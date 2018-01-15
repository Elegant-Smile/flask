from flask import Flask, jsonify, abort
from flask_script import Manager

posts = [
    {
        'id': 1,
        'title': 'Python语法',
        'content': 'python语法很简单，但是每次问题都出现在语法上'
    },
    {
        'id': 2,
        'title': 'HTML',
        'content': '不就是几个标签的问题嘛，但是要细心点'
    }
]

app = Flask(__name__)
manager = Manager(app)


@app.route('/posts')
def get_post_list():
    return jsonify({"posts": posts})


@app.route('/')
def index():
    return 'REstFUl API 开发测试'


@app.route('/posts/<int:pid>')
def get_posts(pid):
    #lambda 变量: 要执行的语句,作用和def类似，但是有很多细微的差别
    #filter()函数接收一个函数 f 和一个list，# 这个函数 f 的作用是对每个元素进行判断，
    # 返回 True或 False，filter()根据判断结果自动过滤掉不符合条件的元素，返回由符合条件元素组成的新list
    p = list(filter(lambda p: p['id'] == pid, posts))
    if len(p) == 0:
        abort(404)
        #前后台通过接口交互时，返回给前台json格式数据时可以使用jsonify
    return jsonify({'posts': p[0]})


if __name__ == '__main__':
    manager.run()
