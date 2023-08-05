from setuptools import find_packages, setup

from socialprofile import __version__ as version

readme = open("README.md").read()

setup(
    name="django-sp",
    version=version,
    url="https://github.com/DLRSP/django-sp",
    license="MIT",
    description="Django Custom Social Profile Auth/User",
    author="DLRSP",
    author_email="dlrsp.dev@gmail.com",
    packages=find_packages(),
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "django-jenkins",
        "django<3",
        "django-errors",
        "python-social-auth",  # <-- Need By Auth Process: OAuth2 Social
        "social-auth-app-django",  # <-- Need By Auth Process: OAuth2 Social
        "django-otp",  # <-- Need By Auth Process: One-Time-Password
        "django-two-factor-auth",  # <-- Need By Auth Process: One-Time-Password
        "django-oauth-toolkit",  # <-- Need By Auth Process: OAuth2 Token
        # 'djangorestframework-jwt',  # <-- Need By Auth Process: Token (deprecated)
        "djangorestframework",  # <-- Need By Rest API
        "easy_thumbnails",  # <-- Need By Imge Cropping
        "django-image-cropping",
        "django-user-sessions",  # <-- Need By Monitor
        "django-axes",  # <-- Need By Monitor
    ],
    tests_require=["runtests.py"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
