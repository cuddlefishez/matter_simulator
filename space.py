from math import hypot,cos,sin,tan,acos,atan,asin,degrees,radians


# Space File
# this file has the classes and functions dealing with coordinate system objects and their math
# only functions that work on or with the classes are for here. Anything like gravity calculations
# should go else where; however displacement, angle, vector calculations can go here


class Position2i:
  def __init__(self,x=0,y=0):
    self.x = int(x)
    self.y = int(y)


  def __str__(self):
    return "("+str(self.x)+","+str(self.y)+")"


class Position2f:
  def __init__(self,x=0.0,y=0.0,angle=None):
    x = float(x)
    y = float(y)

    if angle == None:
      self.x = x
      self.y = y
    else:
      angle = float(angle)
      self.x = cos(radians(angle))
      self.y = sin(radians(angle))
      self.x = round(self.x,6)
      self.y = round(self.y,6)


  def __getattr__(self,key):
    if key == "array":
      return (self.x,self.y)
    elif key == "angle":
      angle = 0
      if self.x:
        angle = degrees(atan(self.y/self.x))
        angle = round(angle,6)
      elif self.y:
        angle = degrees(asin(self.y))
        angle = round(angle,6)
      return angle


  def __str__(self):
    return "("+str(self.x)+","+str(self.y)+")"


  def __eq__(self,other):
    if not isinstance(other,Position2f):
      return False

    if self.x != other.x:
      return False
    if self.y != other.y:
      return False
    return True


  def __add__(self,other):
    if not isinstance(other,Position2f):
      raise Exception("can't add Position2f and",type(other))
    return Position2f(self.x+other.x,self.y+other.y)


  def __radd__(self,other):
    if not isinstance(other,Position2f):
      raise Exception("can't add Position2f and",type(other))
    self.x += other.x
    self.y += other.y


  def __mul__(self,other):
    if isinstance(other,Position2f):
      return Position2f(self.x*other.x,self.y*other.y)
    elif isinstance(other,float):
      return Position2f(self.x*other,self.y*other)
    else:
      raise Exception("can't multiple Position2f and",type(other))


  def __rmul__(self,other):
    if isinstance(other,Position2f):
      self.x *= other.x
      self.y *= other.y
    elif isinstance(other,float):
      self.x *= other
      self.y *= other
    else:
      raise Exception("can't multiple Position2f and",type(other))


  def displacement(self,other):
    if not isinstance(other,Position2f):
      raise Exception("can't calculate displacement between Position2f and",type(other))

    d = Position2f()
    d.x = other.x - self.x
    d.y = other.y - self.y
    return d


class Position3f:
  def __init__(self,x=0.0,y=0.0,z=0.0,angles=None):
    x = float(x)
    y = float(y)
    z = float(z)

    if isinstance(angles,Position2f):
      self.x = sin(radians(angles.y))
      self.y = sin(radians(angles.x))
      if angles.x:
        self.z = cos(radians(angles.x))
      elif angles.y:
        self.z = cos(radians(angles.y))
      else:
        self.z = 1.0
      self.x = round(self.x,6)
      self.y = round(self.y,6)
      self.z = round(self.z,6)
    else:
      self.x = x
      self.y = y
      self.z = z


  def __getattr__(self,key):
    if key == "array":
      return (self.x,self.y,self.z)
    elif key == "angles":
      angles = Position2f()
      if not self.x and not self.y and not self.z:
        return Position2f(0,0)
      elif not self.x and not self.y and self.z:
        return Position2f(0,0)
      elif not self.x and self.y and not self.z:
        return Position2f(90,0)
      elif self.x and not self.y and not self.z:
        return Position2f(0,90)

      if self.z:
        angles.x = degrees(atan(self.y/self.z))
      if self.x:
        angles.y = degrees(atan(self.z/self.x))
      return angles



  def __str__(self):
    return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"


  def __eq__(self,other):
    if not isinstance(other,Position3f):
      return False

    if self.x != other.x:
      return False
    if self.y != other.y:
      return False
    if self.z != other.z:
      return False
    return True


  def __add__(self,other):
    if not isinstance(other,Position3f):
      raise Exception("can't add Position3f and",type(other))
    return Position3f(self.x+other.x,self.y+other.y,self.z+other.z)


  # when doing a += b self is a and other is b
  def __radd__(self,other):
    if not isinstance(other,Position3f):
      raise Exception("can't add Position3f and",type(other))

    self.x += other.x
    self.y += other.y
    self.z += other.z


  def __mul__(self,other):
    if isinstance(other,Position3f):
      return Position3f(self.x*other.x,self.y*other.y,self.z*other.z)
    elif isinstance(other,float):
      return Position3f(self.x*other,self.y*other,self.z*other)
    else:
      raise Exception("can't multiple Position3f and",type(other))


  def __rmul__(self,other):
    if isinstance(other,Position3f):
      self.x *= other.x
      self.y *= other.y
      self.z *= other.z
    elif isinstance(other,float):
      self.x *= other
      self.y *= other
      self.z *= other
    else:
      raise Exception("can't multiple Position3f and",type(other))


  def displacement(self,other):
    if not isinstance(other,Position3f):
      raise Exception("can't calculate displacement between Position3f and",type(other))

    d = Position3f()
    d.x = other.x - self.x
    d.y = other.y - self.y
    d.z = other.z - self.z
    return d


class Vector3f:
  def __init__(self,x=None,y=None,z=None,dx=None,dy=None,dz=None,origin=Position3f(),direction=Position3f()):
    if x != None and y != None and z != None and dx != None and dy != None and dz != None:
      origin = Position3f(x,y,z)
      direction = Position3f(dx,dy,dx)

    self.origin = origin
    self.direction = direction


  def __getattr__(self,key):
    if key == "displacement":
      return Position3f(direction.x-origin.x,direction.y-origin.y,direction.z-origin.z)
    elif key == "angles":
      x = self.direction.x - self.origin.x
      y = self.direction.y - self.origin.y
      z = self.direction.z - self.origin.z
      hyp = Position2f()
      angles = Position2f()
      if y:
        angles.x = degrees(atan(y/z))
        hyp.x = hypot(z,y)
      if x:
        hyp.y = hypot(x,z)
        angles.y = degrees(atan(z/x))
      return angles


  def __eq__(self,other):
    if self.origin != other.origin:
      return False
    elif self.direction != other.direction:
      return False
    return True