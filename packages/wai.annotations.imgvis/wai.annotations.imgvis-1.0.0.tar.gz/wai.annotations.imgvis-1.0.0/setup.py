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
    name="wai.annotations.imgvis",
    description="Image visualization plugins for wai.annotations.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-ufdl/wai-annotations-imgvis",
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
    version="1.0.0",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    install_requires=[
        "wai.annotations.core>=0.1.1",
    ],
    entry_points={
        "wai.annotations.plugins": [
            # ISPs
            "add-annotation-overlay-ic=wai.annotations.imgvis.isp.annotation_overlay.specifier:AnnotationOverlayICISPSpecifier",
            "add-annotation-overlay-is=wai.annotations.imgvis.isp.annotation_overlay.specifier:AnnotationOverlayISISPSpecifier",
            "add-annotation-overlay-od=wai.annotations.imgvis.isp.annotation_overlay.specifier:AnnotationOverlayODISPSpecifier",
            # Sinks
            "image-viewer-ic=wai.annotations.imgvis.sink.image_viewer.specifier:ImageViewerICSinkSpecifier",
            "image-viewer-is=wai.annotations.imgvis.sink.image_viewer.specifier:ImageViewerISSinkSpecifier",
            "image-viewer-od=wai.annotations.imgvis.sink.image_viewer.specifier:ImageViewerODSinkSpecifier",
            "to-annotation-overlay-od=wai.annotations.imgvis.sink.annotation_overlay.specifier:AnnotationOverlayODOutputFormatSpecifier",
        ]
    }
)
