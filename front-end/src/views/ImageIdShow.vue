<template>
  <div style="display: flex; flex-direction: column; justify-content: center;">
    <el-descriptions  :column="3" border>
      <el-descriptions-item label="病人id"  >{{ patientId }}</el-descriptions-item>
      <el-descriptions-item label="当前图片部位" >{{ location }}</el-descriptions-item>
      <el-descriptions-item label="图片张数">
        <el-tag size="small">{{ totalnum }}</el-tag>
      </el-descriptions-item>
    </el-descriptions>
    <div style="display: flex; flex-direction: row; justify-content: center; height: 70vh">
      <div  style="display: flex; flex-direction: column; justify-content: center; ">
        <div style="flex:1; margin-top: 10px; margin-bottom: 20px; font-weight: bold; text-align: center;">原始图像</div>
        <el-carousel  :interval="0" trigger="click" arrow="always" indicator-position="outside"  width="40vw " height="51vh"  class="custom-carousel" @change="carouselChange">
          <!-- 遍历图片路径，创建轮播项 -->
          <el-carousel-item  v-for="(path, index) in imagePaths" :key="index" style="display: flex; justify-content: center" class="custom-carousel-item">
            <div style="width: 40vw; height: 50vh;">
              <img :src="path" :style="{ filter: 'contrast(' + contrastValue + '%)',  width: '100%', height: '100%' }">
            </div>
          </el-carousel-item>
        </el-carousel>
        <div style="display: flex; flex-direction: row; justify-content: center; margin-top: 10px">
          <el-button class="button" @click="changeImageContrast">对比度设置</el-button>
          <input type="range" v-model="contrastValue" min="0" max="200" @input="adjustContrast" />
        </div>
      </div>
      <div>
        <div  class = "card-container">
          <span style="flex:1; margin-top: 10px;  font-weight: bold; text-align: center; font-size: 25px">病症</span>
          <div v-for="(value, index) in checkedResult" :key="index" class="textWithCheckmark" style="flex:1;">
            <span style="text-align: center; font-size: 20px; font-weight: bolder; color: #696969; ">{{ texts[index] }}</span>
            <span v-if="value === 1" class="checkmark" style="margin-left: 3vw">✔️</span>
          </div>
        </div>
        <div style="text-align: center; margin-left: 10%; ">
          <el-button v-if="checkedResult[2] === 1" type="primary" @click ="Segment(imagePath)" style=" margin-top: 10px; border-radius: 10px; font-size: 13px">分割痛风石</el-button>
        </div>
      </div>
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
      patientId: '', // 图片路径
      imagePaths:[],
      checkedResult: [],
      texts:[
          '点状高回声',
          '滑膜增厚',
          '痛风石形成',
          '骨质破坏',
          '关节积液',
          '双轨征'
      ],
      location: '',
      contrastValue: 100, // 默认对比度值,
      totalnum: 0,
    };
  },
  created() {
    this.patientId = this.$route.params.patientID; // 获取路由中传递的图片路径参数
    console.log(this.patientId)
    this.fetchData();
  },
  methods:{
    fetchData() {
      axios.get(`http://localhost:5000/get_imagePath_byId?patientId=${this.patientId}`) // 替换为你的后端地址
      .then(response => {
        this.imagePaths = response.data.imagePaths;
        this.totalnum = response.data.totalnum;
        // sessionStorage.setItem('currentPage', JSON.stringify(this.currentPage));
      })
      .catch(error => {
        console.error('Error fetching table data', error);
      });
    },
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
    carouselChange(index) {
      // 当轮播项切换时，更新当前图片路径
      this.imagePath = this.imagePaths[index];
      // 获取最后一个斜杠的索引
      const lastSlashIndex = this.imagePath.lastIndexOf('/');
      // 获取最后一个下划线的索引
      const lastUnderscoreIndex = this.imagePath.lastIndexOf('_');
      // 获取最后一个下划线前面的数字
      const location = this.imagePath.substring(lastUnderscoreIndex - 1, lastUnderscoreIndex);

      if(location === '0') this.location = '足背';
      else if(location === '1') this.location = '足内侧';
      else this.location = '足底';
      const lastPartOfString = this.imagePath.substring(lastUnderscoreIndex + 1); // 获取字符串中最后一个下划线后面的部分

      // 提取最后一个下划线后的数字并存储在列表中
      this.checkedResult = new Array(6).fill(0); // 创建一个长度为 6 的初始值为 0 的数组

      // 逐位检查数字 1 到 6 是否在字符串中出现
      for (let i = 1; i <= 6; i++) {
        if (lastPartOfString.includes(i.toString())) {
          this.checkedResult[i - 1] = 1; // 如果字符串中包含当前数字，则将对应位置设为 1
        }
      }
      console.log(this.imagePath)
      console.log(this.location)
      console.log(this.checkedResult); // 打印结果 [1, 1, 0, 0, 0, 0]
    },
    Segment(imagePath){
      console.log(imagePath)
      this.$router.push({ name: 'ImagePathSegment', params: { imagePath} });
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
  .custom-carousel {
    overflow: hidden;
  }
  /* 调整轮播组件指示器位置 */
  .el-carousel__indicators {
    top: -10px  !important; /* 调整为你想要的上边距 */
  }
  .custom-carousel-item {
    flex-shrink: 0;
  }
  .custom-carousel .el-carousel__container {
    width: 40vw !important;  /* 调整为你想要的宽度 */
    height: 51vh !important;  /* 调整为你想要的高度 */
  }

  .custom-carousel .el-carousel__item {
    flex-shrink: 0;
  }
  .card-container {
    width: 50vh;
    height: 50vh ;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 10%;
    margin-top:15vh;
    border-radius: 10px;
    transition: 0.3s;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  .card-container:hover {
    transform: scale(1.05);
  }
</style>
