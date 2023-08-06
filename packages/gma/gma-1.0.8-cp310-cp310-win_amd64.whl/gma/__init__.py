# -*- coding: utf-8 -*-

try:
    from gma import index, math, osf, rasp, vesp, smc, raa, config
    from gma.algorithm.dataio import Open
    from importlib.metadata import version
    
except ModuleNotFoundError as F:
    Package = str(F).split()[-1].replace("'",'').split('.')[0]
    if Package == 'osgeo':
        MESS = "缺少 gdal 库！gdal 的 whl 包可从：https://www.lfd.uci.edu/~gohlke/pythonlibs/ 下载。"
    else:
        MESS = f"缺少 {Package} 库，请在终端使用 'pip install {Package}' 安装！"
    raise ModuleNotFoundError(MESS) from None
except ImportError as I:
    Module = str(I).split()
    if 'from' in Module:
        LOC = Module.index('from')
        raise ImportError(f'无法从 {Module[LOC+1]} 中导入 {Module[LOC-1]}！') from None
    else:
        raise ImportError('父包未知，无法进行相对导入！') from None

try:
    __version__ = version(__name__)
except: 
    __version__ = "unknown"
finally:
    del version
    
try:
    __gdalversion__ = rasp._rasp.gdal.__version__
except:
     raise ImportError('不支持当前安装的 gdal ，请更新 gdal！')    
if __gdalversion__ < '3.3.1':
    raise ImportError(f'gdal 版本过低，当前版本 {__gdalversion__}, 最低版本 3.3.1，请更新 gdal！')


