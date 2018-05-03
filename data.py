articles = []
def add_single_article(title, body, author):
    article = {}
    article_count = len(articles) + 1
    article['id'] = article_count
    article['title'] = title
    article['body'] = body
    article['author'] = author
    articles.append(article)

def get_article(id):
    for every_article in articles:
        values = every_article.values()
        if id in values:
            return every_article

def get_all_articles():
    return articles

def update_article(id, title, body):
    for every_article in articles:
        values = every_article.values()
        if id in values:
            every_article['title'] = title
            every_article['body'] = body

def delete_article_id(id):
    articles[:] = [list_value for list_value in articles if list_value.get('id') != id]
    id = 1
    for article in articles:
        article['id'] = id
        id += 1

def Articles():
    articles = [
            {
                'id' : 1,
                'title' : 'Article One',
                'body' : 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                'author' : 'Traversy Media',
                'create_date' : '25-04-2018'
            },
            {
                'id' : 2,
                'title' : 'Article Two',
                'body' : 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                'author' : 'Nitin Singhal',
                'create_date' : '25-04-2018'
            },
            {
                'id' : 3,
                'title' : 'Article Three',
                'body' : 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
                'author' : 'ABC DEF',
                'create_date' : '25-04-2018'
            }
    ]
    return articles
