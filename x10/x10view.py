import sys, traceback, Ice
import x10

status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    base = ic.stringToProxy("Net:default -p 10000")
    net = x10.NetPrx.checkedCast(base)
    if not net:
        raise RuntimeError("Invalid proxy")

    net.printString("Hello World!")
except:
    traceback.print_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1

sys.exit(status)
