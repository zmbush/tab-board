import threading
from tab import *

def test_consistency():
  def add_to_tab(amount):
    t = Tab('test_zach')
    t2 = Tab('test_hayg')

    t.addTo(amount)
    t2.removeFrom(amount)

  def remove_from_tab(amount):
    t = Tab('test_zach')
    t2 = Tab('test_hayg')

    t.removeFrom(amount)
    t2.addTo(amount)

  add = [threading.Thread(target=add_to_tab, args=(i,)) for i in range(100)]
  remove = [threading.Thread(target=remove_from_tab, args=(i,)) for i in range(100)]

  for a in add:
    a.daemon = True
    a.start()
  for r in remove:
    r.daemon = True
    r.start();

  for a in add:
    a.join(10)
  for r in remove:
    r.join(10)

  for a in add:
    assert not a.isAlive()
  for r in remove:
    assert not r.isAlive()
  assert Tab('test_zach').value() == 0
  assert Tab('test_hayg').value() == 0

def test_rm():
  Tab('').rmTabFile()
