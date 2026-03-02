#!/bin/bash

echo "🔧 NS-MeetAI 部署问题修复脚本"
echo "============================="
echo "修复时间: $(date)"
echo ""

# 检查是否在项目目录
if [ ! -f "package.json" ] && [ ! -d "frontend" ]; then
    echo "❌ 错误：请在NS-MeetAI项目根目录运行此脚本"
    echo "当前目录: $(pwd)"
    exit 1
fi

# 备份原始文件
echo "📁 备份原始文件..."
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -f "package.json" ]; then
    cp package.json "$BACKUP_DIR/package.json.original"
fi

if [ -d "frontend" ]; then
    cp frontend/vite.config.ts "$BACKUP_DIR/vite.config.ts.original" 2>/dev/null || true
    cp frontend/tailwind.config.js "$BACKUP_DIR/tailwind.config.js.original" 2>/dev/null || true
    cp frontend/src/styles/globals.css "$BACKUP_DIR/globals.css.original" 2>/dev/null || true
fi

echo "✅ 备份完成到: $BACKUP_DIR"

# 1. 修复根目录 package.json
echo ""
echo "1. 🔧 修复工作区配置..."
if [ -f "package.json" ]; then
    cat > package.json << 'EOF'
{
  "name": "ns-meetai",
  "version": "1.0.0",
  "private": true,
  "workspaces": ["frontend"],
  "scripts": {
    "setup": "cd frontend && npm install",
    "dev": "cd frontend && npm run dev",
    "build": "cd frontend && npm run build",
    "lint": "cd frontend && npm run lint",
    "test": "cd frontend && npm run test",
    "clean": "rm -rf frontend/node_modules frontend/dist frontend/.next",
    "fix": "cd frontend && npm audit fix"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=8.0.0"
  }
}
EOF
    echo "✅ package.json 修复完成"
else
    echo "⚠️ package.json 不存在，跳过..."
fi

# 2. 修复前端配置
if [ -d "frontend" ]; then
    echo ""
    echo "2. 🎨 进入前端目录..."
    cd frontend
    
    # 2.1 修复 vite.config.ts
    echo "  2.1 修复 Vite 配置..."
    if [ ! -f "vite.config.ts" ]; then
        echo "    创建 vite.config.ts..."
    fi
    
    cat > vite.config.ts << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    host: true,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})
EOF
    echo "    ✅ vite.config.ts 修复完成"
    
    # 2.2 安装 @types/node 如果不存在
    echo "  2.2 检查 TypeScript 类型..."
    if ! grep -q "@types/node" package.json; then
        echo "    安装 @types/node..."
        npm install --save-dev @types/node
    fi
    
    # 2.3 修复 tailwind.config.js
    echo "  2.3 修复 Tailwind CSS 配置..."
    cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class'],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      keyframes: {
        'accordion-down': {
          from: { height: 0 },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: 0 },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}
EOF
    echo "    ✅ tailwind.config.js 修复完成"
    
    # 2.4 安装 tailwindcss-animate
    echo "  2.4 安装 Tailwind 插件..."
    if ! grep -q "tailwindcss-animate" package.json; then
        npm install --save-dev tailwindcss-animate
    fi
    
    # 2.5 修复 globals.css
    echo "  2.5 修复 CSS 全局变量..."
    mkdir -p src/styles
    cat > src/styles/globals.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
EOF
    echo "    ✅ globals.css 修复完成"
    
    # 返回根目录
    cd ..
else
    echo "⚠️ frontend 目录不存在，跳过前端修复..."
fi

# 3. 创建修复后的README说明
echo ""
echo "3. 📝 更新项目状态说明..."
cat > README_FIXED.md << 'EOF'
# NS-MeetAI - 修复版本说明

## 🚨 修复的问题

### 1. 工作区配置问题
- **问题**：根目录 `package.json` 配置了不存在的 `backend` 和 `ai-processor` 工作区
- **修复**：更新为仅包含 `frontend` 工作区

