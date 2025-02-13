<template>
  <div>
    <div style="padding:10px 0">
      <el-input style="width: 200px" placeholder="请输入病人id" suffix-icon="el-icon-search" v-model="patientId"></el-input>
      <el-button class="ml-5"  type="primary" @click="fetchTableData">搜索</el-button>
      <el-button type="warning" @click="reset">重置</el-button>
      <el-button type="danger" @click = "del_batch" >批量删除<i class="el-icon-remove-outline"></i></el-button>
      <el-button type="primary" @click="download_batch">批量下载</el-button>
    </div>

    <div style="max-width: 80vw">
      <el-table :data="tableData" border  stripe :header-cell-class-name="headerBg" style="width: 100%"  @selection-change="handleSelectionChange">
        <el-table-column type="selection"></el-table-column>
        <el-table-column prop="patient_id" label="PatientID" ></el-table-column>
        <el-table-column  label="操作" >
          <template slot-scope="scope">
            <el-button slot="reference" @click="handleSeeImage(scope.row.patient_id)">查看病人图片<i class="el-icon-remove-outline"></i></el-button>
            <el-button slot="reference" @click="downloadFile(scope.row.patient_id)">下载病人图片<i class="el-icon-remove-outline"></i></el-button>
            <el-popconfirm
                calss="ml-5"
                confirm-button-text='确定'
                cancel-button-text='取消'
                icon="el-icon-info"
                icon-color="red"
                title="您确定删除吗？"
                @confirm="del(scope.row.patient_id)"
            >
              <el-button slot="reference">删除病人信息<i class="el-icon-remove-outline"></i></el-button>

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
  </div>
</template>

<script>
  import axios from "axios";

  export default {
    name: "PatientBoard",
    data() {
      return {
        pageNum: 1,
        pageSize :5,
        total: 0,
        currentPage: 1,
        tableData: [],
        patientId: '', // 用于存储输入的病人ID
        patientNum: 0,
        multipleSelection: [],
        selectedColumn: '',
        headerBg:'headerBg',
        }

    },
    computed: {
      totalItems() {
        return this.patientNum;
      },
    },
    mounted() {
      this.pageSize = JSON.parse(sessionStorage.getItem('imagePageSize')) || 5; // 设置链接数组
      // this.currentPage = JSON.parse(sessionStorage.getItem('imageCurrentPage')) || 1; // 设置链接数组
      console.log("CurrentPage:"+this.currentPage);
      console.log("pageSize:"+this.pageSize);
      this.fetchTableData();
    },
    created() {
      // console.log('dzghs column value:', this.tableData.map(row => row['dzghs']));
    },
    methods: {
      fetchTableData() {
        console.log(this.selectedColumn)
        console.log(this.currentPage);
        axios.get(`http://localhost:5000/get_patient_ids?page=${this.currentPage}&pageSize=${this.pageSize}&patientId=${this.patientId}`) // 替换为你的后端地址
        .then(response => {
          this.tableData = response.data.result;
          this.tableColumns  =response.data.columns;
          this.patientNum = response.data.total;
          // sessionStorage.setItem('currentPage', JSON.stringify(this.currentPage));
        })
        .catch(error => {
          console.error('Error fetching table data', error);
        });
      },
      handleClick(row) {
        console.log(row);
      },
      handleSizeChange(PageSize) {
        this.pageSize =  PageSize;
        console.log(`每页 ${PageSize} 条`);
        this.fetchTableData(); // 在每页数量改变时重新获取数据
        sessionStorage.setItem('imagePageSize', JSON.stringify(this.pageSize));
      },
      handleSelectionChange(val) {
        console.log(val)
        this.multipleSelection = val
      },
      handleCurrentChange(val) {
        this.currentPage = val;
        console.log(`当前页: ${val}`);
        this.fetchTableData();
        sessionStorage.setItem('imageCurrentPage', JSON.stringify(this.currentPage));
      },
      handleSeeImage(patientID){
        // this.$router.push({ name: 'PatientImages', params: { patientId } });
        this.$router.push({ name: 'ImageIdShow', params: { patientID } });

      },
      del(id){
        axios.delete(`http://localhost:5000/del_patient_data?id=${id}`) // 替换为你的后端地址
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
        let ids = this.multipleSelection.map(v => v.patient_id) //[{}{}{}]=>[1,2,3]将一个对象的数组转换成数组
        axios.delete(`http://localhost:5000/del_patient_batchdata?ids=${ids}`) // 替换为你的后端地址
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
      downloadFile(patientId){
        // 向后端发送 GET 请求以触发 ZIP 文件下载
        console.log(patientId)
        fetch(`http://localhost:5000/download/${patientId}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.blob(); // 获取文件内容的二进制数据
        })
        .then(blob => {
          // 创建一个 URL 对象
          const url = window.URL.createObjectURL(new Blob([blob]));

          // 创建一个 <a> 元素并模拟点击以下载 ZIP 文件
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', patientId +'.zip');
          document.body.appendChild(link);
          link.click();

          // 释放 URL 对象
          window.URL.revokeObjectURL(url);
        })
        .catch(error => {
          console.error('There has been a problem with your fetch operation:', error);
        });
      },
      download_batch(){
        let ids = this.multipleSelection.map(v => v.patient_id) //[{}{}{}]=>[1,2,3]将一个对象的数组转换成数组
        // 向后端发送 GET 请求以触发 ZIP 文件下载
        fetch(`http://localhost:5000/download_batchPatient?ids=${ids}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.blob(); // 获取文件内容的二进制数据
        })
        .then(blob => {
          // 创建一个 URL 对象
          const url = window.URL.createObjectURL(new Blob([blob]));

          // 创建一个 <a> 元素并模拟点击以下载 ZIP 文件
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'download.zip');
          document.body.appendChild(link);
          link.click();

          // 释放 URL 对象
          window.URL.revokeObjectURL(url);
        })
        .catch(error => {
          console.error('There has been a problem with your fetch operation:', error);
        });
      },
      reset() {
        this.patientId = "";
        this.fetchTableData();
      },
      refreshPage() {
        this.fetchTableData();
      },
    },
  }
</script>


<style>
  .headerBg{
    background: #FFFACD !important;
  }
</style>
