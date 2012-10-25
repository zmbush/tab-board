import fcntl

class Tab:
  def __init__(self, name, f="test_file.tab"):
    self.user_name = name
    self.tab_file = f
    open(self.tab_file, 'a').close()

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
    print "File Opened"

    tabs = {}
    for line in f:
      s = line.split()
      if len(s) >= 2:
        tabs[s[0]] = float(s[1])

    f.seek(0)

    if self.user_name not in tabs:
      tabs[self.user_name] = 0

    print "Value: " + str(tabs[self.user_name])
    print "Adding: " + str(amount)

    tabs[self.user_name] += amount

    print "New Value: " + str(tabs[self.user_name])

    for user in sorted(tabs.iterkeys()):
      f.write(user + " " + str(tabs[user]) + "\n")

    print "File Closing"
    print
    self.closeLocked(f)

  def value(self):
    value = 0
    f = self.openReadLocked()
    for line in f:
      if self.user_name in line:
        value = float(line.split()[1])
    self.closeLocked(f)
    return value
