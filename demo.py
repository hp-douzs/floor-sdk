#!/usr/bin/env python
# coding: utf-8
'''
Created on 2017-10-25

@author: 
'''

from ImageConvert import *
from MVSDK import *
import struct
import time
import datetime

g_cameraStatusUserInfo = b"statusInfo"

class BITMAPFILEHEADER(Structure):
    _fields_ = [
                ('bfType', c_ushort),
                ('bfSize', c_uint),
                ('bfReserved1', c_ushort),
                ('bfReserved2', c_ushort),
                ('bfOffBits', c_uint),
                ]
 
class BITMAPINFOHEADER(Structure):
    _fields_ = [
                ('biSize', c_uint),
                ('biWidth', c_int),
                ('biHeight', c_int),
                ('biPlanes', c_ushort),
                ('biBitCount', c_ushort),
                ('biCompression', c_uint),
                ('biSizeImage', c_uint),
                ('biXPelsPerMeter', c_int),
                ('biYPelsPerMeter', c_int),
                ('biClrUsed', c_uint),
                ('biClrImportant', c_uint),
                ] 

# 调色板，只有8bit及以下才需要
# color palette
class RGBQUAD(Structure):
    _fields_ = [
                ('rgbBlue', c_ubyte),
                ('rgbGreen', c_ubyte),
                ('rgbRed', c_ubyte),
                ('rgbReserved', c_ubyte),
                ]

# 取流回调函数
# grabbing callback function                             
def onGetFrame(frame):
    nRet = frame.contents.valid(frame)
    if ( nRet != 0):
        print("frame is invalid!")
        # 释放驱动图像缓存资源
        # release frame resource before return
        frame.contents.release(frame)
        return    
    
    print("BlockId = %d"  %(frame.contents.getBlockId(frame)))
    #此处客户应用程序应将图像拷贝出使用
    #Here you can copy image data out from frame for your own use
    '''
    '''
    # 释放驱动图像缓存资源
    # release frame resource at the end of use
    frame.contents.release(frame)

# 取流回调函数Ex
# grabbing callback function with userInfo parameter
def onGetFrameEx(frame, userInfo):
    nRet = frame.contents.valid(frame)
    if ( nRet != 0):
        print("frame is invalid!")
        # 释放驱动图像缓存资源
        # release frame resource before return
        frame.contents.release(frame)
        return         
 
    print("BlockId = %d userInfo = %s"  %(frame.contents.getBlockId(frame), c_char_p(userInfo).value))
    #此处客户应用程序应将图像拷贝出使用
    #Here you should copy image data out from frame for your own use
    '''
    '''
    # 释放驱动图像缓存资源
    # release frame resource at the end of use
    frame.contents.release(frame)

# 相机连接状态回调函数
# camera connection status change callback
def deviceLinkNotify(connectArg, linkInfo):
    if ( EVType.offLine == connectArg.contents.m_event ):
        print("camera has off line, userInfo [%s]" %(c_char_p(linkInfo).value))
    elif ( EVType.onLine == connectArg.contents.m_event ):
        print("camera has on line, userInfo [%s]" %(c_char_p(linkInfo).value))
    

connectCallBackFuncEx = connectCallBackEx(deviceLinkNotify)
frameCallbackFunc = callbackFunc(onGetFrame)
frameCallbackFuncEx = callbackFuncEx(onGetFrameEx)

# 注册相机连接状态回调
# subscribe camera connection status change
def subscribeCameraStatus(camera):
    # 注册上下线通知
    # subscribe connection status notify
    eventSubscribe = pointer(GENICAM_EventSubscribe())
    eventSubscribeInfo = GENICAM_EventSubscribeInfo()
    eventSubscribeInfo.pCamera = pointer(camera)
    nRet = GENICAM_createEventSubscribe(byref(eventSubscribeInfo), byref(eventSubscribe))
    if ( nRet != 0):
        print("create eventSubscribe fail!")
        return -1
    
    nRet = eventSubscribe.contents.subscribeConnectArgsEx(eventSubscribe, connectCallBackFuncEx, g_cameraStatusUserInfo)
    if ( nRet != 0 ):
        print("subscribeConnectArgsEx fail!")
        # 释放相关资源
        # release subscribe resource before return
        eventSubscribe.contents.release(eventSubscribe)
        return -1  
    
    # 不再使用时，需释放相关资源
    # release subscribe resource at the end of use
    eventSubscribe.contents.release(eventSubscribe) 
    return 0

