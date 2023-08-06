from setuptools import setup, find_packages


setup(
    name='sasapy',
    version='1.0.0',
    packages=find_packages(),

    #作者,プロジェクト情報
    author='sasahara',
    author_email='sasahiro1204@icloud.com',

    #プロジェクトHPのURL
    url='https://github.com/rhoboro/pythonbook',

    #短い説明文と長い説明文を用意
    #content_typeは、text/plain, text/x-rst, text/markdownを選択
    description='this is test package for me.',
    #long_description=open('README.md').read(),
    long_description='this is test for long',
    long_description_content_type='text/markdown',

    #pythonは3.6以上4未満
    python_requires='~=3.6',

    #pypi上の検索、閲覧のために利用される
    #ライセンス、pythonバージョン、osを含めること
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],

    #install_requires=['Click~=7.0',],

    #extras_require={
        #'s3':['boto3~=1.10.0'],
        #'gcs':['google-cloud-storage~=1.23.0'],
    #},

    #package_data={'pythonbook':['data/*']},
)
