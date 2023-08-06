from setuptools import setup
import distutils


class TranslateCommand(distutils.cmd.Command):
    description = "Translation"

    user_options = []
    sub_commands = [
        ('extract_messages', None),
        ('update_catalog', None),
        ('compile_catalog', None),
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="sphinx_nervproject_theme",
    version="2.0.6",
    url="https://procrastinator.nerv-project.eu/nerv-project/sphinx_nervproject_theme",
    license="EUPL 1.2",
    author="Kujiu",
    author_email="kujiu-pypi@kujiu.org",
    description="A Sphinx-doc theme based on Vuepress",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=["sphinx_nervproject_theme"],
    cmdclass={
        'translate': TranslateCommand,
    },
    package_data={
        "sphinx_nervproject_theme": [
            "theme.conf",
            "*.html",
            "locale/*/LC_MESSAGES/*.mo",
            "locale/*/LC_MESSAGES/*.po",
            "util/*.html",
            "ablog/*.html",
            "static/*.css",
            "static/*.js",
            "static/fonts/luciole/*.woff",
            "static/fonts/hack/*.woff",
            "static/fa/*.svg",
            "static/fa/*.txt",
        ]
    },
    entry_points={"sphinx.html_themes": ["nervproject = sphinx_nervproject_theme"]},
    install_requires=[
        "sphinx>=3.0.0",
        "sphinx-fasvg"
    ],
    classifiers=[
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Theme",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
    keywords="sphinx doc theme vue.js",
    project_urls={
        "Source": "https://procrastinator.nerv-project.eu/nerv-project/sphinx_nervproject_theme",
        "Issues": "https://procrastinator.nerv-project.eu/nerv-project/sphinx_nervproject_theme/issues",
    },
)
