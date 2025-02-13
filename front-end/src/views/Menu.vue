<template>
  <div>
    <div style="padding:10px 0">
      <el-input style="width: 200px" placeholder="请输入名称" suffix-icon="el-icon-search" v-model="name"></el-input>
      <el-button class="ml-5"  type="primary" @click="fetchTableData">搜索</el-button>
      <el-button type="warning" @click="reset">重置</el-button>
    </div>
    <el-table :data="tableData" border stripe :header-cell-class-name="headerBg"
              row-key="id" default-expand-all :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
              @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="name" label="名称" ></el-table-column>
      <el-table-column prop="path" label="路径" ></el-table-column>
      <el-table-column prop="icon" label="图标" class-name="fontSize18" align="center" label-class-name="fontSize12" >
        <template slot-scope="scope">
          <span :class="scope.row.icon"/>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" ></el-table-column>
      <el-table-column  label="操作" width="300">
        <template slot-scope="scope">
<!--          <el-button type="primary" @click="handleAdd(scope.row.id)" v-if="!scope.row.pid && !scope.row.path">新增子菜单<i class="el-icon-plus"></i></el-button>-->
          <el-button type="success" @click="handleEdit(scope.row)">编辑<i class="el-icon-edit"></i></el-button>
          <el-popconfirm
              calss="ml-5"
              confirm-button-text='确定'
              cancel-button-text='取消'
              icon="el-icon-info"
              icon-color="red"
              title="您确定删除吗？"
              @confirm="del(scope.row.id)"
          >
            <el-button type="danger" slot="reference">删除<i class="el-icon-remove-outline"></i></el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="菜单信息" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="120px" size="small">
        <el-form-item label="名称" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="路径" :label-width="formLabelWidth">
          <el-input v-model="form.path" autocomplete="off"></el-input>
        </el-form-item>
<!--        <el-form-item label="页面路径" :label-width="formLabelWidth">-->
<!--          <el-input v-model="form.pagePath" autocomplete="off"></el-input>-->
<!--        </el-form-item>-->
        <el-form-item label="图标" :label-width="formLabelWidth">
          <el-input v-model="form.icon" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述" :label-width="formLabelWidth">
          <el-input v-model="form.description" autocomplete="off"></el-input>
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
  name: "User",
  data(){
    return{
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
      options:[]
    }
  },
  created() {
    this.fetchTableData()
  },
  methods: {
    fetchTableData() {
      console.log(this.currentPage);
      axios.get(`http://localhost:5000/get_menu_data?page=${this.currentPage}&pageSize=${this.pageSize}&name=${this.name}`) // 替换为你的后端地址
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
    save(){
      axios.post('http://localhost:5000/change_menu_data', this.form)
          .then(res => {
        if(res.data.code=== '200'){
          this.$message.success("保存成功")
          this.dialogFormVisible=false
          this.fetchTableData()
        }else{
          this.$message.error("保存失败")
        }
      })
    },
    reset() {
      this.name = ""
      this.fetchTableData()
    },
    del(id){
      this.request.delete("/menu/"+id).then(res=>{
        if(res.code === '200'){
          this.$message.success("删除成功")
          this.dialogFormVisible=false
          this.fetchTableData()
        }else{
          this.$message.error("删除失败")
        }
      })
    },
    handleSelectionChange(val){
      console.log(val)
      this.multipleSelection=val
    },
    delBatch(){
      let ids=this.multipleSelection.map(v=>v.id) //[{}{}{}]=>[1,2,3]将一个对象的数组转换成数组
      this.request.post("/menu/del/batch",ids).then(res=>{
        if(res.code === '200'){
          this.$message.success("删除成功")
          this.dialogFormVisible=false
          this.fetchTableData()
        }else{
          this.$message.error("删除失败")
        }
      })
    },
    handleAdd(pid){
      this.dialogFormVisible=true;
      this.form={}
      if (pid){
        this.form.pid=pid
      }
    },
    handleEdit(row){
      this.form=row;
      this.dialogFormVisible=true;
    },

    handleSizeChange(pageSize){
      console.log(pageSize)
      this.pageSize=pageSize
      this.fetchTableData()//请求数据
    },
    handleCurrentChange(pageNum){
      console.log(pageNum)
      this.pageNum=pageNum
      this.fetchTableData()
    },
  }
}
</script>

<style>
.headerBg{
  background: antiquewhite !important;
}
.fontSize18{
  font-size: 18px;
}
.fontSize12{
  font-size: 12px;
}
</style>