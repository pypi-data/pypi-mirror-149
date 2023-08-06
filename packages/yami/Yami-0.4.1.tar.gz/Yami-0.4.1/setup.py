# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yami', 'yami.utils']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['hikari==2.0.0.dev108']

extras_require = \
{'speedups': ['aiodns>=3.0,<4.0',
              'cchardet>=2.1,<3.0',
              'brotli>=1.0,<2.0',
              'ciso8601>=2.2,<3.0']}

entry_points = \
{'console_scripts': ['yami = yami._cli:info']}

setup_kwargs = {
    'name': 'yami',
    'version': '0.4.1',
    'description': 'A command handler that complements Hikari.',
    'long_description': '<h1 align="center">Yami</h1>\n<p align="center">A command handler that complements Hikari. <3</p>\n<p align="center">\n<a href="https://pepy.tech/project/yami"><img height="20" alt="Downloads" src="https://static.pepy.tech/personalized-badge/yami?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads"></a>\n<a href="https://python.org"><img height="20" alt="Python versions" src="https://img.shields.io/pypi/pyversions/yami?label=Python&logo=python"></a>\n</p>\n<p align="center">\n<a href="https://github.com/Jonxslays/Yami/blob/master/LICENSE"><img height="20" alt="License" src="https://img.shields.io/pypi/l/yami?label=License"></a>\n<a href="https://pypi.org/project/yami"><img height="20" alt="Stable version" src="https://img.shields.io/pypi/v/yami?label=Stable&logo=pypi"></a>\n</p>\n<p align="center">\n<a href="https://github.com/Jonxslays/Yami"><img height="20" alt="Last Commit" src="https://img.shields.io/maintenance/yes/2022?label=Maintained"></a>\n<a href="https://github.com/Jonxslays/Yami"><img height="20" alt="Last Commit" src="https://img.shields.io/github/last-commit/jonxslays/yami?label=Last%20Commit&logo=git"></a>\n\n<p align="center">\n<a href="https://github.com/Jonxslays/Yami/actions/workflows/ci.yml"><img height="20" alt="Last Commit" src="https://img.shields.io/github/workflow/status/Jonxslays/Yami/CI?label=Build&logo=github"></a>\n<a href="https://codeclimate.com/github/Jonxslays/Yami"><img height="20" alt="Last Commit" src="https://img.shields.io/codeclimate/coverage/Jonxslays/Yami?label=Coverage&logo=Code%20Climate"></a>\n</p>\n\n---\n\n## Disclaimer\n\nStill in early development. See the [TODO list](#TODO).\n\n## Documentation\n\n- [Stable](https://jonxslays.github.io/Yami)\n- [Development](https://jonxslays.github.io/Yami/master)\n\n## Getting started with Yami\n\nStable release\n\n```bash\npip install yami\n```\n\nDevelopment\n\n```bash\npip install git+https://github.com/Jonxslays/Yami.git\n```\n\n#### Creating a Bot\n\n```py\nimport asyncio\nimport datetime\nimport functools\nimport os\nimport typing\n\nimport hikari\nimport yami\n\nbot = yami.Bot(os.environ["TOKEN"], prefix="$")\n\n\n# Can only be run in guilds.\n@yami.is_in_guild()\n@bot.command("add", "Adds 2 numbers", aliases=["sum"])\nasync def add_cmd(ctx: yami.MessageContext, num1: int, num2: int) -> None:\n    # Basic builtin python types are converted for you using their type\n    # hints (int, float, bool, complex, bytes). More types coming soon™.\n    await ctx.respond(f"The sum is {num1 + num2}")\n\n\n# Can only be run by members with one of these roles.\n@yami.has_any_role("Admin", "Fibonacci")\n@bot.command("fibonacci", aliases=("fib",))\nasync def fibonacci(ctx: yami.MessageContext, num: int) -> None:\n    """Calculates the num\'th term in the fibonacci sequence."""\n    calc: typing.Callable[[int], int] = functools.lru_cache(\n        lambda n: n if n < 2 else calc(n - 1) + calc(n - 2)\n    )\n\n    # Though we cache the function call, let\'s simulate thinking.\n    async with ctx.trigger_typing():\n        await asyncio.sleep(0.75)\n\n    # Make a pretty embed.\n    await ctx.respond(\n        hikari.Embed(\n            title=f"Fibonacci calculator",\n            description=f"```{calc(num)}```",\n            color=hikari.Color(0x8AFF8A),\n            timestamp=datetime.datetime.now(tz=datetime.timezone.utc),\n        )\n        .set_footer(f"Term {num}")\n        .set_author(\n            name=(author := ctx.author).username,\n            icon=author.avatar_url or author.default_avatar_url,\n        )\n    )\n\n\nif __name__ == "__main__":\n    bot.run()\n```\n\n## TODO\n\n<div class="todolist" after=>\n<div class="todocolumn">\n\n<details>\n<summary> :heavy_check_mark: Complete</summary>\n\n- [x] CI\n- [x] Testing (WIP)\n- [x] Fully typed\n- [x] Bot\n- [x] Message Commands\n- [x] Message Subcommands\n- [x] Message Context\n- [x] Modules\n- [x] Exceptions (WIP)\n- [x] Checks (WIP)\n- [x] Basic arg parsing (builtin types)\n- [x] Docs\n- [x] Events (Mostly)\n\n</details>\n</div>\n\n<div class="todocolumn">\n\n<details>\n<summary> :x: Incomplete</summary>\n\n- [ ] Module listeners\n- [ ] Hooks?\n- [ ] Slash Commands\n- [ ] Slash Context\n- [ ] Converters (WIP)\n- [ ] Utils (WIP)\n- [ ] Full blown arg parsing (hikari types)\n- [ ] QOL methods (WIP)\n- [ ] Logging (WIP)\n\n</details>\n</div>\n</div>\n\n---\n\n## Contributing\n\nYami is open to contributions. To get started check out the\n[contributing guide](https://github.com/Jonxslays/Yami/blob/master/CONTRIBUTING.md).\n\n## License\n\nYami is licensed under the [GPLV3](https://github.com/Jonxslays/Yami/blob/master/LICENSE) license.\n',
    'author': 'Jonxslays',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jonxslays/Yami',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
