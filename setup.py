from setuptools import setup, find_packages

setup(
    name='chatbot_lib',
    version='0.3.2',
    author='Emma Do',
    author_email='ttdo@connect.ust.hk',
    description='A library for creating chatbots using OpenAI',
    long_description='A library for creating chatbots using OpenAI',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mylibrary',
    packages=find_packages(),
    install_requires=[
        'openai',
        'python-dotenv'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)