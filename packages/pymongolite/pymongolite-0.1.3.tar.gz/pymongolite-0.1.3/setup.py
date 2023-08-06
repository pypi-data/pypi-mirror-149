# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymongolite',
 'pymongolite.backend',
 'pymongolite.backend.execution_engine',
 'pymongolite.backend.indexing_engine',
 'pymongolite.backend.storage_engine']

package_data = \
{'': ['*']}

install_requires = \
['blist>=1.3.6,<2.0.0']

setup_kwargs = {
    'name': 'pymongolite',
    'version': '0.1.3',
    'description': '',
    'long_description': '# mongolite \nLite mongodb engine in python  \n\n[![Run Tests](https://github.com/hvuhsg/mongolite/actions/workflows/test.yml/badge.svg)](https://github.com/hvuhsg/mongolite/actions/workflows/test.yml)  \n\n---\n\n```commandline\npip install pymongolite\n```\n\n## Examples\n\n```python\nfrom pymongolite import MongoClient\n\nwith MongoClient(dirpath="~/my_db_dir", database="my_db") as client:\n    db = client.get_default_database()\n    collection = db.get_collection("users")\n\n    collection.insert_one({"name": "yoyo"})\n    collection.update_one({"name": "yoyo"}, {"$set": {"age": 20}})\n    user = collection.find_one({"age": 20})\n    print(user) # -> {"_id": ObjectId(...), "name": "yoyo", "age": 20}\n```\n\n```python\nfrom pymongolite import MongoClient\n\nclient = MongoClient(dirpath="~/my_db_dir", database="my_db")\n\ndb = client.get_default_database()\ncollection = db.get_collection("users")\n\ncollection.insert_one({"name": "yoyo"})\ncollection.update_one({"name": "yoyo"}, {"$set": {"age": 20}})\nuser = collection.find_one({"age": 20})\nprint(user) # -> {"_id": ObjectId(...), "name": "yoyo", "age": 20}\n\nclient.close()\n```\n\n#### Indexes\n```python\nfrom pymongolite import MongoClient\n\nclient = MongoClient(dirpath="~/my_db_dir", database="my_db")\n\ndb = client.get_default_database()\ncollection = db.get_collection("users")\n\n# Make query with name faster\ncollection.create_index({"name": 1})\n\ncollection.insert_one({"name": "yoyo"})\ncollection.update_one({"name": "yoyo"}, {"$set": {"age": 20}})\nuser = collection.find_one({"age": 20})\nprint(user) # -> {"_id": ObjectId(...), "name": "yoyo", "age": 20}\n\nindexes = collection.get_indexes()\nprint(indexes)  # -> [{\'id\': UUID(\'8bb4cac8-ae52-4fff-9e69-9f36a99956cd\'), \'field\': \'age\', \'type\': 1, \'size\': 1}]\n\nclient.close()\n```\n\n## Support\nThe goal of this project is to create sqlite version for mongodb\n\nFor now the library is supporting:\n- insert_many / insert_one\n- update_many / update_one\n    - $set\n    - $unset\n    - $inc\n    - $addToSet\n      - $each\n    - $push\n      - $each\n      - $sort\n      - $slice\n    - $pull\n- find / find_one\n    - field matching\n    - $eq\n    - $ne\n    - $gt / $gte\n    - $lt / $lte\n    - $not\n    - $and\n    - $or\n    - $nor\n    - $exists\n    - $in\n    - $nin\n    - filter fields\n- replace_many / replace_one\n- create_collection\n- get_collection\n- drop_collection\n- create_database\n- drop_database\n- thread safety\n- replaceable storage engine\n',
    'author': 'yehoyada',
    'author_email': 'yehoyada.sht@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
