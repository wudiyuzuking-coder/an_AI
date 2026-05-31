Page({
  data: {
    inputText: '',
    chatList: [
      { role: 'assistant', content: '你好！我是校园食堂 AI 助手小安，今天有什么想了解的？' }
    ],
    isLoading: false
  },

  onInputChange(e) {
    this.setData({ inputText: e.detail.value });
  },

  sendQuery() {
    const query = this.data.inputText.trim();
    if (!query || this.data.isLoading) return;

    this.setData({
      chatList: [...this.data.chatList, { role: 'user', content: query }],
      inputText: '',
      isLoading: true
    });

    wx.request({
      url: 'http://172.20.10.7:8080/api/chat',
      method: 'POST',
      data: { question: query },
      header: { 'content-type': 'application/json' },
      success: (res) => {
        if (res.statusCode === 200 && res.data && res.data.answer) {
          this.setData({
            chatList: [...this.data.chatList, { role: 'assistant', content: res.data.answer }]
          });
        } else {
          this.showErrorToast('服务器响应异常');
        }
      },
      fail: (err) => {
        console.error("请求失败：", err);
        this.showErrorToast('无法连接到后端服务');
      },
      complete: () => {
        this.setData({ isLoading: false });
        this.scrollToBottom();
      }
    });
  },

  showErrorToast(msg) {
    wx.showToast({ title: msg, icon: 'none', duration: 2000 });
  },

  scrollToBottom() {
    setTimeout(() => {
      this.setData({
        scrollTop: 999999
      });
    }, 100);
  }
});
