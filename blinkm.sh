#
# Script to write to i2c bus to play BlinkM LED pre-defined script
#
# Assumes i2c has been initialized on the Raspberry Pi
#
# Tested using Rasbian Wheezy 2012-07-15 (already includes i2c)
#
# Prerequisites:
# ==============
#
#   i2c Tools installed : 
#               sudo apt-get install i2c-tools
#
#   Modules added to '/etc/modules' file :
#               i2c-bcm2708
#               i2c-dev
#
#   Add 'pi' user to user group to read from i2c port
#               sudo usermod -a -G i2c pi
#               {logout / login}
#
#   Now should have access to i2c-0 and i2c-1
#      can check by: 
#               sudo i2cdetect -l
#
#
# Uses BlinkM device (see http://thingm.com/ OR https://www.sparkfun.com/products/8579 )
#
#       Blink M Pin     <==>     Raspberry Pi Pin
#     ----------------------------------------------
#         GND (-)                  Pin 6 - Ground
#         PWR (+)                  Pin 1 - 3.3V
#       i2c SDA (d)                Pin 3 - i2c SDA (data)
#       i2c SCL (c)                Pin 5 - i2c SCL (clock)
#
#      Blink M should be on dev i2c-0
#      can check by:
#               sudo i2cdetect 0
#
#      BlinkM device's default i2c address is 0x09
#
#     Basic command to write to i2c for Blink M is
#             i2cset -option port address data... style
#      where we'll use specific for playing script:
#           i2cset -y 0x00 0x09 0x70 0x02 0x03 0x00 i
#                   ^   ^    ^    ^    ^    ^    ^  ^
#                   |   |    |    |    |    |    |  +-- write data as i2c block
#                   |   |    |    |    |    |    +----- Start playing @ beginning
#                   |   |    |    |    |    +---------- Number of repeats (arg#2)
#                   |   |    |    |    +--------------- Script number (arg#1)
#                   |   |    |    +-------------------- Command byte for "play script"
#                   |   |    +------------------------- Address of BlinkM i2c (default)
#                   |   +------------------------------ i2c device port '0'
#                   +---------------------------------- Disable interactive mode of i2cset
#
#
#
#
#This file must have mode changed to executable to run:
#               chmod +x blinkMplay.sh
#               ./BlinkMplay.sh
#
#   2012 -- Shelton C. (SDC)

if [ $# -lt 1 ]
   then
   echo  -e "\nUsage:  $0  [-q] [-h] [script_number  [repeat_times]]"
   echo -e "         where: "
   echo -e "             -q forces BlinkM to quit the current script. "
   echo -e "             -h gives help and lists the scripts,"
   echo -e "             script_number is the ID (in HEX) of the"
   echo -e "                 pre-defined script {0x00 - 0x12}, and"
   echo -e "             [repeat_times] is the optional number of times"
   echo -e "                 to repeat the script"
   echo -e "             -q, -h, and script_number are mutually exclusive arguments.\n"
   
   exit 1
fi

if [ $# -eq 1 ] 
then
   if [ "$1" = "-q" ] ;    then
      echo "Stopping Current Script..."
      sudo i2cset -y 1 0x09 0x6f            # code to stop
      sudo i2cset -y 1 0x09 0x63 0x00 0x00 0x00 i   # code to fade to black
   
   elif [ "$1" = "-h" ] ; then
      # echo "you asked for help.  call script with no arguments and list"
      ./$0
      echo -e "\n BLINKM DEFINED SCRIPTS:"
      echo -e "Number  |    Description"
      echo -e "========|==================="
      echo -e "    0   | default startup"
      echo -e "    1   | RGB"
      echo -e "    2   | white flash"
      echo -e "    3   | red flash"
      echo -e "    4   | green flash"
      echo -e "    5   | blue flash"
      echo -e "    6   | cyan flash"
      echo -e "    7   | magenta flash"
      echo -e "    8   | yellow flash"
      echo -e "    9   | black (off)"
      echo -e "   10   | hue cycle"
      echo -e "   11   | mood light"
      echo -e "   12   | virtual candle"
      echo -e "   13   | water reflections"
      echo -e "   14   | old neon"
      echo -e "   15   | the seasons"
      echo -e "   16   | thunderstorm"
      echo -e "   17   | traffic light"
      echo -e "   18   | morse code SOS"
         
   
   elif ([ $1 -ge 0 ] && [ $1 -lt 19 ]) ; then
      echo "Playing Script $1 indefinitely..."
      sudo i2cset -y 1 0x09 0x70 $1 0x00 0x00 i
      
   else
      # one argument, but it is not understood
      echo -e "\nUnknown argument or script out of range...\n"
      exit 1                      # exit with error (not needed)
   fi
fi

if [ $# -eq 2 ]
   then
   if ([ $1 -ge 0 ] && [ $1 -lt 19 ] && [ $2 -ge 0 ]) ; then
      echo "Playing Script $1 $2 times..."
      sudo i2cset -y 1 0x09 0x70 $1 $2 0x00 i
   else
      # two arguments, but not understood
      echo -e "\n Unknown arguments or script out of range...\n"
      exit 1                     # exit with error (not needed)
   fi
fi

exit 0
