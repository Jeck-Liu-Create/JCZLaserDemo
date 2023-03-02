from ipaddress import IPv4Address
from ctypes import *

# ifndef _MV_CODEREADER_PARAMS_H_
# define _MV_CODEREADER_PARAMS_H_

# include "MvCodeReaderPixelType.h"

# ifndef __cplusplus
# typedef c_char    bool;
# define true    1
# define false   0
# endif

# ********************************宏定义类型************************************************************/
# 设备类型定义
MV_CODEREADER_UNKNOW_DEVICE = 0x00000000           # 未知设备类型
MV_CODEREADER_GIGE_DEVICE = 0x00000001           # GigE设备
MV_CODEREADER_1394_DEVICE = 0x00000002           # 1394-a/b 设备
MV_CODEREADER_USB_DEVICE = 0x00000004           # USB3.0 设备
MV_CODEREADER_CAMERALINK_DEVICE = 0x00000008           # CameraLink设备
MV_CODEREADER_ID_DEVICE = 0x00000010

# 异常消息类型
MV_CODEREADER_EXCEPTION_DEV_DISCONNECT = 0x00008001      # 设备断开连接
MV_CODEREADER_EXCEPTION_VERSION_CHECK = 0x00008002      # SDK与驱动版本不匹配

# 设备的访问模式
# 独占权限，其他APP只允许读CCP寄存器
MV_CODEREADER_ACCESS_Exclusive = 1
# 可以从5模式下抢占权限，然后以独占权限打开
MV_CODEREADER_ACCESS_ExclusiveWithSwitch = 2
# 控制权限，其他APP允许读所有寄存器
MV_CODEREADER_ACCESS_Control = 3
# 可以从5的模式下抢占权限，然后以控制权限打开
MV_CODEREADER_ACCESS_ControlWithSwitch = 4
# 以可被抢占的控制权限打开
MV_CODEREADER_ACCESS_ControlSwitchEnable = 5
# 可以从5的模式下抢占权限，然后以可被抢占的控制权限打开
MV_CODEREADER_ACCESS_ControlSwitchEnableWithKey = 6
# 读模式打开设备，适用于控制权限下
MV_CODEREADER_ACCESS_Monitor = 7

# 设备信息最大长度
INFO_MAX_BUFFER_SIZE = 64                                 # 最大信息长度

# 最大支持的设备个数
MV_CODEREADER_MAX_DEVICE_NUM = 256

# 最大类型个数(适用于枚举类型)
MV_CODEREADER_MAX_XML_SYMBOLIC_NUM = 64             # 支持最大枚举类型最大参数

# GigEVision IP配置方式
MV_CODEREADER_IP_CFG_STATIC = 0x05000000       # 静态IP
MV_CODEREADER_IP_CFG_DHCP = 0x06000000       # DHCP
MV_CODEREADER_IP_CFG_LLA = 0x04000000       # LLA

# Event事件回调信息
MV_CODEREADER_MAX_EVENT_NAME_SIZE = 128          # 相机Event事件名称最大长度

# 最大条码长度
MV_CODEREADER_MAX_BCR_CODE_LEN = 256
# 最大条码长度扩展
MV_CODEREADER_MAX_BCR_CODE_LEN_EX = 4096
# 最大OCR长度
MV_CODEREADER_MAX_OCR_LEN = 128

# 一次最多输出条码个数
MAX_CODEREADER_BCR_COUNT = 200
# 一次最多输出条码个数
MAX_CODEREADER_BCR_COUNT_EX = 300

# 最大数据缓存
MV_CODEREADER_MAX_RESULT_SIZE = (1024*64)

# 一次输出最大抠图个数
MAX_CODEREADER_WAYBILL_COUNT = 50
# 一次输出最大OCR个数
MAX_CODEREADER_OCR_COUNT = 100

# 输出协议类型
CommuPtlSmartSDK = 1          # SamrtSDK协议
CommuPtlTcpIP = 2          # TCPIP协议
CommuPtlSerial = 3          # Serial协议

# 升级最大支持的设备个数
MV_CODEREADER_MAX_UPGARDEDEVICE_NUM = 100

# ***********************************************************************/
# 抠图参数，内部有默认值，可以不设置                             */
# ***********************************************************************/
KEY_WAYBILL_ABILITY = "WAYBILL_Ability"                   # 算法能力集，含面单提取[0x1]，图像增强[0x2]，码提取[0x4]，Box拷贝模块[0x8]，面单提取模块[0x10]，模块最大编号[0x3F]
KEY_WAYBILL_MAX_WIDTH = "WAYBILL_Max_Width"                 # 算法最大宽度，默认5472，范围[0,65535]
KEY_WAYBILL_MAX_HEIGHT = "WAYBILL_Max_Height"                # 算法最大高度，默认3648，范围[0,65535]
KEY_WAYBILL_OUTPUTIMAGETYPE = "WAYBILL_OutputImageType"           # 面单抠图输出的图片格式，默认Jpg，范围[1,3],1为Mono8，2为Jpg，3为Bmp
KEY_WAYBILL_JPGQUALITY = "WAYBILL_JpgQuality"                # jpg编码质量，默认80，范围[1,100]
KEY_WAYBILL_ENHANCEENABLE = "WAYBILL_EnhanceEnable"             # 图像增强使能，默认0，范围[0,1]

