# 测试目录

本目录包含项目的单元测试文件。

## 📋 测试文件列表

- **test_data_loader.py** - 数据加载模块测试
- **test_system_matrix.py** - 系统矩阵模块测试
- **test_reconstruction.py** - 重建算法模块测试
- **test_evaluate.py** - 评估模块测试
- **test_venv_activation.py** - 虚拟环境激活测试

## 🚀 运行测试

### 运行所有测试

```bash
# 确保虚拟环境已激活
python -m unittest discover tests
```

### 运行单个测试文件

```bash
# 运行数据加载测试
python -m unittest tests.test_data_loader

# 运行系统矩阵测试
python -m unittest tests.test_system_matrix

# 运行重建算法测试
python -m unittest tests.test_reconstruction

# 运行评估模块测试
python -m unittest tests.test_evaluate

# 运行虚拟环境测试
python tests/test_venv_activation.py
```

### 直接运行测试文件

```bash
# 直接运行测试脚本
python tests/test_data_loader.py
python tests/test_system_matrix.py
python tests/test_reconstruction.py
python tests/test_evaluate.py
python tests/test_venv_activation.py
```

## 📝 注意事项

1. **路径设置**: 测试文件已配置自动添加项目根目录到 Python 路径，可以直接导入项目模块
2. **数据文件**: 测试使用的数据文件（如 `Proj.dat`, `orbit.xlsx`）应位于项目根目录
3. **输出文件**: 测试生成的输出文件（如图片）保存在 `tests/` 目录下

## 🔍 测试覆盖

- ✅ 数据加载功能测试
- ✅ 系统矩阵计算测试
- ✅ OSEM 重建算法测试
- ✅ 评估指标计算测试
- ✅ 虚拟环境配置测试
