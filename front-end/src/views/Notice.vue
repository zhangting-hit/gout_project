<template>
  <div class="notice-board" >
    <h1>公告栏</h1>
    <div style="padding:10px 0">
      <el-input style="width: 200px" placeholder="请输入名称" suffix-icon="el-icon-search" v-model="name"></el-input>
      <el-button class="ml-5"  type="primary" @click="getNotices">搜索</el-button>
      <el-button type="warning" @click="reset">重置</el-button>
      <el-button type="success" @click = "handleAdd" >发布公告<i class="el-icon-add-location"></i></el-button>
    </div>

    <div v-if="tableData.length > 0" class="notice-list">
      <h2>公告列表：</h2>
      <ul>
        <li v-for="notice in tableData" :key="notice.id" class="notice-item">
          <p class="content">{{ notice.content }}</p>
          <p class="info">发布人：{{ notice.author }}</p>
          <p class="info">发布时间：{{ notice.created_at }}</p>
        </li>
      </ul>
    </div>
    <div class="block">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 10, 20, 30, 40]"
        :page-size="pageSize"
        :layout="'total, sizes, prev, pager, next, jumper'"
        :total="total">
      </el-pagination>
    </div>
    <el-dialog title="编辑公告" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="120px" size="small">
        <el-form-item label="内容" :label-width="formLabelWidth">
          <el-input v-model="form.content" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="发布人" :label-width="formLabelWidth">
          <el-input v-model="form.author" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="发布时间" :label-width="formLabelWidth">
          <el-input v-model="form.created_at" autocomplete="off" aria-required="true"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="createNotice">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Notice",
  data() {
    return {
      notices: [],
      tableData: [],
      total: 0,
      currentPage: 1,
      pageSize :15,
      name: "",
      form:{},
      dialogFormVisible: false,
      multipleSelection:[],
      headerBg:'headerBg',
      formLabelWidth:"200",
      options:[],
      user: sessionStorage.getItem("user") ? JSON.parse(sessionStorage.getItem("user")): {},
    };
  },
  methods: {
    getNotices() {
      console.log(this.currentPage);
      axios.get(`http://localhost:5000/get_notice_data?page=${this.currentPage}&pageSize=${this.pageSize}&name=${this.name}`) // 替换为你的后端地址
      .then(response => {
        this.tableData = response.data.result;
        this.tableColumns  =response.data.columns;
        this.total  =response.data.total;
        console.log(this.tableData)
      })
      .catch(error => {
        console.error('Error fetching table data', error);
      });
    },
    createNotice(){
      console.log(this.form)
      axios.post('http://localhost:5000/insert_notice_data', this.form)
      .then(response => {
        if(response.data.code === '200'){
          this.$message.success("发布成功")
          this.dialogFormVisible=false
          this.fetchTableData()
        }else{
          this.$message.error("发布失败")
        }
      })
    },
    reset() {
      this.name = ""
      this.getNotices()
    },
    handleAdd(){
      this.dialogFormVisible=true;
      this.form = {
        content: '',
        author: this.user.username,
        created_at: new Date().toISOString().substr(0, 10) // 设置当前日期为 YYYY-MM-DD 格式
      };
    },
    handleSizeChange(PageSize) {
      this.pageSize =  PageSize;
      console.log(`每页 ${PageSize} 条`);
      this.fetchTableData(); // 在每页数量改变时重新获取数据
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      console.log(`当前页: ${val}`);
      this.fetchTableData();
    },
  },
  mounted() {
    this.getNotices();
  }
};
</script>
<style scoped>
  .notice-board {
    font-family: Arial, sans-serif;
    max-width: 70%;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  .notice-form {
    margin-bottom: 20px;
  }

  .notice-list {
    border-top: 1px solid #ccc;
    padding-top: 20px;
  }

  .notice-item {
    margin-bottom: 15px;
    padding: 10px;
    background-color: #fff;
    border: 1px solid #eee;
    border-radius: 5px;
  }

  .content {
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 5px;
  }

  .info {
    font-size: 14px;
    color: #555;
  }
</style>