KEY_WAYBILL_MINWIDTH = "WAYBILL_MinWidth"                  # waybill最小宽, 宽是长边, 高是短边，默认100，范围[15,2592]
KEY_WAYBILL_MINHEIGHT = "WAYBILL_MinHeight"                 # waybill最小高，默认100，范围[10,2048]
KEY_WAYBILL_MAXWIDTH = "WAYBILL_MaxWidth"                  # waybill最大宽, 宽是长边, 高是短边，默认3072，最小值15
KEY_WAYBILL_MAXHEIGHT = "WAYBILL_MaxHeight"                 # waybill最大高，默认2048，最小值10
KEY_WAYBILL_MORPHTIMES = "WAYBILL_MorphTimes"                # 膨胀次数，默认0，范围[0,10]
KEY_WAYBILL_GRAYLOW = "WAYBILL_GrayLow"                   # 面单上条码和字符灰度最小值，默认0，范围[0,255]
KEY_WAYBILL_GRAYMID = "WAYBILL_GrayMid"                   # 面单上灰度中间值，用于区分条码和背景，默认70，范围[0,255]
KEY_WAYBILL_GRAYHIGH = "WAYBILL_GrayHigh"                  # 面单上背景灰度最大值，默认130，范围[0,255]
KEY_WAYBILL_BINARYADAPTIVE = "WAYBILL_BinaryAdaptive"            # 自适应二值化，默认1，范围[0,1]
KEY_WAYBILL_BOUNDARYROW = "WAYBILL_BoundaryRow"               # 面单抠图行方向扩边，默认0，范围[0,2000]
KEY_WAYBILL_BOUNDARYCOL = "WAYBILL_BoundaryCol"               # 面单抠图列方向扩边，默认0，范围[0,2000]
KEY_WAYBILL_MAXBILLBARHEIGTHRATIO = "WAYBILL_MaxBillBarHightRatio"      # 最大面单和条码高度比例，默认20，范围[1,100]
KEY_WAYBILL_MAXBILLBARWIDTHRATIO = "WAYBILL_MaxBillBarWidthRatio"      # 最大面单和条码宽度比例，默认5，范围[1,100]
KEY_WAYBILL_MINBILLBARHEIGTHRATIO = "WAYBILL_MinBillBarHightRatio"      # 最小面单和条码高度比例，默认5，范围[1,100]
KEY_WAYBILL_MINBILLBARWIDTHRATIO = "WAYBILL_MinBillBarWidthRatio"      # 最小面单和条码宽度比例，默认2，范围[1,100]
KEY_WAYBILL_ENHANCEMETHOD = "WAYBILL_EnhanceMethod"             # 增强方法，最小值/默认值/不进行增强[0x1]，线性拉伸[0x2]，直方图拉伸[0x3]，直方图均衡化[0x4]，亮度校正/最大值[0x5]
KEY_WAYBILL_ENHANCECLIPRATIOLOW = "WAYBILL_ClipRatioLow"              # 增强拉伸低阈值比例，默认1，范围[0,100]
KEY_WAYBILL_ENHANCECLIPRATIOHIGH = "WAYBILL_ClipRatioHigh"             # 增强拉伸高阈值比例，默认99，范围[0,100]
KEY_WAYBILL_ENHANCECONTRASTFACTOR = "WAYBILL_ContrastFactor"            # 对比度系数，默认100，范围[1,10000]
KEY_WAYBILL_ENHANCESHARPENFACTOR = "WAYBILL_SharpenFactor"             # 锐化系数，默认0，范围[0,10000]
KEY_WAYBILL_SHARPENKERNELSIZE = "WAYBILL_KernelSize"                # 锐化滤波核大小，默认3，范围[3,15]
KEY_WAYBILL_CODEBOUNDARYROW = "WAYBILL_CodeBoundaryRow"           # 码单抠图行方向扩边，默认0，范围[0,2000]
KEY_WAYBILL_CODEBOUNDARYCOL = "WAYBILL_CodeBoundaryCol"           # 码单抠图列方向扩边，默认0，范围[0,2000]

# ***********************************************结构体类型**************************************************************/
def ubyte2str(v: Array) -> str:
    return cast(v, c_char_p).value.decode("utf-8")

EnumType = c_int

# GigE设备信息
class MV_CODEREADER_GIGE_DEVICE_INFO(Structure):
    _fields_ = [
        ("nIpCfgOption", c_uint),                                           # 设备支持的IP类型
        ("nIpCfgCurrent", c_uint),                                          # 设备当前IP类型
        ("nCurrentIp", c_uint),                                             # 设备当前IP
        ("nCurrentSubNetMask", c_uint),                                     # 设备当前子网掩码
        ("nDefultGateWay", c_uint),                                         # 设备默认网关
        ("chManufacturerName", c_ubyte*32),                             # 设备厂商
        ("chModelName", c_ubyte*32),                                    # 设备型号
        ("chDeviceVersion", c_ubyte*32),                                # 设备版本
        ("chManufacturerSpecificInfo", c_ubyte*48),                     # 设备厂商特殊信息
        ("chSerialNumber", c_ubyte*16),                                 # 设备序列号
        ("chUserDefinedName", c_ubyte*16),                              # 设备用户自定义名称
        ("nNetExport", c_uint),                                             # 主机网口IP地址
        ("nCurUserIP", c_uint),                                             # 当前占用设备的用户IP
        ("nReserved", c_uint*3),                                         # 保留字节
    ]

    @property
    def currentIp(self) -> IPv4Address:
        return IPv4Address(self.nCurrentIp)

    @property
    def currentSubNetMask(self) -> IPv4Address:
        return IPv4Address(self.nCurrentSubNetMask)

    @property
    def defultGateWay(self) -> IPv4Address:
        return IPv4Address(self.nDefultGateWay)

    @property
    def manufacturerName(self) -> str:
        return ubyte2str(self.chManufacturerName)

    @property
    def modelName(self) -> str:
        return ubyte2str(self.chModelName)

    @property
    def deviceVersion(self) -> str:
        return ubyte2str(self.chDeviceVersion)

    @property
    def manufacturerSpecificInfo(self) -> str:
        return ubyte2str(self.chManufacturerSpecificInfo)

    @property
    def serialNumber(self) -> str:
        return ubyte2str(self.chSerialNumber)

    @property
    def userDefinedName(self) -> str:
        return ubyte2str(self.chUserDefinedName)

    @property
    def netExport(self) -> IPv4Address:
        return IPv4Address(self.nNetExport)

    @property
    def curUserIP(self) -> IPv4Address:
        return IPv4Address(self.nCurUserIP)

# U3V设备信息
class MV_CODEREADER_USB3_DEVICE_INFO(Structure):
    _fields_=  [
        ("CrtlInEndPoint"                            ,  c_ubyte ),      # 控制输入端点
        ('CrtlOutEndPoint'                           ,  c_ubyte ),      # 控制输出端点
        ('StreamEndPoint'                            ,  c_ubyte ),      # 流端点
        ('EventEndPoint'                             ,  c_ubyte ),      # 事件端点
        ('idVendor'                                  ,  c_ushort),      # 供应商ID号
        ('idProduct'                                 ,  c_ushort),      # 产品ID号
        ('nDeviceNumber'                             ,  c_uint  ),      # 设备序列号
        ('chDeviceGUID'                              ,  c_ubyte*INFO_MAX_BUFFER_SIZE ),      # 设备GUID号
        ('chVendorName'                              ,  c_ubyte*INFO_MAX_BUFFER_SIZE ),      # 供应商名称
        ('chModelName'                              ,  c_ubyte*INFO_MAX_BUFFER_SIZE ),      # 设备型号
        ('chFamilyName'                             ,  c_ubyte*INFO_MAX_BUFFER_SIZE ),      # 设备家族名称
        ('chDeviceVersion'                           ,  c_ubyte*INFO_MAX_BUFFER_SIZE ),      # 设备版本
        ('chManufacturerName'                        ,  c_ubyte*INFO_MAX_BUFFER_SIZE ),      # 设备厂商
        ('chSerialNumber'                           ,  c_ubyte*INFO_MAX_BUFFER_SIZE ),      # 设备序列号
        ('chUserDefinedName'                        ,  c_ubyte*INFO_MAX_BUFFER_SIZE ),      # 设备用户自定义名称
        ('nbcdUSB'                                   ,  c_uint  ),      # 设备支持的USB协议
        ('nReserved'                                ,  c_uint*3  ),      # 保留字节
    ]


