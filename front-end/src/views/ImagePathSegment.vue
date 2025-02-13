<template>
  <div>
    <el-descriptions  :column="3" border>
      <el-descriptions-item label="病人id"  >{{ patient_id }}</el-descriptions-item>
      <el-descriptions-item label="部位" >{{ location }}</el-descriptions-item>
      <el-descriptions-item label="备注">
<!--        <el-tag size="small">学校</el-tag>-->
      </el-descriptions-item>
    </el-descriptions>
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
            <el-button type="primary"   @click ="Segment()" style=" margin-top: 10px; border-radius: 25px;padding: 10px 20px;font-size: 16px;">开始分割</el-button>
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
            <el-button type="success" style="flex:1; margin-top: 10px; border-radius: 25px;padding: 10px 20px;font-size: 16px;"  @click="save">结果准确</el-button>
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
  name: "ImagePathSegment",
  data() {
    return {
      imagePath: '', // 图片路径
      segmentedImagePath: '',
      location: '',
      patient_id:  '',
    };
  },
  mounted() {
    this.segmentedImagePath = JSON.parse(sessionStorage.getItem('segmentedImagePath')) || ''; // 设置链接数组
  },
  created() {
    this.imagePath = this.$route.params.imagePath; // 获取路由中传递的图片路径参数
    console.log(this.imagePath)
    // 获取最后一个斜杠的索引
    const lastSlashIndex = this.imagePath.lastIndexOf('/');
    // 获取最后一个下划线的索引
    const lastUnderscoreIndex = this.imagePath.lastIndexOf('_');
    // 提取最后一个斜杠后面和最后一个下划线前面的部分（即数字）
    this.patient_id = this.imagePath.substring(lastSlashIndex + 1, lastUnderscoreIndex).split('_')[0];
    // 获取最后一个下划线前面的数字
    const location = this.imagePath.substring(lastUnderscoreIndex - 1, lastUnderscoreIndex);

    if(location === '0') this.location = '足背';
    else if(location === '1') this.location = '足内侧';
    else this.location = '足底';
  },
  methods:{
    Segment(){
      axios.get(`http://localhost:5000/seg_image?imagePath=${this.imagePath}`) // 替换为你的后端地址
      .then(response => {
        this.segmentedImagePath = response.data.path;
        sessionStorage.setItem('segmentedImagePath', JSON.stringify(response.data.path));
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
  },

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
</style>