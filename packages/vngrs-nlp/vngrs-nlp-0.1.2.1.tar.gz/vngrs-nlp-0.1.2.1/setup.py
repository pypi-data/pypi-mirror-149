from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding = 'utf-8')

split_lines = [line for line in long_description.split('\n') if ("img src" not in line) and (line != "")]
logo_img = [".. |logo| image:: https://github.com/vngrs-ai/VNLP/blob/main/img/logo.png",
            "   :alt: Logo",
            "   :width: 256"]

usage_example_img = [".. |example| image:: https://github.com/vngrs-ai/VNLP/blob/main/img/dp_vis_sample.png",
            "   :alt: Example",
            "   :width: 512"]
long_description = '\n'.join(logo_img + split_lines + usage_example_img)

setup(
    name='vngrs-nlp',
    version='0.1.2.1',
    description='NLP Tools for Turkish Language.',
    long_description= long_description,
    long_description_content_type='text/markdown',
    author='Meliksah Turker',
    author_email='turkermeliksah@hotmail.com',
    license='GNU Affero General Public License v3.0',
    classifiers=[
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Information Technology',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',

    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
],
    packages=find_packages(exclude=['turkish_embeddings']),
    include_package_data=True,
    install_requires=['tensorflow<2.6.0; python_version < "3.8"',
                      'tensorflow>=2.6.0; python_version >= "3.8"',
                      'regex==2021.8.28', 'cyhunspell'],
    extras_require={"extras": ['gensim', 'spacy']},
    entry_points={"console_scripts": ["vnlp=vnlp.bin.vnlp:main"]}
    )