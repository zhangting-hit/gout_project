<template>
  <div>
    <el-container>
      <!--        头部区域-->
        <el-header style="color: #ffffff; background-color: #014880;">
          <img src="@/assets/img/logo_white.png" alt="" style="width: 40px; height: 40px">
          <span class="title" style="font-size: 35px;margin-left:40px;font-weight:700;  letter-spacing:20px; color: white">痛风图像分割系统</span>
          <div>
<!--            <span style="margin-left: 40px"><el-link style="font-size: 20px; color: #FFFFFF" href="http://localhost:8080/home" target="_blank" >首页</el-link></span>-->
<!--            <span style="margin-left: 20px"><el-link style="font-size: 20px; color: #FFFFFF" href="https://element.eleme.io" target="_blank">系统简介</el-link></span>-->
<!--            <span style="margin-left: 20px"><el-link style="font-size: 20px; color: #FFFFFF" href="https://element.eleme.io" target="_blank">联系我们</el-link></span>-->
          </div>
          <div style="flex: 1; width: 0; display: flex; align-items: center; justify-content: flex-end">
            <i class="el-icon-quipping" style="font-size: 26px" @click="handleFull"></i>
            <el-dropdown placement="bottom">
              <div style="display: flex; align-items: center; cursor: default">
                <img :src="user.avatarUrl" alt="" style="width: 40px; height: 40px; margin: 0 5px">
                <span style="color: #FFFFFF">{{ user.username }}</span>
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>
                  <router-link to="/person">个人信息</router-link>
                </el-dropdown-item>
<!--                <el-dropdown-item>修改密码</el-dropdown-item>-->
                <el-dropdown-item @click="logout">
                  <router-link to="/login">退出登录</router-link>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </el-header>
        <el-container>
          <!--    侧边栏  -->
          <el-aside :width="asideWidth" style="min-height: 100vh; background-color: #1E6CA9">
            <el-menu :default-openeds=opens :collapse="isCollapse" :collapse-transition="false" router
                     background-color="#1E6CA9" text-color="rgba(255, 255, 255)" active-text-color="#fff"
                     style="border: none" :default-active="$route.path">
              <div v-for="item in menus " :key="item.id">
                <div v-if="item.path">
                  <el-menu-item :index="item.path">
                      <i :class="item.icon"></i>
                      <span slot="title">{{ item.label}}</span>
                  </el-menu-item>
                </div>
                <div v-else>
                  <el-submenu :index="item.id + ''">
                    <template slot="title">
                      <i :class="item.icon"></i>
                      <span slot="title">{{ item.label}}</span>
                    </template>
                    <div v-for="subItem in item.children " :key="subItem.id">
                      <el-menu-item :index="subItem.path">
                        <i :class="subItem.icon"></i>
                        <span slot="title">{{ subItem.label}}</span>
                      </el-menu-item>
                    </div>
                  </el-submenu>
                </div>
              </div>
            </el-menu>
          </el-aside>
          <!--        主体区域-->
          <el-main>
              <!-- 在HomeView.vue 组件中 -->
              <div v-if="$route.path === '/home'" class="back" style="margin-top:-20px;margin-left: -20px;"></div>
              <router-view></router-view>
          </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>

import router, {resetRouter} from "@/router";

export default {
  name: 'HomeView',
  data() {
    return {
      menus: sessionStorage.getItem("menus") ? JSON.parse(sessionStorage.getItem("menus")):[],
      opens: sessionStorage.getItem("menus") ? JSON.parse(sessionStorage.getItem("menus")).map(v=> v.id +''):[],
      user: sessionStorage.getItem("user") ? JSON.parse(sessionStorage.getItem("user")): {},
      isCollapse: false,  // 不收缩
      asideWidth: '200px',
      collapseIcon: 'el-icon-s-fold'
    }
  },
  methods: {
    handleFull() {
      document.documentElement.requestFullscreen()
    },
    handleCollapse() {
      this.isCollapse = !this.isCollapse
      this.asideWidth = this.isCollapse ? '64px' : '200px'
      this.collapseIcon = this.isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'
    },
    logout(){
      console.log("正在执行退出操作");
      sessionStorage.removeItem("user")
      sessionStorage.removeItem("menus")
      this.$router.push("/login");
      resetRouter()
      this.$message.success("退出成功")
    }
  }
}
</script>

<style>
.el-menu--inline {
  background-color: #000c17 !important;
}
.el-menu--inline .el-menu-item {
  background-color: #1E6CA9 !important;
  padding-left: 49px !important;
}
.el-menu-item:hover, .el-submenu__title:hover {
  color: #fff !important;
}
.el-submenu__title:hover i {
  color: #fff !important;
}
.el-menu-item:hover i {
  color: #fff !important;
}
.el-menu-item.is-active {
  background-color: #1890ff !important;
  border-radius: 5px !important;
  width: calc(100% - 8px);
  margin-left: 4px;
}
.el-menu-item.is-active i, .el-menu-item.is-active .el-tooltip{
  margin-left: -4px;
}
.el-menu-item {
  height: 40px !important;
  line-height: 40px !important;
}
.el-submenu__title {
  height: 40px !important;
  line-height: 40px !important;
}
.el-submenu .el-menu-item {
  min-width: 0 !important;
}
.el-menu--inline .el-menu-item.is-active {
  padding-left: 45px !important;
}
/*.el-submenu__icon-arrow {*/
/*  margin-top: -5px;*/
/*}*/

.el-aside {
  transition: width .3s;
  box-shadow: 2px 0 6px rgba(0,21,41,.35);
}
.logo-title {
  margin-left: 5px;
  font-size: 20px;
  transition: all .3s;   /* 0.3s */
}
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
