# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybotx_fsm']

package_data = \
{'': ['*']}

install_requires = \
['pybotx>=0.32.0,<0.40.0']

setup_kwargs = {
    'name': 'pybotx-fsm',
    'version': '0.3.7',
    'description': 'FSM middleware for using with pybotx',
    'long_description': '# pybotx-fsm\n\n[![codecov](https://codecov.io/gh/ExpressApp/pybotx-fsm/branch/master/graph/badge.svg?token=JWT9JWU2Z4)](https://codecov.io/gh/ExpressApp/pybotx-fsm)\n\nКонечный автомат (Finite state machine) для ботов на базе библиотеки\n[pybotx](https://github.com/ExpressApp/pybotx).\n\n\n## Возможности\n\n* Лёгкое создание графа состояний и их переключений.\n* Передача данных в следующее состояние при явном вызове перехода.\n\n\n## Подготовка к установке\n\nДля работы библиотеки необходим Redis, который уже встроен в последние версии\n[коробки](https://github.com/ExpressApp/async-box).\n\n\n## Установка\n\nДобавьте эту строку в зависимости проекта в `pyproject.toml`:\n\n```toml\nbotx-fsm = { git = "https://github.com/ExpressApp/pybotx-fsm", rev = "0.2.0" }\n```\n\n## Работа с графом состояний\n\n1. Добавьте экземпляр автомата в мидлвари для того, чтобы бот мог использовать его:\n\n``` python\nBot(\n    collectors=...,\n    bot_accounts=...,\n    middlewares=[FSMMiddleware([myfile.fsm], state_repo_key="redis_repo")],\n)\n```\n\n2. Добавьте в `bot.state.{state_repo_key}` совместимый redis репозиторий:\n\n``` python\nbot.state.redis_repo = await RedisRepo.init(...)\n```\n\n3. Создайте `enum` для возможных состояний автомата:\n\n``` python\nfrom enum import Enum, auto\nfrom pybotx_fsm import FSMCollector\n\n\nclass LoginStates(Enum):\n    enter_email = auto()\n    enter_password = auto()\n\n\nfsm = FSMCollector(LoginStates)\n```\n\n4. Создайте обработчики конкретных состояний:\n\n``` python\n@fsm.on(LoginStates.enter_email)\nasync def enter_email(message: IncomingMessage, bot: Bot) -> None:\n    email = message.body\n\n    if not check_user_exist(email):\n        await bot.answer_message("Wrong email, try again")\n        return\n\n    await message.state.fsm.change_state(LoginStates.enter_password, email=email)\n    await bot.answer_message("Enter your password")\n\n\n@fsm.on(LoginStates.enter_password)\nasync def enter_password(message: IncomingMessage, bot: Bot) -> None:\n    email = message.state.fsm_storage.email\n    password = message.body\n\n    try:\n        login(email, password)\n    except IncorrectPasswordError:\n        await bot.answer_message("Wrong password, try again")\n        return\n\n    await message.state.fsm.drop_state()\n    await bot.answer_message("Success!")\n\n```\n\n5. Передайте управление обработчику состояний из любого обработчика сообщений:\n\n``` python\n@collector.handler(command="/login")\nasync def start_login(message: IncomingMessage, bot: Bot) -> None:\n    await bot.answer_message("Enter your email")\n    await fsm.change_state(LoginStates.enter_email)\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
