from setuptools import setup, find_packages

setup(
    name="py_mess_gb_04_22_client",
    version="0.3.1",
    description="one_machine_messenger_client",
    author="Anton Petrov",
    author_email="nesamurai@yandex.ru",
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
)
