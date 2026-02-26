#!/usr/bin/env node

/**
 * HumanWriter前端测试脚本
 * 模拟用户交互测试各个功能
 */

const http = require('http');

// 测试配置
const BASE_URL = 'http://localhost:3000';

// 测试1: 检查页面是否加载
async function testPageLoad() {
  console.log('\n📊 测试1: 页面加载\n');
  try {
    const response = await getPage(BASE_URL);
    console.log(`✅ 页面加载成功 (${response.statusCode})`);
    console.log(`   标题: ${response.body.match(/<title>(.*?)<\/title>/)?.[1] || 'N/A'}`);

    // 检查关键元素
    if (response.body.includes('HumanWriter')) {
      console.log('   ✅ 页面标题正确');
    }
    if (response.body.includes('多平台内容适配')) {
      console.log('   ✅ 副标题正确');
    }
    if (response.body.includes('AI率检测')) {
      console.log('   ✅ AI检测按钮存在');
    }
    if (response.body.includes('图片处理')) {
      console.log('   ✅ 图片处理区存在');
    }
    if (response.body.includes('选择平台')) {
      console.log('   ✅ 平台选择区存在');
    }
    if (response.body.includes('一键适配生成')) {
      console.log('   ✅ 提交按钮存在');
    }

    return true;
  } catch (error) {
    console.log('❌ 页面加载失败:', error.message);
    return false;
  }
}

// 获取页面HTML
function getPage(url) {
  return new Promise((resolve, reject) => {
    http.get(url, (res) => {
      let html = '';
      res.on('data', chunk => html += chunk);
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          body: html
        });
      });
    }).on('error', reject);
  });
}

// 测试2: 检查API端点（如果后端运行）
async function testAPIEndpoints() {
  console.log('\n📊 测试2: API端点\n');
  const API_BASE = 'http://localhost:8000';

  const endpoints = [
    '/',
    '/api/v1/platforms',
    '/api/v1/accounts'
  ];

  for (const endpoint of endpoints) {
    try {
      const response = await getPage(`${API_BASE}${endpoint}`);
      if (response.statusCode === 200) {
        console.log(`✅ GET ${endpoint} - 正常`);
      } else {
        console.log(`⚠️  GET ${endpoint} - ${response.statusCode}`);
      }
    } catch (error) {
      console.log(`❌ GET ${endpoint} - 失败 (${error.message})`);
    }
  }
}

// 测试3: 检查静态资源
async function testStaticAssets() {
  console.log('\n📊 测试3: 静态资源\n');
  const assets = [
    '/_next/static/css/app/layout.css',
    '/favicon.ico',
    '/_next/static/chunks/main-app.js'
  ];

  for (const asset of assets) {
    try {
      const response = await getPage(`${BASE_URL}${asset}`);
      if (response.statusCode === 200) {
        console.log(`✅ ${asset} - 加载成功`);
      } else {
        console.log(`⚠️  ${asset} - ${response.statusCode}`);
      }
    } catch (error) {
      console.log(`❌ ${asset} - 失败`);
    }
  }
}

// 测试4: 功能完整性检查
async function testFeatureCompleteness() {
  console.log('\n📊 测试4: 功能完整性\n');

  try {
    const response = await getPage(BASE_URL);
    const html = response.body;

    const features = {
      '多平台适配': html.includes('Twitter') && html.includes('知乎') && html.includes('公众号') && html.includes('小红书'),
      '图片上传': html.includes('上传图片'),
      'AI生成': html.includes('AI生成'),
      '图片比例选择': html.includes('16:9') && html.includes('1:1') && html.includes('3:4'),
      '复制按钮': html.includes('复制'),
      '免费试用': html.includes('免费试用7天'),
      '订阅信息': html.includes('¥9/月'),
      '响应式设计': html.includes('lg:grid-cols-2'),
      '深色模式': html.includes('dark:from-slate-900'),
    };

    console.log('\n功能检查结果：');
    for (const [feature, exists] of Object.entries(features)) {
      const status = exists ? '✅' : '❌';
      console.log(`  ${status} ${feature}`);
    }

    const completedCount = Object.values(features).filter(v => v).length;
    const totalCount = Object.keys(features).length;
    const completionRate = (completedCount / totalCount * 100).toFixed(1);

    console.log(`\n功能完成度：${completionRate}% (${completedCount}/${totalCount})`);

    return { features, completionRate };
  } catch (error) {
    console.log('❌ 功能检查失败:', error.message);
    return null;
  }
}