class SpecialInfo(Union):
    _fields_ = [
        ("stGigEInfo", MV_CODEREADER_GIGE_DEVICE_INFO),  # GigE设备信息
        ("stUsb3VInfo", MV_CODEREADER_USB3_DEVICE_INFO)  # U3V设备信息
    ]


# 设备信息
class MV_CODEREADER_DEVICE_INFO(Structure):
    _fields_ = [
        ('nMajorVer', c_ushort),               # 设备主版本号
        ('nMinorVer', c_ushort),               # 设备次版本号
        ('nMacAddrHigh', c_uint),               # 设备MAC地址高位
        ('nMacAddrLow', c_uint),               # 设备MAC地址低位
        ('nTLayerType', c_uint),               # 设备传输层协议类型

        # 是否为指定系列型号相机
        # true -指定系列型号相机 false- 非指定系列型号相机
        ('bSelectDevice',  c_bool),       # ch:选择设备 |en:Choose device
        ('nReserved',   c_uint*3),       # 保留字节
        ('specialInfo', SpecialInfo)
    ]

    @property
    def majorVer(self) -> int:
        return self.nMajorVer

    @property
    def minorVer(self) -> int:
        return self.nMinorVer

    # def macAddr(self) -> str:
    #     return (self.nMacAddrHigh, self.nMacAddrLow)

    @property
    def isSelectDevice(self) -> bool:
        return self.bSelectDevice

    @property
    def layerType(self) -> int:
        return self.nTLayerType

    @property
    def stGigEInfo(self) -> MV_CODEREADER_GIGE_DEVICE_INFO:
        return self.specialInfo.stGigEInfo

    @property
    def stUsb3VInfo(self) -> MV_CODEREADER_USB3_DEVICE_INFO:
        return self.specialInfo.stUsb3VInfo

# 设备信息列表
class MV_CODEREADER_DEVICE_INFO_LIST(Structure):
    _fields_ = [
        ("nDeviceNum", c_uint),    # 在线设备数量
        ("pDeviceInfo", POINTER(MV_CODEREADER_DEVICE_INFO)*MV_CODEREADER_MAX_DEVICE_NUM)   # 设备信息(支持最多256个设备)
    ]

    @property
    def deviceNum(self) -> int:
        return self.nDeviceNum

    def deviceInfo(self, i) -> MV_CODEREADER_DEVICE_INFO:
        return self.pDeviceInfo[i].contents

# # 输出帧信息
# typedef struct _MV_CODEREADER_FRAME_OUT_INFO_
# {
#     c_ushort      nWidth                             # 图像宽
#     c_ushort      nHeight                            # 图像高
#     enum MvCodeReaderGvspPixelType     enPixelType         # 像素格式

#     c_uint        nFrameNum                          # 帧号
#     c_uint        nDevTimeStampHigh                  # 时间戳高32位
#     c_uint        nDevTimeStampLow                   # 时间戳低32位
#     c_uint        nReserved0                         # 保留，8字节对齐
#     c_longlong             nHostTimeStamp                     # 主机生成的时间戳
#     c_uint        nFrameLen                          # 图像长度
#     c_uint        nLostPacket                        # 本帧丢包数
#     c_uint        nReserved[2]  # 保留字节
# }MV_CODEREADER_FRAME_OUT_INFO

# # ch:Chunk内容 | en:The content of ChunkData
# typedef struct _MV_CODEREADER_CHUNK_DATA_CONTENT_
# {
#     c_ubyte * pChunkData
#     c_uint    nChunkID
#     c_uint    nChunkLen
#     c_uint    nReserved[8]  # 保留
# }MV_CODEREADER_CHUNK_DATA_CONTENT

# # 输出帧信息
# typedef struct _MV_CODEREADER_FRAME_OUT_INFO_EX_
# {
#     c_ushort      nWidth                             # 图像宽
#     c_ushort      nHeight                            # 图像高
#     enum MvCodeReaderGvspPixelType     enPixelType         # 像素格式
#     c_uint        nFrameNum                          # 帧号
#     c_uint        nDevTimeStampHigh                  # 时间戳高32位
#     c_uint        nDevTimeStampLow                   # 时间戳低32位
#     c_uint        nReserved0                         # 保留，8字节对齐
#     c_longlong             nHostTimeStamp                     # 主机生成的时间戳
#     c_uint        nFrameLen                          # 图像长度

#     # chunk新增水印信息
#     # 设备水印时标
#     c_uint        nSecondCount                       # 秒数
#     c_uint        nCycleCount                        # 循环计数
#     c_uint        nCycleOffset                       # 循环计数偏移量
#     float               fGain                              # 增益
#     float               fExposureTime                      # 曝光时间
#     c_uint        nAverageBrightness                 # 平均亮度

#     # 白平衡相关
#     c_uint        nRed                               # 红色数据
#     c_uint        nGreen                             # 绿色数据
#     c_uint        nBlue                              # 蓝色数据
#     c_uint        nFrameCounter                      # 图像数量计数
#     c_uint        nTriggerIndex                      # 触发计数

#     # Line 输入/输出
#     c_uint        nInput                             # 输入
#     c_uint        nOutput                            # 输出

#     # ROI区域
#     c_ushort      nOffsetX                           # ROI X轴偏移
#     c_ushort      nOffsetY                           # ROI Y轴偏移
#     c_ushort      nChunkWidth                        # Chunk宽度
#     c_ushort      nChunkHeight                       # Chunk高度
#     c_uint        nLostPacket                        # 本帧丢包数
#     c_uint        nUnparsedChunkNum  # 未解析的Chunkdata个数
#     union
#     {
#         MV_CODEREADER_CHUNK_DATA_CONTENT * pUnparsedChunkContent
#         c_longlong nAligning
#     }UnparsedChunkList

