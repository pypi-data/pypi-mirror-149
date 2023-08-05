# Pygame Tools
This module offers many useful tools that make using pygame easier. \
The goal of this package is to be as reliable as possible offering
many customization options.

### Elements
The element is the base building block of the package, almost every
class inherits from the base Element class and adds some functionality
on top. \
An element, in its most basic form, has a position, a size and an
image. Elements can be anchored to other elements to change their
position dynamically, can be rotated around a pivot and scaled without
loosing any quality of the original image.

```python
# Declaration of an element
element = pgt.Element(
    pos=(100, 100),
    size=(100, 70),
    image=pgt.load_image('sample_image.png')
)
```

### Animations
A subclass of Element is AniElement, an element with animations. \
Animations are very flexible allowing you to change any attribute of
an element, at a constant rate. \
Animations support both a predefined list of frames and a function
that returns the appropriate value.
You can also create your custom animation by creating a class that
inherits from AniBase and defining a couple of methods!
```python
# Creating an animation that changes the alpha of an element
class MyAnimation(pgt.AniBase):
    def start(self, *args, **kwargs):
        self.element_val = self.e.alpha
        super().start(*args, **kwargs)
    
    def set_element(self):
        self.e.alpha = pgt.clamp(0, 255, self.get_frame())
    
    def reset_element(self):
        self.e.alpha = self.element_val
```

### GUI
Pygame Tools also adds a basic GUI system that implements buttons,
text labels, draggable elements, sliders and a layout system that
allows you automatically position elements and adds some functionality
to buttons.

### Draw
Pygame Tools adds some new draw functions that should probably be
in pygame itself. It adds anti-aliased versions of rects, circles
(in pygame anti-aliased circles are only empty) and lines.
The last one is present in pygame but doesn't allow you to change
its thickness

### Lang
Pygame Tools introduces a useful .lang file loader that allows you
to easily implement many languages inside your game, and it's designed
to allow an easy resource-pack implementation.
```
:: This is an example of a .lang file
%=utf-8
$this_is_a_set
  :: a set is a container for related strings
  @this_is_an_attribute:And this is it's value
  :: attributes contain strings
  .~@this_is_a_reference;this_is_an_attribute
  :: references get the value of the specified attribute or set
```

### Math
Pygame Tools adds many useful functions such as easings. \
In the math module there is also a very useful Pos (and Size) class
that can be used to access both the x and y components of the point
simultaneously.

```python
# The point class has 'x' and 'y' as attributes
p1 = Point(2, 3)
p2 = pgt.Pos(2, 3)
speed = [10, 5]

# Move the point by the speed

p1.x += speed[0]
p1.y += speed[1]

p2 += speed  # With Pos it's more concise and readable
```
