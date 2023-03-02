from ctypes import *

from .mvCodeReaderParams import *

ImageCallBackEx2 = CFUNCTYPE(None, POINTER(c_ubyte), POINTER(MV_CODEREADER_IMAGE_OUT_INFO_EX2), c_char_p)
AllEventCallBack = CFUNCTYPE(None, POINTER(MV_CODEREADER_EVENT_OUT_INFO), c_char_p)
ExceptionCallBack = CFUNCTYPE(None, c_uint, c_char_p)

class MvCoderReaderCtrl:
    def __init__(self, dllPath: str) -> None:
        self._handleLv1 = c_void_p()
        self._handleLv2 = pointer(self._handleLv1)

        self.dllPath = dllPath
        self.dll = windll.LoadLibrary(self.dllPath)


    def CODEREADER_RegisterExceptionCallBack(self, userName: str, callback: ExceptionCallBack):
        return self.dll.MV_CODEREADER_RegisterExceptionCallBack(self._handleLv1, callback, userName.encode("utf-8") )

    def CODEREADER_RegisterAllEventCallBack(self, userName: str, callback:AllEventCallBack):
        return self.dll.MV_CODEREADER_RegisterAllEventCallBack(self._handleLv1, callback, userName.encode("utf-8"))

    def CODEREADER_MSC_RegisterImageCallBack(self, userName: str, callback: ImageCallBackEx2):
        return self.dll.MV_CODEREADER_MSC_RegisterImageCallBack(self._handleLv1, callback, userName.encode("utf-8") )

    def CODEREADER_SetEnumValue(self,  key: str, value: int):
        return self.dll.MV_CODEREADER_SetEnumValue(self._handleLv1, key.encode("utf-8"), value)

    def CODEREADER_SetCommandValue(self, cmd: str):
        return self.dll.MV_CODEREADER_SetCommandValue(self._handleLv1, cmd.encode("utf-8"))

    def set_continuous_trigger_mode(self):
        return self.CODEREADER_SetEnumValue("TriggerMode", MV_CODEREADER_TRIGGER_MODE.MV_CODEREADER_TRIGGER_MODE_OFF)

    def set_single_trigger_mode(self):
        return self.CODEREADER_SetEnumValue("TriggerMode", MV_CODEREADER_TRIGGER_MODE.MV_CODEREADER_TRIGGER_MODE_ON)

    def set_trigger_source(self, value: MV_CODEREADER_TRIGGER_SOURCE):
        return self.CODEREADER_SetEnumValue("TriggerSource", value)

    def trigger(self):
        return self.CODEREADER_SetCommandValue("TriggerSoftware")
#ifndef _#MV_CODEREADER_CTRL_H_
#define _#MV_CODEREADER_CTRL_H_

#include "#MVCodeReaderErrorDefine.h"
#include "#MVCodeReaderParams.h"

###
#  @brief  动态库导入导出定义
#  @brief  Import and export definition of the dynamic library
##
#ifndef #MV_CODEREADERCTRL_API

    #if (defined (_WIN32) || defined(WIN64))
        #if defined(#MV_CODEREADERCTRL_EXPORTS)
            #define #MV_CODEREADERCTRL_API __declspec(dllexport)
        #else
            #define #MV_CODEREADERCTRL_API __declspec(dllimport)
        #endif
    #else
        #ifndef __stdcall
            #define __stdcall
        #endif

        #ifndef #MV_CODEREADERCTRL_API
            #define  #MV_CODEREADERCTRL_API
        #endif
    #endif

#endif

#ifndef IN
    #define IN
#endif

#ifndef OUT
    #define OUT
#endif

#ifdef __cplusplus
#extern "C" {
#endif

##########################################################################
## 相机的基本指令和操作                                                 ##
## Camera basic instructions and operations                             ##
##########################################################################
#########################################################################

    def CODEREADER_GetSDKVersion(self):
        """python
        @fn     #MV_CODEREADER_GetSDKVersion()
        @brief  获取SDK版本号
        @param
        @return 始终返回4字节版本号 |主    |次    |修正  |  测试|
                                         8bits  8bits  8bits  8bits

        @fn     #MV_CODEREADER_GetSDKVersion()
        @brief  Get SDK Version
        @param
        @return Always return 4 Bytes of version number |Main    |Sub    |Rev  |  Test|
                                                         8bits  8bits  8bits  8bits
        #########################################################################
        #MV_CODEREADERCTRL_API unsigned int __stdcall #MV_CODEREADER_GetSDKVersion();
        """
        return self.dll.MV_CODEREADER_GetSDKVersion()

    def CODEREADER_EnumDevices(self, pstDevList: MV_CODEREADER_DEVICE_INFO_LIST, nTLayerType: int):
        return self.dll.MV_CODEREADER_EnumDevices(pointer(pstDevList), nTLayerType)