#     c_uint        nReserved[36]  # 保留字节
# }MV_CODEREADER_FRAME_OUT_INFO_EX

# # 图像显示信息
# typedef struct _MV_CODEREADER_DISPLAY_FRAME_INFO_
# {
#     void * hWnd                          # 显示窗口句柄
#     c_ubyte * pData                         # 源图像数据
#     c_uint             nDataLen                      # 源图像数据长度
#     c_ushort           nWidth                        # 源图像宽
#     c_ushort           nHeight                       # 源图像高
#     enum MvCodeReaderGvspPixelType     enPixelType         # 源图像像素格式
#     c_uint             nRes[4]  # 保留字节
# }MV_CODEREADER_DISPLAY_FRAME_INFO

# # 保存图片格式
# enum MV_CODEREADER_IAMGE_TYPE
# {
#     MV_CODEREADER_Image_Undefined = 0,
#     MV_CODEREADER_Image_Mono8 = 1,
#     MV_CODEREADER_Image_Jpeg = 2,
#     MV_CODEREADER_Image_Bmp = 3,
#     MV_CODEREADER_Image_RGB24 = 4,
#     MV_CODEREADER_Image_Png = 5,      # Png图像(暂不支持)
#     MV_CODEREADER_Image_Tif = 6,      # Tif图像(暂不支持)
# }

# # 保存图片参数
# typedef struct _MV_CODEREADER_SAVE_IMAGE_PARAM_T_
# {
#     c_ubyte * pData                            # 输入数据缓存
#     c_uint          nDataLen                         # 输入数据大小
#     enum MvCodeReaderGvspPixelType       enPixelType       # 输入数据的像素格式
#     c_ushort        nWidth                           # 图像宽
#     c_ushort        nHeight                          # 图像高

#     c_ubyte * pImageBuffer                     # 输出图片缓存
#     c_uint          nImageLen                        # 输出图片大小
#     c_uint          nBufferSize                      # 提供的输出缓冲区大小
#     enum MV_CODEREADER_IAMGE_TYPE    enImageType  # 输出图片格式
# }MV_CODEREADER_SAVE_IMAGE_PARAM

# # 图片保存参数
# typedef struct _MV_CODEREADER_SAVE_IMAGE_PARAM_T_EX_
# {
#     c_ubyte * pData                              # 输入数据缓存
#     c_uint        nDataLen                           # 输入数据大小
#     enum MvCodeReaderGvspPixelType     enPixelType         # 输入数据的像素格式
#     c_ushort      nWidth                             # 图像宽
#     c_ushort      nHeight                            # 图像高

#     c_ubyte * pImageBuffer                       # 输出图片缓存
#     c_uint        nImageLen                          # 输出图片大小
#     c_uint        nBufferSize                        # 提供的输出缓冲区大小
#     enum MV_CODEREADER_IAMGE_TYPE  enImageType             # 输出图片格式
#     c_uint        nJpgQuality                        # 编码质量, (50-99]

#     # 格式转为RGB24的插值方法  0-最近邻 1-双线性 2-Hamilton （如果传入其它值则默认为最近邻）
#     c_uint        iMethodValue                       # 插值方式
#     c_uint        nReserved[3]  # 保留字节
# }MV_CODEREADER_SAVE_IMAGE_PARAM_EX

# # 事件回调信息
class MV_CODEREADER_EVENT_OUT_INFO(Structure):
    _fields_ = [
        ("EventName", c_char*MV_CODEREADER_MAX_EVENT_NAME_SIZE),    # Event名称
        ('nEventID', c_ushort),    # Event号
        ('nStreamChannel', c_ushort),    # 流通道序号
        ('nBlockIdHigh', c_uint),    # 帧号高位
        ('nBlockIdLow', c_uint),    # 帧号低位
        ('nTimestampHigh', c_uint),    # 时间戳高位
        ('nTimestampLow', c_uint),    # 时间戳低位
        ('pEventData', c_void_p),    # Event数据
        ('nEventDataSize', c_uint),    # Event数据长度
        ('nReserved', c_uint*16),    # 预留
    ]


# # 文件存取
# typedef struct _MV_CODEREADER_FILE_ACCESS_T
# {
#     const c_char * pUserFileName                         # 用户文件名
#     const c_char * pDevFileName                          # 设备文件名
#     c_uint    nReserved[32]  # 预留字节
# }MV_CODEREADER_FILE_ACCESS

# # 文件存取进度
# typedef struct _MV_CODEREADER_FILE_ACCESS_PROGRESS_T
# {
#     c_longlong nCompleted                                 # 已完成的长度
#     c_longlong nTotal                                     # 总长度
#     c_uint    nReserved[8]  # 预留字节
# }MV_CODEREADER_FILE_ACCESS_PROGRESS

# # Enum类型值
# typedef struct _MV_CODEREADER_ENUMVALUE_T
# {
#     c_uint    nCurValue                                          # 当前值
#     c_uint    nSupportedNum                                      # 有效数据个数
#     c_uint    nSupportValue[MV_CODEREADER_MAX_XML_SYMBOLIC_NUM]  # 支持的枚举类型
#     c_uint    nReserved[4]  # 保留字节
# }MV_CODEREADER_ENUMVALUE

# # Int类型值
# typedef struct _MV_CODEREADER_INTVALUE_T
# {
#     c_uint    nCurValue                          # 当前值
#     c_uint    nMax                               # 最大值
#     c_uint    nMin                               # 最小值
#     c_uint    nInc                               # 增量值
#     c_uint    nReserved[4]  # 保留字节
# }MV_CODEREADER_INTVALUE

# # Int类型值
# typedef struct _MV_CODEREADER_INTVALUE_EX_T
# {
#     c_longlong    nCurValue                               # 当前值
#     c_longlong    nMax                                    # 最大值
#     c_longlong    nMin                                    # 最小值
#     c_longlong    nInc                                    # 增量值
#     c_uint    nReserved[16]  # 保留字节
# }MV_CODEREADER_INTVALUE_EX

# # Float类型值
# typedef struct _MV_CODEREADER_FLOATVALUE_T
# {
#     float           fCurValue                          # 当前值
#     float           fMax                               # 最大值
#     float           fMin                               # 最小值
#     c_uint    nReserved[4]  # 保留字节
# }MV_CODEREADER_FLOATVALUE

# # String类型值
# typedef struct _MV_CODEREADER_STRINGVALUE_T
# {
#     c_char            chCurValue[256]                    # 当前值
#     c_longlong         nMaxLength                         # 最大长度
#     c_uint    nReserved[2]  # 保留字节
# }MV_CODEREADER_STRINGVALUE


