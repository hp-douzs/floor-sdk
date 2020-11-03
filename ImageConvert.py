#!/usr/bin/env python
# coding: utf-8
'''
Created on 2017-10-26

@author: 
'''
from ctypes import *

# 加载ImageConvert库
# load ImageConvert library
# 32bit
#ImageConvertdll = OleDLL("./dll/x86/ImageConvert.dll")
# 64bit
ImageConvertdll = OleDLL("./dll/x64/ImageConvert.dll")

#定义枚举类型
#define enum type
def enum(**enums):
    return type('Enum', (), enums)

# ImageConvert.h => enum tagIMGCNV_EErr
IMGCNV_EErr = enum(
                      IMGCNV_SUCCESS = 0,
                      IMGCNV_ILLEGAL_PARAM = 1,
                      IMGCNV_ERR_ORDER = 2,
                      IMGCNV_NO_MEMORY = 3,
                      IMGCNV_NOT_SUPPORT = 4,
                      )

# ImageConvert.h => struct tagIMGCNV_SOpenParam
class IMGCNV_SOpenParam(Structure):
    _fields_ = [
                ('width', c_int),
                ('height', c_int),
                ('paddingX', c_int),
                ('paddingY', c_int),
                ('dataSize', c_int),
                ('pixelForamt', c_uint),
                ]
# ImageConvert.h => enum tagIMGCNV_EBayerDemosaic
IMGCNV_EErr = enum(
                      IMGCNV_DEMOSAIC_NEAREST_NEIGHBOR = 0,
                      IMGCNV_DEMOSAIC_BILINEAR = 1,
                      IMGCNV_DEMOSAIC_EDGE_SENSING = 2,
                      IMGCNV_DEMOSAIC_NOT_SUPPORT = 255,
                      )

# ImageConvert.h => IMGCNV_ConvertToBGR24(unsigned char* pSrcData, IMGCNV_SOpenParam* pOpenParam, unsigned char* pDstData, int* pDstDataSize)
IMGCNV_ConvertToBGR24 = ImageConvertdll.IMGCNV_ConvertToBGR24

# ImageConvert.h => IMGCNV_ConvertToRGB24(unsigned char* pSrcData, IMGCNV_SOpenParam* pOpenParam, unsigned char* pDstData, int* pDstDataSize)
IMGCNV_ConvertToRGB24 = ImageConvertdll.IMGCNV_ConvertToRGB24

# ImageConvert.h => IMGCNV_ConvertToMono8(unsigned char* pSrcData, IMGCNV_SOpenParam* pOpenParam, unsigned char* pDstData, int* pDstDataSize)
IMGCNV_ConvertToMono8 = ImageConvertdll.IMGCNV_ConvertToMono8

#ImageConvert.h => IMGCNV_ConvertToBGR24_Ex(unsigned char* pSrcData, IMGCNV_SOpenParam* pOpenParam, unsigned char* pDstData, int* pDstDataSize, IMGCNV_EBayerDemosaic eBayerDemosaic)
IMGCNV_ConvertToBGR24_Ex = ImageConvertdll.IMGCNV_ConvertToBGR24_Ex

#ImageConvert.h => IMGCNV_ConvertToRGB24_Ex(unsigned char* pSrcData, IMGCNV_SOpenParam* pOpenParam, unsigned char* pDstData, int* pDstDataSize, IMGCNV_EBayerDemosaic eBayerDemosaic)
IMGCNV_ConvertToRGB24_Ex = ImageConvertdll.IMGCNV_ConvertToRGB24_Ex

#ImageConvert.h => CALLMETHOD IMGCNV_ConvertToMono8_Ex(unsigned char* pSrcData, IMGCNV_SOpenParam* pOpenParam, unsigned char* pDstData, int* pDstDataSize, IMGCNV_EBayerDemosaic eBayerDemosaic)
IMGCNV_ConvertToMono8_Ex = ImageConvertdll.IMGCNV_ConvertToMono8_Ex

#ImageConvert.h => IMGCNV_ConvertToBGRA32_Ex(unsigned char* pSrcData, IMGCNV_SOpenParam* pOpenParam, unsigned char* pDstData, int* pDstDataSize, IMGCNV_EBayerDemosaic eBayerDemosaic)
IMGCNV_ConvertToBGRA32_Ex = ImageConvertdll.IMGCNV_ConvertToBGRA32_Ex
