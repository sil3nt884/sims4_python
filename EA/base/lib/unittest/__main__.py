import sys
    import os.path
    executable = os.path.basename(sys.executable)
    sys.argv[0] = executable + ' -m unittest'
    del os