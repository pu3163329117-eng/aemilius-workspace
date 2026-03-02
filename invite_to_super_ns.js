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
    
    const body = JSON.stringify({
      app_id: process.env.FEISHU_APP_ID,
      app_secret: process.env.FEISHU_APP_SECRET
    });
    
    req.write(body);
    req.end();
  });
}

// 邀请用户加入群聊
async function inviteToChat(chatId, userId) {
  try {
    const token = await getAccessToken();
    console.log('获取到访问令牌');
    
    return new Promise((resolve, reject) => {
      const options = {
        hostname: 'open.feishu.cn',
        port: 443,
        path: `/open-apis/im/v1/chats/${chatId}/members`,
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
            console.log('邀请用户响应:', JSON.stringify(result, null, 2));
            resolve(result);
          } catch (e) {
            reject(e);
          }
        });
      });

      req.on('error', reject);
      
      const body = JSON.stringify({
        id_list: [userId],
        member_type: "user"
      });
      
      console.log(`邀请用户 ${userId} 加入群聊 ${chatId}...`);
      req.write(body);
      req.end();
    });
  } catch (error) {
    console.error('邀请用户失败:', error);
    throw error;
  }
}

// 检查环境变量
if (!process.env.FEISHU_APP_ID || !process.env.FEISHU_APP_SECRET) {
  console.error('错误: 需要设置FEISHU_APP_ID和FEISHU_APP_SECRET环境变量');
  process.exit(1);
}

const chatId = "oc_7604f3568c243772ad758903e150def5";
const userId = "ou_8e05327067e9ac6c1cc2228f51949cf9"; // Rain老板的用户ID

inviteToChat(chatId, userId).then(result => {
  console.log('邀请完成');
  if (result.code === 0) {
    console.log('✅ 成功邀请Rain老板加入Super NS群聊！');
    console.log(`群聊链接: https://applink.feishu.cn/client/chat/${chatId}/open`);
  } else {
    console.log('邀请可能未成功，请检查响应');
  }
}).catch(error => {
  console.error('错误:', error);
});
