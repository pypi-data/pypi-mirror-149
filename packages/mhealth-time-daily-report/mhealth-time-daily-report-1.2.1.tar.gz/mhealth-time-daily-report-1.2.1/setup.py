import setuptools

setuptools.setup(
    name='mhealth-time-daily-report',
    version='1.2.1',
    description='Package to generate daily reports for TIME study data',
    url='https://bitbucket.org/mhealthresearchgroup/daily_report_cluster/src/master/',
    long_description='long_description',
    long_description_content_type="text/markdown",
    author='Aditya Ponnada',
    author_email='ponnada.a@northeastern.edu',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    package_data={'time_daily_report': ['validation_key_ans.json']},
    include_package_data=True,
    python_requires='>=3.6'
)
