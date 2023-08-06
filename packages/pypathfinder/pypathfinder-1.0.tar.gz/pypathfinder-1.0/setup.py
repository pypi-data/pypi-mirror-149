from setuptools import setup, find_packages, Extension

CPATH = "pypathfinder\\fast"
CPACK = CPATH.replace("\\", ".")

ext1 = Extension(f"{CPACK}.ctools", [f"{CPATH}\\ctools.c"])
ext = [ext1]
      
setup(
    name="pypathfinder",
    version="1.0",
    packages=find_packages(),
    ext_modules=ext
)