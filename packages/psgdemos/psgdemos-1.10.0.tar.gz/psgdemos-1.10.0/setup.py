import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="psgdemos",
    version="1.10.0",
    author="PySimpleGUI",
    author_email="PySimpleGUI@PySimpleGUI.org",
    description="Installs the full set of PySimpleGUI Demo Programs and the Demo Browser.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/PySimpleGUI/PySimpleGUI/tree/master/DemoPrograms",
    packages=['psgdemos',],
    install_requires=['PySimpleGUI',],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Utilities",
        "Operating System :: OS Independent"
    ],
    include_package_data=True,
    package_data={"":["*.ico", 'demo_programs/*'],},
    entry_points={
        'gui_scripts': [
            'psgdemos=psgdemos.psgdemos:main'
        ],
    },
)
