<template>
  <div>
    <el-container>
      <!--头部区域-->
        <el-header style="color: #ffffff; background-color: #014880;">
          <img src="@/assets/img/logo_white.png" alt="" style="width: 40px; height: 40px">
          <span class="title" style="font-size: 35px;margin-left:40px;font-weight:700;  letter-spacing:20px;">痛风图像分割系统</span>
          <div>
<!--            <span style="margin-left: 20px"><el-link style="font-size: 20px; color: #FFFFFF" href="https://element.eleme.io" target="_blank">系统简介</el-link></span>-->
<!--            <span style="margin-left: 20px"><el-link style="font-size: 20px; color: #FFFFFF" href="https://element.eleme.io" target="_blank">联系我们</el-link></span>-->
          </div>
          <div style="flex: 1; width: 0; display: flex; align-items: center; justify-content: flex-end">
            <el-button round style="color: #014880; font-size: 20px; font-weight: bold"  @click="login()">登录</el-button>
          </div>
        </el-header>

      <el-container>
          <!--主体区域-->
          <el-main>
              <div class="back" style="margin-top:-20px;margin-left: -20px;"></div>
          </el-main>
      </el-container>

    </el-container>

  </div>
</template>

<script>
export default {
  name: "FirstPage",
  data() {
    return {
    }
  },
  methods: {
    login() {
      this.$router.push('/login')
    },
  }
}
</script>

<style>
.el-header {

  box-shadow: 2px 0 6px rgba(0,21,41,.35);
  display: flex;
  align-items: center;
}
.back {
  background: url("@/assets/img/back.png") no-repeat center;
  height: 94%;
		width: 100%;
		background-size: cover;
		position: fixed;
	}
</style>