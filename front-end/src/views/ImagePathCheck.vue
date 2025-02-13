<template>
  <div>
    <el-descriptions  :column="3" border>
      <el-descriptions-item label="病人id"  >{{ patient_id }}</el-descriptions-item>
      <el-descriptions-item label="部位" >{{ location }}</el-descriptions-item>
      <el-descriptions-item label="备注">
<!--        <el-tag size="small">学校</el-tag>-->
      </el-descriptions-item>
    </el-descriptions>

    <div style="display: flex; flex-direction: row; justify-content: center; height: 70vh">
      <div  style="display: flex; flex-direction: column; justify-content: center; ">
        <div style="flex:1; margin-top: 10px; margin-bottom: 20px; font-weight: bold; text-align: center;">原始图像</div>
        <div v-if = "imagePath !== ''" style="border-style: solid; width: 90vh; height: 60vh; border-color: grey">
          <img :src="imagePath" :style="{ filter: 'contrast(' + contrastValue + '%)' }" style="height: 100%; width: 100%" >
        </div>
        <div v-else style="border-style: solid; width: 90vh; height: 60vh; border-color: grey">
          <p style="text-align: center; line-height: 50vh;"></p>
        </div>
        <div style="display: flex; flex-direction: row; justify-content: center; margin-top: 10px">
          <el-button class="button" @click="changeImageContrast">对比度设置</el-button>
          <input type="range" v-model="contrastValue" min="0" max="200" @input="adjustContrast" />
        </div>
      </div>
      <div>
        <div  class="card-container">
          <span style="flex:1; margin-top: 10px;  font-weight: bold; text-align: center; font-size: 25px">病症</span>
          <div v-for="(value, index) in checkedResult" :key="index" class="textWithCheckmark" style="flex:1;">
            <span style="text-align: center; font-size: 20px; font-weight: bolder; color: #696969; ">{{ texts[index] }}</span>
            <span v-if="value === 1" class="checkmark" style="margin-left: 3vw">✔️</span>
          </div>
        </div>
        <div style="text-align: center; margin-left: 10%; ">
          <el-button v-if="checkedResult[2] === 1" type="primary" @click ="Segment(imagePath)" style=" margin-top: 10px;">分割痛风石</el-button>
        </div>
      </div>

    </div>

  </div>


</template>

<script>
import axios from "axios";

export default {
  name: "ImagePathCheck",
  data() {
    return {
      imagePath: '', // 图片路径
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
      patient_id:  '',
      contrastValue: 100 // 默认对比度值
    };
  },
  created() {
    this.imagePath = this.$route.params.imagePath; // 获取路由中传递的图片路径参数
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
    console.log(this.patient_id)
    console.log(this.checkedResult); // 打印结果 [1, 1, 0, 0, 0, 0]

  },
  methods:{
    Segment(imagePath){
      console.log(imagePath)
      this.$router.push({ name: 'ImagePathSegment', params: { imagePath} });
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
  },
  adjustContrast() {
    const image = document.querySelector('img');
    image.style.filter = `contrast(${this.contrastValue}%)`;
  }
}
</script>

<style scoped>
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