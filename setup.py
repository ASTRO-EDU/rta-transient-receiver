from distutils.core import setup

setup(
    name="voevent-handler",
    author="Antonio Addis, Luca Babboni",
    version="2.0.0",
    packages=['./', 'extractors/', 'extractors/utilis', 'test'],
    data_files=[('voevent_handler_config', ['./config.json'])],
    license='GPL-3.0'
)