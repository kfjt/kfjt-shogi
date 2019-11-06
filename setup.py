import setuptools

setuptools.setup(
    name = 'kfjt-shogi',
    version = '1.1',
    author = '',
    packages = ['kfjtshogi'],
    scripts = [],
    install_requires = [
        'python-shogi',
        'numpy',
        'chainer',
    ],
)
