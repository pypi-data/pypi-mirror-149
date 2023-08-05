import setuptools

_requires = [
    'setuptools-scm',
    'ebs-linuxnode-gui-kivy-core>=3.0.2',
    # EBS Kivy Widgets
    'kivy_garden.ebs.core>=1.3.0',
    'kivy_garden.ebs.pdfplayer>=2.0.0',
]

setuptools.setup(
    name='ebs-linuxnode-gui-kivy-mediaplayer',
    url='https://github.com/ebs-universe/ebs-linuxnode-kivy-mediaplayer',

    author='Chintalagiri Shashank',
    author_email='shashank.chintalagiri@gmail.com',

    description='Media Player for EBS Linuxnode Kivy Applications',
    long_description='',

    packages=setuptools.find_packages(),
    install_requires=_requires,

    setup_requires=['setuptools_scm'],
    use_scm_version=True,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
    ],
)
