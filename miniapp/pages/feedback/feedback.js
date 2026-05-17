Page({
  data: {
    feedbackContent: '',
    isSubmitting: false,
    resultMessage: '',
    categoryTag: ''
  },

  submitFeedback() {
    const content = this.data.feedbackContent.trim();
    if (!content) {
      wx.showToast({ title: '请输入反馈内容', icon: 'none' });
      return;
    }

    this.setData({ isSubmitting: true, resultMessage: '' });

    wx.request({
      url: 'http://127.0.0.1:8080/api/feedback',
      method: 'POST',
      data: { content: content },
      header: { 'content-type': 'application/json' },
      success: (res) => {
        if (res.statusCode === 200 && res.data.status === 'success') {
          this.setData({
            resultMessage: res.data.message,
            categoryTag: res.data.category,
            feedbackContent: ''
          });
        } else {
          wx.showToast({ title: '提交失败，请重试', icon: 'none' });
        }
      },
      fail: () => {
        wx.showToast({ title: '网络连接失败', icon: 'none' });
      },
      complete: () => {
        this.setData({ isSubmitting: false });
      }
    });
  }
});