# # Int型坐标
class MV_CODEREADER_POINT_I(Structure):
    _fields_ = [
        ("x", c_int),
        ('y', c_int)
    ]
# {
#     int x                                              # x坐标
#     int y  # y坐标
# }MV_CODEREADER_POINT_I

# # Float型坐标
# typedef struct _MV_CODEREADER_POINT_F_
# {
#     float x                                            # x坐标
#     float y  # y坐标
# }MV_CODEREADER_POINT_F

# # 输出帧信息
# typedef struct _MV_CODEREADER_IMAGE_OUT_INFO_
# {
#     c_ushort      nWidth                                     # 图像宽
#     c_ushort      nHeight                                    # 图像高
#     MvCodeReaderGvspPixelType   enPixelType                        # 像素或图片格式

#     c_uint        nTriggerIndex                              # 触发序号
#     c_uint        nFrameNum                                  # 帧号
#     c_uint        nFrameLen                                  # 当前帧数据大小
#     c_uint        nTimeStampHigh                             # 时间戳高32位
#     c_uint        nTimeStampLow                              # 时间戳低32位

#     c_uint        nResultType                                # 输出消息类型

#     c_ubyte       chResult[MV_CODEREADER_MAX_RESULT_SIZE]    # 根据消息类型对应不同结构体
#     bool                bIsGetCode                                 # 是否读到条码

#     c_ubyte * pImageWaybill                              # 面单图像
#     c_uint        nImageWaybillLen                           # 面单数据大小
#     enum MV_CODEREADER_IAMGE_TYPE     enWaybillImageType           # 面单图像类型

#     c_uint        bFlaseTrigger                              # 是否误触发
#     c_uint        nFocusScore                                # 聚焦得分

#     c_uint        nChannelID                                 # 对应Stream通道序号
#     c_uint        nImageCost                                 # 帧图像在相机内部的处理耗时

#     c_uint        nReserved[6]  # 保留字节
# }MV_CODEREADER_IMAGE_OUT_INFO

# # 条码信息
# typedef struct _MV_CODEREADER_BCR_INFO_
# {
#     c_uint                nID                                        # 条码ID
#     c_char                        chCode[MV_CODEREADER_MAX_BCR_CODE_LEN]     # 字符
#     c_uint                nLen                                       # 字符长度
#     c_uint                nBarType                                   # 条码类型

#     MV_CODEREADER_POINT_I       pt[4]                                      # 条码位置

#     # 一维码：以图像x正轴为基准，顺时针0-3600度；二维码：以图像x正轴为基准，逆时针0-3600度
#     int                         nAngle                                     # 条码角度(10倍)（0~3600）
#     c_uint                nMainPackageId                             # 主包ID
#     c_uint                nSubPackageId                              # 次包ID
#     c_ushort              sAppearCount                               # 条码被识别的次数
#     c_ushort              sPPM                                       # PPM(10倍)
#     c_ushort              sAlgoCost                                  # 算法耗时
#     c_ushort              sSharpness  # 图像清晰度(10倍)
# } MV_CODEREADER_BCR_INFO

# # 条码信息列表
# typedef struct _MV_CODEREADER_RESULT_BCR_
# {
#     c_uint            nCodeNum                                   # 条码数量
#     MV_CODEREADER_BCR_INFO  stBcrInfo[MAX_CODEREADER_BCR_COUNT]        # 条码信息
#     c_uint            nReserved[4]  # 保留字节
# }MV_CODEREADER_RESULT_BCR

# # 条码质量（质量分5等[0,4], 越高等质量越好; 1D指一维码，2D指二维码）
class MV_CODEREADER_CODE_INFO(Structure):
    _fields_ = [
        # 等级
        ('nOverQuality', c_int),          # 总体质量评分（1D/2D共用）
        ('nDeCode', c_int),          # 译码评分（1D/2D共用）
        ('nSCGrade', c_int),          # Symbol Contrast对比度质量评分（1D/2D共用）
        ('nModGrade', c_int),          # modulation模块均匀性评分（1D/2D共用）
        # 2D等级
        ('nFPDGrade', c_int),                # fixed_pattern_damage评分
        ('nANGrade', c_int),                # axial_nonuniformity码轴规整性评分
        ('nGNGrade', c_int),                # grid_nonuniformity基础grid均匀性质量评分
        ('nUECGrade', c_int),                # unused_error_correction未使用纠错功能评分
        ('nPGHGrade', c_int),                # Print Growth Horizontal 打印伸缩(水平)评分
        ('nPGVGrade', c_int),                # Print Growth Veritical 打印伸缩(垂直)评分
        # 分数
        ('fSCScore', c_float),                # Symbol Contrast对比度质量分数（1D/2D共用）
        ('fModScore', c_float),                # modulation模块均匀性分数（1D/2D共用）
        # 2D分数
        ('fFPDScore', c_float),                # fixed_pattern_damage分数
        ('fAnScore', c_float),                # axial_nonuniformity码轴规整性分数
        ('fGNScore', c_float),                # grid_nonuniformity基础grid均匀性质量分数
        ('fUECScore', c_float),                # unused_error_correction未使用纠错功能分数
        ('fPGHScore', c_float),                # Print Growth Horizontal 打印伸缩(水平)分数
        ('fPGVScore', c_float),                # Print Growth Veritical 打印伸缩(垂直)分数
        ('nRMGrade', c_int),                # reflectance margin反射率余量评分
        ('fRMScore', c_float),                # reflectance margin反射率余量分数
        # 1D等级
        ('n1DEdgeGrade', c_int),               # edge determination     边缘确定度质量等级
        ('n1DMinRGrade', c_int),               # minimum reflectance    最小反射率质量等级
        ('n1DMinEGrade', c_int),               # minimum edge contrast  最小边缘对比度质量等级
        ('n1DDcdGrade', c_int),               # decodability           可译码性质量等级
        ('n1DDefGrade', c_int),               # defects                缺陷质量等级
        ('n1DQZGrade', c_int),               # quiet zone             静区质量等级
        # 1D分数
        ('f1DEdgeScore', c_float),              # edge determination     边缘确定度分数
        ('f1DMinRScore', c_float),              # minimum reflectance    最小反射率分数
        ('f1DMinEScore', c_float),              # minimum edge contrast  最小边缘对比度分数
        ('f1DDcdScore', c_float),              # decodability           可译码性分数
        ('f1DDefScore', c_float),              # defects                缺陷分数
        ('f1DQZScore', c_float),              # quiet zone             静区分数
        ('nReserved', c_int*18),  # 预留
    ]

