import time
import sys

from scheduler import *
from configmanager import config
from autoblog import * 

scheduler = Scheduler()
scheduler.start(config['blog_posts_per_wk'])  # Schedules the task to run every x times per week

def _get_articles():
    return get_articles(config['shopify_store'], config['shopify_access_token'], config['shopify_blog_id'])

try:
    print(_get_articles())
    while True:
        time.sleep(1) 
except KeyboardInterrupt:
    print("Program terminated by user.")
    scheduler.stop()  # Stop the scheduler if you have a stop method

# ############## config API ##############
# @app.route('/config', methods=['GET'])
# def get_config():
#     global config
#     config = ConfigManager().read_config()
#     return jsonify(config)

# @app.route('/config', methods=['POST'])
# def update_config():
#     data = request.json
#     if not data:
#         return jsonify({"error": "No data provided"}), 400

#     ConfigManager().write_config(data)
#     global config
#     config = ConfigManager().read_config()

#     scheduler.edit_interval("AutoBlog", config['blog_posts_per_wk'])

#     return jsonify({"message": "Config replaced successfully"})

# ############## task API ##############
# @app.route('/getTasks', methods=['GET'])
# def get_tasks():
#     status = scheduler.get_status()
#     return jsonify(status)


# ############## blog API ##############
# @app.route('/getBlogs', methods=['GET'])
# def get_blogs():
#     return get_shop_blogs(config['shopify_store'], config['shopify_access_token'])

# @app.route('/deleteArticle', methods=['POST'])
# def _delete_article():
#     blogId = request.args.get('blogId')
#     articleId = request.args.get('articleId')

#     return delete_article(config['shopify_store'], config['shopify_access_token'], articleId, blogId)

# @app.route('/getArticles', methods=['GET'])
# def _get_articles():
#     return get_articles(config['shopify_store'], config['shopify_access_token'], config['shopify_blog_id'])

# @app.route('/postBlog', methods=['GET'])
# def _post_blog():
#     return post_blog(config['shopify_store'], config['shopify_access_token'], config['neetsai_api_key'], config['shopify_blog_id'])

# ############## orders API ##############
# @app.route('/getOrders', methods=['GET'])
# def _get_orders():
#     return get_orders(config['shopify_store'], config['shopify_access_token'])