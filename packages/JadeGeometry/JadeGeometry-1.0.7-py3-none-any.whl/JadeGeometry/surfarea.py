
import math


def rect_prism(length, width, height):
  sa = 2 * (length*width) + (2 * (length*height)) + (2*(width*height))
  return sa


def irregular_prism(height, paremeter, base):
  sa = height*paremeter + 2*base
  return sa


def cylinder(radius, height):
  sa = 2*math.pi*(radius*radius) + 2*math.pi*radius*height
  return round(sa, 1)

def trapizoid(paremeter, base1, base2, height):
  b = height/2* (base1 + base2)
  sa = height*paremeter + 2*b
  return sa