# # 带质量信息的BCR信息

class MV_CODEREADER_BCR_INFO_EX(Structure):
    _fields_ = [
        ("nID", c_uint),  # 条码ID
        ("chCode", c_char*MV_CODEREADER_MAX_BCR_CODE_LEN),     # 字符识别长度为256
        ('nLen', c_uint),  # 字符长度
        ('nBarType', c_uint),  # 条码类型
        ('pt', MV_CODEREADER_POINT_I*4),   # 条码位置
        ('stCodeQuality', MV_CODEREADER_CODE_INFO),   # 条码质量评价
        # 一维码：以图像x正轴为基准，顺时针0-3600度；二维码：以图像x正轴为基准，逆时针0-3600度
        ('nAngle', c_int),                              # 条码角度(10倍)（0~3600）
        ('nMainPackageId', c_uint),                        # 主包ID
        ('nSubPackageId', c_uint),                        # 次包ID
        ('sAppearCount', c_ushort),                        # 条码被识别的次数
        ('sPPM', c_ushort),                        # PPM(10倍)
        ('sAlgoCost', c_ushort),                        # 算法耗时(ms)
        ('sSharpness', c_ushort),                        # 清晰度
        ('bIsGetQuality', c_bool),                              # 是否支持二维码质量评级
        ('nIDRScore', c_uint),                        # 读码评分
        ('n1DIsGetQuality', c_uint),                        # 是否支持一维码质量评级(0-不支持 1-支持)
        ('nTotalProcCost', c_uint),                        # 从触发开始到APP输出时间统计(ms)
        ('nReserved', c_uint*28),

    ]

# # 条码信息加条码质量列表
class MV_CODEREADER_RESULT_BCR_EX(Structure):
    _fields_ = [
        ("nCodeNum", c_uint),
        ("stBcrInfoEx", MV_CODEREADER_BCR_INFO_EX*MAX_CODEREADER_BCR_COUNT),
        ("nReserved", c_uint*4)
    ]
# {
#     c_uint                        nCodeNum                                   # 条码数量
#     MV_CODEREADER_BCR_INFO_EX           stBcrInfoEx[MAX_CODEREADER_BCR_COUNT]      # 条码信息
#     c_uint                        nReserved[4]  # 保留字节
# }MV_CODEREADER_RESULT_BCR_EX

# # 带质量信息且条码字符扩展的BCR信息


class MV_CODEREADER_BCR_INFO_EX2(Structure):
    _fields_ = [
        ('nID', c_uint),  # 条码ID
        ('chCode', c_char*MV_CODEREADER_MAX_BCR_CODE_LEN_EX),  # 字符可识别长度扩展至4096
        ('nLen', c_uint),  # 字符实际真实长度
        ('nBarType', c_uint),  # 条码类型
        ('pt', MV_CODEREADER_POINT_I*4),   # 条码位置
        ('stCodeQuality', MV_CODEREADER_CODE_INFO),   # 条码质量评价
        # 一维码：以图像x正轴为基准，顺时针0-3600度；二维码：以图像x正轴为基准，逆时针0-3600度
        ('nAngle', c_int),                             # 条码角度(10倍)（0~3600）
        ('nMainPackageId', c_uint),                       # 主包ID
        ('nSubPackageId', c_uint),                       # 次包ID
        ('sAppearCount', c_ushort),                       # 条码被识别的次数
        ('sPPM', c_ushort),                       # PPM(10倍)
        ('sAlgoCost', c_ushort),                       # 算法耗时(ms)
        ('sSharpness', c_ushort),                       # 清晰度
        ('bIsGetQuality', c_bool),                             # 是否支持二维码质量评级
        ('nIDRScore', c_uint),                       # 读码评分
        ('n1DIsGetQuality', c_uint),                       # 是否支持一维码质量评级(0-不支持 1-支持)
        ('nTotalProcCost', c_uint),                       # 从触发开始到APP输出时间统计(ms)
        ('nReserved', c_int*63),  # 预留

    ]

# # 条码信息字符扩展加条码质量列表

class MV_CODEREADER_RESULT_BCR_EX2(Structure):
    _fields_ = [
        ('nCodeNum', c_uint),  # 条码数量（扩展）
        ('stBcrInfoEx2', MV_CODEREADER_BCR_INFO_EX2*MAX_CODEREADER_BCR_COUNT_EX),  # 条码信息（条码字符扩展）
        ('nReserved', c_uint*8),  # 保留字节
    ]


# # 抠图面单信息
class MV_CODEREADER_WAYBILL_INFO(Structure):
    # 面单坐标信息
    _fields_ = [
        ('fCenterX', c_float),            # 中心点列坐标
        ('fCenterY', c_float),            # 中心点行坐标
        ('fWidth', c_float),            # 矩形宽度，宽度为长半轴
        ('fHeight', c_float),            # 矩形高度，高度为短半轴
        ('fAngle', c_float),            # 矩形角度
        ('fConfidence', c_float),            # 置信度

        # 面单图片
        ('pImageWaybill', POINTER(c_ubyte)),
        ('nImageLen', c_uint),

        ('nOcrRowNum', c_uint),     # 当前面单内的ocr行数
        ('nReserved', c_uint*11)
    ]


# # 面单信息列表
class MV_CODEREADER_WAYBILL_LIST(Structure):
    _fields_ = [
        ('nWaybillNum', c_uint),    # 面单数量
        ('enWaybillImageType', EnumType) ,   # 面单图像类型，可选择bmp、raw、jpg输出
        ('stWaybillInfo', MV_CODEREADER_WAYBILL_INFO*MAX_CODEREADER_WAYBILL_COUNT),    # 面单信息
        ('nOcrAllNum', c_uint),       # 所有面单内的OCR总行数 面单1(ocr)+面单2(ocr)+...
        ('nReserved', c_uint*3),      # 保留字节
    ]

# # OCR基础信息


