import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open("requirements.txt", "r") as fh:
#     requirements = fh.read()

setuptools.setup(
    name="odoo-tools",
    version="0.0.65",
    author="Archeti",
    author_email="info@archeti.ca",
    description="Odoo Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/archeti-org/odoo-utils.git",
    packages=setuptools.find_packages(),
    install_requires=[
        "giturlparse",
        "toposort",
        "toml",
        "requests",
        "pathlib2; python_version < '3.0'",
        "packaging",
        "lxml",
        "docutils",
        "polib",
        "six>=1.12.0",
        "cryptography",
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    entry_points={
        "console_scripts": [
            "odoo-modules-search = odoo_tools.cli.find_modules:command",
            "odoo-modules-manifest = odoo_tools.cli.get_manifest:command",
            "odoo-modules-dependencies = odoo_tools.cli.get_dependencies:command",
            "odoo-addons-paths = odoo_tools.cli.get_addons_paths:command",
            "odoo-gen-buildout = odoo_tools.cli.prepare:prepare_main",
            "odoo-fetch-addons = odoo_tools.cli.fetch_addons:command",
            "odoo-copy-addons = odoo_tools.cli.copy_addons:command",
            "odoo-git-credentials = odoo_tools.cli.git_credentials:command",
            "odoo-install = odoo_tools.cli.odoo_install:command",
            "odoo-pip = odoo_tools.cli.get_requirements:command",
            "odoo-export-i18n = odoo_tools.cli.odoo_export_i18n:command",
            "odoo-service = odoo_tools.cli.odoo_service:command",
            "odoo-service-image = odoo_tools.cli.odoo_service_image:command",
            "odoo-platform-arch = odoo_tools.cli.odoo_platform:command",
            "odoo-entrypoint = odoo_tools.cli.entrypoint:command",
            "odoo-shell = odoo_tools.cli.shell:command",
        ],
    },
    package_data={
        "odoo_tools": [
            "requirements/*.txt"
        ],
    }
)
