<template>
<div>
  <div>
    <input type="file" ref="excelInput" style="display: none" multiple @change="handleExcelUpload">
    <input type="file" ref="zipInput" style="display: none" multiple @change="handleZipUpload">

    <el-button size="medium" type="primary" @click="openZipInput" style="border-radius: 25px;">选择要处理的 Zip 文件</el-button>
    <el-button size="medium" type="primary" @click="openExcelInput" style="border-radius: 25px;">选择对应 Excel 文件</el-button>
    <el-button size="medium" type="success" @click="handleFileUpload">开始分析</el-button>
  </div>
  <el-card v-loading="uploading"
    element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)"
    style="height: 800px; "
  >

    <div v-for="file in fileList" :key="file">
      <router-link :to="'/file/' + file">文件 {{ file }} 上传成功 </router-link>
    </div>

    <div v-for="patientId in patientIds" :key="patientId" class="patient-card"  >
      <router-link :to="'/patients/' + patientId" style="margin-top: 1.5vh; margin-left: 2vh" >病人 {{ patientId }}</router-link>
      <el-button style="height: 5vh; margin-top: 1.5vh;  margin-right: 10vw; border-radius: 10px; font-size: 13px" size="mini" type="primary" @click="downloadFile(patientId)">下载该病人文件</el-button>
    </div>
  </el-card>

</div>
</template>

<script>
export default {
  name: "upload",
  data() {
    return {
      fileList: [],
      patientIds: [],
      mountPatientIds: [],
      uploading: false,
      excelFile: null,
      zipFile: null
    };
  },
  mounted() {
    this.fileList = JSON.parse(sessionStorage.getItem('fileList')) || []; // 设置链接数组
    this.patientIds = JSON.parse(sessionStorage.getItem('allPatientIds')) || []; // 设置链接数组
  },
  methods: {
    openExcelInput() {
      this.$refs.excelInput.click();
    },
    openZipInput() {
      this.$refs.zipInput.click();
    },
    handleExcelUpload(event) {
      this.excelFile = event.target.files[0];
      this.$message.success("excel文件上传成功")
    },
    handleZipUpload(event) {
      this.zipFile = event.target.files[0];
      this.$message.success("zip文件上传成功")
    },
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload() {
      this.uploading = true;
      const formData = new FormData();
      if (this.excelFile) {
        formData.append('file', this.excelFile);
        console.log(formData)
      }
      if (this.zipFile) {
        formData.append('file', this.zipFile);
      }
      console.log(formData)
      fetch('http://localhost:5000/upload',  {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {

        this.patientIds = data.patientIds; // 设置病人 ID 列表，用于显示链接
        sessionStorage.setItem('allPatientIds', JSON.stringify(data.patientIds));
        sessionStorage.setItem('fileList', JSON.stringify(data.files));
        this.fileList = data.files

        console.log('文件上传成功！返回的文件列表:', data.files);
        console.log('返回的病人id列表:', data.patientIds);
        // 可以根据返回的文件列表进行其他操作，如展示列表、更新界面等
        this.uploading = false
      })
      .catch(error => {
        console.error('文件上传失败:', error);
      });

    },
    downloadFile(patientId){
      // 向后端发送 GET 请求以触发 ZIP 文件下载
      fetch(`http://localhost:5000/download/${patientId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.blob(); // 获取文件内容的二进制数据
      })
      .then(blob => {
        // 创建一个 URL 对象
        const url = window.URL.createObjectURL(new Blob([blob]));

        // 创建一个 <a> 元素并模拟点击以下载 ZIP 文件
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', patientId +'.zip');
        document.body.appendChild(link);
        link.click();

        // 释放 URL 对象
        window.URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
      });
    },
    downloadAllFile(){
      // 向后端发送 GET 请求以触发 ZIP 文件下载
      fetch(`http://localhost:5000/downloadAllFile`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.blob(); // 获取文件内容的二进制数据
      })
      .then(blob => {
        // 创建一个 URL 对象
        const url = window.URL.createObjectURL(new Blob([blob]));

        // 创建一个 <a> 元素并模拟点击以下载 ZIP 文件
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download',  'imageData.zip');
        document.body.appendChild(link);
        link.click();

        // 释放 URL 对象
        window.URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
      });
    },
  }
}
</script>

<style scoped>
  .custom-loading {
    width: 200px;
    height: 20px;
    background: repeating-linear-gradient(
      -45deg,
      deepskyblue,
      lawngreen 10px,
      #f3f3f3 10px,
      #f3f3f3 20px
    );
    animation: slide 2s linear infinite;
  }

  @keyframes slide {
    0% {
      background-position: 0 0;
    }
    100% {
      background-position: 40px 40px;
    }
  }


  .patient-card {
    display: flex;
    justify-content: space-between;
    height: 10vh;
    width: 80%;
    margin-bottom: 5px;
    border-color: #99a9bf;
    border-width: 2px;
    border-style: solid;
    font-size: 20px;
    font-weight: bold;
    border-radius: 10px;
    transition: 0.3s;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .patient-card:hover {
    transform: scale(1.02);
  }

</style>