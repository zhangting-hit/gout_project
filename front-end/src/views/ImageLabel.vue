<template>
  <div style="display: flex;flex-direction: column">
    <div style="display: flex; justify-content: center">
      <canvas ref="canvas" :width="canvasWidth" :height="canvasHeight" style="border: 1px solid #ccc;"></canvas>
    </div>
    <div style="display: flex; flex-direction: row; justify-content: center; ">
      <el-button type="warning" style=" margin-right: 10%; margin-top: 3%;" @click="cancelLabel">清除标注</el-button>
      <el-button type="success" style=" margin-left: 10%;  margin-top: 3%;" @click="saveImage">保存标注图片</el-button>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      imagePath: '', // 从路由中获取的图像路径
      canvasWidth: 1024,
      canvasHeight: 768,
      drawing: false,
      lastX: 0,
      lastY: 0
    };
  },
  created() {
    this.imagePath = this.$route.params.imagePath; // 获取路由中传递的图片路径参数-->
    console.log(this.imagePath)
  },
  methods: {
    drawImage() {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');
      const img = new Image();
      img.crossOrigin= 'anonymous';
      img.onload = () => {
        ctx.drawImage(img, 0, 0, this.canvasWidth, this.canvasHeight);
      };
      img.src = this.imagePath;
    },
    handleMouseDown(e) {
      this.drawing = true;
      this.lastX = e.offsetX;
      this.lastY = e.offsetY;
    },
    handleMouseMove(e) {
      if (this.drawing) {
        const canvas = this.$refs.canvas;
        const ctx = canvas.getContext('2d');
        ctx.beginPath();
        ctx.moveTo(this.lastX, this.lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.stroke();
        this.lastX = e.offsetX;
        this.lastY = e.offsetY;
      }
    },
    handleMouseUp() {
      this.drawing = false;
    },
    saveImage() {
      const canvas = this.$refs.canvas;
      const imageData = canvas.toDataURL('image/png'); // 获取Canvas中的图像数据（base64编码）
      const file_name =  this.imagePath
      // 将base64编码的图像数据发送到后端保存
      fetch('http://localhost:5000/save_imageLabel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageData: imageData ,file_name: file_name})
      })
      .then(res => {
        this.$message.success('图片保存成功！');
        // 处理后端响应
        console.log('图片保存成功！');
      })
      .catch(error => {
        console.error('图片保存失败：', error);
      });
    },
    cancelLabel(){
      // 清除Canvas内容
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
      this.drawImage(); // 重新绘制原始图像
    }
  },
  mounted() {
    // this.imagePath = JSON.parse(sessionStorage.getItem('imagePath')) || []; // 设置链接数组
    this.drawImage(); // 加载图像到Canvas
    const canvas = this.$refs.canvas;
    canvas.addEventListener('mousedown', this.handleMouseDown);
    canvas.addEventListener('mousemove', this.handleMouseMove);
    canvas.addEventListener('mouseup', this.handleMouseUp);
  },
  beforeDestroy() {
    const canvas = this.$refs.canvas;
    canvas.removeEventListener('mousedown', this.handleMouseDown);
    canvas.removeEventListener('mousemove', this.handleMouseMove);
    canvas.removeEventListener('mouseup', this.handleMouseUp);
  },

};
</script>

<style scoped>
/* 样式 */
</style>
