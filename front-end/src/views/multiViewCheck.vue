<template>
  <div>
    <div>
      <div style="display: flex; ">
        <!-- File Inputs -->
        <input type="file" ref="fileInput1" style="display: none" @change="handleFileUpload(1, $event)">
        <input type="file" ref="fileInput2" style="display: none" @change="handleFileUpload(2, $event)">
        <input type="file" ref="fileInput3" style="display: none" @change="handleFileUpload(3, $event)">

        <!-- Upload Buttons -->
        <el-button size="small" type="primary" @click="openFileInput(1)">上传第一张图像<i class="el-icon-upload el-icon--right"></i></el-button>
        <el-button size="small" type="primary" @click="openFileInput(2)">上传第二张图像<i class="el-icon-upload el-icon--right"></i></el-button>
        <el-button size="small" type="primary" @click="openFileInput(3)">上传第三张图像<i class="el-icon-upload el-icon--right"></i></el-button>
        <el-button type="success" @click="Check()" >开始检测</el-button>
      </div>
    </div>

    <!-- Display Image Containers -->
    <div style="display: flex; justify-content: space-around; height: 70vh; margin-top: 20px;">
      <div v-for="(image, index) in images" :key="index" style="display: flex; flex-direction: column; text-align: center;">
        <div style="margin-bottom: 10px; font-weight: bold;">图像 {{ index + 1 }}</div>
        <div class="content" style="border: solid 1px grey; width: 25vw; height: 40vh;">
          <img v-if="image.path" :src="image.path" style="width: 100%; height: 100%;">
          <p v-else style="line-height: 40vh;">暂无图片</p>
        </div>
      </div>
    </div>

    <!-- Detection Results -->
    <div class="container" >
      <div>
        <h2 class="title">检测结果</h2>
      </div>
      <div class="result-box">

        <div v-for="(value, index) in texts" :key="index" class="result-item">
          <span style="font-size: 20px; font-weight: bold; color: dodgerblue;">{{ texts[index] }}</span>
          <span v-if="checkedResult[index] === 1" class="checkmark">✔️</span>
          <span v-else class="checkmark" style="color: red;">❌</span>
        </div>
      </div>
    </div>

  </div>
</template>


<script>
import axios from "axios";

export default {
  name: "multiViewCheck",
  data() {
    return {
      images: [
        { path: "", result: [] }, // Image 1
        { path: "", result: [] }, // Image 2
        { path: "", result: [] }, // Image 3
      ],
      checkedResult: [], // Detection results
      texts: ["点状高回声", "痛风石形成", "骨质破坏", "双轨征", "综合结果"], // Result descriptions
    };
  },
  // created() {
  //   // Initialize images and results if available
  //   const imagePath = this.$route.params.imagePath || [];
  //   this.images = imagePath.map((path) => ({ path, result: [] }));
  //   this.checkedResult = this.$route.params.checkedResult || [];
  // },
  methods: {
    openFileInput(imageIndex) {
      const fileInput = this.$refs[`fileInput${imageIndex}`];
      if (fileInput) {
        fileInput.click();
      } else {
        console.error(`File input ref 'fileInput${imageIndex}' not found.`);
      }
    },
    handleFileUpload(imageIndex, event) {
      const file = event.target.files[0];
      if (!file) {
        console.error("No file selected.");
        return;
      }
      console.log(`Uploading image ${imageIndex}:`, file);
      console.log("length", this.images.length);
      if (imageIndex < 1 || imageIndex > this.images.length) {
        console.error("Invalid image index:", imageIndex);
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      axios
        .post("http://localhost:5000/image_upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((response) => {
          const uploadedImage = this.images[imageIndex - 1];
          if (uploadedImage) {
            uploadedImage.path = response.data.path;
            this.$set(this.images, imageIndex - 1, { ...uploadedImage });
            console.log(`Image ${imageIndex} uploaded:`, uploadedImage);
          } else {
            console.error(`Image at index ${imageIndex - 1} is undefined.`);
          }
        })
        .catch((error) => {
          console.error("Error uploading image:", error);
        });
    },
    Check() {
      const imagePaths = this.images.map((image) => image.path);
      console.log("Checking images:", imagePaths);
      axios
        .post("http://localhost:5000/multi_view_check_image", { imagePaths })
        .then((response) => {
          this.checkedResult = response.data.res || [];
        })
        .catch((error) => {
          console.error("Error checking images:", error);
        });
    },
  },
};
</script>


<style scoped>
.container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-top: -13%;
}

.result-box {
  width: 50%;
  max-width: 600px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-right: 19%;
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  margin-right: 100px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.checkmark {
  font-size: 20px;
}
</style>