#########################################################################
 #  @fn     #MV_CODEREADER_EnumDevices()
 #  @brief  枚举设备 （支持虚拟相机）
 #  @param  nTLayerType            [IN]           枚举传输层
 #  @param  pstDevList             [IN][OUT]      设备列表
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_EnumDevices()
 #  @brief  Enumerate Device(support virtual camera)
 #  @param  nTLayerType            [IN]           Enumerate TLs
 #  @param  pstDevList             [IN][OUT]      Device List
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#ifndef __cplusplus
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_EnumDevices(IN OUT #MV_CODEREADER_DEVICE_INFO_LIST# pstDevList, IN unsigned int nTLayerType);
#else
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_EnumDevices(IN OUT #MV_CODEREADER_DEVICE_INFO_LIST# pstDevList, IN unsigned int nTLayerType = #MV_CODEREADER_GIGE_DEVICE);
#endif

#########################################################################
#  @fn     #MV_CODEREADER_EnumCodeReader()
#  @brief  私有协议枚举设备 （虚拟相机不支持）
#  @param  pstDevList             [IN][OUT]          设备列表
#  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

#  @fn     #MV_CODEREADER_EnumIDDevices()
#  @brief  Enumerate devices by private protocol (virtual camera does not support)
#  @param  pstDevList             [IN][OUT]          Device List
#  @return Success, return #MV_CODEREADER_OK. Failure, return error code
#########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_EnumIDDevices(IN OUT #MV_CODEREADER_DEVICE_INFO_LIST# pstDevList);

#########################################################################
 #  @fn     #MV_CODEREADER_EnumCodeReader()
 #  @brief  枚举指定系列设备 （虚拟相机可枚举，但bSelectDevice不生效，不可指定系列设备）
 #  @param  pstDevList             [IN][OUT]          设备列表
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_EnumCodeReader()
 #  @brief  Enumerate Specified Series Device (virtual camera can be enumerated, but bSelectDevice is not effective, not specified series equipment)
 #  @param  pstDevList             [IN][OUT]          Device List
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_EnumCodeReader(IN OUT #MV_CODEREADER_DEVICE_INFO_LIST# pstDevList);

#########################################################################
 #  @fn     #MV_CODEREADER_IsDeviceAccessible()
 #  @brief  设备是否可达（虚拟相机可调用，若参数正确，默认都是可达）
 #  @param  pstDevInfo             [IN]           设备信息结构体
 #  @param  nAccessMode            [IN]           访问权限
 #  @return 可达，返回true；不可达，返回false

 #  @fn     #MV_CODEREADER_IsDeviceAccessible()
 #  @brief  Is the device accessible(virtual camera can call, not support test equipment whether can reach)
 #  @param  pstDevInfo             [IN]           Device Information Structure
 #  @param  nAccessMode            [IN]           Access Right
 #  @return Access, return true. Not access, return false
 #########################################################################
#MV_CODEREADERCTRL_API bool __stdcall #MV_CODEREADER_IsDeviceAccessible(IN #MV_CODEREADER_DEVICE_INFO# pstDevInfo, IN unsigned int nAccessMode);

#########################################################################
 #  @fn     #MV_CODEREADER_CreateHandle()
 #  @brief  创建设备句柄（支持虚拟相机）
 #  @param  handle                 [IN][OUT]      句柄地址
 #  @param  pstDevInfo             [IN]           设备信息结构体
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_CreateHandle()
 #  @brief  Create Device Handle(support virtual camera)
 #  @param  handle                 [IN][OUT]      Handle Address
 #  @param  pstDevInfo             [IN]           Device Information Structure
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_CreateHandle(IN OUT void ## handle, IN const #MV_CODEREADER_DEVICE_INFO# pstDevInfo);
    def CODEREADER_CreateHandle(self, pstDevInfo: MV_CODEREADER_DEVICE_INFO):
        return self.dll.MV_CODEREADER_CreateHandle(self._handleLv2, pointer(pstDevInfo) )

#########################################################################
 #  @fn     #MV_CODEREADER_CreateHandleBySerialNumber()
 #  @brief  创建设备句柄（支持虚拟相机）
 #  @param  handle                 [IN][OUT]      句柄地址
 #  @param  chSerialNumber         [IN]           设备序列号
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_CreateHandleBySerialNumber()
 #  @brief  Create Device Handle(support virtual camera)
 #  @param  handle                 [IN][OUT]      Handle Address
 #  @param  chSerialNumber         [IN]           Device SerialNumber
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_CreateHandleBySerialNumber(IN OUT void ## handle, IN const char# chSerialNumber);
    def CODEREADER_CreateHandleBySerialNumber(self, chSerialNumber: str):
        sn = chSerialNumber.encode("utf-8")
        return self.dll.MV_CODEREADER_CreateHandleBySerialNumber(self._handleLv2, c_char_p(sn))


#########################################################################
 #  @fn     #MV_CODEREADER_DestroyHandle()
 #  @brief  销毁设备句柄（支持虚拟相机）
 #  @param  handle                 [IN]          句柄
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_DestroyHandle()
 #  @brief  Destroy Device Handle(support virtual camera)
 #  @param  handle                 [IN]          Handle
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_DestroyHandle(IN void # handle);
    def CODEREADER_DestroyHandle(self):
        return self.dll.MV_CODEREADER_DestroyHandle(self._handleLv1)

#########################################################################
 #  @fn     #MV_CODEREADER_OpenDevice()
 #  @brief  打开设备 （支持虚拟相机）
 #  @param  handle                 [IN]          句柄
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_OpenDevice()
 #  @brief  Open Device(support virtual camera)
 #  @param  handle                 [IN]          Handle
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_OpenDevice(IN void# handle);
    def CODEREADER_OpenDevice(self):
        return self.dll.MV_CODEREADER_OpenDevice(self._handleLv1)

########################################################################
 #  @fn         #MV_CODEREADER_CloseDevice()
 #  @brief      关闭相机 （支持虚拟相机）
 #  @param       handle                 [IN]          句柄
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_CloseDevice()
 #  @brief      Close Device(support virtual camera)
 #  @param      handle                 [IN]          Handle
 #  @return     Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_CloseDevice(IN void# handle);
    def CODEREADER_CloseDevice(self):
        return self.dll.MV_CODEREADER_CloseDevice(self._handleLv1)

##########################################################################
## 针对注册图像回调和获取帧图像相关接口                            ##
## General interface for register image data callback get image data        ##
## 注意说明：
#若固件支持识别条码长度超256，针对#MV_CODEREADER_RESULT_BCR、
#MV_CODEREADER_RESULT_BCR_EX结构体中的条码字符（chCode）字符会截断适配至256 ##
## tips:
#If the camera supports the bar code length greater than 256, the code characters (chCode) in the #MV_CODEREADER_RESULT_BCR
#and #MV_CODEREADER_RESULT_BCR_EX structures are truncated to 256 ##
##########################################################################

########################################################################
 #  @fn         #MV_CODEREADER_RegisterImageCallBack()
 #  @brief      注册图像数据回调，开始取流之前调用 （支持虚拟相机）
 #  @remark     虚拟相机的图像结构体支持的字段：宽、高、像素格式、触发序号始终为1、帧号（循环采集图像数）、帧数据大小、
 #               是否读到条码、条码结构体中的条码数量、条码信息结构体中的字符、字符长度、条码类型和条码位置；其余字段不支持；
#              虚拟相机RAW模式不支持
 #  @param       handle                 [IN]          句柄
 #  @param       cbOutput               [IN][OUT]     回调函数指针
 #  @param       pUser                  [IN]          用户自定义变量
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_RegisterImageCallBack()
 #  @brief      register image data callback, before Start Grabbing (support virtual camera)
 #  @remark     The field of virtual camera image structure support: nWidth, nHeight, enPixelType, nTriggerIndex(always 1), nFrameNum,
  #              nFrameLen, bIsGetCode, nCodeNum, nID, chCode, nLen, nBarType, pt[4](point location);
  #              The virtual camera RAW mode does not support.
 #  @param       handle                 [IN]          Handle
 #  @param       cbOutput               [IN][OUT]     Callback function pointer
 #  @param       pUser                  [IN]          User defined variable
 #  @return      Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_RegisterImageCallBack(IN void# handle,
 #                                                        void(__stdcall# cbOutput)(unsigned char # pData, #MV_CODEREADER_IMAGE_OUT_INFO# pstFrameInfo, void# pUser),
 #                                                        void# pUser);

########################################################################
 #  @fn         #MV_CODEREADER_RegisterImageCallBackEx()
 #  @brief      注册图像数据回调，开始取流之前调用（支持虚拟相机）
 #  @remark     针对条码字符chCode 若字符长度大于256
 #  @remark     虚拟相机的图像结构体支持的字段：宽、高、像素格式、触发序号始终为1、帧号（循环采集图像数）、帧数据大小、
 #               是否读到条码、条码结构体中的条码数量、条码信息结构体中的字符、字符长度、条码类型和条码位置；其余字段不支持；
 #               虚拟相机RAW模式不支持
 #  @param       handle                 [IN]          句柄
 #  @param       cbOutput               [IN]          回调函数指针
 #  @param       pUser                  [IN]          用户自定义变量
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_RegisterImageCallBackEx()
 #  @brief      register image data callback, before Start Grabbing (support virtual camera)
 #  @remark     The field of virtual camera image structure support: nWidth, nHeight, enPixelType, nTriggerIndex(always 1), nFrameNum,
 #               nFrameLen, bIsGetCode, nCodeNum, nID, chCode, nLen, nBarType, pt[4](point location);
 #               The virtual camera RAW mode does not support.
 #  @param       handle                 [IN]          Handle
 #  @param       cbOutput               [IN]          Callback function pointer
 #  @param       pUser                  [IN]          User defined variable
 #  @return      Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_RegisterImageCallBackEx(IN void# handle,
 #                                                                       void(__stdcall# cbOutput)(unsigned char # pData, #MV_CODEREADER_IMAGE_OUT_INFO_EX# pstFrameInfo, void# pUser),
 #                                                                       void# pUser);

########################################################################
 #  @fn         #MV_CODEREADER_RegisterImageCallBackEx2()
 #  @brief      注册图像数据(数据包含二维码质量评级)回调, 开始取流之前调用 （支持虚拟相机）
 #  @remark     该接口支持ID5000系列读码器获取二维码质量信息，兼容无二维码评级功能的其余读码器，即二维码质量信息为0
 #  @remark      虚拟相机的图像结构体支持的字段：宽、高、像素格式、触发序号始终为1、帧号（循环采集图像数）、帧数据大小、
 #                是否读到条码、条码结构体中的条码数量、条码信息结构体中的字符、字符长度、条码类型和条码位置；其余字段不支持；
 #                虚拟相机RAW模式不支持
 #  @param       handle                 [IN]          句柄
 #  @param       cbOutput               [IN][OUT]     回调函数指针
 #  @param       pUser                  [IN]          用户自定义变量
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_RegisterImageCallBackEx2()
 #  @brief      register image data(Include QR quality info) callback, before Start Grabbing (support virtual camera)
 #  @remark     The field of virtual camera image structure support: nWidth, nHeight, enPixelType, nTriggerIndex(always 1), nFrameNum,
  #              nFrameLen, bIsGetCode, nCodeNum, nID, chCode, nLen, nBarType, pt[4](point location);
  #              The virtual camera RAW mode does not support.
 #  @param       handle                 [IN]          Handle
 #  @param       cbOutput               [IN][OUT]     Callback function pointer
 #  @param       pUser                  [IN]          User defined variable
 #  @return      Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_RegisterImageCallBackEx2(IN void# handle,
  #                                                                      void(__stdcall# cbOutput)(unsigned char # pData, #MV_CODEREADER_IMAGE_OUT_INFO_EX2# pstFrameInfo, void# pUser),
   #                                                                     void# pUser);
#
########################################################################
 #  @fn         #MV_CODEREADER_MSC_RegisterImageCallBack()
 #  @brief      注册指定一路流通道图像数据(数据包含二维码质量评级)回调，开始取流之前调用 （支持虚拟相机）
 #  @remark     该接口与其他注册图像回调接口存在互斥关系，与获取图像相关接口存在互斥关系
 #  @remark     该接口支持IDX系列智能读码器多路通道同时轮询指定不同流通道号（0#1）输出指定通道图像信息，原单通道固件流通道号参数默认为0
 #  @remark     该接口支持ID5000系列智能读码器获取二维码质量信息，兼容无二维码评级功能的其余读码器，即二维码质量信息为0
 #  @remark     该接口需停止#取消注册指定路流通道回调时，将cbOutput参数置为NULL即可。
 #  @remark      虚拟相机的图像结构体支持的字段：宽、高、像素格式、触发序号始终为1、帧号（循环采集图像数）、帧数据大小、
  #               是否读到条码、条码结构体中的条码数量、条码信息结构体中的字符、字符长度、条码类型和条码位置；其余字段不支持；
 #                虚拟相机RAW模式不支持
 #  @param       handle                 [IN]          句柄
 #  @param       nChannelID             [IN]          流通道号（单通道固件通道号为0, 多通道固件通道号为0#1(根据多通道sensor个数)）
 #  @param       cbOutput               [IN]          回调函数指针
 #  @param       pUser                  [IN]          用户自定义变量
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_MSC_RegisterImageCallBack()
 #  @brief      register image data(Include QR quality info) callback, before Start Grabbing (support virtual camera)
 #  @remark     The field of virtual camera image structure support: nWidth, nHeight, enPixelType, nTriggerIndex(always 1), nFrameNum,
  #              nFrameLen, bIsGetCode, nCodeNum, nID, chCode, nLen, nBarType, pt[4](point location);
  #              The virtual camera RAW mode does not support.
 #  @param       handle                 [IN]          Handle
 #  @param       nChannelID             [IN]          Stream Channel ID(one sensor is 0, Multichannel is 0#1(follow sensor num))
 #  @param       cbOutput               [IN]          Callback function pointer
 #  @param       pUser                  [IN]          User defined variable
 #  @return      Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_MSC_RegisterImageCallBack(IN void# handle, unsigned int nChannelID,
 #                                                                       void(__stdcall# cbOutput)(unsigned char # pData, #MV_CODEREADER_IMAGE_OUT_INFO_EX2# pstFrameInfo, void# pUser),
 #                                                                       void# pUser);

########################################################################
 #  @fn         #MV_CODEREADER_StartGrabbing()
 #  @brief      开始取流 （支持虚拟相机）
 #  @param       handle                 [IN]          句柄
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_StartGrabbing()
 #  @brief      Start Grabbing (support virtual camera)
 #  @param      handle                 [IN]          Handle
 #  @return     Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_StartGrabbing(IN void# handle);
    def CODEREADER_StartGrabbing(self):
        return self.dll.MV_CODEREADER_StartGrabbing(self._handleLv1)

########################################################################
 #  @fn         #MV_CODEREADER_StopGrabbing()
 #  @brief      停止取流 （支持虚拟相机）
 #  @param       handle                 [IN]          句柄
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_StopGrabbing()
 #  @brief      Stop Grabbing (support virtual camera)
 #  @param      handle                 [IN]          Handle
 #  @return     Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_StopGrabbing(IN void# handle);
    def CODEREADER_StopGrabbing(self):
        return self.dll.MV_CODEREADER_StopGrabbing(self._handleLv1)

########################################################################
 #  @fn         #MV_CODEREADER_GetOneFrameTimeout()
 #  @brief      采用超时机制获取一帧图片，SDK内部等待直到有数据时返回 （支持虚拟相机）
 #  @remark     虚拟相机的图像结构体支持的字段：宽、高、像素格式、触发序号始终为1、帧号（循环采集图像数）、帧数据大小、
 #                是否读到条码、条码结构体中的条码数量、条码信息结构体中的字符、字符长度、条码类型和条码位置；其余字段不支持；
  #              虚拟相机RAW模式不支持
 #  @param       handle                 [IN]          句柄
 #  @param       pData                  [OUT]         图像数据接收指针
 #  @param       pstFrameInfo           [OUT]         图像信息结构体
 #  @param       nMsec                  [IN]          等待超时时间, 以毫秒为单位
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_GetOneFrameTimeout()
 #  @brief      Timeout mechanism is used to get image, and the SDK waits inside until the data is returned (support virtual camera)
 #  @remark     The field of virtual camera image structure support: nWidth, nHeight, enPixelType, nTriggerIndex(always 1), nFrameNum,
 #               nFrameLen, bIsGetCode, nCodeNum, nID, chCode, nLen, nBarType, pt[4](point location);
 #               The virtual camera RAW mode does not support.
 #  @param       handle                 [IN]          Handle
 #  @param       pData                  [OUT]         Recevied image data pointer
 #  @param       pstFrameInfo           [OUT]         Image information structure
 #  @param       nMsec                  [IN]          Waiting timeout, speed in milliseconds
 #  @return      Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetOneFrameTimeout(IN void# handle, IN OUT unsigned char ## pData, IN OUT #MV_CODEREADER_IMAGE_OUT_INFO# pstFrameInfo, IN unsigned int nMsec);

########################################################################
 #  @fn         #MV_CODEREADER_GetOneFrameTimeoutEx()
 #  @brief      采用超时机制获取一帧图片，SDK内部等待直到有数据时返回（支持虚拟相机）
 #  @remark     虚拟相机的图像结构体支持的字段：宽、高、像素格式、触发序号始终为1、帧号（循环采集图像数）、帧数据大小、
 #               是否读到条码、条码结构体中的条码数量、条码信息结构体中的字符、字符长度、条码类型和条码位置；其余字段不支持；
 #               虚拟相机RAW模式不支持
 #  @param       handle                 [IN]          句柄
 #  @param       pData                  [OUT]         图像数据接收指针
 #  @param       pstFrameInfo           [OUT]         图像信息结构体
 #  @param       nMsec                  [IN]          等待超时时间, 以毫秒为单位
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_GetOneFrameTimeoutEx()
 #  @brief      Timeout mechanism is used to get image, and the SDK waits inside until the data is returned (support virtual camera)
 #  @remark     The field of virtual camera image structure support: nWidth, nHeight, enPixelType, nTriggerIndex(always 1), nFrameNum,
 #              nFrameLen, bIsGetCode, nCodeNum, nID, chCode, nLen, nBarType, pt[4](point location);
 #               The virtual camera RAW mode does not support.
 #  @param       handle                 [IN]          Handle
 #  @param       pData                  [OUT]         Recevied image data pointer
 #  @param       pstFrameInfo           [OUT]         Image information structure
 #  @param       nMsec                  [IN]          Waiting timeout, speed in milliseconds
 #  @return      Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetOneFrameTimeoutEx(IN void# handle, IN OUT unsigned char ## pData, IN OUT #MV_CODEREADER_IMAGE_OUT_INFO_EX# pstFrameInfo, IN unsigned int nMsec);

########################################################################
 #  @fn         #MV_CODEREADER_GetOneFrameTimeoutEx2()
 #  @brief      采用超时机制获取一帧图片，SDK内部等待直到有数据时返回（支持虚拟相机）
 #  @remark     该接口支持ID5000系列读码器获取二维码质量信息，兼容无二维码评级功能的其余读码器，即二维码质量信息为0
 #  @remark     虚拟相机的图像结构体支持的字段：宽、高、像素格式、触发序号始终为1、帧号（循环采集图像数）、帧数据大小、
 #               是否读到条码、条码结构体中的条码数量、条码信息结构体中的字符、字符长度、条码类型和条码位置；其余字段不支持；
 #              虚拟相机RAW模式不支持
 #  @param       handle                 [IN]          句柄
 #  @param       pData                  [OUT]         图像数据接收指针
 #  @param       pstFrameInfoEx         [OUT]         图像信息结构体(包含二维码质量信息)
 #  @param       nMsec                  [IN]          等待超时时间, 以毫秒为单位
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码
    def CODEREADER_GetOneFrameTimeoutEx2(self, pData, pstFrameInfo, nMsec ):
        return self.dll.MV_CODEREADER_GetOneFrameTimeoutEx2(self._handleLv1, pointer(pData), pointer(pstFrameInfo), nMsec )

 #  @fn         #MV_CODEREADER_GetOneFrameTimeoutEx2()
 #  @brief      Timeout mechanism is used to get image, and the SDK waits inside until the data is returned (support virtual camera)
 #  @remark     The field of virtual camera image structure support: nWidth, nHeight, enPixelType, nTriggerIndex(always 1), nFrameNum,
 #               nFrameLen, bIsGetCode, nCodeNum, nID, chCode, nLen, nBarType, pt[4](point location);
 #               The virtual camera RAW mode does not support.
 #  @param       handle                 [IN]          Handle
 #  @param       pData                  [OUT]         Recevied image data(Include QR quality info) pointer
 #  @param       pstFrameInfoEx         [OUT]         Image information structure
 #  @param       nMsec                  [IN]          Waiting timeout, speed in milliseconds
 #  @return      Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetOneFrameTimeoutEx2(IN void# handle, IN OUT unsigned char ## pData, IN OUT #MV_CODEREADER_IMAGE_OUT_INFO_EX2# pstFrameInfo, IN unsigned int nMsec);

########################################################################
 #  @fn         #MV_CODEREADER_MSC_GetOneFrameTimeout()
 #  @brief      采用超时机制获取一路流通道一帧图片，SDK内部等待直到有数据时返回（支持虚拟相机）
 #  @remark     该接口支持IDX系列智能读码器多路通道同时轮询指定不同流通道号（0#1）输出指定通道图像信息，原单通道固件流通道号参数默认为0
 #  @remark     该接口支持ID5000系列智能读码器获取二维码质量信息，兼容无二维码评级功能的其余读码器，即二维码质量信息为0
 #  @remark     虚拟相机的图像结构体支持的字段：宽、高、像素格式、触发序号始终为1、帧号（循环采集图像数）、帧数据大小、
 #               是否读到条码、条码结构体中的条码数量、条码信息结构体中的字符、字符长度、条码类型和条码位置；其余字段不支持；
 #               虚拟相机RAW模式不支持
 #  @param       handle                 [IN]          句柄
 #  @param       pData                  [OUT]         图像数据接收指针
 #  @param       pstFrameInfo           [OUT]         图像信息结构体(包含二维码质量信息)
 #  @param       nChannelID             [IN]          流通道ID(单通道固件通道号为0, 多通道固件通道号为0#1(根据多通道sensor个数))
 #  @param       nMsec                  [IN]          等待超时时间, 以毫秒为单位
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn         #MV_CODEREADER_MSC_GetOneFrameTimeout()
 #  @brief      Timeout mechanism is used to get image, and the SDK waits inside until the data is returned (support virtual camera)
 #  @remark     The field of virtual camera image structure support: nWidth, nHeight, enPixelType, nTriggerIndex(always 1), nFrameNum,
 #               nFrameLen, bIsGetCode, nCodeNum, nID, chCode, nLen, nBarType, pt[4](point location);
 #               The virtual camera RAW mode does not support.
 #  @param       handle                 [IN]          Handle
 #  @param       pData                  [OUT]         Recevied image data pointer
 #  @param       pstFrameInfo           [OUT]         Image information structure(Include QR code quality Info)
 #  @param       nChannelID             [IN]          Stream Channel ID(one sensor is 0, Multichannel is 0#1(follow sensor num))
 #  @param       nMsec                  [IN]          Waiting timeout, speed in milliseconds
 #  @return      Success, return #MV_CODEREADER_OK. Failure, return error code
 ########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_MSC_GetOneFrameTimeout(IN void# handle, IN OUT unsigned char ##pData,
#                                                                          IN OUT #MV_CODEREADER_IMAGE_OUT_INFO_EX2# pstFrameInfo,
#                                                                           IN unsigned int nChannelID, unsigned int nMsec);

#########################################################################
 #  @fn     #MV_CODEREADER_GetDeviceInfo()
 #  @brief  获取设备信息（支持虚拟相机）
 #  @param  void# handle                     [IN]        相机句柄
 #  @param  pstDevInfo                       [IN][OUT]   返回给调用者有关相机设备信息结构体指针
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_GetDeviceInfo()
 #  @brief  Get device information (virtual camera can call, not support returning equipment information, interface returns success)
 #  @param  void# handle                     [IN]        Handle
 #  @param  pstDevInfo                       [IN][OUT]   Structure pointer of device information
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #
 #          Refer to the definition of #MV_CC_DEVICE_INFO in CameraParam.h
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetDeviceInfo(IN void # handle, IN OUT #MV_CODEREADER_DEVICE_INFO# pstDevInfo);
    def CODEREADER_GetDeviceInfo(self, pstDevInfo: MV_CODEREADER_DEVICE_INFO):
        return self.dll.MV_CODEREADER_GetDeviceInfo(self._handleLv1, pointer(pstDevInfo))

##########################################################################
## 设置和获取相机参数的万能接口                                         ##
## General interface for getting and setting camera parameters          ##
## 虚拟相机支持万能接口：
#   虚拟相机对支持的节点，配置节点返回成功，并有实际功能效果；
#   虚拟相机对不支持的节点，配置时返回成功，但无实际功能效果##
## virtual camera support universal interface:
#   To support node, the node is configured to return success, and has the actual effect;
#   Does not support node, configuration returns success, but no actual effect ##
##########################################################################
#########################################################################
 #  @fn     #MV_CODEREADER_GetIntValue()
 #  @brief  获取Integer属性值
 #  @param  void# handle                [IN]        相机句柄
 #  @param  char# strKey                [IN]        属性键值，如获取宽度信息则为"Width"
 #  @param  #MVCC_INTVALUE# pstValue     [IN][OUT]   返回给调用者有关相机属性结构体指针
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_GetIntValue()
 #  @brief  Get Integer value
 #  @param  void# handle                [IN]        Handle
 #  @param  char# strKey                [IN]        Key value, for example, using "Width" to get width
 #  @param  #MVCC_INTVALUE# pstValue     [IN][OUT]   Structure pointer of camera features
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetIntValue(IN void# handle,IN const char# strKey,IN OUT #MV_CODEREADER_INTVALUE_EX #pIntValue);

#########################################################################
 #  @fn     #MV_CODEREADER_SetIntValue()
 #  @brief  设置Integer型属性值
 #  @param  void# handle                [IN]        相机句柄
 #  @param  char# strKey                [IN]        属性键值，如宽度信息则为"Width"
 #          const unsigned int nValue   [IN]        想要设置的相机的属性值
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_SetIntValue()
 #  @brief  Set Integer value
 #  @param  void# handle                [IN]        Handle
 #  @param  char# strKey                [IN]        Key value, for example, using "Width" to set width
 #          const unsigned int nValue   [IN]        Feature value to set
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_SetIntValue(IN void# handle,IN const char# strKey,IN int64_t nValue);

#########################################################################
 #  @fn     #MV_CODEREADER_GetEnu#MValue()
 #  @brief  获取Enum属性值
 #  @param  void# handle                   [IN]        相机句柄
 #  @param  char# strKey                   [IN]        属性键值，如获取像素格式信息则为"PixelFormat"
 #  @param  #MVCC_ENU#MVALUE# pEnu#MValue     [IN][OUT]   返回给调用者有关相机属性结构体指针
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_GetEnu#MValue()
 #  @brief  Get Enum value
 #  @param  void# handle                   [IN]        Handle
 #  @param  char# strKey                   [IN]        Key value, for example, using "PixelFormat" to get pixel format
 #  @param  #MVCC_ENU#MVALUE# pEnu#MValue     [IN][OUT]   Structure pointer of camera features
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetEnu#MValue(IN void# handle,IN const char# strKey, IN OUT #MV_CODEREADER_ENU#MVALUE #pEnu#MValue);

#########################################################################
 #  @fn     #MV_CODEREADER_SetEnu#MValue()
 #  @brief  设置Enum型属性值
 #  @param  void# handle                [IN]        相机句柄
 #  @param  char# strKey                [IN]        属性键值，如获取像素格式信息则为"PixelFormat"
 #          const unsigned int nValue   [IN]        想要设置的相机的属性值
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_SetEnu#MValue()
 #  @brief  Set Enum value
 #  @param  void# handle                [IN]        Handle
 #  @param  char# strKey                [IN]        Key value, for example, using "PixelFormat" to set pixel format
 #          const unsigned int nValue   [IN]        Feature value to set
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_SetEnu#MValue(IN void# handle,IN const char# strKey,IN unsigned int nValue);

#########################################################################
 #  @fn     #MV_CODEREADER_SetEnu#MValueByString()
 #  @brief  设置Enum型属性值
 #  @param  void# handle                [IN]        相机句柄
 #  @param  char# strKey                [IN]        属性键值，如获取像素格式信息则为"PixelFormat"
 #          char# sValue                [IN]        想要设置的相机的属性字符串
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_SetEnu#MValueByString()
 #  @brief  Set Enum value
 #  @param  void# handle                [IN]        Handle
 #  @param  char# strKey                [IN]        Key value, for example, using "PixelFormat" to set pixel format
 #          char# sValue                [IN]        Feature String to set
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_SetEnu#MValueByString(IN void# handle,IN const char# strKey,IN const char# sValue);

#########################################################################
 #  @fn     #MV_CODEREADER_GetFloatValue()
 #  @brief  获取Float属性值
 #  @param  void# handle                     [IN]        相机句柄
 #  @param  char# strKey                     [IN]        属性键值
 #  @param  #MVCC_FLOATVALUE #pFloatValue     [IN][OUT]   返回给调用者有关相机属性结构体指针
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_GetFloatValue()
 #  @brief  Get Float value
 #  @param  void# handle                     [IN]        Handle
 #  @param  char# strKey                     [IN]        Key value
 #  @param  #MVCC_FLOATVALUE #pFloatValue     [IN][OUT]   Structure pointer of camera features
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetFloatValue(IN void# handle,IN const char# strKey, IN OUT #MV_CODEREADER_FLOATVALUE #pFloatValue);

#########################################################################
 #  @fn     #MV_CODEREADER_SetFloatValue()
 #  @brief  设置Float型属性值
 #  @param  void# handle                [IN]        相机句柄
 #  @param  char# strKey                [IN]        属性键值
 #          float fValue                [IN]        想要设置的相机的属性值
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_SetFloatValue()
 #  @brief  Set Enum value
 #  @param  void# handle                [IN]        Handle
 #  @param  char# strKey                [IN]        Key value
 #          float fValue                [IN]        Feature value to set
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_SetFloatValue(IN void# handle,IN const char# strKey,IN float fValue);

#########################################################################
 #  @fn     #MV_CODEREADER_GetBoolValue()
 #  @brief  获取Boolean属性值
 #  @param  void# handle                     [IN]        相机句柄
 #  @param  char# strKey                     [IN]        属性键值
 #  @param  bool #pBoolValue                 [IN][OUT]   返回给调用者有关相机属性值
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_GetBoolValue()
 #  @brief  Get Boolean value
 #  @param  void# handle                     [IN]        Handle
 #  @param  char# strKey                     [IN]        Key value
 #  @param  bool #pBoolValue                 [IN][OUT]   Structure pointer of camera features
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetBoolValue(IN void# handle,IN const char# strKey,IN OUT bool #pBoolValue);

#########################################################################
 #  @fn     #MV_CODEREADER_SetBoolValue()
 #  @brief  设置Boolean型属性值
 #  @param  void# handle                [IN]        相机句柄
 #  @param  char# strKey                [IN]        属性键值
 #          bool bValue                 [IN]        想要设置的相机的属性值
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_SetBoolValue()
 #  @brief  Set Boolean value
 #  @param  void# handle                [IN]        Handle
 #  @param  char# strKey                [IN]        Key value
 #          bool bValue                 [IN]        Feature value to set
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_SetBoolValue(IN void# handle,IN const char# strKey,IN bool bValue);

#########################################################################
 #  @fn     #MV_CODEREADER_GetStringValue()
 #  @brief  获取String属性值
 #  @param  void# handle                       [IN]        相机句柄
 #  @param  char# strKey                       [IN]        属性键值
 #  @param  #MVCC_STRINGVALUE #pStringValue     [IN][OUT]   返回给调用者有关相机属性结构体指针
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_GetStringValue()
 #  @brief  Get String value
 #  @param  void# handle                       [IN]        Handle
 #  @param  char# strKey                       [IN]        Key value
 #  @param  #MVCC_STRINGVALUE #pStringValue     [IN][OUT]   Structure pointer of camera features
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetStringValue(IN void# handle,IN const char# strKey, IN OUT #MV_CODEREADER_STRINGVALUE #pStringValue);

#########################################################################
 #  @fn     #MV_CODEREADER_SetStringValue()
 #  @brief  设置String型属性值
 #  @param  void# handle                  [IN]        相机句柄
 #  @param  char# strKey                  [IN]        属性键值
 #          char # sValue                 [IN]        想要设置的相机的属性值
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_SetStringValue()
 #  @brief  Set String value
 #  @param  void# handle                  [IN]        Handle
 #  @param  char# strKey                  [IN]        Key value
 #          char # sValue                 [IN]        Feature value to set
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_SetStringValue(IN void# handle,IN const char# strKey,IN const char # sValue);

#########################################################################
 #  @fn     #MV_CODEREADER_SetCommandValue()
 #  @brief  设置Command型属性值
 #  @param  void# handle                  [IN]        相机句柄
 #  @param  char# strKey                  [IN]        属性键值
 #  @return 成功,返回#MV_CODEREADER_OK,失败,返回错误码

 #  @fn     #MV_CODEREADER_SetCommandValue()
 #  @brief  Set Command value
 #  @param  void# handle                  [IN]        Handle
 #  @param  char# strKey                  [IN]        Key value
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_SetCommandValue(IN void# handle,IN const char# strKey);

#########################################################################
 #  @fn     #MV_CODEREADER_GetOptimalPacketSize()
 #  @brief  获取最佳的packet size，该接口目前只支持GigE相机 (虚拟相机 该接口返回成功(0))
 #  @param  void# handle                  [IN]        相机句柄
 #  @return 最佳packetsize

 #  @fn     #MV_CODEREADER_GetOptimalPacketSize()
 #  @brief  Get the optimal Packet Size, Only support GigE Camera
 #  @param  void# handle                  [IN]        Camera handle
 #  @return Optimal packetsize
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetOptimalPacketSize(IN void# handle);

#########################################################################
 #  @fn     #MV_CODEREADER_ReadMemory()
 #  @brief  读内存（虚拟相机不支持）
 #  @param  handle：设备句柄
 #  @param  pBuffer：作为返回值使用，保存读到的内存值（内存值是按照大端模式存储的）
 #  @param  nAddress：待读取的内存地址，该地址可以从设备的Camera.xml文件中获取，形如xxx_RegAddr的xml节点值
 #                 （设备的Camera.xml文件会在设备打开之后自动生成在应用程序的当前目录中）
 #  @param  nLength：待读取的内存长度
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_ReadMemory()
 #  @brief  Read Memory(virtual camera does not support)
 #  @param  handle: Device Handle
 #  @param  pBuffer: Used as a return value, save the read-in memory value ( Memory value is stored in accordance with the big end model)
 #  @param  nAddress: Memory address to be read, which can be obtained from the Camera.xml file of the device, the form xml node value of xxx_RegAddr
 #                    (Camera.xml file of device is automatically generated in the application's current directory after the device is opened)
 #  @param  nLength: Length of the memory to be read
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
##########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_ReadMemory(IN void# handle , IN OUT void #pBuffer, IN int64_t nAddress, IN int64_t nLength);

#########################################################################
 #  @fn     #MV_CODEREADER_WriteMemory()
 #  @brief  写内存（虚拟相机不支持）
 #  @param  handle：设备句柄
 #  @param  pBuffer：待写入的内存值（注意内存值要按照大端模式存储）
 #  @param  nAddress：待写入的内存地址，该地址可以从设备的Camera.xml文件中获取，形如xxx_RegAddr的xml节点值
 #                 （设备的Camera.xml文件会在设备打开之后自动生成在应用程序的当前目录中）
 #  @param  nLength：待写入的内存长度
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_WriteMemory()
 #  @brief  Write Memory(virtual camera does not support)
 #  @param  handle: Device Handle
 #  @param  pBuffer: Memory value to be written ( Note the memory value to be stored in accordance with the big end model)
 #  @param  nAddress: Memory address to be written, which can be obtained from the Camera.xml file of the device, the form xml node value of xxx_RegAddr
 #                    (Camera.xml file of device is automatically generated in the application's current directory after the device is opened)
 #  @param  nLength: Length of the memory to be written
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
#########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_WriteMemory(IN void# handle , IN const void #pBuffer, IN int64_t nAddress, IN int64_t nLength);

## 注册异常消息回调，在打开设备之后调用
## Register exception message callback, call after open device
#########################################################################
 #  @fn     #MV_CODEREADER_RegisterExceptionCallBack()
 #  @brief  注册异常消息回调，在打开设备之后调用（虚拟相机一直返回OK，但实际不支持，无效果）
 #  @param  handle：设备句柄
 #  @param  cbException       [IN]      异常回调函数指针
 #  @param  pUser             [IN]      用户自定义变量
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_RegisterExceptionCallBack()
 #  @brief  Register Exception Message CallBack, call after open device(virtual camera has been return OK, but it does not support, no effect)
 #  @param  handle: Device handle
 #  @param  cbException       [IN]       Exception Message CallBack Function Pointer
 #  @param  pUser             [IN]       User defined variable
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
#########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_RegisterExceptionCallBack(IN void# handle,
#                                                             void(__stdcall# cbException)(unsigned int nMsgType, void# pUser),
#                                                             void# pUser);

## 注册触发回调(由相机固件提供触发)，在打开设备之后调用
## Register Trigger callback(camera provide), call after open device
#########################################################################
#  @fn     #MV_CODEREADER_RegisterTriggerCallBack()
#  @brief  注册触发回调，在打开设备之后调用（虚拟相机不支持）
#  @param  handle：设备句柄
#  @param  cbTrigger         [IN]      触发回调函数指针
#  @param  pUser             [IN]      用户自定义变量
#  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

#  @fn     #MV_CODEREADER_RegisterTriggerCallBack()
#  @brief  Register Trigger CallBack, call after open device(virtual camera does not support)
#  @param  handle: Device handle
#  @param  cbTrigger         [IN]       Trigger CallBack Function Pointer
#  @param  pUser             [IN]       User defined variable
#  @return Success, return #MV_CODEREADER_OK. Failure, return error code
#########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_RegisterTriggerCallBack(IN void# handle,
#                                                                            void(__stdcall# cbTrigger)(#MV_CODEREADER_TRIGGER_INFO_DATA# pstTriggerInfo, void# pUser),
#                                                                            void# pUser);


#########################################################################
 #  @fn     #MV_CODEREADER_RegisterAllEventCallBack()
 #  @brief  注册全部事件回调，在打开设备之后调用(该接口需要固件支持)（虚拟相机不支持）
 #  @remark 支持节点ArithmeticModel、BillCombineEnable，调用该接口后，对节点数值进行变更，事件回调中有事件数据
 #  @param  handle                      [IN]            设备句柄
 #  @param  cbEvent                     [IN][OUT]       事件回调函数指针
 #  @param  pUser                       [IN]            用户自定义变量
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_RegisterAllEventCallBack()
 #  @brief  Register all event callback, which is called after the device is opened(the API need device support)(virtual camera does not support)
 #  @remark Support node ArithmeticModel、BillCombineEnable, after event callback, change the node number,
 #           the pEventInfo will have data
 #  @param  handle                      [IN]            Device handle
 #  @param  cbEvent                     [IN][OUT]       Event CallBack Function Pointer
 #  @param  pUser                       [IN]            User defined variable
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
#########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_RegisterAllEventCallBack(void# handle,
 #                                                                          void(__stdcall# cbAllEvent)(#MV_CODEREADER_EVENT_OUT_INFO# pEventInfo, void# pUser),
 #                                                                          void# pUser);

#########################################################################
 #  @fn     #MV_CODEREADER_GIGE_ForceIp()
 #  @brief  强制IP设置（虚拟相机不支持）
 #  @remark 该接口为适配兼容SI系列智能读码器，不支持设置子网掩码和网关异常值报错；
 #           只支持设置IP错误报错，ip设置为0将配置为DHCP自动获取ip的模式，不报错。
 #  @param  handle：设备句柄
 #  @param  nIP               [IN]      设置的IP
 #  @param  nSubNetMask       [IN]      子网掩码
 #  @param  nDefaultGateWay   [IN]      默认网关
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_GIGE_ForceIp()
 #  @brief  Force IP (virtual camera does not support)
 #  @remark The interface for the adapter is compatible with SI series intelligent reading code,
 #           does not support setting the correct subnet mask and gateway outlier; Only allows you to
 #           set the IP error an error, the IP is set to 0 will automatically get configured for DHCP IP mode, is not an error.
 #  @param  handle: Device handle
 #  @param  nIP               [IN]      IP to set
 #  @param  nSubNetMask       [IN]      Subnet mask
 #  @param  nDefaultGateWay   [IN]      Default gateway
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
#########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GIGE_ForceIp(IN void# handle, IN unsigned int nIP, IN unsigned int nSubNetMask, IN unsigned int nDefaultGateWay);

#########################################################################
 #  @fn     #MV_CODEREADER_GIGE_SetIpConfig
 #  @brief  配置IP方式（虚拟相机不支持）
 #  @remark SI系列智能读码器不支持通过该接口设置IP配置类型, SI系列若设置STATIC则直接返回OK；
 #           若需DHCP则调用#MV_CODEREADER_GIGE_ForceIp()接口的nIP设置为0；设置LLA则返回不支持
 #  @param  handle                      [IN]            设备句柄
 #  @param  nType                       [IN]            IP类型，见#MV_IP_CFG_x
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_GIGE_SetIpConfig
 #  @brief  IP configuration method (virtual camera does not support)
 #  @remark SI series intelligent reading code device does not support through the interface set IP configuration type,
 #           if SI series set STATIC returned directly OK;Set the LLA returns does not support.
 #          if need DHCP call #MV_CODEREADER_GIGE_ForceIp () the nIP of the interface is set to 0.
 #  @param  handle                      [IN]            Device handle
 #  @param  nType                       [IN]            IP type, refer to #MV_IP_CFG_x
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
#########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GIGE_SetIpConfig(IN void# handle, IN unsigned int nType);

#########################################################################
 #  @fn     #MV_CODEREADER_FileAccessRead()
 #  @brief  从相机读取文件（虚拟相机不支持）
 #  @param  handle                [IN]           句柄地址
 #  @param  pstFileAccess         [IN]           文件存取结构体
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_FileAccessRead()
 #  @brief  Read the file from the camera (virtual camera does not support)
 #  @param  handle                [IN]           Handle
 #  @param  pstFileAccess         [IN]           File access structure
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_FileAccessRead(IN void# handle, IN #MV_CODEREADER_FILE_ACCESS # pstFileAccess);

#########################################################################
 #  @fn     #MV_CODEREADER_FileAccessWrite()
 #  @brief  将文件写入相机（虚拟相机不支持）
 #  @param  handle                [IN]           句柄地址
 #  @param  pstFileAccess         [IN]           文件存取结构体
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_FileAccessWrite()
 #  @brief  Write the file to camera (virtual camera does not support)
 #  @param  handle                [IN]           Handle
 #  @param  pstFileAccess         [IN]           File access structure
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_FileAccessWrite(IN void# handle, IN #MV_CODEREADER_FILE_ACCESS # pstFileAccess);

#########################################################################
 #  @fn     #MV_CODEREADER_GetFileAccessProgress
 #  @brief  获取文件存取的进度（虚拟相机不支持）
 #  @param  handle                      [IN]            设备句柄
 #  @param  pstFileAccessProgress       [IN][OUT]       进度内容
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码 （当前文件存取的状态）

 #  @fn     #MV_CODEREADER_GetFileAccessProgress
 #  @brief  Get File Access Progress (virtual camera does not support)
 #  @param  handle                      [IN]            Device handle
 #  @param  pstFileAccessProgress       [IN][OUT]       File access Progress
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetFileAccessProgress(IN void# handle, IN OUT #MV_CODEREADER_FILE_ACCESS_PROGRESS # pstFileAccessProgress);

##########################################################################
## 设置和获取抠图算法接口（虚拟相机不支持）                                        ##
## General interface for getting and setting waybill parameters (virtual camera does not support)##
##########################################################################

#########################################################################
 #  @fn     #MV_CODEREADER_SetWayBillEnable()
 #  @brief  设置抠图使能（虚拟相机不支持）
 #  @remark 读码器本身抠图使能节点DisplayBillInfoEnable开启可获取抠图坐标信息，同时该接口参数设置True，可获取面单图片pImageWaybill。
 #  @param  handle                 [IN]          句柄
 #  @param  bWaybillEnable         [IN]          抠图使能
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_SetWayBillEnable()
 #  @brief  Set WayBill Enable (virtual camera does not support)
 #  @param  handle                 [IN]          Handle
 #  @param  bWaybillEnable         [IN]          WayBillEnable
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_SetWayBillEnable(IN void# handle, IN bool bWaybillEnable);

#########################################################################
 #  @fn     #MV_CODEREADER_GetWayBillInfo()
 #  @brief  获取当前输入图像的面单信息（输入图像对应 #MV_CODEREADER_IMAGE_OUT_INFO_EX 该结构体信息）（虚拟相机不支持）
 #  @param  handle                 [IN]          句柄
 #  @param  pData                  [IN]          原始图像指针
 #  @param  pstFrameInfo           [IN][OUT]     图像信息结构体
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_GetWayBillInfo()
 #  @brief  Get the WayBill Info of current input image (virtual camera does not support)
 #  @param  handle                 [IN]          Handle
 #  @param  pData                  [IN]          Received image data pointer
 #  @param  pstFrameInfo           [IN][OUT]     Image information structure
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetWayBillInfo(IN void# handle, IN unsigned char# pData, IN OUT #MV_CODEREADER_IMAGE_OUT_INFO_EX# pstFrameInfo);

#########################################################################
 #  @fn     #MV_CODEREADER_GetWayBillInfoEx()
 #  @brief  获取当前输入图像的面单信息（输入图像对应 #MV_CODEREADER_IMAGE_OUT_INFO_EX2 该结构体信息） （虚拟相机不支持）
 #  @param  handle                 [IN]          句柄
 #  @param  pData                  [IN]          原始图像指针
 #  @param  pstFrameInfoEx         [IN][OUT]     图像信息结构体
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_GetWayBillInfoEx()
 #  @brief  Get the WayBill Info of current input image (virtual camera does not support)
 #  @param  handle                 [IN]          Handle
 #  @param  pData                  [IN]          Received image data pointer
 #  @param  pstFrameInfoEx         [IN][OUT]     Image information structure
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GetWayBillInfoEx(IN void# handle, IN unsigned char# pData, IN OUT #MV_CODEREADER_IMAGE_OUT_INFO_EX2# pstFrameInfo);

#########################################################################
 #  @fn     #MV_CODEREADER_Algorithm_SetIntValue()
 #  @brief  设置整型参数（虚拟相机不支持）
 #  @param  handle                 [IN]          句柄
 #  @param  strParamKeyName        [IN]          属性键值
 #  @param  nValue                 [IN]          参数值
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_Algorithm_SetIntValue()
 #  @brief  Set Integer Value (virtual camera does not support)
 #  @param  handle                 [IN]          Handle
 #  @param  strParamKeyName        [IN]          Param KeyName
 #  @param  nValue                 [IN]          Value
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_Algorithm_SetIntValue(IN void# handle, IN const char# const strParamKeyName, IN const int nValue);

#########################################################################
 #  @fn     #MV_CODEREADER_Algorithm_GetIntValue()
 #  @brief  获取整型参数（虚拟相机不支持）
 #  @param  handle                 [IN]          句柄
 #  @param  strParamKeyName        [IN]          属性键值
 #  @param  pnValue                [IN][OUT]     参数值
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_Algorithm_GetIntValue()
 #  @brief  Get Integer Value (virtual camera does not support)
 #  @param  handle                 [IN]          Handle
 #  @param  strParamKeyName        [IN]          Param KeyName
 #  @param  pnValue                [IN][OUT]     Value
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_Algorithm_GetIntValue(IN void# handle, IN const char# const strParamKeyName, IN OUT int# const pnValue);

#########################################################################
 #  @fn     #MV_CODEREADER_SaveImage()
 #  @brief  保存图片，支持Bmp和Jpeg.编码质量在50-99之间（虚拟相机不支持）
 #  @param  pSaveParam             [IN][OUT]          保存图片参数结构体
 #  @return 成功，返回#MV_CODEREADER_OK；错误，返回错误码

 #  @fn     #MV_CODEREADER_SaveImage()
 #  @brief  Save image, support Bmp and Jpeg. Encoding quality, (50-99] (virtual camera does not support)
 #  @param  pSaveParam             [IN][OUT]           Save image parameters structure
 #  @return Success, return #MV_CODEREADER_OK. Failure, return error code
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_SaveImage(IN void# handle, IN OUT #MV_CODEREADER_SAVE_IMAGE_PARAM_EX# pSaveParam);

#########################################################################
 #  @fn     #MV_CODEREADER_GIGE_SetGvcpTimeout
 #  @brief  设置GVCP命令超时时间（虚拟相机一直返回OK，但实际不支持，无效果）
 #  @param  handle                      [IN]            设备句柄
 #  @param  nMillisec                   [IN]            超时时间，以毫秒为单位，范围：0-10000
 #  @return 成功，返回#MV_OK；错误，返回错误码
 #  @remarks 连接设备之后调用该接口可以设置GVCP命令超时时间。

 #  @fn     #MV_CODEREADER_GIGE_SetGvcpTimeout
 #  @brief  Set GVCP cammand timeout
 #  @param  handle                      [IN]            Device handle
 #  @param  nMillisec                   [IN]            Timeout, ms as unit, range: 0-10000
 #  @return Success, return #MV_OK. Failure, return error code
 #  @remarks After the device is connected, call this interface to set GVCP command timeout time.
 #########################################################################
#MV_CODEREADERCTRL_API int __stdcall #MV_CODEREADER_GIGE_SetGvcpTimeout(IN void# handle, IN unsigned int nMillisec);

#ifdef __cplusplus

#endif

#endif ##_#MV_CODEREADER_CTRL_H_
