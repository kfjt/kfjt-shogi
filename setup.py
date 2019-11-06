import setuptools

setuptools.setup(
    name = 'kfjt-shogi',
    version = '0.0.1',
    author = '',
    packages = ['kfjtshogi'],
    scripts = [],
    install_requires = [
        'python-shogi',
        'numpy',
        'chainer',
    ],
)
