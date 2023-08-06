from cProfile import run
import math, socket, time, os, timeit
from datetime import datetime
def add(x, y):
  return x + y
def sub(x, y):
  return x - y
def mul(x, y):
  return x*y
def div(x, y):
  return x/y
def power(y, z):
  return y**z 
def intdiv(x, y):
  return x//y
def modl(x, y):
  return x%y
def value(x, y):
  if x > y:
    return x
  elif x<y:
    return y
  elif x == y:
    return 'Same.'
  else:
    print('Not Found.')
def acos(x):
  return math.acos(x)
def acosh(x):
  return math.acosh(x)
def asin(x):
  return math.asin(x)
def asinh(x):
  return math.asinh(x)
def atan(x):
  return math.atan(x)
def atan2(x):
  return math.atan2(x)
def atanh(x):
  return math.atanh(x)
def ceil(x):
  return math.ceil(x)
def comb(k, n):
  return math.comb(k, n)
def copsig(x, y):
  return math.copysign(x, y)
def cos(x):
  return math.cos(x)
def cosh(x):
 return math.cosh(x) 
def deg(x):
  return math.degrees(x)
def dist(x, y):
  return math.dist(x, y)
def erf(x):
  return math.erf(x)
def exp(x):
  return math.exp(x)
def expm(x):
  return math.expm1(x)
def abs(x):
  return math.fabs(x)
def fact(x):
    return math.factorial(x)
def flr(x):
    return math.floor(x)
def fmod(x):
    return math.fmod(x)
def frexp(x):
    return math.frexp(x)
def gsum(x):
    return math.gsum(x)
def gamma(x):
    return math.gamma(x)
def gcd(x, y):
    return math.gcd(x, y)
def hypot(c):
    return math.hypot(c)
def icl(c, x):
    return math.isclose(c, x)
def ifin(x):
    return math.isfinite(x)
def iinf(x):
    return math.isinf(x)
def inan(x):
    return math.isnan(x)
def flsqrt(x):
    return math.isqrt(x)
def log(x, y):
    return math.log(x, y)
def log1(x):
    return math.log1p(x)
def log2(x):
    return math.log2(x)
def radc(x):
    return math.radians(x)
def sin(x):
    return math.sin(x)
def sinh(x):
    return math.sinh(x)
def sqrt(x):
    return math.sqrt(x)
def tan(x):
    return math.tan(x)
def tanh(x):
    return math.tanh(x)
def trunc(x):
    return math.trunc(x)
def e():
    return math.e()
def pi():
    return math.pi()
def tau():
    return math.tau()
def ip():
    print (socket.gethostbyname(socket.gethostname()))
def wait(nums):
  time.sleep(nums)
def libs():
      os.system("pip3 freeze > requirements.txt")
def package(packagename):
  os.system(f"pip3 install {packagename}")
def osc(command):
  os.system(f"{command}")
def filec(filename, extension):
  with open(f'{filename}.{extension}', 'w') as f:
    f.write('')
  return f'File {filename} has been made.'
def git():
      osc('git init')
def gpush():
      osc('git push')
def gcommit():
      osc('git commit')
def ls():
      osc('ls')
def cd():
      osc('cd')
def cdr(dir):
      osc(f'cd {dir}')
def malDB():
  osc('git clone https://github.com/Endermanch/MalwareDatabase.git')
  return 'Password to Zips: mysubsarethebest'
def folder(foldername):
  osc(f'mkdir {foldername}')
def running():
  osc('top')
def vi(newfile, extension):
  osc(f'vi {newfile}.{extension}')
def ctime():
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  return "Current Time =", current_time
def py3():
  osc("python3")
def runf(filename): # run only filename, no extension.
  osc(f'python3 {filename}.py')