// 测试5: 性能测试
async function testPerformance() {
  console.log('\n📊 测试5: 性能测试\n');

  try {
    const start = Date.now();
    const response = await getPage(BASE_URL);
    const end = Date.now();

    const loadTime = end - start;
    const htmlSize = response.body.length;
    const pageSize = (htmlSize / 1024).toFixed(2);

    console.log(`页面加载时间：${loadTime}ms`);
    console.log(`页面大小：${pageSize}KB`);
    console.log(`HTTP状态码：${response.statusCode}`);

    if (loadTime < 500) {
      console.log('✅ 加载速度优秀 (<500ms)');
    } else if (loadTime < 1000) {
      console.log('⚠️  加载速度一般 (500-1000ms)');
    } else {
      console.log('❌ 加载速度慢 (>1000ms)');
    }

    if (pageSize < 50) {
      console.log('✅ 页面体积小 (<50KB)');
    } else if (pageSize < 100) {
      console.log('⚠️  页面体积适中 (50-100KB)');
    } else {
      console.log('❌ 页面体积大 (>100KB)');
    }

    return { loadTime, pageSize };
  } catch (error) {
    console.log('❌ 性能测试失败:', error.message);
    return null;
  }
}

// 测试6: 响应式设计检查
async function testResponsiveDesign() {
  console.log('\n📊 测试6: 响应式设计\n');

  try {
    const response = await getPage(BASE_URL);
    const html = response.body;

    const desktopFeatures = html.includes('lg:grid-cols-2');
    const mobileFeatures = html.includes('grid-cols-1');
    const darkMode = html.includes('dark:from-slate-900');

    console.log(`桌面端布局：${desktopFeatures ? '✅' : '❌'}`);
    console.log(`移动端布局：${mobileFeatures ? '✅' : '❌'}`);
    console.log(`深色模式：${darkMode ? '✅' : '❌'}`);

    if (desktopFeatures && mobileFeatures) {
      console.log('✅ 响应式设计完整');
    } else {
      console.log('⚠️ 响应式设计不完整');
    }

    return { desktopFeatures, mobileFeatures, darkMode };
  } catch (error) {
    console.log('❌ 响应式设计检查失败:', error.message);
    return null;
  }
}

// 生成测试报告
async function generateReport() {
  console.log('\n' + '='*60);
  console.log('HumanWriter 自动化测试报告');
  console.log('='*60);

  // 执行所有测试
  const [pageLoadResult, apiResult, staticResult, featureResult, performanceResult, responsiveResult] = await Promise.all([
    testPageLoad(),
    testAPIEndpoints(),
    testStaticAssets(),
    testFeatureCompleteness(),
    testPerformance(),
    testResponsiveDesign()
  ]);

  // 汇总
  console.log('\n' + '='*60);
  console.log('测试汇总');
  console.log('='*60);

  const results = {
    页面加载: pageLoadResult ? '✅ 通过' : '❌ 失败',
    API端点: apiResult ? '✅ 通过' : '❌ 失败',
    静态资源: staticResult ? '✅ 通过' : '❌ 失败',
    功能完整性: featureResult ? `${featureResult.completionRate}%` : '❌ 失败',
    性能: performanceResult ? `${performanceResult.loadTime}ms` : '❌ 失败',
    响应式设计: responsiveResult ? (responsiveResult.desktopFeatures && responsiveResult.mobileFeatures ? '✅ 通过' : '⚠️ 部分') : '❌ 失败'
  };

  for (const [test, result] of Object.entries(results)) {
    console.log(`${test}: ${result}`);
  }

  // 建议
  console.log('\n' + '='*60);
  console.log('测试建议');
  console.log('='*60);

  if (pageLoadResult) {
    console.log('✅ 页面加载正常，可以进行功能测试');
    console.log('💡 建议手动测试：');
    console.log('   1. 访问 http://localhost:3000');
    console.log('   2. 粘贴测试内容到输入框');
    console.log('   3. 选择平台（Twitter/知乎/公众号/小红书）');
    console.log('   4. 点击"一键适配生成"');
    console.log('   5. 查看生成的结果');
  } else {
    console.log('❌ 页面加载失败，需要检查配置');
  }

  if (!apiResult) {
    console.log('⚠️ 后端API未启动，AI检测功能无法使用');
    console.log('💡 启动后端：');
    console.log('   cd backend');
    console.log('   pip install -r requirements.txt');
    console.log('   uvicorn main:app --reload');
  }

  console.log('\n' + '='*60);
}

// 主函数
(async () => {
  try {
    await generateReport();
    process.exit(0);
  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    process.exit(1);
  }
})();
