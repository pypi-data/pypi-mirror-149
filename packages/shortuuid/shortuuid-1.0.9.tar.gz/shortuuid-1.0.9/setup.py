# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shortuuid']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['shortuuid = shortuuid:cli.main']}

setup_kwargs = {
    'name': 'shortuuid',
    'version': '1.0.9',
    'description': 'A generator library for concise, unambiguous and URL-safe UUIDs.',
    'long_description': 'Description\n===========\n\n`shortuuid` is a simple python library that generates concise, unambiguous, URL-safe\nUUIDs.\n\nOften, one needs to use non-sequential IDs in places where users will see them, but the\nIDs must be as concise and easy to use as possible.  `shortuuid` solves this problem by\ngenerating uuids using Python\'s built-in `uuid` module and then translating them to\nbase57 using lowercase and uppercase letters and digits, and removing similar-looking\ncharacters such as l, 1, I, O and 0.\n\n[![image](https://travis-ci.org/skorokithakis/shortuuid.svg?branch=master)](https://travis-ci.org/skorokithakis/shortuuid)\n\n\nInstallation\n------------\n\nTo install `shortuuid` you need:\n\n-   Python 3.x.\n\nIf you have the dependencies, you have multiple options of installation:\n\n-   With pip (preferred), do `pip install shortuuid`.\n-   With setuptools, do `easy_install shortuuid`.\n-   To install the source, download it from\n    https://github.com/stochastic-technologies/shortuuid and run `python setup.py\n    install`.\n\n\nUsage\n-----\n\nTo use `shortuuid`, just import it in your project like so:\n\n```python\n>>> import shortuuid\n```\n\nYou can then generate a short UUID:\n\n```python\n>>> shortuuid.uuid()\n\'vytxeTZskVKR7C7WgdSP3d\'\n```\n\nIf you prefer a version 5 UUID, you can pass a name (DNS or URL) to the call and it will\nbe used as a namespace (`uuid.NAMESPACE_DNS` or `uuid.NAMESPACE_URL`) for the resulting\nUUID:\n\n```python\n>>> shortuuid.uuid(name="example.com")\n\'exu3DTbj2ncsn9tLdLWspw\'\n\n>>> shortuuid.uuid(name="<http://example.com>")\n\'shortuuid.uuid(name="<http://example.com>")\'\n```\n\nYou can also generate a cryptographically secure random string (using `os.urandom()`\ninternally) with:\n\n```python\n>>> shortuuid.ShortUUID().random(length=22)\n\'RaF56o2r58hTKT7AYS9doj\'\n```\n\nTo see the alphabet that is being used to generate new UUIDs:\n\n```python\n>>> shortuuid.get_alphabet()\n\'23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz\'\n```\n\nIf you want to use your own alphabet to generate UUIDs, use `set_alphabet()`:\n\n```python\n>>> shortuuid.set_alphabet("aaaaabcdefgh1230123")\n>>> shortuuid.uuid()\n\'0agee20aa1hehebcagddhedddc0d2chhab3b\'\n```\n\n`shortuuid` will automatically sort and remove duplicates from your alphabet to ensure\nconsistency:\n\n```python\n>>> shortuuid.get_alphabet()\n\'0123abcdefgh\'\n```\n\nIf the default 22 digits are too long for you, you can get shorter IDs by just\ntruncating the string to the desired length. The IDs won\'t be universally unique any\nlonger, but the probability of a collision will still be very low.\n\nTo serialize existing UUIDs, use `encode()` and `decode()`:\n\n```python\n>>> import uuid\n>>> u = uuid.uuid4()\n>>> u\nUUID(\'6ca4f0f8-2508-4bac-b8f1-5d1e3da2247a\')\n\n>>> s = shortuuid.encode(u)\n>>> s\n\'MLpZDiEXM4VsUryR9oE8uc\'\n\n>>> shortuuid.decode(s) == u\nTrue\n\n>>> short = s[:7]\n>>> short\n\'MLpZDiE\'\n\n>>> h = shortuuid.decode(short)\nUUID(\'00000000-0000-0000-0000-009a5b27f8b9\')\n\n>>> shortuuid.decode(shortuuid.encode(h)) == h\nTrue\n```\n\n\nClass-based usage\n-----------------\n\nIf you need to have various alphabets per-thread, you can use the `ShortUUID` class,\nlike so:\n\n```python\n>>> su = shortuuid.ShortUUID(alphabet="01345678")\n>>> su.uuid()\n\'034636353306816784480643806546503818874456\'\n\n>>> su.get_alphabet()\n\'01345678\'\n\n>>> su.set_alphabet("21345687654123456")\n>>> su.get_alphabet()\n\'12345678\'\n```\n\n\nCommand-line usage\n------------------\n\n`shortuuid` provides a simple way to generate a short UUID in a terminal:\n\n```bash\n$ shortuuid\nfZpeF6gcskHbSpTgpQCkcJ\n```\n\n\nDjango field\n------------\n\n`shortuuid` includes a Django field that generates random short UUIDs by default, for\nyour convenience:\n\n```python\nfrom shortuuid.django_fields import ShortUUIDField\n\nclass MyModel(models.Model):\n    # A primary key ID of length 16 and a short alphabet.\n    id = ShortUUIDField(\n        length=16,\n        max_length=40,\n        prefix="id_",\n        alphabet="abcdefg1234",\n        primary_key=True,\n    )\n\n    # A short UUID of length 22 and the default alphabet.\n    api_key = ShortUUIDField()\n```\n\nThe field is the same as the `CharField`, with a `length` argument (the length of the\nID), an `alphabet` argument, and the `default` argument removed. Everything else is\nexactly the same, e.g. `index`, `help_text`, `max_length`, etc.\n\n\nCompatibility note\n------------------\n\nVersions of ShortUUID prior to 1.0.0 generated UUIDs with their MSB last, i.e. reversed.\nThis was later fixed, but if you have some UUIDs stored as a string with the old method,\nyou need to pass `legacy=True` to `decode()` when converting your strings back to UUIDs.\n\nThat option will go away in the future, so you will want to convert your UUIDs to\nstrings using the new method. This can be done like so:\n\n```python\n>>> new_uuid_str = encode(decode(old_uuid_str, legacy=True))\n```\n\nLicense\n-------\n\n`shortuuid` is distributed under the BSD license.\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skorokithakis/shortuuid/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
