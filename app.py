from os import environ
from flask import Flask, Response, jsonify, request, url_for, redirect
from textwrap import dedent
from werkzeug.exceptions import NotFound

app = Flask(__name__)


def html(head, body=None):
    if body is None:
        head, body = None, head  # Support html(body) invocations.
    return dedent('''
        <html><head>
            {head}
        </head><body>
            {body}
        </body></html>
    '''.lstrip('\n').format(head=head or '', body=body or ''))


def text(body, status_code=200):
    return Response(mimetype='text/plain', status_code=status_code,
                    response=dedent(body.lstrip('\n')))


@app.route("/")
def index():
    return html('''
        <h1>It works!</h1>
        <a href="about">About</a>
        <a href="http://twitter.com/paulscott">External link.</a>
    ''')


if 'NOROBOTS' not in environ:
    @app.route("/robots.txt")
    def robots():
        return text('''
            Disallow: *
        ''')


@app.route("/about")
def about():
    return html('''
        <p>This application serves as a collection of pages with different
           linking characteristics in order to test crawlers.</p>
        <p><a href="">Back to index.</a></p>
    ''')


@app.route("/blog/<int:post>")
def blog(post):
    posts = {1: 'Post A', 2: 'Post B', 3: 'Post C',
             4: 'Post D', 5: 'Post E', 6: 'Post F'}
    if post not in posts:
        raise NotFound()

    # No quotes.
    p = '<a href=/blog/%d>Prev</a>' % (post - 1) if post > 1 else ''
    # Single quotes. Missing leading slash. <base /> should take care of it.
    n = "<a href='blog/%d'>Next</a>" % (post + 1) if post < 6 else ''

    # Absolute-path base.
    return html('<base href="/">', '''
        <h1>{content}</h1>
        {p} {n}
    '''.format(content=posts[post], p=p, n=n))


@app.route("/redirect")
def index_redirect():
    try:
        count = int(request.args.get('count', '0'))
    except ValueError:
        count = 0

    if count > 0:
        return redirect(url_for('index_redirect', count=count - 1))
    else:
        return redirect('')


@app.route("/json")
def json():
    return jsonify(x=10, y=20)


if __name__ == "__main__":
    app.run(use_reloader=True, debug=False)
