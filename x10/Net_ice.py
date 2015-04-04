# **********************************************************************
#
# Copyright (c) 2003-2011 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************
#
# Ice version 3.4.2
#
# <auto-generated>
#
# Generated from file `Net.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

import Ice, IcePy, __builtin__

# Start of module x10
_M_x10 = Ice.openModule('x10')
__name__ = 'x10'

if not _M_x10.__dict__.has_key('Net'):
    _M_x10.Net = Ice.createTempClass()
    class Net(Ice.Object):
        def __init__(self):
            if __builtin__.type(self) == _M_x10.Net:
                raise RuntimeError('x10.Net is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::x10::Net')

        def ice_id(self, current=None):
            return '::x10::Net'

        def ice_staticId():
            return '::x10::Net'
        ice_staticId = staticmethod(ice_staticId)

        def sendMsg(self, s, current=None):
            pass

        def showEnvironment(self, current=None):
            pass

        def getEnvironment(self, current=None):
            pass

        def setActive(self, name, current=None):
            pass

        def setInactive(self, name, current=None):
            pass

        def addModule(self, name, code, mtype, current=None):
            pass

        def delModule(self, name, current=None):
            pass

        def getAlarm(self, name, current=None):
            pass

        def setAlarm(self, name, sh, sm, eh, em, act, current=None):
            pass

        def isSensor(self, name, current=None):
            pass

        def delModulebyCode(self, code, current=None):
            pass

        def changeNamebyCode(self, name, code, current=None):
            pass

        def changeName(self, newname, name, current=None):
            pass

        def isActivebyCode(self, code, current=None):
            pass

        def isAtive(self, name, current=None):
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_x10._t_Net)

        __repr__ = __str__

    _M_x10.NetPrx = Ice.createTempClass()
    class NetPrx(Ice.ObjectPrx):

        def sendMsg(self, s, _ctx=None):
            return _M_x10.Net._op_sendMsg.invoke(self, ((s, ), _ctx))

        def begin_sendMsg(self, s, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_sendMsg.begin(self, ((s, ), _response, _ex, _sent, _ctx))

        def end_sendMsg(self, _r):
            return _M_x10.Net._op_sendMsg.end(self, _r)

        def showEnvironment(self, _ctx=None):
            return _M_x10.Net._op_showEnvironment.invoke(self, ((), _ctx))

        def begin_showEnvironment(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_showEnvironment.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_showEnvironment(self, _r):
            return _M_x10.Net._op_showEnvironment.end(self, _r)

        def getEnvironment(self, _ctx=None):
            return _M_x10.Net._op_getEnvironment.invoke(self, ((), _ctx))

        def begin_getEnvironment(self, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_getEnvironment.begin(self, ((), _response, _ex, _sent, _ctx))

        def end_getEnvironment(self, _r):
            return _M_x10.Net._op_getEnvironment.end(self, _r)

        def setActive(self, name, _ctx=None):
            return _M_x10.Net._op_setActive.invoke(self, ((name, ), _ctx))

        def begin_setActive(self, name, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_setActive.begin(self, ((name, ), _response, _ex, _sent, _ctx))

        def end_setActive(self, _r):
            return _M_x10.Net._op_setActive.end(self, _r)

        def setInactive(self, name, _ctx=None):
            return _M_x10.Net._op_setInactive.invoke(self, ((name, ), _ctx))

        def begin_setInactive(self, name, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_setInactive.begin(self, ((name, ), _response, _ex, _sent, _ctx))

        def end_setInactive(self, _r):
            return _M_x10.Net._op_setInactive.end(self, _r)

        def addModule(self, name, code, mtype, _ctx=None):
            return _M_x10.Net._op_addModule.invoke(self, ((name, code, mtype), _ctx))

        def begin_addModule(self, name, code, mtype, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_addModule.begin(self, ((name, code, mtype), _response, _ex, _sent, _ctx))

        def end_addModule(self, _r):
            return _M_x10.Net._op_addModule.end(self, _r)

        def delModule(self, name, _ctx=None):
            return _M_x10.Net._op_delModule.invoke(self, ((name, ), _ctx))

        def begin_delModule(self, name, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_delModule.begin(self, ((name, ), _response, _ex, _sent, _ctx))

        def end_delModule(self, _r):
            return _M_x10.Net._op_delModule.end(self, _r)

        def getAlarm(self, name, _ctx=None):
            return _M_x10.Net._op_getAlarm.invoke(self, ((name, ), _ctx))

        def begin_getAlarm(self, name, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_getAlarm.begin(self, ((name, ), _response, _ex, _sent, _ctx))

        def end_getAlarm(self, _r):
            return _M_x10.Net._op_getAlarm.end(self, _r)

        def setAlarm(self, name, sh, sm, eh, em, act, _ctx=None):
            return _M_x10.Net._op_setAlarm.invoke(self, ((name, sh, sm, eh, em, act), _ctx))

        def begin_setAlarm(self, name, sh, sm, eh, em, act, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_setAlarm.begin(self, ((name, sh, sm, eh, em, act), _response, _ex, _sent, _ctx))

        def end_setAlarm(self, _r):
            return _M_x10.Net._op_setAlarm.end(self, _r)

        def isSensor(self, name, _ctx=None):
            return _M_x10.Net._op_isSensor.invoke(self, ((name, ), _ctx))

        def begin_isSensor(self, name, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_isSensor.begin(self, ((name, ), _response, _ex, _sent, _ctx))

        def end_isSensor(self, _r):
            return _M_x10.Net._op_isSensor.end(self, _r)

        def delModulebyCode(self, code, _ctx=None):
            return _M_x10.Net._op_delModulebyCode.invoke(self, ((code, ), _ctx))

        def begin_delModulebyCode(self, code, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_delModulebyCode.begin(self, ((code, ), _response, _ex, _sent, _ctx))

        def end_delModulebyCode(self, _r):
            return _M_x10.Net._op_delModulebyCode.end(self, _r)

        def changeNamebyCode(self, name, code, _ctx=None):
            return _M_x10.Net._op_changeNamebyCode.invoke(self, ((name, code), _ctx))

        def begin_changeNamebyCode(self, name, code, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_changeNamebyCode.begin(self, ((name, code), _response, _ex, _sent, _ctx))

        def end_changeNamebyCode(self, _r):
            return _M_x10.Net._op_changeNamebyCode.end(self, _r)

        def changeName(self, newname, name, _ctx=None):
            return _M_x10.Net._op_changeName.invoke(self, ((newname, name), _ctx))

        def begin_changeName(self, newname, name, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_changeName.begin(self, ((newname, name), _response, _ex, _sent, _ctx))

        def end_changeName(self, _r):
            return _M_x10.Net._op_changeName.end(self, _r)

        def isActivebyCode(self, code, _ctx=None):
            return _M_x10.Net._op_isActivebyCode.invoke(self, ((code, ), _ctx))

        def begin_isActivebyCode(self, code, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_isActivebyCode.begin(self, ((code, ), _response, _ex, _sent, _ctx))

        def end_isActivebyCode(self, _r):
            return _M_x10.Net._op_isActivebyCode.end(self, _r)

        def isAtive(self, name, _ctx=None):
            return _M_x10.Net._op_isAtive.invoke(self, ((name, ), _ctx))

        def begin_isAtive(self, name, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_x10.Net._op_isAtive.begin(self, ((name, ), _response, _ex, _sent, _ctx))

        def end_isAtive(self, _r):
            return _M_x10.Net._op_isAtive.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_x10.NetPrx.ice_checkedCast(proxy, '::x10::Net', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_x10.NetPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

    _M_x10._t_NetPrx = IcePy.defineProxy('::x10::Net', NetPrx)

    _M_x10._t_Net = IcePy.defineClass('::x10::Net', Net, (), True, None, (), ())
    Net._ice_type = _M_x10._t_Net

    Net._op_sendMsg = IcePy.Operation('sendMsg', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string),), (), None, ())
    Net._op_showEnvironment = IcePy.Operation('showEnvironment', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (), (), IcePy._t_string, ())
    Net._op_getEnvironment = IcePy.Operation('getEnvironment', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (), (), IcePy._t_string, ())
    Net._op_setActive = IcePy.Operation('setActive', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string),), (), None, ())
    Net._op_setInactive = IcePy.Operation('setInactive', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string),), (), None, ())
    Net._op_addModule = IcePy.Operation('addModule', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_string)), (), None, ())
    Net._op_delModule = IcePy.Operation('delModule', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string),), (), None, ())
    Net._op_getAlarm = IcePy.Operation('getAlarm', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string),), (), IcePy._t_string, ())
    Net._op_setAlarm = IcePy.Operation('setAlarm', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_string), ((), IcePy._t_bool)), (), None, ())
    Net._op_isSensor = IcePy.Operation('isSensor', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string),), (), IcePy._t_bool, ())
    Net._op_delModulebyCode = IcePy.Operation('delModulebyCode', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string),), (), None, ())
    Net._op_changeNamebyCode = IcePy.Operation('changeNamebyCode', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string)), (), None, ())
    Net._op_changeName = IcePy.Operation('changeName', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string), ((), IcePy._t_string)), (), None, ())
    Net._op_isActivebyCode = IcePy.Operation('isActivebyCode', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string),), (), IcePy._t_bool, ())
    Net._op_isAtive = IcePy.Operation('isAtive', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, (), (((), IcePy._t_string),), (), IcePy._t_bool, ())

    _M_x10.Net = Net
    del Net

    _M_x10.NetPrx = NetPrx
    del NetPrx

# End of module x10
