<template>
  <div>
    <el-row>
      <el-card>
        <div style="display: flex;">
          <h3 slot="header" style="display: flex">Model </h3>
          <el-button type="primary" @click = "handleAdd" style = "margin-left: 70%; margin-bottom: 1%">添加模型<i class="el-icon-add-location"></i></el-button>
        </div>

        <!-- 数据展示的组件 -->
        <div class="model-info">
          <!-- 这里展示从后端获取的模型信息 -->
          <el-card v-for="model in tableData" :key="model.id">
            <h4>{{ model.name }}</h4>
            <div>
              <div>
                上传时间：<el-tag size="small">{{ model.upload_time }}</el-tag>
                上传者：<el-tag size="small">{{ model.upload_user }}</el-tag>
              </div>
              <span>描述:<el-tag size="small" style="font-size: 15px">{{ model.description }}</el-tag></span>
<!--              <span>参数量(Params (M)):<el-tag size="small">{{ model.params }}</el-tag></span>-->
<!--              FPS:<el-tag size="small">{{ model.FPS }}</el-tag>-->
<!--              IoU:<el-tag size="small">{{ model.IOU }}</el-tag>-->
<!--              F1-value:<el-tag size="small">{{ model.F1_value }}</el-tag>-->
            </div>
            <!-- Assuming the path column in the database contains the path to the pth file -->
            <a :href="model.path" download>下载pth文件</a>
          </el-card>
        </div>
      </el-card>
    </el-row>
    <el-dialog title="模型信息" :visible.sync="dialogFormVisible" width="30%">
      <input type="file" ref="fileInput" style="display: none" multiple @change="handleUpload">
      <el-button size="small" type="primary" @click="openFileInput">上传模型文件<i class="el-icon-upload el-icon--right"></i></el-button>
      <el-form label-width="120px" size="small">
        <el-form-item label="名称" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述" :label-width="formLabelWidth">
          <el-input v-model="form.description" autocomplete="off"></el-input>
        </el-form-item>
<!--        <el-form-item label="参数量" :label-width="formLabelWidth">-->
<!--          <el-input v-model="form.params" autocomplete="off"></el-input>-->
<!--        </el-form-item>-->
<!--        <el-form-item label="FPS" :label-width="formLabelWidth">-->
<!--          <el-input v-model="form.FPS" autocomplete="off"></el-input>-->
<!--        </el-form-item>-->
<!--        <el-form-item label="IOU" :label-width="formLabelWidth">-->
<!--          <el-input v-model="form.IOU" autocomplete="off"></el-input>-->
<!--        </el-form-item>-->
<!--        <el-form-item label="F1_value" :label-width="formLabelWidth">-->
<!--          <el-input v-model="form.F1_value" autocomplete="off"></el-input>-->
<!--        </el-form-item>-->
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import axios from "axios";

export default {
  name: "modelShow",
  data() {
    return {
      imagePath: '', // 图片路径
      segmentedImagePath: [],
      dialogFormVisible: false,
      form:{},
      formLabelWidth:"200",
      tableData:[],
      user: sessionStorage.getItem("user") ? JSON.parse(sessionStorage.getItem("user")): {},
    };
  },
  mounted() {
    this.fetchTableData();
  },
  methods:{
    fetchTableData() {
      axios.get(`http://localhost:5000/get_model_data`) // 替换为你的后端地址
      .then(response => {
        this.tableData = response.data.result;
        console.log(this.tableData)
        // sessionStorage.setItem('currentPage', JSON.stringify(this.currentPage));
      })
      .catch(error => {
        console.error('Error fetching table data', error);
      });
    },
    handleAdd(){
      this.dialogFormVisible=true;
      this.form={}
      this.form.upload_user = this.user.username
    },
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleUpload(event){
      const formData = new FormData();
      formData.append('file', event.target.files[0]);
      console.log(formData)
      fetch('http://localhost:5000/upload_model',  {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        this.form.path = data.path;
      })
      .catch(error => {
        console.error('文件上传失败:', error);
      });

    },
    save(){
      console.log(this.form)
      axios.post('http://localhost:5000/insert_model_data', this.form)
      .then(response => {
        if(response.data.code === '200'){
          this.$message.success("添加成功")
          this.dialogFormVisible=false
          this.fetchTableData()
        }else{
          this.$message.error("添加失败")
        }
      })
    },
  }
}
</script>

<style scoped>
/* 自定义样式 */
.model-info {
  /* 样式 */
}

.image-preview {
  /* 样式 */
}
</style>
