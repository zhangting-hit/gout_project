<template>
  <div style="display: flex; flex-direction: column; justify-content: center;">
    <el-descriptions  :column="3" border>
      <el-descriptions-item label="病人id"  >{{ patientId }}</el-descriptions-item>
      <el-descriptions-item label="部位" >{{ location }}</el-descriptions-item>
      <el-descriptions-item label="备注">
<!--        <el-tag size="small">学校</el-tag>-->
      </el-descriptions-item>
    </el-descriptions>


    <div  class="content" style="margin-top:10px; margin-bottom:10px; display: flex; justify-content: center; width: 47vw; height: 70vh; ">
      <img :src="imagePath"   :style="{ filter: 'contrast(' + contrastValue + '%)' }">
    </div>
    <div style="display: flex; flex-direction: row; justify-content: center; margin-top: 10px">
      <el-button class="button" @click="changeImageContrast" style="border-radius: 25px; padding: 10px 20px; font-size: 16px;">对比度设置</el-button>
      <input type="range" v-model="contrastValue" min="0" max="200" @input="adjustContrast" />
    </div>
    <div style="display: flex; flex-direction: row; justify-content: center; margin-top: 10px">
          <el-button type="success" style=" margin-top: 10px; border-radius: 25px;padding: 10px 20px;font-size: 16px;" @click="save">保存修改</el-button>
          <el-button type="warning" style=" margin-top: 10px; margin-left: 20%; border-radius: 25px;padding: 10px 20px;font-size: 16px;" @click="cancelEdit">取消修改</el-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import router from "@/router";

export default {
  data() {
    return {
      imagePath: '',
      location: '',
      contrastValue: 100, // 默认对比度值
      patientId: '',
    };
  },
  created() {
    this.imagePath = this.$route.params.imagePath; // 获取路由中传递的图片路径参数
    // 获取最后一个斜杠的索引
    const lastSlashIndex = this.imagePath.lastIndexOf('/');
    // 获取最后一个下划线的索引
    const lastUnderscoreIndex = this.imagePath.lastIndexOf('_');
    // 提取最后一个斜杠后面和最后一个下划线前面的部分（即数字）
    this.patientId = this.imagePath.substring(lastSlashIndex + 1, lastUnderscoreIndex).split('_')[0];
    // 获取最后一个下划线前面的数字
    const location = this.imagePath.substring(lastUnderscoreIndex - 1, lastUnderscoreIndex);

    if(location === '0') this.location = '足背';
    else if(location === '1') this.location = '足内侧';
    else this.location = '足底';
  },
  methods:{
    changeImageContrast(){
      axios.get(`http://localhost:5000/change_image_contrast?imagePath=${this.imagePath}`) // 替换为你的后端地址
      .then(response => {
        this.imagePath = response.data.path;
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
    },
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
