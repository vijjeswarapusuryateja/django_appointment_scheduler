from setuptools import setup, find_packages

setup(
    name='django_appointment_scheduler',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.0',
        'djangorestframework',
    ],
    description='A generic and flexible appointment scheduling system for Django applications',
    author='NavaTeja (Parne Naveen Reddy & Vijjeswarapu Surya Teja)',
    author_email='team@navateja.com',
    url='https://github.com/vijjeswarapusuryateja/django_appointment_scheduler',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)
