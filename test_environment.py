#!/usr/bin/env python3
"""
环境测试脚本
运行此脚本检查所有依赖是否正确安装
"""

import sys

def test_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python版本符合要求 (>= 3.8)")
        return True
    else:
        print("❌ Python版本过低，需要 >= 3.8")
        return False


def test_dependencies():
    """检查依赖包"""
    dependencies = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'fuzzywuzzy': 'fuzzywuzzy',
        'Levenshtein': 'python-Levenshtein',
        'plotly': 'plotly'
    }
    
    all_ok = True
    
    for module_name, package_name in dependencies.items():
        try:
            if module_name == 'Levenshtein':
                import Levenshtein
                version = Levenshtein.__version__ if hasattr(Levenshtein, '__version__') else 'unknown'
            elif module_name == 'streamlit':
                import streamlit
                version = streamlit.__version__
            elif module_name == 'pandas':
                import pandas
                version = pandas.__version__
            elif module_name == 'numpy':
                import numpy
                version = numpy.__version__
            elif module_name == 'fuzzywuzzy':
                import fuzzywuzzy
                version = fuzzywuzzy.__version__ if hasattr(fuzzywuzzy, '__version__') else 'unknown'
            elif module_name == 'plotly':
                import plotly
                version = plotly.__version__
            
            print(f"✅ {package_name:25s} 版本: {version}")
        except ImportError:
            print(f"❌ {package_name:25s} 未安装")
            all_ok = False
    
    return all_ok


def test_file_structure():
    """检查文件结构"""
    import os
    
    required_files = [
        'app.py',
        'citation_search_engine.py',
        'requirements.txt',
        '.streamlit/config.toml'
    ]
    
    all_ok = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path:30s} 存在")
        else:
            print(f"❌ {file_path:30s} 缺失")
            all_ok = False
    
    return all_ok


def test_import_core_module():
    """测试核心模块导入"""
    try:
        from citation_search_engine import (
            search_single_report,
            normalize_text,
            check_match
        )
        print("✅ 核心模块导入成功")
        
        # 简单测试
        text = "Test String  With   Spaces"
        normalized = normalize_text(text)
        if normalized == "test string with spaces":
            print("✅ 文本标准化功能正常")
        else:
            print("⚠️  文本标准化结果异常")
            
        return True
    except Exception as e:
        print(f"❌ 核心模块导入失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("UNEP FI引用查询系统 - 环境测试")
    print("=" * 60)
    print()
    
    # 测试Python版本
    print("【1/4】检查Python版本...")
    py_ok = test_python_version()
    print()
    
    # 测试依赖包
    print("【2/4】检查依赖包...")
    deps_ok = test_dependencies()
    print()
    
    # 测试文件结构
    print("【3/4】检查文件结构...")
    files_ok = test_file_structure()
    print()
    
    # 测试核心模块
    print("【4/4】测试核心模块...")
    module_ok = test_import_core_module()
    print()
    
    # 总结
    print("=" * 60)
    print("测试结果总结")
    print("=" * 60)
    
    all_passed = py_ok and deps_ok and files_ok and module_ok
    
    if all_passed:
        print("🎉 所有测试通过！环境配置正确。")
        print()
        print("下一步：")
        print("  1. 准备数据文件（参考 DATA_FORMAT.md）")
        print("  2. 运行应用: streamlit run app.py")
        print("  3. 在浏览器中访问 http://localhost:8501")
        print()
        return 0
    else:
        print("⚠️  部分测试失败，请检查上述错误信息。")
        print()
        print("建议操作：")
        if not deps_ok:
            print("  1. 重新安装依赖: pip install -r requirements.txt")
        if not files_ok:
            print("  2. 确保所有文件都在正确位置")
        if not module_ok:
            print("  3. 检查代码文件是否完整")
        print()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
