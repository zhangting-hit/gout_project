<template>
  <div>
    <div>
      <input type="file" ref="fileInput" style="display: none" multiple @change="handleFileUpload">
      <el-button size="small" type="primary" @click="openFileInput" style=" border-radius: 25px;padding: 10px 20px;font-size: 16px;">上传文件<i class="el-icon-upload el-icon--right"></i></el-button>
    </div>
    <div>
      <div style="display: flex; flex-direction: row; justify-content: center; ">
        <div  style="display: flex; flex-direction: column; justify-content: center; ">
          <div style="flex:1; margin-top: 10px; margin-bottom: 20px; font-weight: bold; text-align: center;">原始图像</div>
          <div v-if="imagePath !== ''" style="border-style: solid; width: 80vh; height: 50vh; border-color: grey">
            <img :src="imagePath" style="width: 100%; height: 100%; ">
          </div>
          <div v-else style="border-style: solid; width: 80vh; height: 50vh; border-color: grey">
            <!-- 默认的占位图或提示 -->
            <p style="text-align: center; line-height: 50vh;">暂无图片</p>
          </div>
          <div style="text-align: center">
            <el-button type="primary"   @click ="Segment" style=" margin-top: 10px; border-radius: 25px;padding: 10px 20px;font-size: 16px;">开始检测</el-button>
          </div>
        </div>
        <div  style="display: flex; flex-direction: column; justify-content: center; margin-left: 10px ;">
          <div style="flex:1; margin-top: 10px; margin-bottom: 20px; font-weight: bold; text-align: center;">检测结果</div>
          <div v-if="segmentedImagePath !== ''" style="border-style: solid; width: 80vh; height: 50vh; border-color: grey">
            <img :src="segmentedImagePath + '?timestamp=' + Date.now()" style="width: 100%; height: 100%;">
          </div>
          <div v-else style="border-style: solid; width: 80vh; height: 50vh; border-color: grey">
            <!-- 默认的占位图或提示 -->
            <p style="text-align: center; line-height: 50vh;"></p>
          </div>

          <div style="display: flex; flex-direction: row; justify-content: center;">
            <el-button type="success" style="flex:1; margin-top: 10px;  border-radius: 25px;padding: 10px 20px;font-size: 16px;" @click="save">结果准确</el-button>
            <el-button type="warning" style="flex:1; margin-top: 10px; border-radius: 25px;padding: 10px 20px;font-size: 16px;" @click="Correction(imagePath)">结果矫正</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ImageDetect",
  data() {
    return {
      imagePath: '', // 图片路径
      segmentedImagePath: ''
    };
  },
  mounted() {
    this.imagePath = JSON.parse(sessionStorage.getItem('imagePath')) || ''; // 设置链接数组
    this.segmentedImagePath = JSON.parse(sessionStorage.getItem('segmentedImagePath')) || ''; // 设置链接数组
  },
  created() {
    this.imagePath = this.$route.params.imagePath; // 获取路由中传递的图片路径参数
    this.segmentedImagePath = this.$route.params.segmentedImagePath;
    console.log(this.imagePath)
    console.log(this.segmentedImagePath)
  },
  methods:{
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const files = event.target.files;
      const formData = new FormData();

      for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
      }

      axios.post('http://localhost:5000/image_upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        // 从后端获取返回的图片路径
        this.imagePath = response.data.path;
        sessionStorage.setItem('imagePath', JSON.stringify(response.data.path));
      })
      .catch(error => {
        console.error('Error converting DICOM to PNG', error);
      })
    },
    Segment(){
      axios.get(`http://localhost:5000/detect_image?imagePath=${this.imagePath}`) // 替换为你的后端地址
      .then(response => {
        this.segmentedImagePath = response.data.path;
        sessionStorage.setItem('segmentedImagePath', JSON.stringify(response.data.path));

        // 刷新整个页面
        window.location.reload(true); // 设置为 true 可以强制从服务器重新加载页面
      })
      .catch(error => {
        console.error('Error fetching table data', error);
      });
    },
    Correction(imagePath){
      this.$router.push({ name: 'ImageLabel', params: { imagePath} })
    },
    save(){
      axios.get(`http://localhost:5000/save_seg_image?segmentedImagePath=${this.segmentedImagePath}`) // 替换为你的后端地址
      .then(response => {
        if(response.data.status === 'success'){
          this.$message.success("保存成功")
        }
      })
      .catch(error => {
        console.error('Error', error);
      });
    }
  }
}
</script>

<style scoped>
  .my-label {
    background: #E1F3D8;
  }

  .my-content {
    background: #FDE2E2;
  }

  .image-row {
    display: flex; /* 使用 Flexbox 布局 */
    height: 50vh; /* 占满屏幕高度 */
    overflow: hidden; /* 隐藏溢出部分 */
  }

  .image {
    flex: 1; /* 图片平分父容器宽度 */
    height: auto; /* 自适应高度 */
    max-width: 50%; /* 图片最大宽度为100% */
  }
  /*.el-button {*/
  /*  background-color: #4caf50;*/
  /*  border-color: #4caf50;*/
  /*  border-radius: 25px;*/
  /*  padding: 10px 20px;*/
  /*  font-size: 16px;*/
  /*}*/

  .el-button:hover {
    background-color: #388e3c;
    border-color: #388e3c;
  }
</style>
