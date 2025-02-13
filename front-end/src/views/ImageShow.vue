<template>
  <div style="display: flex; flex-direction: column; justify-content: center;">
    <el-descriptions  :column="3" border>
      <el-descriptions-item label="病人id"  >{{ patient_id }}</el-descriptions-item>
      <el-descriptions-item label="日期" >{{ studyDate }}</el-descriptions-item>
      <el-descriptions-item label="备注">
<!--        <el-tag size="small">学校</el-tag>-->
      </el-descriptions-item>
    </el-descriptions>
    <div>
      <input type="file" ref="fileInput" style="display: none" multiple @change="handleFileUpload">
      <el-button size="small" type="primary" @click="openFileInput" style="border-radius: 25px;padding: 10px 20px;font-size: 16px;">上传文件 <i class="el-icon-upload el-icon--right"></i></el-button>
    </div>
    <div style="display: flex; flex-direction: row; justify-content: center;">
<!--      <el-button class="button" @click="suoxiao">裁剪</el-button>-->
		  <el-button class="button" @click="changeImageContrast" style="border-radius: 25px;padding: 10px 20px;font-size: 16px;">对比度设置</el-button>
      <input type="range" v-model="contrastValue" min="0" max="200" @input="adjustContrast" />
    </div>

    <div  class="content" style="margin-top:10px; margin-bottom:10px; display: flex; justify-content: center; width: 47vw; height: 70vh; ">
      <img :src="imagePath"   :style="{ filter: 'contrast(' + contrastValue + '%)' }">
    </div>

    <div style="display: flex; flex-direction: row; justify-content: center;">
          <el-button type="success" style=" margin-top: 10px; border-radius: 25px;padding: 10px 20px;font-size: 16px;" @click="save" >保存修改</el-button>
          <el-button type="warning" style=" margin-top: 10px; margin-left: 20% ; border-radius: 25px;padding: 10px 20px;font-size: 16px;" @click="cancelEdit">取消修改</el-button>
    </div>
    <!-- 其他编辑操作... -->
  </div>
</template>

<script>
import axios from "axios";
import router from "@/router";

export default {
  data() {
    return {
      imagePath: '', // 图片路径
      contrastValue: 100, // 默认对比度值
      patient_id: '',
      studyDate: '',
    };
  },
  created() {
    this.imagePath = this.$route.params.imagePath; // 获取路由中传递的图片路径参数
    console.log(this.imagePath)
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

      axios.post('http://localhost:5000/dicom_upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        // 从后端获取返回的图片路径
        this.imagePath = response.data.path;
        this.patient_id = response.data.patientID;
        this.studyDate = response.data.studyDate;
      })
      .catch(error => {
        console.error('Error converting DICOM to PNG', error);
      })
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${ file.name }？`);
    },
    changeImageContrast(){
      axios.get(`http://localhost:5000/change_image_contrast?imagePath=${this.imagePath}`) // 替换为你的后端地址
      .then(response => {
        this.imagePath = response.data.path;
        // sessionStorage.setItem('changedImagePath', JSON.stringify(response.data.path));

        // // 刷新整个页面
        // window.location.reload(true); // 设置为 true 可以强制从服务器重新加载页面
      })
      .catch(error => {
        console.error('Error fetching table data', error);
      });
    },
    adjustContrast() {
      const image = document.querySelector('img');
      image.style.filter = `contrast(${this.contrastValue}%)`;
    },
    cancelEdit(){
      router.push("/home/imageBoard")
    },
    save(){
      this.$message.success("保存成功")
    }
  },
};
</script>

<style>
  .content {
		width: 100%;
		height: 100%;
		background: #ebebeb;
		margin: 0 auto;
		overflow: hidden;
		position: relative;

	}
</style>
