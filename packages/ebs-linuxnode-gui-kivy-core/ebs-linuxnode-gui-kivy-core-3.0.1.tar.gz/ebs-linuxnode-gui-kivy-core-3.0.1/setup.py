import setuptools

_requires = [
    'six',
    'setuptools-scm',
    'appdirs',
    'kivy>=2.1.0',
    'kivy-garden',

    # ebs Widgets
    'kivy_garden.ebs.core>=1.3.0',
    'kivy_garden.ebs.progressspinner>=1.2.0',

    'ebs-linuxnode-core>=3.0.0',
]

setuptools.setup(
    name='ebs-linuxnode-gui-kivy-core',
    url='https://github.com/ebs-universe/ebs-linuxnode-coregui-kivy',

    author='Chintalagiri Shashank',
    author_email='shashank.chintalagiri@gmail.com',

    description='Kivy GUI Core for EBS Linuxnode Applications',
    long_description='',

    packages=setuptools.find_packages(),
    package_dir={'ebs.linuxnode.gui.kivy.core': 'ebs/linuxnode/gui/kivy/core'},
    package_data={'ebs.linuxnode.gui.kivy.core': ['images/background.png',
                                                  'images/no-internet.png',
                                                  'images/no-server.png']},

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
