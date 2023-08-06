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
    name="wai.annotations.video",
    description="Various plugins for managing video with wai.annotations.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-ufdl/wai-annotations-video",
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
        "opencv-python",
        "numpy",
        "termplotlib",
    ],
    entry_points={
        "wai.annotations.plugins": [
            # sources
            "from-video-file-od=wai.annotations.video.format.video_file.specifier:VideoFileODInputFormatSpecifier",
            "from-webcam-od=wai.annotations.video.format.webcam.specifier:WebCamODInputFormatSpecifier",
            # ISPs
            "drop-frames=wai.annotations.video.isp.drop_frames.specifier:DropFramesISPSpecifier",
            "skip-similar-frames=wai.annotations.video.isp.skip_similar_frames.specifier:SkipSimilarFramesISPSpecifier",
            # sinks
            "to-video-file-od=wai.annotations.video.format.video_file.specifier:VideoFileODOutputFormatSpecifier",
            "calc-frame-changes=wai.annotations.video.format.calc_frame_changes.specifier:CalcFrameChangesODOutputFormatSpecifier",
        ]
    }
)
