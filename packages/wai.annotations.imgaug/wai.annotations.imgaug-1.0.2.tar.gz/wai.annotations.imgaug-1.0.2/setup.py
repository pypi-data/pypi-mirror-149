from setuptools import setup, find_namespace_packages


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="wai.annotations.imgaug",
    description="Various inline stream processors for image augmentation.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-ufdl/wai-annotations-imgaug",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "wai",
        "wai.annotations",
    ],
    version="1.0.2",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    install_requires=[
        "wai.annotations.core>=0.1.1",
        "imgaug>=0.4.0",
        "matplotlib",
    ],
    entry_points={
        "wai.annotations.plugins": [
            # ISPs
            "add-annotation-overlay-od=wai.annotations.imgaug.isp.annotation_overlay.specifier:AnnotationOverlayISPSpecifier",
            "crop=wai.annotations.imgaug.isp.crop.specifier:CropISPSpecifier",
            "flip=wai.annotations.imgaug.isp.flip.specifier:FlipISPSpecifier",
            "gaussian-blur=wai.annotations.imgaug.isp.gaussian_blur.specifier:GaussianBlurISPSpecifier",
            "hsl-grayscale=wai.annotations.imgaug.isp.hsl_grayscale.specifier:HSLGrayScaleISPSpecifier",
            "linear-contrast=wai.annotations.imgaug.isp.linear_contrast.specifier:LinearContrastISPSpecifier",
            "rotate=wai.annotations.imgaug.isp.rotate.specifier:RotateISPSpecifier",
            "scale=wai.annotations.imgaug.isp.scale.specifier:ScaleISPSpecifier",
        ]
    }
)
