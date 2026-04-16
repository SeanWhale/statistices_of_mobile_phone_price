fetch('/api/export')
  .then(res => {
    if (res.status === 400) {
      alert("错误：当前没有可导出的数据！"); // 这就是边界处理
    }
  })