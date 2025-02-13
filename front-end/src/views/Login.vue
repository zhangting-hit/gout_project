<template>
	<div class="back" >
    <img src="@/assets/img/logo_blue.png" alt="" style="width: 50px; height: 50px; margin-left:40px; margin-top: -15px;">
    <span class="title" style="font-size: 40px;margin-left:40px;  font-weight:700;  letter-spacing:20px;">痛风图像分割系统</span>
		<div style="  color: #F7F9FA ;margin-top: -100px">
			<el-form label-width="80px" label-position="left" ref="form" :model="form" :rules="rules" style="" class="login-box"  size="mini" >
        <div style="margin-bottom: 40px">
          <span style="font-size: 30px; color: black;">欢迎登陆</span>
          <div style="font-size: 15px; color: black;">
            没有账号 ？<router-link to="/register" class="title" style="color: #1E6CA9; font-size: 15px">注册</router-link>
          </div>
        </div>
        <el-form-item label="用户类型" class="label"  >
          <el-select v-model="roleId" placeholder="请选择用户类型" style="width: 330px">
            <el-option label="管理员" value=1></el-option>
            <el-option label="技术人员" value=2></el-option>
            <el-option label="医护人员" value=3></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="用户名" class="label">
          <el-input type="text" placeholder="请输入用户名" v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="密码" class="label">
          <el-input type="password"  prefix-icon="el-icon-lock" placeholder="请输入密码"  v-model="form.pwd" show-password> </el-input>
        </el-form-item>

				<el-form-item class="button">
					<el-button  type="primary" round @click="onSubmit" style="width: 200px; margin-left: -40px;  margin-top: 20px; font-size: 15px"  >登录</el-button>
				</el-form-item>
<!--				<el-form-item class="button2">-->
<!--					<el-button type="text" @click="onpassword" style="color: #1E6CA9; font-size: 15px;">忘记密码</el-button>-->
<!--				</el-form-item>-->
			</el-form>
		</div>
	</div>
</template>

<script>
	import axios from 'axios';
	export default {
		name: 'Login',
		data() {
			return {
				form: {
					name: '',
					pwd: '',
				},
				rules: {
					name: [{
							required: true,
							message: '请输入账号',
							trigger: 'blur'
						},
						{
							min: 2,
							max: 10,
							message: '长度在 2 到 10 个字符',
							trigger: 'blur'
						}
					],
					pwd: [{
							required: true,
							message: '请输入密码',
							trigger: 'blur'
						},
						{
							min: 2,
							max: 10,
							message: '长度在 2 到 10 个字符',
							trigger: 'blur'
						}
					]
				},
        roleId : '',
			}
		},
		methods: {
			onSubmit() {
				const path = 'http://localhost:5000/login';
				const msg = {
					name: this.form.name,
					password: this.form.pwd,
          roleId: this.roleId,
				};
				axios.post(path, msg).then((res) => {
					var success = res.data.status;
          console.log(res.data.userData)
          console.log(res.data.menus)
					if (success === 'success') {
						sessionStorage.setItem('user', JSON.stringify(res.data.userData));
            sessionStorage.setItem('menus',JSON.stringify(res.data.menus))//存储用户信息到浏览器
						this.run();
					} else if (success === 'admin') {
						sessionStorage.setItem('name', this.form.name);
						this.$router.push({
							name: 'Admin',
							query: {
								'name': this.form.name
							}
						});
					} else {
						this.$message({
							message: '账号或密码错误',
							type: 'warning'
						});
					}

				})


			},
			run() {
				this.$router.push({
					name: 'home',
					query: {
						'name': this.form.name
					}

				});
			},

		},
	}
</script>

<style lang="css" >
	.login-box {
		width: 450px;
		height: 400px;
		margin: 150px auto;
		border: 1px solid black;
		padding: 20px;
		border-radius: 10px;
		box-shadow: 0 0 40px black;
	}

	.el-button--succe {
		font-size: 16px;
		width: 100px;
		background: #006594;
		border: 1px solid #00FFFF;
		box-shadow: 0 0 10px #00FFFF;
		border-radius: 5px;
		color: #FFF;

	}



	.back {
    background: url("../assets/img/result.png") no-repeat center;
    height: 100%;
		width: 100%;
		background-size: cover;
		position: fixed;

	}


	.title {
    color: black;
		font-size: 20px;
		text-align: center;
	}

	.button {
		border: none;
		text-align: center;
	}

	.button::after {
		border: 0;
    width: 300px;
	}

	.button2 {
		text-align: right;
	}
  .label .el-form-item__label{
    color: black;
    font-size: 15px;
  }
</style>

