# string-color   
   
string-color is just another python module for coloring strings in print statements.   
   
### Installation   
   
`$ pip install string-color`   
   
### Python Module Usage   
   
```python   
from stringcolor import * 
   
# a few examples without background colors.   
# for color names see CLI usage below.   
print(cs("here we go", "orchid"))   
print(cs("away to space!", "DeepPink3"))   
print(cs("final fantasy", "#ffff87"))   
print()  

# bold and underline also available.  
print(cs("purple number 4, bold", "purple4").bold())  
print(cs("blue, underlined", "blue").underline())  
print(bold("bold AND underlined!").underline().cs("red", "gold"))
print(underline("the bottom line."))
print()

# yellow text with a red background.   
# color names, hex values, and ansi numbers will work.   
print(cs("warning!", "yellow", "#ff0000")) 
print()

# concat
print(cs("wild", "pink")+" stuff")
print("nothing "+cs("something", "DarkViolet2", "lightgrey6"))
print()

# use any working rgb or hex values.
# it will find the closest color available.
print(cs("this will show up red", "#ff0009"))
print(cs("so will this", "rgb(254, 0, 1)"))
print()

# use with format and f-strings
print(f"this is a test {cs('to check formatting with f-strings', 'yellow', 'grey').bold().underline()}")
print("this is a test {}".format(cs('to check the format function', 'purple', 'lightgrey11').bold().underline()))
```   
  
![Usage Screep Cap][screencap]

[screencap]: https://believe-it-or-not-im-walking-on-air.s3.amazonaws.com/sc-screen-cap.jpg "Usage Screen Cap"
  
### CLI Usage     
   
```
usage: string-color [-h] [-x] [-r] [--hsl] [-a] [-v] [color]

just another mod for printing strings in color.

positional arguments:
  color          show info for a specific color:
                 $ string-color red
                 $ string-color '#ffff87'
                 $ string-color *grey* # wildcards acceptable
                 $ string-color '#E16A7F' # any hex not found will return the closest match

optional arguments:
  -h, --help     show this help message and exit
  -x, --hex      show hex values
  -r, --rgb      show rgb values
  --hsl          show hsl values
  -a, --alpha    sort by name
  -v, --version  show program's version number and exit
```  
  
`$ string-color`   
   
display a list of all 256 colors   
   
`$ string-color yellow`   
   
show color info for the color yellow   
   
`$ string-color "#ff0000"`   
   
show color info for the hex value #ff0000   
   
`$ string-color *grey*`  
  
show all colors with "grey" in the name. also works with "grey\*" and "\*grey"  
  
![CLI Screep Cap][cliscreencap]  
  
[cliscreencap]: https://believe-it-or-not-im-walking-on-air.s3.amazonaws.com/sc-screen-cap2.jpg  "CLI Screen Cap"  
  

