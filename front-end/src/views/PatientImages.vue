<template>
  <div>
    <!-- 显示病人图片 -->
    <h2>病人 {{ $route.params.patientId }} 的图片：</h2>
    <!-- 图片展示逻辑 -->
<!--    <button @click="goBack">返回</button>-->
    <div style="width: 100%; height: 100%">
      <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelectionChange">
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
        <el-table-column  label="操作" width="410">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row.imagePath)">编辑</el-button>
            <el-button slot="reference" @click="handleCheck(scope.row.imagePath)">查看病症<i class="el-icon-remove-outline"></i></el-button>
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
      <!-- 编辑图片弹窗 -->
      <el-dialog :visible="dialogVisible" @close="dialogVisible = false">
        <img v-if="currentImage" :src="currentImage" alt="编辑图片" style="max-width: 400px; max-height: 400px;" />
      </el-dialog>
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
  data() {
    return {
      pageNum: 1,
      pageSize :5,
      total: 0,
      currentPage: 1,
      tableData: [],
      dialogVisible: false, // 编辑图片弹窗的显示状态
      currentImage: '', // 当前选中行的图片路径
      fileList: [],
      tableColumns: [] ,// 从后端获取的列名数组,
      patientId: '', // 用于存储输入的病人ID
      imageNum: 0,
      multipleSelection: [],
      selectedColumn: '',
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
  created() {
    this.patientId = this.$route.params.patientId; // 获取路由中传递的图片路径参数
    console.log(this.imagePath)
  },
  mounted() {
    // 从路由参数中获取病人 ID
    this.patientId = this.$route.params.patientId;
    this.fetchTableData();
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
  methods: {
    fetchTableData() {
      console.log(this.selectedColumn)
      axios.get(`http://localhost:5000/get_image_data?page=${this.currentPage}&pageSize=${this.pageSize}&patientId=${this.patientId}&selectedColumn=${this.selectedColumn}`) // 替换为你的后端地址
      .then(response => {
        this.tableData = response.data.result;
        this.tableColumns  =response.data.columns;
        this.imageNum = response.data.total;
      })
      .catch(error => {
        console.error('Error fetching table data', error);
      });
    },
    goBack() {
      this.$router.push('/home/upload'); // 返回到上传文件页面
    },
    handleEdit(imagePath) {
      this.$router.push({ name: 'EditImage', params: { imagePath } });
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
    handleCheck(imagePath) {
      this.$router.push({ name: 'CheckImage', params: { imagePath} });
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
  },
};
</script>
