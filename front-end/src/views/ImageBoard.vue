<template>
  <div>
    <div style="padding:10px 0">
      <el-input style="width: 200px" placeholder="请输入病人id" suffix-icon="el-icon-search" v-model="patientId"></el-input>
      <el-button class="ml-5"  type="primary" @click="fetchTableData">搜索</el-button>
      <el-button type="warning" @click="reset">重置</el-button>
      <el-button type="danger" @click = "del_batch" >批量删除<i class="el-icon-remove-outline"></i></el-button>
      <el-button type="primary" @click="download_batch">批量下载</el-button>
      <el-select v-model="selectedColumn" placeholder="请选择字段"  @change="refreshPage">
        <!-- options 是数据库中的字段列表 -->
        <el-option v-for="option in options" :key="option.value" :label="option.label" :value="option.value" />
      </el-select>
    </div>

    <div style="max-width: 80vw">
      <el-table :data="tableData" border  stripe :header-cell-class-name="headerBg"  @selection-change="handleSelectionChange">
        <el-table-column type="selection"></el-table-column>
        <el-table-column v-for="column in tableColumns" :key="column" :label="getCustomLabel(column)" :prop="column" v-if="column !== 'imagePath'" >
          <template slot-scope="scope">
            <span v-if="column === 'location'">
              {{ getLocationValue(scope.row[column]) }}
            </span>
            <span v-else>
              {{ getValue(scope.row[column]) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="图片" prop="imagePath">
          <template slot-scope="scope">
            <img :src="scope.row.imagePath" alt="图片" style="max-width: 100px; max-height: 100px;" />
          </template>
        </el-table-column>
        <el-table-column  label="操作" width="300">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row.imagePath)">编辑<i class="el-icon-edit"></i></el-button>
            <el-button slot="reference" @click="handleCheck(scope.row.imagePath)">查看病症<i class="el-icon-video-play"></i></el-button>
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
        currentImage: '', // 当前选中行的图片路径
        fileList: [],
        tableColumns: [] ,// 从后端获取的列名数组,
        patientId: '', // 用于存储输入的病人ID
        imageNum: 0,
        multipleSelection: [],
        selectedColumn: '',
        headerBg:'headerBg',
        options: [{label:  '无', value: ''},
                  {label:  '点状高回声', value: 'dzghs'},
                  {label:  '滑膜增厚', value: 'hmzh'},
                  {label:  '痛风石形成', value: 'tfsxc'},
                  {label:  '骨质破坏', value: 'gzph'},
                  {label:  '关节积液', value: 'gjjy'},
                  {label:  '双轨征', value: 'sgz'},
                  ]
        }

    },
    computed: {
      totalItems() {
        return this.imageNum;
      },
      paginatedData() {
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = this.currentPage * this.pageSize;
        return this.tableData.slice(startIndex, endIndex);
      },
      getLocationValue(){
        return (value) => {
          if (value === '0') {
            return '足背';
          } else if (value === '1') {
            return '足内侧';
          } else {
            return '足底'; // 其他值保持不变
          }
        };
      },
      getValue() {
        return (value) => {
          if (value === '1') {
            return '✔';
          } else if (value === '0') {
            return '✘';
          } else {
            return value; // 其他值保持不变
          }
        };
      }
    },
    mounted() {
      // this.currentPage = JSON.parse(sessionStorage.getItem('currentPage')) || 1; // 设置链接数组
      this.pageSize = JSON.parse(sessionStorage.getItem('imagePageSize')) || 5; // 设置链接数组
      this.currentPage = JSON.parse(sessionStorage.getItem('imageCurrentPage')) || 1; // 设置链接数组
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
        axios.get(`http://localhost:5000/get_image_data?page=${this.currentPage}&pageSize=${this.pageSize}&patientId=${this.patientId}&selectedColumn=${this.selectedColumn}`) // 替换为你的后端地址
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
      handleEdit(imagePath) {
        this.$router.push({ name: 'ImagePathEdit', params: { imagePath } });
      },
      handleCheck(imagePath) {
        this.$router.push({ name: 'CheckImage', params: { imagePath} });
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
      getCustomLabel(columnKey) {
        // console.log(columnKey)
        if (columnKey === 'location') {
          return '位置'; // 更改 columnName1 的列名为 Custom Name 1
        } else if (columnKey === 'dzghs') {
          return '点状高回声'; // 更改 columnName2 的列名为 Custom Name 2
        }
        else if (columnKey === 'hmzh') {
          return '滑膜增厚'; // 更改 columnName2 的列名为 Custom Name 2
        }
        else if (columnKey === 'tfsxc') {
          return '痛风石形成'; // 更改 columnName2 的列名为 Custom Name 2
        }
        else if (columnKey === 'gzph') {
          return '骨质破坏'; // 更改 columnName2 的列名为 Custom Name 2
        }
        else if (columnKey === 'gjjy') {
          return '关节积液'; // 更改 columnName2 的列名为 Custom Name 2
        }
        else if (columnKey === 'sgz') {
          return '双轨征'; // 更改 columnName2 的列名为 Custom Name 2
        }
        // 其他列保持不变
        return columnKey;
      },
      del(id){
        axios.delete(`http://localhost:5000/del_data?id=${id}`) // 替换为你的后端地址
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
        axios.delete(`http://localhost:5000/del_batchdata?ids=${ids}`) // 替换为你的后端地址
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
      download_batch(){
        let ids = this.multipleSelection.map(v => v.id) //[{}{}{}]=>[1,2,3]将一个对象的数组转换成数组
        // 向后端发送 GET 请求以触发 ZIP 文件下载
        fetch(`http://localhost:5000/download_batch?ids=${ids}`)
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
      refreshPage(){
        this.fetchTableData();
      }
    },
  }
</script>


<style>
  .headerBg{
    background: antiquewhite !important;
  }
</style>