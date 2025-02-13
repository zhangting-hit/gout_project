<template>
  <div style="display: flex; justify-content: center">
    <el-card style="width: 500px;">
      <el-form label-width="120px" size="small">
        <el-upload
            class="avatar-uploader"
            action="http://localhost:5000/upload_avartar"
            :show-file-list="false"
            :on-success="handleAvatarSuccess">
          <img v-if="form.avatarUrl" :src="form.avatarUrl" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>

        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="form.username" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="角色" :label-width="formLabelWidth">
          <el-input v-model="roleName" disabled autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="电话" :label-width="formLabelWidth">
          <el-input v-model="form.phone" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="save">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>

</template>

<script>

import axios from "axios";

export default {
  name: "Person",
  data(){
    return{
      form: {},
      user: sessionStorage.getItem("user") ? JSON.parse(sessionStorage.getItem("user")): {},
      formLabelWidth: '50'
    }
  },
  created() {
    this.getUser().then(response => {
      console.log(response)
      this.form = response.userData;
    })
  },
  computed: {
    roleName() {
      switch (this.form.role) {
        case '1':
          return '管理员';
        case '2':
          return '医护人员';
        case '3':
          return '技术人员';
        default:
          return '未知角色';
      }
    }
  },
  methods:{
    async getUser(){
      return (await axios.get(`http://localhost:5000/get_User?name=${this.user.username}`) ).data
      // console.log(this.user)
      // axios.get(`http://localhost:5000/get_User?name=${this.user.username}`) // 替换为你的后端地址
      // .then(response => {
      //   this.form = response.data.userData;
      // })
      // .catch(error => {
      //   console.error('Error fetching table data', error);
      // });
    },
    save(){
      console.log(this.form)
      axios.post('http://localhost:5000/update_logged_userdata', this.form)
      .then(response => {
        if(response.data.code === '200'){
          this.$message.success("保存成功")
          // this.$emit("refreshUser")
          // 更新浏览器存储的用户信息
          this.getUser().then(res => {
            // res.token=JSON.parse(sessionStorage.getItem("user")).token
            // sessionStorage.setItem("user",JSON.stringify(res))
            sessionStorage.setItem('user', JSON.stringify(res.userData));
          })

        }else{
          this.$message.error("保存失败")
        }
      })
    },
    handleAvatarSuccess(res){
      console.log(res)
      this.form.avatarUrl=res
    }
  }
}
</script>

<style >
.avatar-uploader{
  text-align: center;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
  padding-bottom: 10px;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 138px;
  height: 138px;
  line-height: 138px;
  text-align: center;
}
.avatar {
  width: 138px;
  height: 138px;
  display: block;
}
</style>