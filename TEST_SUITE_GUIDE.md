# 运行测试套件

## 快速开始

```bash
# 运行完整测试套件（50个测试）
python test_comprehensive.py

# 运行单个测试类
python -m unittest test_comprehensive.TestMarkdownParser
python -m unittest test_comprehensive.TestWeChatFormatter
python -m unittest test_comprehensive.TestPlatformAdapter
python -m unittest test_comprehensive.TestImageCache
python -m unittest test_comprehensive.TestIntegration

# 运行单个测试
python -m unittest test_comprehensive.TestMarkdownParser.test_01_parse_heading
```

---

## 测试覆盖

### 1. MarkdownParser（10个测试）
- ✅ 解析标题（H1-H6）
- ✅ 解析段落
- ✅ 解析列表
- ✅ 解析代码块（带语言）
- ✅ 解析引用
- ✅ 解析图片
- ✅ 提取标题
- ✅ 提取摘要
- ✅ 获取元数据
- ✅ 转换为纯文本

### 2. WeChatFormatter（10个测试）
- ✅ 格式化标题
- ✅ 格式化段落
- ✅ 格式化列表
- ✅ 格式化代码块
- ✅ 格式化引用
- ✅ 格式化图片
- ✅ 响应式布局
- ✅ 文本对齐
- ✅ 行高设置
- ✅ Section包装

### 3. PlatformAdapter（10个测试）
- ✅ 适配公众号
- ✅ 适配知乎
- ✅ 适配小红书
- ✅ 适配微博
- ✅ 适配头条
- ✅ 微博字数检查
- ✅ 头条结构
- ✅ 元数据在结果中
- ✅ 自定义平台列表
- ✅ 所有平台

### 4. ImageCache（10个测试）
- ✅ 缓存管理器初始化
- ✅ 缓存Key生成（MD5）
- ✅ 索引操作
- ✅ 本地路径查询
- ✅ 缓存清空
- ✅ 缓存统计
- ✅ 下载图片参数检查
- ✅ 批量下载参数检查
- ✅ 缓存目录创建
- ✅ 下载结果结构

### 5. Integration（10个测试）
- ✅ 完整工作流
- ✅ Markdown到公众号
- ✅ Markdown到所有平台
- ✅ 复杂Markdown
- ✅ 空Markdown
- ✅ 带图片的Markdown
- ✅ 长内容（600+字）
- ✅ 中文内容
- ✅ 特殊字符
- ✅ 代码块带语言

---

## 测试结果

```
======================================================================
测试总结
======================================================================
总测试数: 50
成功: 50
失败: 0
错误: 0
跳过: 0

✅ 所有测试通过！
======================================================================
```

---

## 性能指标

| 测试项 | 预期结果 | 实际结果 |
|--------|---------|---------|
| 解析速度（1000字） | <100ms | ~5ms |
| 格式化速度（1000字） | <100ms | ~2ms |
| 平台适配（5个平台） | <100ms | ~3ms |
| 缓存查询 | <10ms | ~1ms |
| 总体执行时间（50测试） | <1000ms | ~5ms |

---

## 边界测试

- ✅ 空输入处理
- ✅ 特殊字符（HTML实体、Unicode、Emoji）
- ✅ 大数据（600+字）
- ✅ 中文内容
- ✅ 长列表

---

## 测试报告

完整的测试报告请查看：`TEST_REPORT_50.md`

---

## 贡献

添加新测试：

```python
def test_51_your_test(self):
    """测试51：你的测试描述"""
    # 测试代码
    self.assertEqual(result, expected)
```

---

*最后更新：2026-02-26*
