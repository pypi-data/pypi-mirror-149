# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coveo_styles']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1', 'emoji', 'typing_extensions']

setup_kwargs = {
    'name': 'coveo-styles',
    'version': '2.1',
    'description': 'Styles, colors and emojis for the command line.',
    'long_description': '# coveo-styles\n\nDon\'t let your CLI app spit out hundreds of boring lines!\n\nManage your user feedback a bit like you manage logs, and get bonus colors and emojis just because we can!\n\nThis module provides an `echo` symbol that you can use instead of `print` for convenience.\n\nIt is also completely customizable!\n\n\n## predefined themes for common actions\n\nHere\'s how a ci run could look like:\n\n```python\nfrom coveo_styles.styles import echo\n\necho.step("Launching ci operations")\necho.normal("pytest", emoji=\'hourglass\')\necho.normal("black", emoji=\'hourglass\')\necho.noise("Generated test reports in .ci/")\necho.success()\necho.warning("Formatting errors detected")\necho.suggest("The --fix switch will automatically fix these for you and re-run the test !!smile!!")\necho.error("The CI run detected errors you need to fix", pad_after=False)\necho.error_details("Black reported files to reformat", item=True)\necho.error_details("Details as items is nice!", item=True)\n```\n\n\n```\nLaunching ci operations\n\n⌛ pytest\n⌛ black\nGenerated test reports in .ci/\n\n✔ Success!\n\n\n⚠ Formatting errors detected\n\n\n🤖 The --fix switch will automatically fix these for you and re-run the test 😄\n\n\n💥 The CI run detected errors you need to fix\n · Black reported files to reformat\n · Details as items is nice\n```\n\nIt\'s even nicer with colors! :) This doc needs a few animated gifs!\n\n\n\n# exception hook\n\nException handlers may re-raise an exception as an `ExitWithFailure` in order to hide the traceback from the user and show a helpful error message.\n\nHere\'s an example for the sake of demonstration:\n\n```python\nfrom pathlib import Path\nfrom coveo_styles.styles import ExitWithFailure\n\ntry:\n    project = Path(\'./project\').read_text()\nexcept FileNotFoundError as exception:\n    raise ExitWithFailure(suggestions=\'Use the --list switch to see which projects I can see\') from exception\n```\n\nThe stacktrace will be hidden, the app will exit with code 1 after printing the exception type and message:\n\n```\n! FileNotFoundError: [Errno 2] No such file or directory: \'project\'\n\n🤖 Use the --list switch to see which projects I can see\n```\n\nUnhandled exceptions (those that are not wrapped by an ExitWithFailure), will display the usual python feedback and stacktrace.\n\n\n\n# hunting for emojis\n\nEmoji support is provided by the [emoji](https://pypi.org/project/emoji/) package. \nTheir description provides different links to help with your emoji hunt, but for some reason not everything is supported or has the name it should have.\n\nThe only foolproof way I have found is to actually inspect the `emoji` package, either by opening `site-packages/emoji/unicode_codes/en.py` in my IDE or programmatically like this:\n\n```python\nfrom coveo_styles.styles import echo\nfrom emoji.unicode_codes.en import EMOJI_UNICODE_ENGLISH, EMOJI_ALIAS_UNICODE_ENGLISH\n\nquery = \'smile\'.lower()\n\nfor emoji_name in {*EMOJI_UNICODE_ENGLISH, *EMOJI_ALIAS_UNICODE_ENGLISH}:\n    emoji_name = emoji_name.strip(\':\')\n    if query in emoji_name.lower():\n        echo.normal(f\'{emoji_name}: !!{emoji_name}!!\')\n```\n\n```\nsweat_smile: 😅\ncat_face_with_wry_smile: 😼\nsmile: 😄\nsmiley: 😃\nsmiley_cat: 😺\nsmile_cat: 😸\n```\n',
    'author': 'Jonathan Piché',
    'author_email': 'tools@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coveooss/coveo-python-oss/tree/main/coveo-styles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
