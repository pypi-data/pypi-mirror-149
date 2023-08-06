import sys
import xdg
import inspect
from pathlib import Path

def findconfig(filename, allow_dot=True, use_xdg=True, use_home=True,
                         use_src=True, more_paths = [], src_climb = 1,
                         exception = False, verbose = False):
  """
  Find a config file.

  :param filename: The filename to search for.
  :param allow_dot: Whether to allow a prepended dot to the filename.
  :param use_xdg: Whether to search in the XDG config directories.
  :param use_home: Whether to search in the user home directory.
  :param use_src: Whether to search in the source directory of the caller module
                  and in its ancestor directories, until they contain a
                  __init__.py file, plus additional src_levels levels.
  :param src_climb: The number of levels to go up in the caller module's source
                    directory, when there is no __init__.py (default: 1).
  :param more_paths: A list of additional paths to search in (default: [])
  :param exception: Whether to raise an exception if the file is not found
                    (default: False).
  :param verbose: Whether to print the found path to stderr (default: False).
  :return: The path to the file, or None if not found.
  """
  search_paths = []
  assert(filename)
  if allow_dot:
    if filename[0] == ".":
      allow_dot = False
  if use_xdg:
    search_paths.append(xdg.xdg_config_home())
    search_paths += xdg.xdg_config_dirs()
  if use_home:
    search_paths.append(Path.home())
  if use_src:
    stk = inspect.stack()
    if len(stk) > 1:
      srcdir = Path(stk[1].filename).parent
      while srcdir.joinpath('__init__.py').exists():
        search_paths.append(srcdir)
        srcdir = srcdir.parent
      for i in range(src_climb):
        search_paths.append(srcdir)
        srcdir = srcdir.parent
      search_paths.append(srcdir)
  search_paths += [Path(p) for p in more_paths]
  for path in search_paths:
    if path.is_dir():
      filenames = [path / filename]
      if allow_dot:
        filenames.append(path / f".{filename}")
      for f in filenames:
        if f.is_file():
          if verbose:
            print(f"Configuration file: {f}", file=sys.stderr)
          return f
  if exception:
    if allow_dot:
      filename = f"{filename} or .{filename}"
    search_paths_formatted = '\n'.join([f"  {p.resolve()}" for p in search_paths])
    raise FileNotFoundError(f"No file {filename} could be found "+\
                            f"in any of the following paths:\n"+\
                            search_paths_formatted)
  return None
