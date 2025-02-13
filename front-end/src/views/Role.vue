<template>
  <div>
    <div style="padding:10px 0">
      <el-input style="width: 200px" placeholder="请输入用户名" suffix-icon="el-icon-search" v-model="rolename"></el-input>
      <el-button class="ml-5"  type="primary" @click="fetchTableData">搜索</el-button>
      <el-button type="warning" @click="reset">重置</el-button>
      <el-button type="danger" @click = "del_batch" >批量删除<i class="el-icon-remove-outline"></i></el-button>
      <el-button type="success" @click = "handleAdd" >增加<i class="el-icon-add-location"></i></el-button>
    </div>

    <div style="width: 100%; height: 100%">
      <el-table :data="tableData" border  stripe :header-cell-class-name="headerBg" style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection"></el-table-column>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="名称" ></el-table-column>
        <el-table-column  label="操作" width="410">
          <template slot-scope="scope">
            <el-button type="info" @click="selectMenu(scope.row)">分配菜单<i class="el-icon-menu"></i></el-button>
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
    <el-dialog title="菜单分配" :visible.sync="menuDialogVis" width="30%">
      <el-tree
          :props="defaultProps"
          :data="menuData"
          show-checkbox
          node-key="id"
          ref="tree"
          :default-checked-keys="checks"
          :default-expanded-keys="expends"
          @check-change="handleCheckChange">
        <span class="custom-tree-node" slot-scope="{ node, data }">
          <span><i :class="data.icon"></i> {{ data.label }}</span>
        </span>
      </el-tree>

      <div slot="footer" class="dialog-footer">
        <el-button @click="menuDialogVis = false">取 消</el-button>
        <el-button type="primary" @click="saveRoleMenu">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="角色信息" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="120px" size="small">
        <el-form-item label="名称" :label-width="formLabelWidth">
          <el-input v-model="form.name" autocomplete="off"></el-input>
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
    name: "ImageBoard",
    data() {
      return {
        pageNum: 1,
        pageSize :5,
        total: 0,
        currentPage: 1,
        tableData: [],
        dialogFormVisible: false, // 编辑图片弹窗的显示状态
        menuDialogVis : false,
        fileList: [],
        tableColumns: [] ,// 从后端获取的列名数组,
        imageNum: 0,
        multipleSelection: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        menuData: [],
        headerBg:'headerBg',
        expends:  [],
        checks: [],
        rolename: '',
        form:{},
        formLabelWidth:"200",
      }

    },
    computed: {
      totalItems() {
        return this.imageNum;
      },
    },
    mounted() {
      console.log(this.currentPage);
      this.fetchTableData();
    },
    created() {
    },
    methods: {
      fetchTableData() {
        console.log(this.currentPage);
        axios.get(`http://localhost:5000/get_role_data?page=${this.currentPage}&pageSize=${this.pageSize}&name=${this.rolename}`) // 替换为你的后端地址
        .then(response => {
          this.tableData = response.data.result;
          this.tableColumns  =response.data.columns;
          this.imageNum = response.data.total;
          // sessionStorage.setItem('currentPage', JSON.stringify(this.currentPage));
        })
        .catch(error => {
          console.error('Error fetching table data', error);
        });
      },
      handleSizeChange(PageSize) {
        this.pageSize =  PageSize;
        console.log(`每页 ${PageSize} 条`);
        this.fetchTableData(); // 在每页数量改变时重新获取数据
      },
      handleEdit(row){
        this.form=row;
        this.dialogVisible=true;
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
      saveRoleMenu(){
        axios.post(`http://localhost:5000/save_rolemenu?id=${this.roleId}`, this.$refs.tree.getCheckedKeys())
        .then(res => {
            if(res.data.code==='200'){
              this.$message.success("绑定成功")
              this.menuDialogVis=false

            }else{
              this.$message.error(res.msg)
            }
          })
      },
      selectMenu(role){
        this.menuDialogVis=true;
        this.roleId=role.id
        //请求菜单数据
        axios.get(`http://localhost:5000/get_expend_menu`) // 获取所有父级菜单
        .then(response => {
          this.menuData = response.data.data;
          console.log(this.menuData)
          //把后台返回的菜单数据处理成id数组
          this.expends=this.menuData.map(v => v.id)
        })
        axios.get(`http://localhost:5000/get_check_menu?id=${this.roleId}`) // 获取当前角色分配的菜单id
        .then(res => {
          this.menuDialogVis=true

          this.checks= res.data.result;
          axios.get(`http://localhost:5000/get_menu_ids`) // 将没被选中的菜单取消勾选
          .then(r => {
            const ids = r.data.result;
            ids.forEach(id=>{
              if(!this.checks.includes(id)){
                this.$refs.tree.setChecked(id,false)
              }
            })
          })
        })
      },
      handleAdd(){
        this.dialogFormVisible=true;
        this.form={}
      },
      save(){
        console.log(this.form)
        axios.post('http://localhost:5000/insert_roledata', this.form)
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
      del(id){
        axios.delete(`http://localhost:5000/del_roledata?id=${id}`) // 替换为你的后端地址
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
        axios.delete(`http://localhost:5000/del_rolebatchdata?ids=${ids}`) // 替换为你的后端地址
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
        this.rolename = "";
        this.fetchTableData();
      },
      handleCheckChange(data, checked, indeterminate) {
        console.log(data, checked, indeterminate);
      },
    },
  }
</script>


<style>
  .headerBg{
    background: antiquewhite !important;
  }
</style>