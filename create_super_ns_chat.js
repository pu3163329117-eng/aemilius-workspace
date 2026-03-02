// 创建Super NS群聊
const https = require('https');

// 获取飞书访问令牌
function getAccessToken() {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'open.feishu.cn',
      port: 443,
      path: '/open-apis/auth/v3/tenant_access_token/internal',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.code === 0) {
            resolve(result.tenant_access_token);
          } else {
            reject(new Error(`获取token失败: ${JSON.stringify(result)}`));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    
    // 从环境变量获取app_id和app_secret
    const body = JSON.stringify({
      app_id: process.env.FEISHU_APP_ID,
      app_secret: process.env.FEISHU_APP_SECRET
    });
    
    req.write(body);
    req.end();
  });
}

// 创建群聊
async function createChat() {
  try {
    const token = await getAccessToken();
    console.log('获取到访问令牌');
    
    return new Promise((resolve, reject) => {
      const options = {
        hostname: 'open.feishu.cn',
        port: 443,
        path: '/open-apis/im/v1/chats',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          try {
            const result = JSON.parse(data);
            console.log('创建群聊响应:', JSON.stringify(result, null, 2));
            resolve(result);
          } catch (e) {
            reject(e);
          }
        });
      });

      req.on('error', reject);
      
      // 创建Super NS群聊 - 私有群，需要邀请才能加入
      const body = JSON.stringify({
        name: "Super NS",
        description: "AI助手团队协作群 - 为Rain老板创建的专属团队",
        chat_mode: "group", // 群聊模式
        chat_type: "private", // 私有群，需要邀请
        join_message_visibility: "all_members", // 所有成员可见
        leave_message_visibility: "all_members", // 所有成员可见
        membership_approval: "no_approval_required" // 无需审批
      });
      
      console.log('发送创建群聊请求...');
      req.write(body);
      req.end();
    });
  } catch (error) {
    console.error('创建群聊失败:', error);
    throw error;
  }
}

// 检查环境变量
if (!process.env.FEISHU_APP_ID || !process.env.FEISHU_APP_SECRET) {
  console.error('错误: 需要设置FEISHU_APP_ID和FEISHU_APP_SECRET环境变量');
  console.log('请运行:');
  console.log('export FEISHU_APP_ID="your_app_id"');
  console.log('export FEISHU_APP_SECRET="your_app_secret"');
  console.log('node create_super_ns_chat.js');
  process.exit(1);
}

createChat().then(result => {
  console.log('群聊创建完成');
  if (result.data && result.data.chat_id) {
    console.log(`群聊ID: ${result.data.chat_id}`);
    console.log(`群聊链接: https://applink.feishu.cn/client/chat/${result.data.chat_id}/open`);
    
    // 保存群聊信息到文件
    const fs = require('fs');
    const chatInfo = {
      chat_id: result.data.chat_id,
      name: "Super NS",
      created_at: new Date().toISOString()
    };
    fs.writeFileSync('/root/.openclaw/workspace/super_ns_chat.json', JSON.stringify(chatInfo, null, 2));
    console.log('群聊信息已保存到 super_ns_chat.json');
  }
}).catch(error => {
  console.error('错误:', error);
});