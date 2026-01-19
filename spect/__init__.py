"""
SPECT 图像重建核心模块包

本包包含 SPECT 图像重建的核心功能模块：
- data_loader: 数据加载模块
- system_matrix: 系统矩阵计算模块
- reconstruction: OSEM 重建算法模块
- evaluate: 评估和滤波模块
"""

from .data_loader import SPECTDataLoader
from .system_matrix import SystemMatrix
from .reconstruction import OSEMReconstructor
from .evaluate import Evaluator

__all__ = [
    'SPECTDataLoader',
    'SystemMatrix',
    'OSEMReconstructor',
    'Evaluator',
]

__version__ = '1.0.0'