### 2. Vite路径别名问题
- **问题**：`vite.config.ts` 缺少 `@` 别名配置
- **修复**：添加了完整的别名解析配置

### 3. Tailwind CSS变量问题
- **问题**：缺少CSS变量颜色声明
- **修复**：补全了所有必要的颜色变量

### 4. CSS全局变量问题
- **问题**：`globals.css` 中使用了未定义的CSS变量
- **修复**：添加了完整的CSS变量定义

## 🚀 快速开始

### 环境要求
- Node.js 18+
- npm 8+

### 安装依赖
```bash
npm run setup
```

### 启动开发服务器
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

## 📁 项目结构
```
NS-MeetAI/
├── frontend/          # 前端项目（已完成）
│   ├── src/          # 源代码
│   ├── public/       # 静态资源
│   └── package.json  # 前端依赖
├── backend/          # 后端项目（待开发）
└── ai-processor/     # AI处理器（待开发）
```

## 🔧 技术支持
如果遇到问题：
1. 清理缓存：`npm run clean`
2. 重新安装：删除 `node_modules` 和 `package-lock.json` 后运行 `npm run setup`
3. 查看日志：运行 `npm run dev` 查看详细错误信息

## 📞 联系
- GitHub Issues: 提交问题
- 文档: 查看修复说明
EOF

echo "✅ README_FIXED.md 创建完成"

# 4. 创建验证脚本
echo ""
echo "4. 🧪 创建验证脚本..."
cat > verify_fix.sh << 'EOF'
#!/bin/bash

echo "🔍 NS-MeetAI 修复验证脚本"
echo "========================"

# 检查关键文件
echo "1. 检查关键文件..."
FILES=("package.json" "frontend/vite.config.ts" "frontend/tailwind.config.js" "frontend/src/styles/globals.css")

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file 存在"
    else
        echo "  ❌ $file 不存在"
    fi
done

# 检查配置内容
echo ""
echo "2. 检查配置内容..."

# 检查 package.json 工作区
if grep -q '"workspaces": \["frontend"\]' package.json; then
    echo "  ✅ package.json 工作区配置正确"
else
    echo "  ❌ package.json 工作区配置错误"
fi

# 检查 vite.config.ts 别名
if [ -f "frontend/vite.config.ts" ] && grep -q "'@': path.resolve" frontend/vite.config.ts; then
    echo "  ✅ vite.config.ts 别名配置正确"
else
    echo "  ❌ vite.config.ts 别名配置错误"
fi

# 检查 tailwind.config.js 颜色变量
if [ -f "frontend/tailwind.config.js" ] && grep -q "border: 'hsl(var(--border))'" frontend/tailwind.config.js; then
    echo "  ✅ tailwind.config.js 颜色变量配置正确"
else
    echo "  ❌ tailwind.config.js 颜色变量配置错误"
fi

echo ""
echo "✅ 验证完成"
EOF

chmod +x verify_fix.sh
echo "✅ 验证脚本创建完成"

# 5. 总结
echo ""
echo "🎉 修复完成总结"
echo "==============="
echo "✅ 修复的文件："
echo "  1. package.json - 工作区配置"
echo "  2. frontend/vite.config.ts - Vite别名配置"
echo "  3. frontend/tailwind.config.js - Tailwind CSS变量"
echo "  4. frontend/src/styles/globals.css - CSS全局变量"
echo ""
echo "📁 创建的文件："
echo "  1. README_FIXED.md - 修复说明文档"
echo "  2. verify_fix.sh - 验证脚本"
echo "  3. $BACKUP_DIR/ - 原始文件备份"
echo ""
echo "🚀 下一步操作："
echo "  1. 安装依赖：npm run setup"
echo "  2. 启动开发：npm run dev"
echo "  3. 验证修复：./verify_fix.sh"
echo ""
echo "📝 注意："
echo "  - 原始文件已备份到 $BACKUP_DIR/"
echo "  - 如果遇到问题，可以恢复备份文件"
echo "  - 详细说明请查看 README_FIXED.md"
echo ""
echo "✅ 所有修复完成！"