import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='parrot-nlp',
    version='0.0.1',
    author='tsaruggan',
    author_email='tsaruggan@gmail.com',
    description='elegant NLP solutions and visualizations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tsaruggan/parrot',
    license='MIT',
    packages=['parrot'],
    install_requires=['requests'],
)