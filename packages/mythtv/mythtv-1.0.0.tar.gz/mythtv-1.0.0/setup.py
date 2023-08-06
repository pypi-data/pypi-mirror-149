from distutils.core import setup, Extension


def main():
    setup(name="mythtv",
          version="1.0.0",
          description="Python interface for MythTV filehash function",
          author="Mathias Jansen",
          author_email="matthias.jansen@gmx.de",
          ext_modules=[Extension("mythtv", ["mythtvmodule.c"])])


if __name__ == "__main__":
    main()
