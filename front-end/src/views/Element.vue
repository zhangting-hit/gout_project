<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="6"><div class="grid-content bg-purple"></div></el-col>
      <el-col :span="6"><div class="grid-content bg-purple"></div></el-col>
      <el-col :span="6"><div class="grid-content bg-purple"></div></el-col>
      <el-col :span="6"><div class="grid-content bg-purple"></div></el-col>
    </el-row>

    <el-row>
      <el-button>默认按钮</el-button>
      <el-button type="primary">主要按钮</el-button>
      <el-button type="success">成功按钮</el-button>
      <el-button type="info">信息按钮</el-button>
      <el-button type="warning">警告按钮</el-button>
      <el-button type="danger">危险按钮</el-button>
    </el-row>
    <el-row>
      <el-input v-model="input" placeholder="请输入内容"></el-input>
      <el-input show-password style= "width: 200px" v-model="password" placeholder="请输入密码"> </el-input>
      <el-input style= "width: 200px" v-model="value1" placeholder="请输入内容" prefix-icon="el-icon-search" clearable></el-input>
      <el-input style= "width: 200px" v-model="value1" placeholder="请输入内容" suffix-icon="el-icon-user"></el-input>
    </el-row>

    <el-row>
      <el-autocomplete style="width: 300px" placeholder="请输入内容，我来帮你猜一猜" :fetch-suggestions=
          "querySearch" :trigger-on-focus="false" v-model="value3">
      </el-autocomplete>
    </el-row>

    <el-row>
      <el-select v-model="value" placeholder="请选择">
        <el-option value="青哥哥"></el-option>
        <el-option value="亲哥哥"></el-option>
        <el-option value="情哥哥"></el-option>
      </el-select>

      <el-select v-model="value" placeholder="请选择">
        <el-option
          v-for="item in coffees"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
    </el-row>

    <el-row>
      <el-date-picker v-model="date" placeholder="选择日期" value-format="yyyy-MM-dd" @change="changeDate"></el-date-picker>
    </el-row>

    <el-row>
      <el-table :data="tableData" border :header-cell-style="{ background: 'aliceblue', fontSize: '16px' }">
        <el-table-column label="序号" prop="id" align="center"></el-table-column>
        <el-table-column label="名称" prop="name" align="center"></el-table-column>
        <el-table-column label="年龄" prop="age" align="center"></el-table-column>
        <el-table-column label="地址" prop="address" align="center"></el-table-column>
        <el-table-column label="操作">
          <template v-slot="scope">
            <el-button type="primary" @click="edit(scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "Element",
  data(){
    return{
      input:'',
      password:'',
      value:'',
      value1:'',
      value3:'',
      coffees: [{ value: '1星巴克咖啡' },{ value: '1栖巢咖啡' }, {value: '2瑞幸咖啡'}, {value: '3库迪咖啡'}], // 值必须带value
      date:'',
      tableData: [
        {  name: '青哥哥哥', address: '安徽省合肥市', id: 1, age: '30' },
        {  name: '青哥哥哥', address: '安徽省合肥市', id: 1, age: '30' },
        {  name: '青哥哥哥', address: '安徽省合肥市', id: 1, age: '30' },
        {  name: '青哥哥哥', address: '安徽省合肥市', id: 1, age: '30' },
        {  name: '青哥哥哥', address: '安徽省合肥市', id: 1, age: '30' },
        {  name: '青哥哥哥', address: '安徽省合肥市', id: 1, age: '30' },
        {  name: '青哥哥哥', address: '安徽省合肥市', id: 1, age: '30' },
      ],
    }
  },
  methods:{
    querySearch(query, cb) {  // callback
      let result =  query ? this.coffees.filter(v => v.value.includes(query)) : this.coffees
      console.log(result)
      cb(result);
    },
    changeDate(){
      console.log(this.date)
    },
    edit(row){
      // alert(row.name)
      // this.$message.success(row.name)
      // this.$message.warning(row.name)
      // this.$notify.success(row.name)

      this.$confirm('这是什么个玩意儿？', '提示', {
        type: 'warning'
      }).then(res => {
        this.$message.success("ok 我点击了确认")
      }).catch(() => {
        this.$message.warning("ok 我点击了取消")
      })
    }
  }
}
</script>

<style scoped>
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>