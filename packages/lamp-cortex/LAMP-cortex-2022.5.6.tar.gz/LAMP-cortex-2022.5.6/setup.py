# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cortex',
 'cortex.primary',
 'cortex.raw',
 'cortex.secondary',
 'cortex.utils',
 'cortex.visualizations']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.3,<5.0',
 'LAMP-core>=2021.5.18,<2022.0.0',
 'altair>=4.1.0,<5.0.0',
 'compress-pickle>=2.0.1,<3.0.0',
 'fastdtw>=0.3.4,<0.4.0',
 'geopy>=2.1.0,<3.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pymongo>=4.1.1,<5.0.0',
 'pytz>=2021.1,<2022.0',
 'pyyaml>=5.4.1,<6.0.0',
 'scipy>=1.6.2,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'similaritymeasures>=0.4.4,<0.5.0',
 'sklearn>=0.0,<0.1',
 'statsmodels>=0.12.2,<0.13.0',
 'tzwhere>=3.0.3,<4.0.0']

entry_points = \
{'console_scripts': ['cortex = cortex.feature_types:_main']}

setup_kwargs = {
    'name': 'lamp-cortex',
    'version': '2022.5.6',
    'description': 'The Cortex data analysis toolkit for the LAMP Platform.',
    'long_description': '# Cortex data analysis pipeline for the LAMP Platform.\n\n## Overview\n\nThis API client is used to process and featurize data collected in LAMP. [Visit our documentation](https://docs.lamp.digital/data_science/cortex/getting-started) for more information about using cortex and the LAMP API.\n\n### Jump to:\n\n- [Setting up Cortex](#setting_up_cortex)\n- [Cortex example](#example_cortex_query)\n- [Find a bug?](#bug_report)\n- [Developing Cortex](#cortex_dev)\n- [Command-line usage](#advanced)\n\n<a name="setting_up_cortex"></a>\n# Setting up Cortex\n\nYou will need Python 3.4+ and `pip` installed in order to use Cortex. \n  - You may need root permissions, using `sudo`.\n  - Alternatively, to install locally, use `pip --user`.\n  - If `pip` is not recognized as a command, use `python3 -m pip`.\n\nIf you meet the prerequisites, install Cortex:\n\n```sh\npip install git+https://github.com/BIDMCDigitalPsychiatry/LAMP-cortex.git@master\n```\n\nIf you do not have your environment variables set up you will need to perform the initial server credentials configuraton below:\n\n```python\nimport os\nos.environ[\'LAMP_ACCESS_KEY\'] = \'YOUR_EMAIL_ADDRESS\'\nos.environ[\'LAMP_SECRET_KEY\'] = \'YOUR_PASSWORD\'\nos.environ[\'LAMP_SERVER_ADDRESS\'] = \'YOUR_SERVER_ADDRESS\'\n```\n\n<a name="example_cortex_query"></a>\n## Example: Passive data features from Cortex\nThe primary function of Cortex is to provide a set of features derived from pasive data. Data can be pulled either by calling Cortex functions directly, or by using the `cortex.run()` function to parse multiple participants or features simultaneously. For example, one feature of interest is screen_duration or the time spent with the phone "on".\n\nFirst, we can pull this data using the Cortex function. Let\'s say we want to compute the amount of time spent by\nparticipant: "U1234567890" from 11/15/21 (epoch time: 1636952400000) to 11/30/21 (epoch time: 1638248400000) each day (resolution = miliseconds in a day = 86400000):\n\n```python\nimport cortex\nscreen_dur = cortex.secondary.screen_duration.screen_duration("U1234567890", start=1636952400000, end=1638248400000, resolution=86400000)\n```\n\nThe output would look something like this:\n```\n{\'timestamp\': 1636952400000,\n \'duration\': 1296000000,\n \'resolution\': 86400000,\n \'data\': [{\'timestamp\': 1636952400000, \'value\': 0.0},\n  {\'timestamp\': 1637038800000, \'value\': 0.0},\n  {\'timestamp\': 1637125200000, \'value\': 0.0},\n  {\'timestamp\': 1637211600000, \'value\': 0.0},\n  {\'timestamp\': 1637298000000, \'value\': 0.0},\n  {\'timestamp\': 1637384400000, \'value\': 0.0},\n  {\'timestamp\': 1637470800000, \'value\': 8425464},\n  {\'timestamp\': 1637557200000, \'value\': 54589034},\n  {\'timestamp\': 1637643600000, \'value\': 50200716},\n  {\'timestamp\': 1637730000000, \'value\': 38500923},\n  {\'timestamp\': 1637816400000, \'value\': 38872835},\n  {\'timestamp\': 1637902800000, \'value\': 46796405},\n  {\'timestamp\': 1637989200000, \'value\': 42115755},\n  {\'timestamp\': 1638075600000, \'value\': 44383154}]}\n ```\nThe \'data\' in the dictionary holds the start timestamps (of each day from 11/15/21 to 11/29/21) and the screen duration for each of these days.\n \nSecond, we could have pulled this same data using the `cortex.run` function. Note that `resolution` is automatically set to a day in `cortex.run`. To invoke `cortex.run`, you must provide a specific ID or a `list` of IDs (only `Researcher`, `Study`, or `Participant` IDs are supported). Then, you specify the behavioral features to generate and extract. Once Cortex finishes running, you will be provided a `dict` where each key is the behavioral feature name, and the value is a dataframe. You can use this dataframe to save your output to a CSV file, for example, or continue data processing and visualization. This function call would look like this:\n\n ```python\nimport cortex\nscreen_dur = cortex.run("U1234567890", [\'screen_duration\'], start=1636952400000, end=1638248400000)\n```\nAnd the output might look like:\n```\n{\'screen_duration\':              id           timestamp       value\n 0   U1234567890 2021-11-15 05:00:00         0.0\n 1   U1234567890 2021-11-16 05:00:00         0.0\n 2   U1234567890 2021-11-17 05:00:00         0.0\n 3   U1234567890 2021-11-18 05:00:00         0.0\n 4   U1234567890 2021-11-19 05:00:00         0.0\n 5   U1234567890 2021-11-20 05:00:00         0.0\n 6   U1234567890 2021-11-21 05:00:00   8425464.0\n 7   U1234567890 2021-11-22 05:00:00  54589034.0\n 8   U1234567890 2021-11-23 05:00:00  50200716.0\n 9   U1234567890 2021-11-24 05:00:00  38500923.0\n 10  U1234567890 2021-11-25 05:00:00  38872835.0\n 11  U1234567890 2021-11-26 05:00:00  46796405.0\n 12  U1234567890 2021-11-27 05:00:00  42115755.0\n 13  U1234567890 2021-11-28 05:00:00  44383154.0}\n ```\nThe output is the same as above, except the \'data\' has been transformed into a Pandas DataFrame. Additionally, the dictionary is indexed by feature -- this way you can add to the list of features processed at once. Finally, a column "id" has been added so that multiple participants can be processed simultaneously. \n\n<a name="bug_report"></a>\n### Find a bug?\n\nOur forum has many answers to common questions. If you find a bug, need help with working with Cortex, or have a suggestion for how the code can be improved please make a post [on the forum] (https://mindlamp.discourse.group/).\n\n<a name="cortex_dev"></a>\n### Adding features to Cortex\nIf you are interesting in developing new features for Cortex, please check out our docs [here] (https://docs.lamp.digital/data_science/cortex/developing_cortex). Note that the unittests in this repository will fail for users outside of BIDMC since you do not have access to our data.\n\n<a name="advanced"></a>\n### Advanced Configuration\n\nEnsure your `server_address` is set correctly. If using the default server, it will be `api.lamp.digital`. Keep your `access_key` (sometimes an email address) and `secret_key` (sometimes a password) private and do not share them with others. While you are able to set these parameters as arguments to the `cortex` executable, it is preferred to set them as session-wide environment variables. You can also run the script from the command line:\n\n```bash\nLAMP_SERVER_ADDRESS=api.lamp.digital LAMP_ACCESS_KEY=XXX LAMP_SECRET_KEY=XXX python3 -m \\\n  cortex significant_locations \\\n    --id=U26468383 \\\n    --start=1583532346000 \\\n    --end=1583618746000 \\\n    --k_max=9\n```\n\nOr another example using the CLI arguments instead of environment variables (and outputting to a file):\n\n```bash\npython3 -m \\\n  cortex --format=csv --server-address=api.lamp.digital --access-key=XXX --secret-key=XXX \\\n    survey --id=U26468383 --start=1583532346000 --end=1583618746000 \\\n    2>/dev/null 1>./my_cortex_output.csv\n```\n',
    'author': 'Division of Digital Psychiatry at Beth Israel Deaconess Medical Center',
    'author_email': 'team@digitalpsych.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.lamp.digital',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
