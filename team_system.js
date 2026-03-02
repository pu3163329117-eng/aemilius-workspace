// Super NS 团队协作系统
// 管理多个"分身"角色的响应逻辑

const TEAM_MEMBERS = {
  'aiden': {
    name: 'Aiden',
    role: '技术专家',
    emoji: '🔧',
    expertise: ['开发', '代码', '技术', '架构', '编程', 'API', '数据库', '前端', '后端'],
    responseStyle: '严谨、技术导向、注重细节',
    signature: '🔧 Aiden | 技术专家'
  },
  'diana': {
    name: 'Diana',
    role: '文档专家', 
    emoji: '📚',
    expertise: ['文档', '整理', '记录', '知识', '规范', '流程', '会议', '笔记'],
    responseStyle: '细致、有条理、系统化',
    signature: '📚 Diana | 文档专家'
  },
  'oscar': {
    name: 'Oscar',
    role: '运营专家',
    emoji: '⏰',
    expertise: ['日程', '安排', '提醒', '任务', '进度', '时间', '跟踪', '计划'],
    responseStyle: '高效、准时、计划性强',
    signature: '⏰ Oscar | 运营专家'
  },
  'aemilius': {
    name: '文歆 (Aemilius)',
    role: '团队协调者',
    emoji: '🤝',
    expertise: ['协调', '管理', '决策', '综合', '领导'],
    responseStyle: '温暖贴心、正式专业、幽默风趣',
    signature: '🤝 文歆 | 团队协调者'
  }
};

// 根据消息内容判断应该由哪个角色响应
function determineResponder(message) {
  const lowerMsg = message.toLowerCase();
  
  // 检查是否有直接@某个角色
  if (lowerMsg.includes('@aiden') || lowerMsg.includes('技术') || lowerMsg.includes('开发') || lowerMsg.includes('代码')) {
    return 'aiden';
  }
  if (lowerMsg.includes('@diana') || lowerMsg.includes('文档') || lowerMsg.includes('整理') || lowerMsg.includes('记录')) {
    return 'diana';
  }
  if (lowerMsg.includes('@oscar') || lowerMsg.includes('日程') || lowerMsg.includes('安排') || lowerMsg.includes('提醒')) {
    return 'oscar';
  }
  
  // 根据关键词匹配
  for (const [id, member] of Object.entries(TEAM_MEMBERS)) {
    if (id === 'aemilius') continue; // 主协调者作为默认
  
    for (const keyword of member.expertise) {
      if (lowerMsg.includes(keyword.toLowerCase())) {
        return id;
      }
    }
  }
  
  // 默认由主协调者响应
  return 'aemilius';
}

// 获取角色响应格式
function getRoleResponse(roleId, content) {
  const member = TEAM_MEMBERS[roleId];
  if (!member) return content;
  
  return `${member.emoji} **${member.name}** (${member.role})\n\n${content}\n\n_${member.signature}_`;
}

// 团队协作日志
function logTeamAction(action, details) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    action,
    details,
    team: 'Super NS'
  };
  
  // 这里可以保存到日志文件
  console.log(`[团队日志] ${timestamp} - ${action}:`, details);
  return logEntry;
}

module.exports = {
  TEAM_MEMBERS,
  determineResponder,
  getRoleResponse,
  logTeamAction
};