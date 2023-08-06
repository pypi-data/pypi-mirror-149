from distutils.core import setup, Extension

def main():
    setup(
          name="list_str_diff",
          version="1.0.0",
          description="Takes the difference of a list and a string.",
          author="Nagy Zoltán",
          author_email="zolika3400@gmail.com",
          ext_modules=[Extension('list_str_diff', ['list_str_diff.c'])]
          )

if __name__ == "__main__":
    main()
