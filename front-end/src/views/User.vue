<template>
  <div>
    <div style="padding:10px 0">
      <el-input style="width: 200px" placeholder="请输入用户名" suffix-icon="el-icon-search" v-model="search_name"></el-input>
      <el-button class="ml-5"  type="primary" @click="fetchTableData">搜索</el-button>
      <el-button type="warning" @click="reset">重置</el-button>
      <el-button type="danger" @click = "del_batch" >批量删除<i class="el-icon-remove-outline"></i></el-button>
    </div>

    <div style="width: 100%; height: 100%">
      <el-table :data="tableData" border  stripe :header-cell-class-name="headerBg" style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection"></el-table-column>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="username" label="名字" ></el-table-column>
        <el-table-column prop="password" v-if="showPasswordColumn"  label="密码" ></el-table-column>
        <el-table-column prop="role" label="职位" >
          <template slot-scope="scope">
            {{ getValue(scope.row['role']) }}
          </template>
        </el-table-column>
        <el-table-column  label="操作" width="410">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row)">编辑</el-button>
            <el-popconfirm
                calss="ml-5"
                confirm-button-text='确定'
                cancel-button-text='取消'
                icon="el-icon-info"
                icon-color="red"
                title="您确定删除吗？"
                @confirm="del(scope.row.id)"
            >
              <el-button slot="reference">删除<i class="el-icon-remove-outline"></i></el-button>

            </el-popconfirm>

          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="block">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 10, 20, 30, 40]"
        :page-size="pageSize"
        :layout="'total, sizes, prev, pager, next, jumper'"
        :total="totalItems">
      </el-pagination>
    </div>
    <el-dialog title="用户信息" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="120px" size="small">
        <el-form-item label="名字" :label-width="formLabelWidth">
          <el-input v-model="form.username" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="职位" :label-width="formLabelWidth">
          <el-input v-model="form.role" autocomplete="off"></el-input>
        </el-form-item>
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
    name: "Manage",
    data() {
      return {
        pageNum: 1,
        pageSize :5,
        total: 0,
        search_name: '',
        currentPage: 1,
        tableData: [],
        dialogFormVisible: false, // 编辑图片弹窗的显示状态
        dialogStatus: '',
        currentImage: '', // 当前选中行的图片路径
        fileList: [],
        form:{},
        tableColumns: [] ,// 从后端获取的列名数组,
        multipleSelection: [],
        selectedColumn: '',
        headerBg:'headerBg',
        formLabelWidth:"200",
        showPasswordColumn: false,
        }

    },
    computed: {
      totalItems() {
        return this.imageNum;
      },
      getValue() {
        return (value) => {
          if (value === '1') {
            return '管理员';
          } else if (value === '2') {
            return '技术人员';
          } else {
            return '医护人员'; // 其他值保持不变
          }
        };
      }
    },
    mounted() {
      // this.currentPage = JSON.parse(sessionStorage.getItem('currentPage')) || 1; // 设置链接数组
      console.log(this.currentPage);
      this.fetchTableData();
      // console.log('dzghs column value:', this.tableData.map(row => row['dzghs']));
    },
    created() {
      // console.log('dzghs column value:', this.tableData.map(row => row['dzghs']));
    },
    methods: {
      fetchTableData() {
        console.log(this.currentPage);
        axios.get(`http://localhost:5000/get_user_data?page=${this.currentPage}&pageSize=${this.pageSize}&name=${this.search_name}`) // 替换为你的后端地址
        .then(response => {
          this.tableData = response.data.result;
          this.tableColumns  =response.data.columns;
          this.imageNum = response.data.total;
          console.log(this.tableData)
          // sessionStorage.setItem('currentPage', JSON.stringify(this.currentPage));
        })
        .catch(error => {
          console.error('Error fetching table data', error);
        });
      },
      handleEdit(row){
        this.dialogStatus = 'edit';
        this.form=row;
        console.log(row);
        this.dialogFormVisible=true;
      },
      handleSizeChange(PageSize) {
        this.pageSize =  PageSize;
        console.log(`每页 ${PageSize} 条`);
        this.fetchTableData(); // 在每页数量改变时重新获取数据
      },
      handleSelectionChange(val) {
        console.log(val)
        this.multipleSelection = val
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        console.log(`当前页: ${val}`);
        this.fetchTableData();
      },

      del(id){
        axios.delete(`http://localhost:5000/del_userdata?id=${id}`) // 替换为你的后端地址
        .then(response => {
          if(response.data.code === '200'){
            this.$message.success("删除成功")
            this.dialogFormVisible=false
            this.fetchTableData()
          }else{
            this.$message.error("删除失败")
          }
        })
      },
      del_batch(){
        let ids = this.multipleSelection.map(v => v.id) //[{}{}{}]=>[1,2,3]将一个对象的数组转换成数组
        axios.delete(`http://localhost:5000/del_userbatchdata?ids=${ids}`) // 替换为你的后端地址
        .then(response => {
          if(response.data.code === '200'){
            this.$message.success("删除成功")
            this.dialogFormVisible=false
            this.fetchTableData()
          }else{
            this.$message.error("删除失败")
          }
        })
      },

      reset() {
        this.search_name = "";
        this.fetchTableData();
      },
      save(){
        if (this.dialogStatus === 'add') {
          // 添加操作
          this.addUser();
        } else if (this.dialogStatus === 'edit') {
          // 编辑操作
          this.updateUser();
        }
      },
      addUser(){
        console.log(this.form)
        axios.post('http://localhost:5000/insert_data', this.form)
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
      updateUser(){
        // 发送更新用户信息的请求
        axios.post('http://localhost:5000/update_data', this.form)
        .then(response => {
          if(response.data.code === '200'){
            this.$message.success("更新成功")
            this.dialogFormVisible=false
            this.fetchTableData()
          }else{
            this.$message.error("更新失败")
          }
        })
      },
    },
  }
</script>


<style>
  .headerBg{
    background: antiquewhite !important;
  }
</style>