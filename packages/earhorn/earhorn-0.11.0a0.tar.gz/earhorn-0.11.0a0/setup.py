# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['earhorn']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'httpx>=0.21.1,<0.23.0',
 'loguru>=0.5.3,<0.7.0',
 'lxml>=4.6.3,<4.9.0',
 'more-itertools>=8.10.0,<9.0.0',
 'prometheus-client>=0.14.1,<0.15.0',
 'pydantic>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['earhorn = earhorn.main:cli']}

setup_kwargs = {
    'name': 'earhorn',
    'version': '0.11.0a0',
    'description': 'Listen, monitor and archive your streams!',
    'long_description': '# earhorn\n\nListen, monitor and archive your streams!\n\n[![](https://mermaid.ink/svg/pako:eNqNlD9PwzAQxb_KySNqFySWqCoDMLAw0AEhgiorvhIriV1dnAJCfHcuzj8nzsDmvHv383Muzo_IrEKRiNpJh_dafpCstpfr1AB4CVJxcJIc4AWNg1waVSKlAmTdGsgdB4k73q7eYbvdLwsx7Ey2QpdjU4ekQO06JkiADV0TWZ-O7aI-NlTCbpflVme436-DQnMCj35_V0PbqvCkDSq4jUN3ppU34AutfxZiSuy1BF4xTkwoq_9HHtx95vYxDj3ntr1ZjlnRi1GMVNy1ZSCsLD92ru50Yd9ablvEsUcEl06Wiq4QkhbHsYU_DQ90aGTsbZdwtlX3PoMzLOdT6tqhmY9m1CK3pCzXl7l71Lx7DLuGWhSnznCn58Z0eGqM0eZjGu0A84ioOtCW1X7pZb5rCTx8abe4X2gUIJElcHb10rLh6A1L4lRh8GCIRxC4nux88xepHfDU4YZtmTWqv96frE8Y3zFSPDQ2zJXoMxYbUSFVUiv-d_20DangT6jCVCS85Ashm9KlIjW_bG3OigM-KO0sieQkyxo3QjbOHr5NJhJHDQ6m_hfYu37_AFEs0XE)](https://mermaid.live/edit#pako:eNqNlD9PwzAQxb_KySNqFySWqCoDMLAw0AEhgiorvhIriV1dnAJCfHcuzj8nzsDmvHv383Muzo_IrEKRiNpJh_dafpCstpfr1AB4CVJxcJIc4AWNg1waVSKlAmTdGsgdB4k73q7eYbvdLwsx7Ey2QpdjU4ekQO06JkiADV0TWZ-O7aI-NlTCbpflVme436-DQnMCj35_V0PbqvCkDSq4jUN3ppU34AutfxZiSuy1BF4xTkwoq_9HHtx95vYxDj3ntr1ZjlnRi1GMVNy1ZSCsLD92ru50Yd9ablvEsUcEl06Wiq4QkhbHsYU_DQ90aGTsbZdwtlX3PoMzLOdT6tqhmY9m1CK3pCzXl7l71Lx7DLuGWhSnznCn58Z0eGqM0eZjGu0A84ioOtCW1X7pZb5rCTx8abe4X2gUIJElcHb10rLh6A1L4lRh8GCIRxC4nux88xepHfDU4YZtmTWqv96frE8Y3zFSPDQ2zJXoMxYbUSFVUiv-d_20DangT6jCVCS85Ashm9KlIjW_bG3OigM-KO0sieQkyxo3QjbOHr5NJhJHDQ6m_hfYu37_AFEs0XE)\n\n## Install\n\nIf you need to listen or archive an Icecast stream, you will need `ffmpeg`:\n\n```sh\nsudo apt install ffmpeg\n```\n\nInstall earhorn from pip:\n\n```sh\npip install earhorn\n```\n\nYou can start archiving an Icecast stream by providing a stream url and an archive path:\n\n```sh\nearhorn \\\n  --stream-url https://stream.example.org/live.ogg \\\n  --archive-path=/to/my/archive\n```\n\nYou can also start exporting the Icecast stats as prometheus metrics by providing an Icecast stats url:\n\n```sh\nearhorn \\\n  --stats-url https://stream.example.org/admin/stats.xml \\\n  --stats-user admin \\\n  --stats-password hackme\n```\n\n### Docker\n\n```sh\ndocker pull ghcr.io/jooola/earhorn\n```\n\n## Usage\n\n```\nUsage: earhorn [OPTIONS]\n\n  See the ffmpeg documentation for details about the `--archive-segment-*` options:\n  https://ffmpeg.org/ffmpeg-formats.html#segment_002c-stream_005fsegment_002c-ssegment\n\nOptions:\n  --listen-port INTEGER           Listen port for the prometheus metrics endpoint.  [default: 9950]\n  --hook PATH                     Path to a custom script executed to handle stream state `events`.\n  --stream-url TEXT               URL to the icecast stream.\n  --stats-url TEXT                URL to the icecast admin xml stats page.\n  --stats-user TEXT               Username for the icecast admin xml stats page.  [default: admin]\n  --stats-password TEXT           Password for the icecast admin xml stats page.\n  --archive-path PATH             Path to the archive storage directory. If defined, the archiver will save the\n                                  `stream` in segments in the storage path.\n  --archive-segment-size INTEGER  Archive segment size in seconds.  [default: 3600]\n  --archive-segment-filename TEXT\n                                  Archive segment filename (without extension).  [default: archive-%Y%m%d_%H%M%S]\n  --archive-segment-format TEXT   Archive segment format.  [default: ogg]\n  --archive-segment-format-options TEXT\n                                  Archive segment format options.\n  --archive-copy-stream           Copy the `stream` without transcoding (reduce CPU usage). WARNING: The stream has to\n                                  be in the same format as the `--archive-segment-format`.\n  --help                          Show this message and exit.\n\n```\n\n## Developmement\n\nTo develop this project, start by reading the `Makefile` to have a basic understanding of the possible tasks.\n\nInstall the project and the dependencies in a virtual environment:\n\n```sh\nmake install\nsource .venv/bin/activate\nearhorn --help\n```\n\n## Releases\n\nTo release a new version, first bump the version number in `pyproject.toml` by hand or by using:\n\n```sh\n# poetry version --help\npoetry version <patch|minor|major>\n```\n\nRun the release target:\n\n```sh\nmake release\n```\n\nFinally, push the release commit and tag to publish them to Pypi:\n\n```sh\ngit push --follow-tags\n```\n',
    'author': 'Joola',
    'author_email': 'jooola@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
