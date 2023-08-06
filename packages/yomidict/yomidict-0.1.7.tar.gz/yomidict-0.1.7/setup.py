# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yomidict']

package_data = \
{'': ['*']}

install_requires = \
['EbookLib>=0.17.1,<0.18.0',
 'SudachiDict-full>=20211220,<20211221',
 'SudachiPy>=0.6.3,<0.7.0',
 'ass-tag-parser>=2.3.1,<3.0.0',
 'ass>=0.5.2,<0.6.0',
 'fugashi>=1.1.0,<2.0.0',
 'srt>=3.4.1,<4.0.0',
 'unidic>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'yomidict',
    'version': '0.1.7',
    'description': 'Create frequency dictionaries for yomichan out of a variety of media',
    'long_description': '# yomidict\nCreate frequency dictionaries for yomichan out of media.\\\nCurrently supported formats are: epub, html, srt, ass, txt\n\n\n![](https://github.com/exc4l/yomidict/blob/main/example.png)\n\n```python\npip install yomidict\n```\n\n\nMWE:\n```python\nimport yomidict\ndm = yomidict.DictMaker()\nfilelist = ["test.html"]*5 + ["test.epub"]*2 + ["test.srt"]*2\ndm.feed_files(filelist)\ndm.save("zipfile.zip", "name_in_yomichan", use_suffix=True)\n```\n\n# Docs:\n\n## DictMaker Object\n### wcounter\nIs a Counter which saves the number of occurences for the tokens that were found during feeding.\n\n### refcounter\nKeeps track of in how many files a certain token was found. E.g. a value of 0.5 (if normalized) would mean that the token occurs in 50% of all files that were fed.\n\n## DictMaker.feedfiles()\n```python\ndef feed_files(\n        self,\n        filelist,\n        skip_errors=True,\n        reset_refcounter=True,\n        normalize_refcounter=True,\n    )\n```\nskip_erros: does exactly as the name suggests, it skips errors. During processing of a bunch of files all sorts of errors could occur which would abort the feeding. This might be undesirable and so they can be skipped. The errored files will also be taken in consideration when calculating the DictMaker.refcounter.\n\nreset_refcounter: resets the refcounter before feeding files.\n\nnormalize_refcounter: count/total_number_of_files. Therefore, if a token comes up in 8 out of 10 books the value of the counter would be 0.8 instead of 8. This makes it easier to read even without knowing the total number of files that were fed into DictMaker.\n\n## DictMaker.save()\n```python\ndef save(\n        self,\n        filepath,\n        dictname,\n        only_rank_and_freq=False,\n        use_suffix=True,\n        use_suffix_rank=False,\n        use_suffix_freq=False,\n    )\n```\nonly_rank_and_freq: by default it the word rank, the word frequency and the refcounter_value get saved. This deactivates the refcounter_value.\n\nuse_suffix: activates use_suffix_rank and use_suffix_freq.\n\nuse_suffix_rank: if the number is above 1000 the number gets replaced by "num/1000 K" e.g. 2530 becomes 2K and 2434455 becomes 2M.\n\nuse_suffix_freq: same as use_suffix_freq but for the frequency\n\n## DictMaker.feed_text()\n```python\ndef feed_text(self, text, refcounter_add=False)\n```\ncan be used to feed a string into DictMaker.\n\nrefcounter_add: If true it adds 1 occurrence in refcounter to all the tokens that were found in the fed text.\n\n### How to feed a large text file\n\nDo you want to use refcounter? If yes, do you know the number of works inside the large text file? No? Don\'t use refcounter.\n\nIf you do know the number of works inside the large text file, do you know where one work ends and the other begins? Nice, just read it as chunks and let it add to the refcounter and normalize it in the end. If not, don\'t use refcounter.\n\nTo feed a large text file you can just read the text file line by line or sentence by sentence and utilizie the `DictMaker._clean_txt()` function.\n\n```python\ndm = yomidict.DictMaker()\nfor line in large_txt_file:\n    dm.feed_text(dm._clean_txt(line))\n```\n\nIf you know the boundaries of each work and can it eat in chunks you could something like this:\n\n```python\ndm = yomidict.DictMaker()\nfor work in large_txt_file:\n    dm.feed_text(dm._clean_txt(work), refcounter_add=True)\ndm.normalize_refcounter(works_in_large_txt_file)\n```\n',
    'author': 'exc4l',
    'author_email': 'cps0537@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exc4l/yomidict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
