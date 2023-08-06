import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tflash',
    version='0.5.1',
    url='https://github.com/nuggfr/tflash',
    license='MIT',
    author='Nugroho Fredivianus',
    author_email='nuggfr@gmail.com',
    description='Quick detection practice for images and videos using TensorFlow',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include=['tflash']),
    install_requires=['tensorflow', 'imageio', 'tqdm'],
    include_package_data=True,
    keywords='machine learning, tensorflow, object detection',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
