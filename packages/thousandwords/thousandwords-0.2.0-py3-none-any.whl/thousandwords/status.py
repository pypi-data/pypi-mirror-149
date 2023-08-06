import sys

class Status:
  def __init__(self, text):
    self.text = text

  def __enter__(self):
    print(f'thousandwords:{self.text}', end='', file=sys.stderr)
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    if exc_value is not None:
      print(' [Failure]', file=sys.stderr)
    else:
      print(' [Success]', file=sys.stderr)
    sys.stderr.flush()
    return False