class MV_CODEREADER_OCR_ROW_INFO(Structure):
    _fields_ = [
        ('nID', c_uint),    # OCR ID
        ('nOcrLen', c_uint),    # OCR字符实际真实长度
        ('chOcr', c_char*MV_CODEREADER_MAX_OCR_LEN),             # 识别到的OCR字符
        ('fc_charConfidence', c_float),            # 字符行整体置信度
        ('nOcrRowCenterX', c_uint),    # 单行OCR中心点列坐标
        ('nOcrRowCenterY', c_uint),    # 单行OCR中心点行坐标
        ('nOcrRowWidth', c_uint),    # 单行OCR矩形宽度，宽度为长半轴
        ('nOcrRowHeight', c_uint),    # 单行OCR矩形高度，高度为短半轴
        ('fOcrRowAngle', c_float),          # 单行OCR矩形角度
        ('fDeteConfidence', c_float),          # 单行OCR定位置信度
        ('sOcrAlgoCost', c_ushort),    # OCR算法耗时 单位ms
        ('sReserved', c_ushort),    # 预留
        ('nReserved', c_int*31),     #
    ]


# # OCR信息列表
class MV_CODEREADER_OCR_INFO_LIST(Structure):
    _fields_ = [
        ('nOCRAllNum', c_uint),      # 所有面单内的OCR总行数
        ('stOcrRowInfo', MV_CODEREADER_OCR_ROW_INFO*MAX_CODEREADER_OCR_COUNT),      # OCR行基础信息
        ('nReserved', c_int*8),    # 保留字节
    ]


# # 图像输出信息扩展(OCR信息)
# typedef struct _MV_CODEREADER_IMAGE_OUT_INFO_EX_
# {
#     c_ushort              nWidth                     # 图像宽
#     c_ushort              nHeight                    # 图像高
#     MvCodeReaderGvspPixelType   enPixelType                # 像素或图片格式

#     c_uint                nTriggerIndex              # 触发序号
#     c_uint                nFrameNum                  # 帧号
#     c_uint                nFrameLen                  # 当前帧数据大小
#     c_uint                nTimeStampHigh             # 时间戳高32位
#     c_uint                nTimeStampLow              # 时间戳低32位
#     c_uint                bFlaseTrigger              # 是否误触发
#     c_uint                nFocusScore                # 聚焦得分
#     bool                        bIsGetCode                 # 是否读到条码
#     MV_CODEREADER_RESULT_BCR * pstCodeList                 # 条码信息列表
#     MV_CODEREADER_WAYBILL_LIST * pstWaybillList             # 面单信息

#     c_uint                nEventID                   # 事件ID
#     c_uint                nChannelID                 # 对应Stream通道序号
#     c_uint                nImageCost                 # 帧图像在相机内部的处理耗时

#     union
#     {
#         MV_CODEREADER_OCR_INFO_LIST * pstOcrList     # OCR信息
#         c_longlong nAligning
#     }UnparsedOcrList

#     c_uint                nReserved[4]  # 保留字节
# }MV_CODEREADER_IMAGE_OUT_INFO_EX

class UnparsedBcrList(Union):
    _fields_ = [
        ("pstCodeListEx2", POINTER(MV_CODEREADER_RESULT_BCR_EX2)),
        ("nAligning", c_longlong)
    ]

class UnparsedOcrList(Union):
    _fields_ = [
        ("pstOcrList", POINTER(MV_CODEREADER_OCR_INFO_LIST)),
        ("nAligning", c_longlong)
    ]

# # 图像输出信息扩展(条码信息扩展，条码最大个数，条码字符长度扩展为4096)


class MV_CODEREADER_IMAGE_OUT_INFO_EX2(Structure):
    _fields_ = [
        ('nWidth',  c_ushort),    # 图像宽
        ('nHeight',  c_ushort),    # 图像高
        ('enPixelType',  EnumType),    # 像素或图片格式
        ('nTriggerIndex', c_uint),           # 触发序号
        ('nFrameNum', c_uint),           # 帧号
        ('nFrameLen', c_uint),           # 当前帧数据大小
        ('nTimeStampHigh', c_uint),           # 时间戳高32位
        ('nTimeStampLow', c_uint),           # 时间戳低32位
        ('bFlaseTrigger', c_uint),           # 是否误触发
        ('nFocusScore', c_uint),           # 聚焦得分
        ('bIsGetCode', c_bool),               # 是否读到条码
        ('pstCodeListEx', POINTER(MV_CODEREADER_RESULT_BCR_EX)  ),             # 条码信息列表
        ('pstWaybillList', POINTER(MV_CODEREADER_WAYBILL_LIST) ),             # 面单信息
        ('nEventID', c_uint),                 # 事件ID
        ('nChannelID', c_uint),                 # 对应Stream通道序号
        ('nImageCost', c_uint),                 # 帧图像在相机内部的处理耗时

        ('UnparsedBcrList', UnparsedBcrList),

        ('UnparsedOcrList', UnparsedOcrList),
        ("nReserved", c_uint*26)
    ]




# # 触发信息
# typedef struct _MV_CODEREADER_TRIGGER_INFO_DATA_
# {
#     c_uint     nTriggerIndex            # 触发序号 即同步触发号
#     c_uint     nTriggerFlag  # 触发状态 （1开始 0结束）

#     # 当前的触发状态对应的时间戳（分高、低位传输各4个字节）
#     c_uint     nTriggerTimeHigh          # 触发时间高4位
#     c_uint     nTriggerTimeLow           # 触发时间低4位

#     c_uint     nOriginalTrigger          # 原生触发号（相机自带的触发号）
#     c_ushort   nIsForceOver              # 是否强制结束（0--正常结束 1--强制结束 属于相机内部机制主动传输 上层无法设置生效）
#     c_ushort   nIsMainCam                # 主从标记 1--主相机 0--从相机
#     c_longlong          nHostTimeStamp            # 主机生成的时间戳
#     c_uint     reserved[30]  # 预留
# }MV_CODEREADER_TRIGGER_INFO_DATA

# # 触发模式
# typedef enum _MV_CODEREADER_TRIGGER_MODE_
# {
#     MV_CODEREADER_TRIGGER_MODE_OFF = 0,            # 触发关闭
#     MV_CODEREADER_TRIGGER_MODE_ON = 1,            # 触发打开
# }MV_CODEREADER_TRIGGER_MODE

class MV_CODEREADER_TRIGGER_MODE:
    MV_CODEREADER_TRIGGER_MODE_OFF = 0
    MV_CODEREADER_TRIGGER_MODE_ON = 1

