from setuptools import setup, find_packages

setup(
    name="casai-home-frontend",
    version="20220503.0",
    description="The Casai Home frontend",
    url="https://github.com/hotel-casai/hass-frontend-dev",
    author="Casai",
    author_email="alfonso.gonzalez@casai.com",
    license="Apache License 2.0",
    packages=find_packages(include=["hass_frontend", "hass_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)
