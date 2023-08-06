
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

def trapizoid(paremeter, base1, base2, height1, height_of_base):
  b = height1/2* (base1 + base2)
  sa = height_of_base*paremeter + 2*b
  return sa

def cones(radius, slant_height):
  sa = math.pi*(radius*radius) + math.pi*radius*slant_height
  return sa

def pyramids(slant_height, base_paremeter, base_area):
  pass