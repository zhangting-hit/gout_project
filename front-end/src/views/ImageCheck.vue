<template>
  <div>
    <div>
      <input type="file" ref="fileInput" style="display: none" multiple @change="handleFileUpload">
      <el-button size="small" type="primary" @click="openFileInput">上传文件<i class="el-icon-upload el-icon--right"></i></el-button>
    </div>

    <div style="display: flex; flex-direction: row; justify-content: center; height: 70vh">
      <div  style="display: flex; flex-direction: column; justify-content: center; ">
        <div style="flex:1; margin-top: 10px; margin-bottom: 20px; font-weight: bold; text-align: center;">原始图像</div>
        <div v-if = "imagePath !== ''" class="content" style="border-style: solid; width: 80vh; height: 50vh; border-color: grey">
          <img :src="imagePath" style="width: 100%; height: 100%; ">
        </div>
        <div v-else class="content" style="border-style: solid; width: 80vh; height: 50vh; border-color: grey">
          <p style="text-align: center; line-height: 50vh;">暂无图片</p>
        </div>
        <div style="text-align: center">
          <el-button type="primary"   @click ="Check()" style=" margin-top: 10px; ">开始检测</el-button>
        </div>
      </div>
<!--      <div>-->
<!--        <div  style="width: 50vh; height: 50vh ;display: flex; flex-direction: column; justify-content: center; margin-left: 10%; margin-top:15vh; background-color: #d3dce6;">-->
<!--          <span style="flex:1; margin-top: 10px;  font-weight: bold; text-align: center;">检测结果</span>-->
<!--          <div v-for="(value, index) in checkedResult" :key="index" class="textWithCheckmark" style="flex:1;">-->
<!--            <span style="text-align: center">{{ texts[index] }}</span>-->
<!--            <span v-if="value === 1" class="checkmark" style="margin-left: 3vw">✔️</span>-->
<!--          </div>-->

<!--        </div>-->
<!--        <div style="text-align: center; margin-left: 10%; ">-->
<!--          <el-button v-if="checkedResult[1] === 1" type="primary" @click ="Segment(imagePath)" style=" margin-top: 10px;">分割痛风石</el-button>-->
<!--        </div>-->
<!--      </div>-->
      <div class="container">
        <div class="result-box">
          <h2 class="title">检测结果</h2>
          <div v-for="(value, index) in checkedResult" :key="index" class="result-item">
            <span style="font-size: 20px;font-weight: bolder; color: dodgerblue; margin-top: 15%">{{ texts[index] }}</span>
            <span v-if="value === 1" class="checkmark">✔️</span>
          </div>
        </div>
        <div class="button-wrapper">
          <el-button v-if="checkedResult[1] === 1" type="primary" @click="Segment(imagePath)">分割痛风石</el-button>
        </div>
      </div>

    </div>
  </div>


</template>

<script>
import axios from "axios";

export default {
  name: "ImageCheck",
  data() {
    return {
      imagePath: '', // 图片路径
      checkedResult: [],
      texts:[
          '点状高回声',
          '痛风石形成',
          '骨质破坏',
          '双轨征'
      ],
    };
  },
  mounted() {
    this.imagePath = JSON.parse(sessionStorage.getItem('imagePath')) || ''; // 设置链接数组
    this.checkedResult = JSON.parse(sessionStorage.getItem('checkedResult')) || ''; // 设置链接数组
  },
  created() {
    this.imagePath = this.$route.params.imagePath; // 获取路由中传递的图片路径参数
    this.checkedResult = this.$route.params.checkedResult;
    console.log(this.imagePath)
    console.log(this.checkedResult)
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
    Check(){
      axios.get(`http://localhost:5000/check_image?imagePath=${this.imagePath}`) // 替换为你的后端地址
      .then(response => {
        this.checkedResult = response.data.res;
        console.log(this.checkedResult)
        sessionStorage.setItem('checkedResult', JSON.stringify(response.data.res));

        // 刷新整个页面
        // window.location.reload(true); // 设置为 true 可以强制从服务器重新加载页面
      })
      .catch(error => {
        console.error('Error fetching table data', error);
      });
    },
    Segment(imagePath){
      console.log(imagePath)
      this.$router.push({ name: 'ImagePathSegment', params: { imagePath} });
    },
  }
}
</script>

<style scoped>
  /*.content {*/
	/*	width: 100%;*/
	/*	height: 100%;*/
	/*	background: #ebebeb;*/
	/*	margin: 0 auto;*/
	/*	overflow: hidden;*/
	/*	position: relative;*/

	/*}*/
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
  .container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    /*height: 100vh;*/
    /*background-color: #f5f5f5;*/
  }

  .result-box {
    width: 50%;
    max-width: 600px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
  }

  .title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
  }

  .result-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }

  .checkmark {
    color: #4caf50;
  }

  .button-wrapper {
    margin-top: 20px;
    text-align: center;
  }

  .el-button {
    background-color: #4caf50;
    border-color: #4caf50;
    border-radius: 25px;
    padding: 10px 20px;
    font-size: 16px;
  }

  .el-button:hover {
    background-color: #388e3c;
    border-color: #388e3c;
  }
</style>