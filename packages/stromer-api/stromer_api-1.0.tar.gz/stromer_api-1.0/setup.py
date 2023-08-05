from setuptools import setup

setup(
    name='stromer_api',
    version='1.0',
    packages=['stromer_api'],
    keywords=['Stromer', 'Python', 'API'],
    url='https://github.com/elnkosc/stromer_api',
    license='GPL',
    author='Koen',
    author_email='koen@schilders.org',
    description='Stomer API for accessing data from your Stromer Speed Bike.',
    long_description=open('README.md', 'rt').read(),
    long_description_content_type='text/markdown'
)
