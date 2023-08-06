pydevmgr extention for VLT devices. 

**Under construction So far only Motor and IoDev has been implemented**

The rest will be implemented on demand

# Install 

```bash
> pip install pydevmgr_vlt
```

# Basic usage 

```python 
from pydevmgr_vlt import VltMotor
from pydevmgr_core import wait

m1 = VltMotor( "m1", address="opc.tcp://192.168.1.11:4840", prefix="MAIN.Motor001")

io = VltIoDev( "m1", address="opc.tcp://192.168.1.11:4840", prefix="MAIN.IODev1")

try:
    m1.connect()
    io.connect()
    
    wait( m1.init() )

    wait( m1.move_abs(4.0, 1.0) )

    print(m1.stat.pos_actual.get())


    io.set_do( [False]*8 )
    io.set_do( {2:True, 5:True} 
    io.set_ao( {0: 45.6, 1:89.2} )

finally:
    m1.disconnect()
    io.disconnect()

```
