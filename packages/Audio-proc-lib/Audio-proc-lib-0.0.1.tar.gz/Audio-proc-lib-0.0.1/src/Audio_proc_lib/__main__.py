"""
Entrypoint module, in case you use `python -mAudio_proc_lib`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""
from Audio_proc_lib.cli import main

if __name__ == "__main__":
    main()