# 反注册相机连接状态回调
# unsubscribe camera connection status change
def unsubscribeCameraStatus(camera):
    # 反注册上下线通知
    # unsubscribe connection status notify
    eventSubscribe = pointer(GENICAM_EventSubscribe())
    eventSubscribeInfo = GENICAM_EventSubscribeInfo()
    eventSubscribeInfo.pCamera = pointer(camera)
    nRet = GENICAM_createEventSubscribe(byref(eventSubscribeInfo), byref(eventSubscribe))
    if ( nRet != 0):
        print("create eventSubscribe fail!")
        return -1
        
    nRet = eventSubscribe.contents.unsubscribeConnectArgsEx(eventSubscribe, connectCallBackFuncEx, g_cameraStatusUserInfo)
    if ( nRet != 0 ):
        print("unsubscribeConnectArgsEx fail!")
        # 释放相关资源
        # release subscribe resource before return
        eventSubscribe.contents.release(eventSubscribe)
        return -1
    
    # 不再使用时，需释放相关资源
    # release subscribe resource at the end of use
    eventSubscribe.contents.release(eventSubscribe)
    return 0   

# 设置软触发
# set software trigger
def setSoftTriggerConf(camera):
    # 创建AcquisitionControl节点
    # create AcquisitionControl node
    acqCtrlInfo = GENICAM_AcquisitionControlInfo()
    acqCtrlInfo.pCamera = pointer(camera)
    acqCtrl = pointer(GENICAM_AcquisitionControl())
    nRet = GENICAM_createAcquisitionControl(pointer(acqCtrlInfo), byref(acqCtrl))
    if ( nRet != 0 ):
        print("create AcquisitionControl fail!")
        return -1
    
    # 设置触发源为软触发
    # set trigger source to Software
    trigSourceEnumNode = acqCtrl.contents.triggerSource(acqCtrl)
    nRet = trigSourceEnumNode.setValueBySymbol(byref(trigSourceEnumNode), b"Software")
    if ( nRet != 0 ):
        print("set TriggerSource value [Software] fail!")
        # 释放相关资源
        # release node resource before return
        trigSourceEnumNode.release(byref(trigSourceEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1
    
    # 需要释放Node资源
    # release node resource at the end of use
    trigSourceEnumNode.release(byref(trigSourceEnumNode))
    
    # 设置触发方式
    # set trigger selector to FrameStart
    trigSelectorEnumNode = acqCtrl.contents.triggerSelector(acqCtrl)
    nRet = trigSelectorEnumNode.setValueBySymbol(byref(trigSelectorEnumNode), b"FrameStart")
    if ( nRet != 0 ):
        print("set TriggerSelector value [FrameStart] fail!")
        # 释放相关资源
        # release node resource before return
        trigSelectorEnumNode.release(byref(trigSelectorEnumNode))
        acqCtrl.contents.release(acqCtrl) 
        return -1
     
    # 需要释放Node资源
    # release node resource at the end of use
    trigSelectorEnumNode.release(byref(trigSelectorEnumNode))
    
    # 打开触发模式
    # set trigger mode to On
    trigModeEnumNode = acqCtrl.contents.triggerMode(acqCtrl)
    nRet = trigModeEnumNode.setValueBySymbol(byref(trigModeEnumNode), b"On")
    if ( nRet != 0 ):
        print("set TriggerMode value [On] fail!")
        # 释放相关资源
        # release node resource before return
        trigModeEnumNode.release(byref(trigModeEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1
    
    # 需要释放相关资源
    # release node resource at the end of use
    trigModeEnumNode.release(byref(trigModeEnumNode))
    acqCtrl.contents.release(acqCtrl)
    
    return 0     

# 设置外触发
# set external trigger
def setLineTriggerConf(camera):
    # 创建AcquisitionControl节点
    # create AcquisitionControl node
    acqCtrlInfo = GENICAM_AcquisitionControlInfo()
    acqCtrlInfo.pCamera = pointer(camera)
    acqCtrl = pointer(GENICAM_AcquisitionControl())
    nRet = GENICAM_createAcquisitionControl(pointer(acqCtrlInfo), byref(acqCtrl))
    if ( nRet != 0 ):
        print("create AcquisitionControl fail!")
        return -1
    
    # 设置触发源为外触发Line1
    # set trigger source to Line1
    trigSourceEnumNode = acqCtrl.contents.triggerSource(acqCtrl)
    nRet = trigSourceEnumNode.setValueBySymbol(byref(trigSourceEnumNode), b"Line1")
    if ( nRet != 0 ):
        print("set TriggerSource value [Line1] fail!")
        # 释放相关资源
        # release node resource before return
        trigSourceEnumNode.release(byref(trigSourceEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1
    
    # 需要释放Node资源
    # release node resource at the end of use
    trigSourceEnumNode.release(byref(trigSourceEnumNode))
    
    # 设置触发方式
    # set trigger selector to FrameStart
    trigSelectorEnumNode = acqCtrl.contents.triggerSelector(acqCtrl)
    nRet = trigSelectorEnumNode.setValueBySymbol(byref(trigSelectorEnumNode), b"FrameStart")
    if ( nRet != 0 ):
        print("set TriggerSelector value [FrameStart] fail!")
        # 释放相关资源
        # release node resource before return
        trigSelectorEnumNode.release(byref(trigSelectorEnumNode))
        acqCtrl.contents.release(acqCtrl) 
        return -1
     
    # 需要释放Node资源
    # release node resource at the end of use
    trigSelectorEnumNode.release(byref(trigSelectorEnumNode))
    
    # 打开触发模式
    # set trigger mode to On
    trigModeEnumNode = acqCtrl.contents.triggerMode(acqCtrl)
    nRet = trigModeEnumNode.setValueBySymbol(byref(trigModeEnumNode), b"On")
    if ( nRet != 0 ):
        print("set TriggerMode value [On] fail!")
        # 释放相关资源
        # release node resource before return
        trigModeEnumNode.release(byref(trigModeEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1
    
    # 需要释放Node资源
    # release node resource at the end of use
    trigModeEnumNode.release(byref(trigModeEnumNode))
    
    # 设置触发沿
    # set trigger activation to RisingEdge
    trigActivationEnumNode = acqCtrl.contents.triggerActivation(acqCtrl)
    nRet = trigActivationEnumNode.setValueBySymbol(byref(trigActivationEnumNode), b"RisingEdge")
    if ( nRet != 0 ):
        print("set TriggerActivation value [RisingEdge] fail!")
        # 释放相关资源
        # release node resource before return
        trigActivationEnumNode.release(byref(trigActivationEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1
    
    # 需要释放Node资源
    # release node resource at the end of use
    trigActivationEnumNode.release(byref(trigActivationEnumNode))
    acqCtrl.contents.release(acqCtrl)
    return 0 

# 打开相机
# open camera
def openCamera(camera):
    # 连接相机
    # connect camera
    nRet = camera.connect(camera, c_int(GENICAM_ECameraAccessPermission.accessPermissionControl))
    if ( nRet != 0 ):
        print("camera connect fail!")
        return -1
    else:
        print("camera connect success.")
  
    # 注册相机连接状态回调
    # subscribe camera connection status change
    nRet = subscribeCameraStatus(camera)
    if ( nRet != 0 ):
        print("subscribeCameraStatus fail!")
        return -1

    return 0

# 关闭相机
# close camera
def closeCamera(camera):
    # 反注册相机连接状态回调
    # unsubscribe camera connection status change
    nRet = unsubscribeCameraStatus(camera)
    if ( nRet != 0 ):
        print("unsubscribeCameraStatus fail!")
        return -1
  
    # 断开相机
    # disconnect camera
    nRet = camera.disConnect(byref(camera))
    if ( nRet != 0 ):
        print("disConnect camera fail!")
        return -1
    
    return 0    

# 设置曝光
# set camera ExposureTime
def setExposureTime(camera, dVal):
    # 通用属性设置:设置曝光 --根据属性类型，直接构造属性节点。如曝光是 double类型，构造doubleNode节点
    # create corresponding property node according to the value type of property, here is doubleNode
    exposureTimeNode = pointer(GENICAM_DoubleNode())
    exposureTimeNodeInfo = GENICAM_DoubleNodeInfo() 
    exposureTimeNodeInfo.pCamera = pointer(camera)
    exposureTimeNodeInfo.attrName = b"ExposureTime"
    nRet = GENICAM_createDoubleNode(byref(exposureTimeNodeInfo), byref(exposureTimeNode))
    if ( nRet != 0 ):
        print("create ExposureTime Node fail!")
        return -1
      
    # 设置曝光时间
    # set ExposureTime
    nRet = exposureTimeNode.contents.setValue(exposureTimeNode, c_double(dVal))  
    if ( nRet != 0 ):
        print("set ExposureTime value [%f]us fail!"  % (dVal))
        # 释放相关资源
        # release node resource before return
        exposureTimeNode.contents.release(exposureTimeNode)
        return -1
    else:
        print("set ExposureTime value [%f]us success." % (dVal))
            
    # 释放节点资源
    # release node resource at the end of use
    exposureTimeNode.contents.release(exposureTimeNode)    
    return 0
    
# 枚举相机
# enumerate camera
def enumCameras():
    # 获取系统单例
    # get system instance
    system = pointer(GENICAM_System())
    nRet = GENICAM_getSystemInstance(byref(system))
    if ( nRet != 0 ):
        print("getSystemInstance fail!")
        return None, None

    # 发现相机
    # discover camera 
    cameraList = pointer(GENICAM_Camera()) 
    cameraCnt = c_uint()
    nRet = system.contents.discovery(system, byref(cameraList), byref(cameraCnt), c_int(GENICAM_EProtocolType.typeAll));
    if ( nRet != 0 ):
        print("discovery fail!")
        return None, None
    elif cameraCnt.value < 1:
        print("discovery no camera!")
        return None, None
    else:
        print("cameraCnt: " + str(cameraCnt.value))
        return cameraCnt.value, cameraList

def grabOne(camera):
    # 创建流对象
    # create stream source object
    streamSourceInfo = GENICAM_StreamSourceInfo()
    streamSourceInfo.channelId = 0
    streamSourceInfo.pCamera = pointer(camera)
      
    streamSource = pointer(GENICAM_StreamSource())
    nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(streamSource))
    if ( nRet != 0 ):
        print("create StreamSource fail!")     
        return -1
    
    # 创建AcquisitionControl节点
    # create AcquisitionControl node
    acqCtrlInfo = GENICAM_AcquisitionControlInfo()
    acqCtrlInfo.pCamera = pointer(camera)
    acqCtrl = pointer(GENICAM_AcquisitionControl())
    nRet = GENICAM_createAcquisitionControl(pointer(acqCtrlInfo), byref(acqCtrl))
    if ( nRet != 0 ):
        print("create AcquisitionControl fail!")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)  
        return -1
        
    # 执行一次软触发
    # execute software trigger once
    trigSoftwareCmdNode = acqCtrl.contents.triggerSoftware(acqCtrl)
    nRet = trigSoftwareCmdNode.execute(byref(trigSoftwareCmdNode))
    if( nRet != 0 ):
        print("Execute triggerSoftware fail!")
        # 释放相关资源
        # release node resource before return
        trigSoftwareCmdNode.release(byref(trigSoftwareCmdNode))
        acqCtrl.contents.release(acqCtrl)
        streamSource.contents.release(streamSource)   
        return -1   

    # 释放相关资源
    # release node resource at the end of use
    trigSoftwareCmdNode.release(byref(trigSoftwareCmdNode))
    acqCtrl.contents.release(acqCtrl)
    streamSource.contents.release(streamSource) 
    
    return 0  

# 设置感兴趣区域  --- 感兴趣区域的宽高 和 xy方向的偏移量  入参值应符合对应相机的递增规则
# set ROI
def setROI(camera, OffsetX, OffsetY, nWidth, nHeight):
    # 获取原始的宽度
    # get the max width of image
    widthMaxNode = pointer(GENICAM_IntNode())
    widthMaxNodeInfo = GENICAM_IntNodeInfo() 
    widthMaxNodeInfo.pCamera = pointer(camera)
    widthMaxNodeInfo.attrName = b"WidthMax"
    nRet = GENICAM_createIntNode(byref(widthMaxNodeInfo), byref(widthMaxNode))
    if ( nRet != 0 ):
        print("create WidthMax Node fail!")
        return -1
    
    oriWidth = c_longlong()
    nRet = widthMaxNode.contents.getValue(widthMaxNode, byref(oriWidth))
    if ( nRet != 0 ):
        print("widthMaxNode getValue fail!")
        # 释放相关资源
        # release node resource before return
        widthMaxNode.contents.release(widthMaxNode)
        return -1  
    
    # 释放相关资源
    # release node resource at the end of use
    widthMaxNode.contents.release(widthMaxNode)
    
    # 获取原始的高度
    # get the max height of image
    heightMaxNode = pointer(GENICAM_IntNode())
    heightMaxNodeInfo = GENICAM_IntNodeInfo() 
    heightMaxNodeInfo.pCamera = pointer(camera)
    heightMaxNodeInfo.attrName = b"HeightMax"
    nRet = GENICAM_createIntNode(byref(heightMaxNodeInfo), byref(heightMaxNode))
    if ( nRet != 0 ):
        print("create HeightMax Node fail!")
        return -1
    
    oriHeight = c_longlong()
    nRet = heightMaxNode.contents.getValue(heightMaxNode, byref(oriHeight))
    if ( nRet != 0 ):
        print("heightMaxNode getValue fail!")
        # 释放相关资源
        # release node resource before return
        heightMaxNode.contents.release(heightMaxNode)
        return -1
    
    # 释放相关资源
    # release node resource at the end of use
    heightMaxNode.contents.release(heightMaxNode)
        
    # 检验参数
    # check parameter valid
    if ( ( oriWidth.value < (OffsetX + nWidth)) or ( oriHeight.value < (OffsetY + nHeight)) ):
        print("please check input param!")
        return -1
    
    # 设置宽度
    # set image width
    widthNode = pointer(GENICAM_IntNode())
    widthNodeInfo = GENICAM_IntNodeInfo() 
    widthNodeInfo.pCamera = pointer(camera)
    widthNodeInfo.attrName = b"Width"
    nRet = GENICAM_createIntNode(byref(widthNodeInfo), byref(widthNode))
    if ( nRet != 0 ):
        print("create Width Node fail!") 
        return -1
    
    nRet = widthNode.contents.setValue(widthNode, c_longlong(nWidth))
    if ( nRet != 0 ):
        print("widthNode setValue [%d] fail!" % (nWidth))
        # 释放相关资源
        # release node resource before return
        widthNode.contents.release(widthNode)
        return -1  
    
    # 释放相关资源
    # release node resource at the end of use
    widthNode.contents.release(widthNode)
    
    # 设置高度
    # set image height
    heightNode = pointer(GENICAM_IntNode())
    heightNodeInfo = GENICAM_IntNodeInfo() 
    heightNodeInfo.pCamera = pointer(camera)
    heightNodeInfo.attrName = b"Height"
    nRet = GENICAM_createIntNode(byref(heightNodeInfo), byref(heightNode))
    if ( nRet != 0 ):
        print("create Height Node fail!")
        return -1
    
    nRet = heightNode.contents.setValue(heightNode, c_longlong(nHeight))
    if ( nRet != 0 ):
        print("heightNode setValue [%d] fail!" % (nHeight))
        # 释放相关资源
        # release node resource before return
        heightNode.contents.release(heightNode)
        return -1    
    
    # 释放相关资源
    # release node resource at the end of use
    heightNode.contents.release(heightNode)    
    
    # 设置OffsetX
    # set OffsetX
    OffsetXNode = pointer(GENICAM_IntNode())
    OffsetXNodeInfo = GENICAM_IntNodeInfo() 
    OffsetXNodeInfo.pCamera = pointer(camera)
    OffsetXNodeInfo.attrName = b"OffsetX"
    nRet = GENICAM_createIntNode(byref(OffsetXNodeInfo), byref(OffsetXNode))
    if ( nRet != 0 ):
        print("create OffsetX Node fail!")
        return -1
    
    nRet = OffsetXNode.contents.setValue(OffsetXNode, c_longlong(OffsetX))
    if ( nRet != 0 ):
        print("OffsetX setValue [%d] fail!" % (OffsetX))
        # 释放相关资源
        # release node resource before return
        OffsetXNode.contents.release(OffsetXNode)
        return -1    
    
    # 释放相关资源
    # release node resource at the end of use
    OffsetXNode.contents.release(OffsetXNode)  
    
    # 设置OffsetY
    # set OffsetY
    OffsetYNode = pointer(GENICAM_IntNode())
    OffsetYNodeInfo = GENICAM_IntNodeInfo() 
    OffsetYNodeInfo.pCamera = pointer(camera)
    OffsetYNodeInfo.attrName = b"OffsetY"
    nRet = GENICAM_createIntNode(byref(OffsetYNodeInfo), byref(OffsetYNode))
    if ( nRet != 0 ):
        print("create OffsetY Node fail!")
        return -1
    
    nRet = OffsetYNode.contents.setValue(OffsetYNode, c_longlong(OffsetY))
    if ( nRet != 0 ):
        print("OffsetY setValue [%d] fail!" % (OffsetY))
        # 释放相关资源
        # release node resource before return
        OffsetYNode.contents.release(OffsetYNode)
        return -1    
    
    # 释放相关资源
    # release node resource at the end of use
    OffsetYNode.contents.release(OffsetYNode)   
    return 0

def demo():    
    # 发现相机
    # enumerate camera
    cameraCnt, cameraList = enumCameras()
    if cameraCnt is None:
        return -1
    
    # 显示相机信息
    # print camera info
    for index in range(0, cameraCnt):
        camera = cameraList[index]
        print("\nCamera Id = " + str(index))
        print("Key           = " + str(camera.getKey(camera)))
        print("vendor name   = " + str(camera.getVendorName(camera)))
        print("Model  name   = " + str(camera.getModelName(camera)))
        print("Serial number = " + str(camera.getSerialNumber(camera)))
        
    camera = cameraList[0]

    # 打开相机
    # open camera
    nRet = openCamera(camera)
    if ( nRet != 0 ):
        print("openCamera fail.")
        return -1;
        
    # 创建流对象
    # create stream source object
    streamSourceInfo = GENICAM_StreamSourceInfo()
    streamSourceInfo.channelId = 0
    streamSourceInfo.pCamera = pointer(camera)
      
    streamSource = pointer(GENICAM_StreamSource())
    nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(streamSource))
    if ( nRet != 0 ):
        print("create StreamSource fail!")
        return -1
    
    # 通用属性设置:设置触发模式为off --根据属性类型，直接构造属性节点。如触发模式是 enumNode，构造enumNode节点
    # create corresponding property node according to the value type of property, here is enumNode
    # 自由拉流：TriggerMode 需为 off
    # set trigger mode to Off for continuously grabbing
    trigModeEnumNode = pointer(GENICAM_EnumNode())
    trigModeEnumNodeInfo = GENICAM_EnumNodeInfo() 
    trigModeEnumNodeInfo.pCamera = pointer(camera)
    trigModeEnumNodeInfo.attrName = b"TriggerMode"
    nRet = GENICAM_createEnumNode(byref(trigModeEnumNodeInfo), byref(trigModeEnumNode))
    if ( nRet != 0 ):
        print("create TriggerMode Node fail!")
        # 释放相关资源
        # release node resource before return
        streamSource.contents.release(streamSource) 
        return -1
    
    nRet = trigModeEnumNode.contents.setValueBySymbol(trigModeEnumNode, b"Off")
    if ( nRet != 0 ):
        print("set TriggerMode value [Off] fail!")
        # 释放相关资源
        # release node resource before return
        trigModeEnumNode.contents.release(trigModeEnumNode)
        streamSource.contents.release(streamSource) 
        return -1
      
    # 需要释放Node资源
    # release node resource at the end of use  
    trigModeEnumNode.contents.release(trigModeEnumNode) 
          
    # 注册拉流回调函数
    # subscribe grabbing callback
    userInfo = b"test"
    nRet = streamSource.contents.attachGrabbingEx(streamSource, frameCallbackFuncEx, userInfo)    
    if ( nRet != 0 ):
        print("attachGrabbingEx fail!")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)  
        return -1
          
    # 开始拉流
    # start grabbing
    nRet = streamSource.contents.startGrabbing(streamSource, c_ulonglong(0), \
                                               c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
    if( nRet != 0):
        print("startGrabbing fail!")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)   
        return -1
      
    # 自由拉流3秒
    # grabbing 3 seconds
    time.sleep(3)
  
    # 反注册回调函数
    # unsubscribe grabbing callback
    nRet = streamSource.contents.detachGrabbingEx(streamSource, frameCallbackFuncEx, userInfo) 
    if ( nRet != 0 ):
        print("detachGrabbingEx fail!")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)  
        return -1

    # 停止拉流
    # stop grabbing
    nRet = streamSource.contents.stopGrabbing(streamSource)
    if ( nRet != 0 ):
        print("stopGrabbing fail!")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)  
        return -1
    
    # 设置软触发
    # set software trigger config
    nRet = setSoftTriggerConf(camera)
    if ( nRet != 0 ):
        print("set SoftTriggerConf fail!")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)   
        return -1
    else:
        print("set SoftTriggerConf success!")
                    
    # 开始拉流
    # start grabbing
    nRet = streamSource.contents.startGrabbing(streamSource, c_ulonglong(0), \
                                               c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
    if( nRet != 0 ):
        print("startGrabbing fail!")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)   
        return -1

    # Sleep 1秒
    # sleep 1 second
    time.sleep(1)

    # 软触发取一张图
    # execute software trigger to grab one frame 
    nRet = grabOne(camera)  
    if( nRet != 0 ):
        print("grabOne fail!")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)   
        return -1      
    else:
        print("trigger time: " + str(datetime.datetime.now()))
    
    # 主动取图
    # get one frame
    frame = pointer(GENICAM_Frame())
    nRet = streamSource.contents.getFrame(streamSource, byref(frame), c_uint(1000))
    if ( nRet != 0 ):
        print("SoftTrigger getFrame fail! timeOut [1000]ms")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)   
        return -1 
    else:
        print("SoftTrigger getFrame success BlockId = " + str(frame.contents.getBlockId(frame))) 
        print("get frame time: " + str(datetime.datetime.now()))   
      
    nRet = frame.contents.valid(frame)
    if ( nRet != 0 ):
        print("frame is invalid!")
        # 释放驱动图像缓存资源
        # release frame resource before return
        frame.contents.release(frame)
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)
        return -1 
      
    # 将裸数据图像拷出
    # copy image data out from frame
    imageSize = frame.contents.getImageSize(frame)
    buffAddr = frame.contents.getImage(frame)
    frameBuff = c_buffer(b'\0', imageSize)
    memmove(frameBuff, c_char_p(buffAddr), imageSize)
  
    # 给转码所需的参数赋值
    # fill conversion parameter
    convertParams = IMGCNV_SOpenParam()
    convertParams.dataSize = imageSize
    convertParams.height = frame.contents.getImageHeight(frame)
    convertParams.width = frame.contents.getImageWidth(frame)
    convertParams.paddingX = frame.contents.getImagePaddingX(frame)
    convertParams.paddingY = frame.contents.getImagePaddingY(frame)
    convertParams.pixelForamt = frame.contents.getImagePixelFormat(frame)
      
    # 释放驱动图像缓存
    # release frame resource at the end of use
    frame.contents.release(frame)
  
    # 保存bmp图片
    # save bmp image  
    bmpInfoHeader = BITMAPINFOHEADER() 
    bmpFileHeader = BITMAPFILEHEADER()
  
    uRgbQuadLen = 0
    rgbQuad = (RGBQUAD * 256)() # 调色板信息 | color palette info
    rgbBuff = c_buffer(b'\0', convertParams.height * convertParams.width * 3)
    
    # 如果图像格式是 Mono8 不需要转码
    # no format conversion required for Mono8
    if convertParams.pixelForamt == EPixelType.gvspPixelMono8:
        # 初始化调色板rgbQuad 实际应用中 rgbQuad 只需初始化一次
        # initialize color palette
        for i in range(0, 256):
            rgbQuad[i].rgbBlue = rgbQuad[i].rgbGreen = rgbQuad[i].rgbRed = i;

        uRgbQuadLen = sizeof(RGBQUAD) * 256    
        bmpFileHeader.bfSize = sizeof(bmpFileHeader) + sizeof(bmpInfoHeader) + uRgbQuadLen + convertParams.dataSize
        bmpInfoHeader.biBitCount = 8
    else:
        # 转码 => BGR24
        # convert to BGR24
        rgbSize = c_int()
        nRet = IMGCNV_ConvertToBGR24(cast(frameBuff, c_void_p), byref(convertParams), \
                                     cast(rgbBuff, c_void_p), byref(rgbSize))
      
        if ( nRet != 0 ):
            print("image convert fail! errorCode = " + str(nRet))
            # 释放相关资源
            # release stream source object before return
            streamSource.contents.release(streamSource)
            return -1 
        
        bmpFileHeader.bfSize = sizeof(bmpFileHeader) + sizeof(bmpInfoHeader) + rgbSize.value
        bmpInfoHeader.biBitCount = 24   
    
    bmpFileHeader.bfType = 0x4D42 # 文件头类型 'BM'(42 4D) | file type,  must be BM
    bmpFileHeader.bfReserved1 = 0 # 保留字 | reserved
    bmpFileHeader.bfReserved2 = 0 # 保留字 | reserved
    bmpFileHeader.bfOffBits = 54 + uRgbQuadLen # 位图像素数据的起始位置 | offset from the beginning of the BITMAPFILEHEADER structure to the bitmap bits
      
    bmpInfoHeader.biSize = 40     # 信息头所占字节数 | number of bytes required by the structure
    bmpInfoHeader.biWidth = convertParams.width
    bmpInfoHeader.biHeight = -convertParams.height
    bmpInfoHeader.biPlanes = 1    # 位图平面数| number of planes
    
    bmpInfoHeader.biCompression = 0 # 压缩类型，0 即不压缩 | compression type
    bmpInfoHeader.biSizeImage = 0
    bmpInfoHeader.biXPelsPerMeter = 0
    bmpInfoHeader.biYPelsPerMeter = 0
    bmpInfoHeader.biClrUsed = 0
    bmpInfoHeader.biClrImportant = 0    
      
    fileName = './image/image.bmp'
    imageFile = open(fileName, 'wb+') 
      
    imageFile.write(struct.pack('H', bmpFileHeader.bfType))
    imageFile.write(struct.pack('I', bmpFileHeader.bfSize))
    imageFile.write(struct.pack('H', bmpFileHeader.bfReserved1))
    imageFile.write(struct.pack('H', bmpFileHeader.bfReserved2))
    imageFile.write(struct.pack('I', bmpFileHeader.bfOffBits))
      
    imageFile.write(struct.pack('I', bmpInfoHeader.biSize))
    imageFile.write(struct.pack('i', bmpInfoHeader.biWidth))
    imageFile.write(struct.pack('i', bmpInfoHeader.biHeight))
    imageFile.write(struct.pack('H', bmpInfoHeader.biPlanes))
    imageFile.write(struct.pack('H', bmpInfoHeader.biBitCount))
    imageFile.write(struct.pack('I', bmpInfoHeader.biCompression))
    imageFile.write(struct.pack('I', bmpInfoHeader.biSizeImage))
    imageFile.write(struct.pack('i', bmpInfoHeader.biXPelsPerMeter))
    imageFile.write(struct.pack('i', bmpInfoHeader.biYPelsPerMeter))
    imageFile.write(struct.pack('I', bmpInfoHeader.biClrUsed))
    imageFile.write(struct.pack('I', bmpInfoHeader.biClrImportant))    
     
    if convertParams.pixelForamt == EPixelType.gvspPixelMono8:
        # 写入调色板信息
        # write out color palette info
        for i in range(0, 256):
            imageFile.write(struct.pack('B', rgbQuad[i].rgbBlue)) 
            imageFile.write(struct.pack('B', rgbQuad[i].rgbGreen))   
            imageFile.write(struct.pack('B', rgbQuad[i].rgbRed))           
            imageFile.write(struct.pack('B', rgbQuad[i].rgbReserved))
        
        imageFile.writelines(frameBuff)
    else: 
        imageFile.writelines(rgbBuff)
        
    imageFile.close()
    print("save " + fileName + " success.")
    print("save bmp time: " + str(datetime.datetime.now()))   
         
    # 停止拉流
    # stop grabbing
    nRet = streamSource.contents.stopGrabbing(streamSource)
    if( nRet != 0 ):
        print("stopGrabbing fail!")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)   
        return -1
      
    # 设置曝光
    # set ExposureTime
    nRet = setExposureTime(camera, 20000)
    if ( nRet != 0 ):
        print("set ExposureTime fail")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)   
        return -1
           
    # 关闭相机
    # close camera
    nRet = closeCamera(camera)
    if ( nRet != 0 ):
        print("closeCamera fail")
        # 释放相关资源
        # release stream source object before return
        streamSource.contents.release(streamSource)   
        return -1
     
    # 释放相关资源
    # release stream source object at the end of use
    streamSource.contents.release(streamSource)    
    
    return 0
    
if __name__=="__main__": 

    nRet = demo()
    if nRet != 0:
        print("Some Error happend")
    print("--------- Demo end ---------")
    # 3s exit
    time.sleep(3) 	