# # 触发源
# typedef enum _MV_CODEREADER_TRIGGER_SOURCE_
# {
#     MV_CODEREADER_TRIGGER_SOURCE_LINE0 = 0,     # Line0
#     MV_CODEREADER_TRIGGER_SOURCE_LINE1 = 1,     # Line1
#     MV_CODEREADER_TRIGGER_SOURCE_LINE2 = 2,     # Line2
#     MV_CODEREADER_TRIGGER_SOURCE_LINE3 = 3,     # Line3
#     MV_CODEREADER_TRIGGER_SOURCE_COUNTER0 = 4,     # Line4
#     MV_CODEREADER_TRIGGER_SOURCE_SOFTWARE = 7,     # 软触发
#     MV_CODEREADER_TRIGGER_SOURCE_FrequencyConverter = 8,     # 变频器触发
# }MV_CODEREADER_TRIGGER_SOURCE
class MV_CODEREADER_TRIGGER_SOURCE:
    MV_CODEREADER_TRIGGER_SOURCE_LINE0 = 0     # Line0
    MV_CODEREADER_TRIGGER_SOURCE_LINE1 = 1     # Line1
    MV_CODEREADER_TRIGGER_SOURCE_LINE2 = 2     # Line2
    MV_CODEREADER_TRIGGER_SOURCE_LINE3 = 3     # Line3
    MV_CODEREADER_TRIGGER_SOURCE_COUNTER0 = 4     # Line4
    MV_CODEREADER_TRIGGER_SOURCE_SOFTWARE = 7     # 软触发
    MV_CODEREADER_TRIGGER_SOURCE_FrequencyConverter = 8     # 变频器触发

# # 条码类型
# typedef enum _MV_CODEREADER_CODE_TYPE_
# {
#     MV_CODEREADER_CODE_NONE = 0,                    # 无可识别条码

#     # 二维码
#     MV_CODEREADER_TDCR_DM = 1,                    # DM码
#     MV_CODEREADER_TDCR_QR = 2,                    # QR码

#     # 一维码
#     MV_CODEREADER_BCR_EAN8 = 8,                    # EAN8码
#     MV_CODEREADER_BCR_UPCE = 9,                    # UPCE码
#     MV_CODEREADER_BCR_UPCA = 12,                   # UPCA码
#     MV_CODEREADER_BCR_EAN13 = 13,                   # EAN13码
#     MV_CODEREADER_BCR_ISBN13 = 14,                   # ISBN13码
#     MV_CODEREADER_BCR_CODABAR = 20,                   # 库德巴码
#     MV_CODEREADER_BCR_ITF25 = 25,                   # 交叉25码
#     MV_CODEREADER_BCR_CODE39 = 39,                   # Code 39
#     MV_CODEREADER_BCR_CODE93 = 93,                   # Code 93
#     MV_CODEREADER_BCR_CODE128 = 128,                  # Code 128

#     MV_CODEREADER_TDCR_PDF417 = 131,                  # PDF417码

#     MV_CODEREADER_BCR_MATRIX25 = 26,                   # MATRIX25码
#     MV_CODEREADER_BCR_MSI = 30,                   # MSI码
#     MV_CODEREADER_BCR_CODE11 = 31,                   # code11
#     MV_CODEREADER_BCR_INDUSTRIAL25 = 32,                   # industrial25
#     MV_CODEREADER_BCR_CHINAPOST = 33,                   # 中国邮政码
#     MV_CODEREADER_BCR_ITF14 = 27,                   # 交叉14码

#     MV_CODEREADER_TDCR_ECC140 = 133,                  # ECC140码制

# }MV_CODEREADER_CODE_TYPE


# # 节点访问模式
# enum MV_CODEREADER_XML_AccessMode
# {
#     MV_CODEREADER_AM_NI,                                # 节点未实现
#     MV_CODEREADER_AM_NA,                                # 节点不可达
#     MV_CODEREADER_AM_WO,                                # 节点只写
#     MV_CODEREADER_AM_RO,                                # 节点只读
#     MV_CODEREADER_AM_RW,                                # 节点可读可写
#     MV_CODEREADER_AM_Undefined,                         # 节点未定义
#     MV_CODEREADER_AM_CycleDetect,                       # 节点需周期检测
# }

# # 每个节点对应的接口类型
# enum MV_CODEREADER_XML_InterfaceType
# {
#     MV_CODEREADER_IFT_IValue,                       # Value类型值
#     MV_CODEREADER_IFT_IBase,                        # Base类型值
#     MV_CODEREADER_IFT_IInteger,                     # Integer类型值
#     MV_CODEREADER_IFT_IBoolean,                     # Boolean类型值
#     MV_CODEREADER_IFT_ICommand,                     # Command类型值
#     MV_CODEREADER_IFT_IFloat,                       # Float类型值
#     MV_CODEREADER_IFT_IString,                      # String类型值
#     MV_CODEREADER_IFT_IRegister,                    # Register类型值
#     MV_CODEREADER_IFT_ICategory,                    # Category类型值
#     MV_CODEREADER_IFT_IEnumeration,                 # Enumeration类型值
#     MV_CODEREADER_IFT_IEnumEntry,                   # EnumEntry类型值
#     MV_CODEREADER_IFT_IPort,                        # Port类型值
# }

# # 输出信息类型
# enum MvCodeReaderType
# {
#     CodeReader_ResType_NULL = 0,    # 没有结果输出
#     CodeReader_ResType_BCR = 1,    # 输出信息为BCR(对应结构体 MV_CODEREADER_RESULT_BCR)
# }

# # ***********************************************************************/
# # 升级相关高级参数                                                      */
# # ***********************************************************************/

# # 设备运行状态
# enum MV_CODEREADER_PROGRAM_STATE
# {
#     MV_CODEREADER_PROGRAM_UNKNOWN,                      # 未知状态
#     MV_CODEREADER_PROGRAM_RUNNING,                      # 设备正在运行
#     MV_CODEREADER_PROGRAM_STOP                          # 设备停止运行
# }

# # 设备当前连接状态
# typedef enum _MV_CODEREADER_DEVICE_CONNECT_STATUS_
# {
#     MV_CODEREADER_DEVICE_STATUS_FREE = 1,      # 空闲状态
#     MV_CODEREADER_DEVICE_STATUS_BASE = 2,      # 第三方连接状态

# }MV_CODEREADER_DEVICE_CONNECT_STATUS

# # 明场/暗场矫正模式
# typedef enum _MV_CODEREADER_FIELD_CORRECT_MODE_
# {
#     MV_CODEREADER_DARK_FILED_CORRECT = 0,       # 暗场校验
#     MV_CODEREADER_BRIGHT_FILED_CORRECT = 1,       # 明场校验
#     MV_CODEREADER_INVAILED_FILED_CORRECT = 2,       # 无效校验

# }MV_CODEREADER_FIELD_CORRECT_MODE

# # endif # _MV_CODEREADER_PARAMS_H_ */
