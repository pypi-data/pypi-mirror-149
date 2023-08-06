import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-seeding-data',
    version='0.1',
    packages=['seeding'],
    include_package_data=True,
    license='BSD License',
    description='Data seeding package',
    long_description=README,
    url='https://oscar-studio.ru/',
    author='Oleg Maslov',
    author_email='oleg.gnome@gmail.com',
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
