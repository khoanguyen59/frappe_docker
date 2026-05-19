from setuptools import find_packages, setup


setup(
    name="org_logistics_control",
    version="0.1.0",
    description="Company-based Frappe Desk UI control and logistics tracking",
    author="Your Team",
    author_email="admin@example.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["frappe>=16.0.0"],
)
