// 尝试使用飞书API创建群聊
// 飞书创建群聊API: POST https://open.feishu.cn/open-apis/im/v1/chats

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
    
    // 需要从环境变量获取app_id和app_secret
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
      
      const body = JSON.stringify({
        name: "项目推广客户交流群",
        description: "用于项目宣传推广和客户交流的群聊",
        chat_mode: "group", // 群聊模式
        chat_type: "public", // 公开群
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

// 使用配置文件中的app_id和app_secret
const FEISHU_APP_ID = "cli_a9151bc145b85cd3";
const FEISHU_APP_SECRET = "eKEkbBeHEvTnsVV6wrlLep0gDN8Kd5v6";

// 设置环境变量供后续使用
process.env.FEISHU_APP_ID = FEISHU_APP_ID;
process.env.FEISHU_APP_SECRET = FEISHU_APP_SECRET;

createChat().then(result => {
  console.log('群聊创建完成');
  if (result.data && result.data.chat_id) {
    console.log(`群聊ID: ${result.data.chat_id}`);
    console.log(`群聊链接: https://applink.feishu.cn/client/chat/${result.data.chat_id}/open`);
  }
}).catch(error => {
  console.error('错误:', error);
});