
### Jade-Geometry
``pip install JadeGeometry``
####Example:
```py
import JadeGeometry as JG

sa = JG.rect_prism(1, 5, 19)
print(f"The surface area of the rectangular prism is {sa}")

all = JG.add(sa, JG.rect_prism(4, 1, 29))
print(f"And added by my second prism will be will be {all}")
```
