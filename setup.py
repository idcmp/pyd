try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name="pyd",
    version="0.1",
    packages=find_packages(),
    scripts=[
        'din',
        'dout',
        'dtodo',
        'dscrum',
        'edit',
    ],
    
    author='JAmes Atwill',
    author_email='james@linuxstuff.org'
)
