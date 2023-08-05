import setuptools
import importlib.util


# Workaround for `python 3.6` ModuleNotFoundError error on project import
serialix_meta_spec = importlib.util.spec_from_file_location('serialix.meta', './serialix/meta.py')
serialix_meta_module = importlib.util.module_from_spec(serialix_meta_spec)
serialix_meta_spec.loader.exec_module(serialix_meta_module)


package_name = 'serialix'
package_version = serialix_meta_module.version

# Form extras
extras_require = {
    'ujson': ['ujson<=6.0.0'],
    'yaml': ['ruamel.yaml<=1.0.0'],
    'toml': ['toml<=1.0.0']
}

all_base_requirements = [dep for v in extras_require.values() for dep in v]

#  Installation with all parsers
extras_require.update({
    'full': all_base_requirements
})

#  Installation for testing
extras_require.setdefault('test', all_base_requirements.copy()).append('pytest<7')

with open('README.rst', 'r') as f:
    readme_text = f.read()

setuptools.setup(
    name=package_name,
    version=package_version,
    python_requires='~=3.5',
    author='maximilionus',
    author_email='maximilionuss@gmail.com',
    description='Powerful and easy to use tool for working with various human-readable data serialization languages (like json, yaml, etc)',
    long_description_content_type='text/x-rst',
    long_description=readme_text,
    keywords='serialization format files parse json yaml toml',
    packages=setuptools.find_packages(),
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'serialixcli = serialix.cli:start'  # Deprecated in '2.3.0'
        ]
    },
    license='MIT',
    url='https://github.com/maximilionus/serialix',
    project_urls={
        'Documentation': 'https://maximilionus.github.io/serialix',
        'Tracker': 'https://github.com/maximilionus/serialix/issues'
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing'
    ]
)
