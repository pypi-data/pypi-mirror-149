import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='wiliot',
                 use_scm_version = {
                    'git_describe_command' : "git describe --long --tags --match [0-9]*.[0-9]*.[0-9]*",
                    'write_to' : "wiliot/version.py",
                    'write_to_template' :  '__version__ = "{version}"',
                    'root' : ".",
                 },
                 setup_requires=['setuptools_scm'],
                 author='Wiliot',
                 author_email='support@wiliot.com',
                 description="A library for interacting with Wiliot's private API",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='',
                 project_urls={
                     "Bug Tracker": "https://WILIOT-ZENDESK-URL",
                 },
                 license='MIT',
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 packages=setuptools.find_packages(),
                 package_data={"": ["*.*"]},  # add all support files to the installation
                 install_requires=[
                     'requests',
                     'pyserial',
                     'pc_ble_driver_py',
                     'nrfutil',
                     'yoctopuce',
                     'pandas',
                     'joblib',
                     'numpy',
                     'scipy',
                     'pyqtgraph',
                     'PySimpleGUI',
                     'matplotlib',
                     'PyQt5',
                     'pygubu>=0.11',
                     'bokeh',  # for wiliot_internal only
                     'pytest',  # for wiliot_internal only
                     'importlib_metadata',  # for wiliot_internal only
                     'pyjwt',
                     'pycryptodome',  # for wiliot_internal only
                     'setuptools_scm',
                     'appdirs'
                 ],
                 zip_safe=False,
                 python_requires='>=3.6',
                 include_package_data=True
                 )
