import fcntl
import os

class Tab:
  def __init__(self, name, f="test_file.tab"):
    self.user_name = name
    self.tab_file = f
    open(self.tab_file, 'a').close()

  def rmTabFile(self):
    os.remove(self.tab_file)

  def openReadLocked(self):
    fd = open(self.tab_file, 'r+')
    fcntl.flock(fd, fcntl.LOCK_SH)
    return fd

  def openWriteLocked(self):
    fd = open(self.tab_file, 'r+')
    fcntl.flock(fd, fcntl.LOCK_EX)
    return fd

  def closeLocked(self, fd):
    fd.flush()
    fcntl.flock(fd, fcntl.LOCK_UN)
    fd.close()

  def removeFrom(self, amount):
    self.addTo(-amount)

  def addTo(self, amount):
    f = self.openWriteLocked()

    tabs = {}
    for line in f:
      s = line.split()
      if len(s) >= 2:
        tabs[s[0]] = float(s[1])

    f.seek(0)

    if self.user_name not in tabs:
      tabs[self.user_name] = 0

    tabs[self.user_name] += amount

    for user in sorted(tabs.iterkeys()):
      f.write("%-50s%07.2f\n" % (user, tabs[user]))

    self.closeLocked(f)

  def value(self):
    value = 0
    f = self.openReadLocked()
    for line in f:
      if self.user_name in line:
        value = float(line.split()[1])
    self.closeLocked(f)
    return value
