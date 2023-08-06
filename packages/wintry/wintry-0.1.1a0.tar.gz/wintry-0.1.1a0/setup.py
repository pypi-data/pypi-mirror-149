# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wintry',
 'wintry.drivers',
 'wintry.errors',
 'wintry.mqs',
 'wintry.query',
 'wintry.repository',
 'wintry.transactions',
 'wintry.utils']

package_data = \
{'': ['*']}

install_requires = \
['Inject>=4.3.1,<5.0.0',
 'dataclass-wizard>=0.22.0,<0.23.0',
 'fastapi>=0.75.2,<0.76.0',
 'motor>=2.5.1,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pyee>=9.0.4,<10.0.0',
 'uvicorn>=0.17.6,<0.18.0']

extras_require = \
{'postgres': ['SQLAlchemy>=1.4.35,<2.0.0', 'asyncpg>=0.25.0,<0.26.0']}

setup_kwargs = {
    'name': 'wintry',
    'version': '0.1.1a0',
    'description': 'A Web Framework for you, the developer, in a clean way, a cool way',
    'long_description': '# Wintry ==> A new python web framework with cool features for ... everybody\n\n\n\n\n![](https://img.shields.io/static/v1?label=code&message=python&color=<blue>&style=plastic&logo=github&logoColor=4ec9b0)\n![](https://img.shields.io/static/v1?label=web&message=framework&color=<blue>&style=plastic&logo=github&logoColor=4ec9b0)\n![](https://img.shields.io/static/v1?label=Tests&message=Passing&color=<blue>&style=plastic&logo=github&logoColor=4ec9b0)\n![](https://img.shields.io/static/v1?label=pypi%20package&message=v0.1.0&color=<blue>&style=plastic&logo=github&logoColor=4ec9b0)\n\n\nHello, friend, welcome to Wintry. You may have stumble with this project searching\nfor a python web framework, well, you got what you want.\n\nPherhaps you know many other frameworks, pherhaps you know Django, or maybe Flask,\nor hopefully FastAPI. And odds are that you are willing to take a new project for a\nride with a new alternative. Well, Wintry is this, your new alternative, one that\ndo not push you out of your confort zone, but do not take the "written before" path.\n\nBeign accured, if you have used FastAPI, you would feel at home, Wintry is heavilly\ninspired in FastAPI, it actually uses it whenever it can. But it add a bunch of \n\'cool\' stuff on top.\n\nLet me tell you a story, that would give an idea from where this project come from.\n\n## Inspirations\n---------------\n\nI have used FastAPI a lot for the last year, and I am absolutely fascinated about it.\nSpeed + Python on the same sentence, that\'s something to really appreciate. I know, a big\nthanks to starlette project which is the real hero on that movie, but, FastAPI adds a ton\nof cool features on top, if I would describe them in one word, it would be: Pydantic.\n\nOk, but, Django has a lot of cool features too, it is even called \'Batteries included\nframework\', and it is true, I mean, who doesn\'t love the Django\'s builtin Admin Interface,\nor Django Forms?, not to mention DjangoRestFramework which is a REAALLY cool piece of software.\n\nEnough flattering, Wintry will try to be the new Kid in Town, to provide a DDD\nfocused experience, with builtin Dependency Injection system, a dataclasses based\nRepository Pattern implementation, Unit Of Work, Events Driven Components and a lot more.\nActually, I aimed to provide a similar experience with Repositories than that of\nSpring JPA. Just look at the example, it is really easy to write decoupled and modularized applications with **Wintry**.\n\nLet\'s see what **Wintry** looks like:\n\n```python\nfrom wintry.models import entity, fromdict\nfrom wintry.repository import Repository\nfrom wintry.controllers import controller, post, get\nfrom wintry.dependency_injection import provider\nfrom wintry.errors import NotFoundError\nfrom dataclasses import field\nfrom bson import ObjectId\nfrom pydantic import BaseModel\nfrom wintry import ServerTypes, Winter\nfrom wintry.settings import BackendOptions, ConnectionOptions, WinterSettings\n\n@entity(create_metadata=True)\nclass Hero:\n    city: str\n    name: str\n    id: str = field(default_factory=lambda: str(ObjectId()))\n\n@entity(create_metadata=True)\nclass Villain:\n    name: str\n    city: str\n    id: str = field(default_factory=lambda: str(ObjectId()))\n    hero: Hero | None = None\n\nclass HeroForm(BaseModel):\n    city: str\n    name: str\n\nclass HeroDetails(BaseModel):\n    name: str\n    id: str\n\n    class Config:\n        orm_mode = True\n\nclass VillainDetails(BaseModel):\n    name: str\n    id: str\n    hero: Hero | None = None\n\n    class Config:\n        orm_mode = True\n\n@provider\nclass HeroRepository(Repository[Hero, str], entity=Hero):\n    pass\n\n@provider\nclass VillainRepository(Repository[Villain, str], entity=Villain):\n    async def get_by_name(self, *, name: str) -> Villain | None:\n        ...\n\n@controller\nclass MarvelController:\n    def __init__(self, heroes: HeroRepository, villains: VillainRepository):\n        self.heroes = heroes\n        self.villains = villains\n\n    @post(\'/hero\', response_model=HeroDetails)\n    async def save_hero(self, hero_form: HeroForm = Body(...)):\n        hero = fromdict(hero_form.dict())\n        await self.heroes.create(hero)\n        return hero\n\n    @get(\'/villain/{name}\', response_model=VillainDetails)\n    async def get_villain(self, name: str):\n        villain = await self.villains.get_by_name(name=name)\n        if villain is None:\n            raise NotFoundError()\n\n        return villain\n\n\nsettings = WinterSettings(\n    backends=[\n        BackendOptions(\n            connection_options=ConnectionOptions(\n                url="postgresql+asyncpg://postgres:secret@localhost/tests"\n            )\n        )\n    ],\n    app_root="test_app",\n    server_title="Testing Server API",\n    server_version="0.0.1",\n)\n\nWinter.setup(settings)\n\napi = Winter.factory(settings, server_type=ServerTypes.API)\n```\n\nNote that the method **get_by_name** is NOT IMPLEMENTED, but it somewhow still works :). The thing is Repositories are query compilers,\nand you dont need to implement them, only learn a very simple\nquery syntax. That\'s not the only thing, the **@provider** decorator\nallows the repositories to be injected inside the marvel controller\nconstructor, just like happens in .NET Core or Java Spring.\n\nNote that my Hero and Villain entities, does not contain anything special, they are merely dataclasses (That\'s the only restriction, models needs to be dataclasses), and the relation is being automatically build for us. We even get an instance of **Hero** when\nwe call **get_villain** if the **Villain** has any **Hero** assigned.\n\nFuthermore, if I want to change to use **MongoDB** instead of **Postgres**, is as easy as\nto change the configuration url, and THERE IS NO NEED TO CHANGE THE CODE,\nit would just work. In fact, for consistency, the only recomended change to the code would\nbe to remove the create_metadata=True from the @entity decorator:\n\n```python\n\n...\n\n@entity\nclass Hero:\n    ...\n\n@entity\nclass Villain:\n    ...\n\n...\n```\n\nYou can look for a complete example under [test_app](https://github.com/adriangs1996/winter/tree/master/test_app)\n\n## Installation\n---------------\nAs simple as use\n\n```\n$ pip install wintry\n```\n\nor with poetry\n\n```\n$ poetry add wintry\n```\n\n## Features\n-----------\nThere is a lot more to know about Wintry:\n\n* Stack of patterns (RepositoryPattern, UnitOfWork, ProxyPattern,\nMVC, Event-Driven-Desing,\nCQRS, etc.)\n\n* Automatic Relational Database metadata creation\n\n* Automatic Query Creation\n\n* Reactive Domain Models\n\n* Dependency Injection\n\n* Publisher Subscribers\n\n* Services\n\n* Everything from FastAPI y a really confortable way\n\n* Settings based on Pydantic\n\nThis is the continuation of NEXTX, which would be deprecated\nin favor of this\n\n## ROADMAP\n----------\n* Create documentation\n\n* Add more features to the feature list with links to\nthe corresponding documentation\n\n* Add RPC support (Maybe protobuf, raw TCP, Redis, RabbitMQ, Kafka, etc)\n\n* Ease registration of Middlewares\n\n* Provide Implementation of Authorization Services\n\n* Create CLI for managing project\n\n* Provide Support for migrations (from the cli)\n\n* Templates\n\n* Maybe some ViewEngine (Jinja, or we could go deep and try Brython ??? IDK)\n\n## Contributions\n----------------\n\nEvery single contribution is very appreciated. From ideas, issues,\nPR, criticism, anything you can imagine.\n\nIf you are willing to provide a PR for a feature, just try to\ngive at least some tests for the feature, I try my best\nmantaining a pool of tests that will be growing with time\n\n- [Issue Tracker](https://github.com/adriangs1996/winter/issues)\n\n- [Fork the repo, change it, and make a PR](https://github.com/adriangs1996/winter)\n\n## Thanks\n--------\nTo @tiangolo for the amazing [SQLModel](https://github.com/tiangolo/sqlmodel) and [FastAPI](https://github.com/tiangolo/fastapi)\n\nTo the amazing [Django Team](https://github.com/django/django)\n\nTo the Spring Project and [NestJS](https://nestjs.com/) for such amazing frameworks\n\n\nLicense\n-------\n\nThis project is licensed under the MIT License',
    'author': 'adriangs1996',
    'author_email': 'adriangonzalezsanchez1996@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://adriangs1996.github.io/wintry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
