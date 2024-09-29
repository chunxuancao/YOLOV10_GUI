import os

import numpy as np
import rasterio
from PIL import Image
from PIL.ImageWin import Window
from contextlib import contextmanager
import os
import numpy as np
from PIL import Image
import rasterio
from rasterio.windows import Window
import shutil

def convert_yolo_to_geo( slice_info, detects):
    geo_polygons = []
    for detect in detects:
        x_min, y_min, x_max, y_max = detect['box']['x1'],detect['box']['y1'],detect['box']['x2'],detect['box']['y2']
        # 计算切片的地理坐标
        geo_x_min = slice_info["transform"][0] * x_min + slice_info["transform"][2]
        geo_y_min = slice_info["transform"][4] * y_min + slice_info["transform"][5]
        geo_x_max = slice_info["transform"][0] * x_max + slice_info["transform"][2]
        geo_y_max = slice_info["transform"][4] * y_max + slice_info["transform"][5]
        # 生成面数据（四个顶点）
        polygon = [
            (geo_x_min, geo_y_min),  # 左下角
            (geo_x_max, geo_y_min),  # 右下角
            (geo_x_max, geo_y_max),  # 右上角
            (geo_x_min, geo_y_max),  # 左上角
            (geo_x_min, geo_y_min)   # 闭合多边形
        ]
        info={
                "class": detect['class'],  # 获取类名
                "class_id": detect['class_id'],  # 类别号
                "conf": detect['conf'],  # 置信度
                "polygon": polygon
            }
        geo_polygons.append(info)
    return geo_polygons



class GetSlices:
    def __init__(self, tif_file, cache_path: str, tile_size: int = 512, stride: int = 512):
        self.tif_file = tif_file
        self.cache_path = cache_path
        self.tile_size = tile_size
        self.stride = stride
        self.slice_infos = []

    def __enter__(self):
        # 确保缓存路径存在
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

        # 打开 TIF 文件并生成切片
        with rasterio.open(self.tif_file) as src:
            width, height = src.width, src.height
            transform = src.transform
            # 计算切片的数量
            num_x_slices = (width - self.tile_size) // self.stride + 1
            num_y_slices = (height - self.tile_size) // self.stride + 1
            for x in range(num_x_slices):
                for y in range(num_y_slices):
                    col_off = x * self.stride
                    row_off = y * self.stride
                    window = Window(col_off, row_off, self.tile_size, self.tile_size)
                    # 处理边界情况
                    if col_off + self.tile_size > width:
                        window = Window(width - self.tile_size, row_off, self.tile_size, self.tile_size)
                    if row_off + self.tile_size > height:
                        window = Window(col_off, height - self.tile_size, self.tile_size, self.tile_size)

                    # 读取切片图像并处理
                    slice_transform = rasterio.windows.transform(window, transform)
                    slice_image = src.read(window=window)
                    slice_image = np.moveaxis(slice_image, 0, -1)  # 转换为 HWC 格式
                    slice_image = np.clip(slice_image, 0, 255).astype(np.uint8)
                    slice_pil_image = Image.fromarray(slice_image)
                    if slice_pil_image.mode == 'RGBA':
                        slice_pil_image = slice_pil_image.convert('RGB')
                    # 保存切片
                    slice_filename = f"{os.path.basename(self.tif_file)}_slice_{x}_{y}.jpg"
                    slice_path = os.path.join(self.cache_path, slice_filename)
                    slice_pil_image.save(slice_path)
                    slice_info = {
                        "file_name": slice_path,
                        "transform": slice_transform
                    }
                    self.slice_infos.append(slice_info)
        return self.slice_infos

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 清理缓存目录及其内容
        shutil.rmtree(self.cache_path, ignore_errors=True)



# def Get_Slices(tif_file, cache_path: str, tile_size: int = 512, stride: int = 512,band=3):
#     try:
#         # 确保缓存路径存在，用于放入切片的图像
#         if not os.path.exists(cache_path):
#             os.makedirs(cache_path)
#         # 调用库进行记录地理信息，对于图像必须要个大于512尺寸的
#         with rasterio.open(tif_file) as src:
#             profile = src.profile
#             image = src.read()
#             transform = src.transform
#             # TODO：如今对3、4波段的数据处理较多，写的逻辑上只适用于3到4波段的数据进行预测，都变成3波段的数据，如果要预测4波段的数据
#             # 存储切片数据，设置空列表
#             slice_info = []
#             # 获取图像的高宽进行计算如何切片
#             width, height = src.width, src.height
#             # 减去最终切片大小计算切片次数
#             num_x_slices = (width - tile_size) // stride + 1
#             num_y_slices = (height - tile_size) // stride + 1
#             for x in range(num_x_slices):
#                 for y in range(num_y_slices):
#                     col_off = x * stride
#                     row_off = y * stride
#                     window = Window(col_off, row_off, tile_size, tile_size)
#                     # 处理边界情况
#
#                     # 当最终点大于宽度时
#                     # 从宽度往前进行减去分片大小后进行取窗口
#                     if col_off + tile_size > width:
#                         window = Window(width - tile_size, row_off, tile_size, tile_size)
#                     # 当最终点大于高度时
#                     # 从高度往前进行减去分片大小后进行取窗口
#                     if row_off + tile_size > height:
#                         window = Window(col_off, height - tile_size, tile_size, tile_size)
#
#                     # 缩放转换
#                     transform_slice = transform * transform.scale(
#                         width / window.width,
#                         height / window.height
#                     )
#                     slice_image = src.read(window=window)
#                     slice_image = np.moveaxis(slice_image, 0, -1)
#                     slice_image = np.clip(slice_image, 0, 255).astype(np.uint8)
#                     slice_pil_image = Image.fromarray(slice_image)
#                     slice_filename = f"{tif_file.filename}_slice_{x}_{y}.jpg"
#                     slice_path = os.path.join(cache_path, slice_filename)
#                     slice_pil_image.save(slice_path)
#                     # 分片图像存放到缓存中
#                     # 存入一些必要的转换参数
#                     slice_info.append({
#                         "filename": slice_path,
#                         "bounds": {
#                             "left": window.col_off,
#                             "top": window.row_off,
#                             "right": window.col_off + window.width,
#                             "bottom": window.row_off + window.height
#                         },
#                         "transform": {
#                             "scale_x": transform_slice[0],
#                             "scale_y": transform_slice[4],
#                             "translation_x": transform_slice[2],
#                             "translation_y": transform_slice[5]
#                         }
#                     })
#         return slice_info
#     except Exception as e:
#         return None