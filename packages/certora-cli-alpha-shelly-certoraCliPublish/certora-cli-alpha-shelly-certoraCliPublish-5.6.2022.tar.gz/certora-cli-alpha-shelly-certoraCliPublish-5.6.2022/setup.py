
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="certora-cli-alpha-shelly-certoraCliPublish",
        version="5.6.2022",
        author="Certora",
        author_email="support@certora.com",
        description="Utilities for building smart contracts for verification using the Certora Prover, and for running the Certora Prover",
        long_description="Commit db99b16. Build and Run scripts for executing the Certora Prover on Solidity smart contracts.",
        long_description_content_type="text/markdown",
        url="https://github.com/Certora/CertoraCLI",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=['tabulate', 'requests', 'pycryptodome', 'tqdm', 'click', 'sly'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        entry_points={
            "console_scripts": [
                "certoraRun = certora_cli.certoraRun:entry_point"
            ]
        },
        python_requires='>=3.5',
    )
        