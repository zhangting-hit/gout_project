<template>
	<div class="back" >
    <img src="@/assets/img/logo_blue.png" alt="" style="width: 50px; height: 50px; margin-left:40px; margin-top: -15px;">
    <span class="title" style="font-size: 40px;margin-left:40px;  font-weight:700;  letter-spacing:20px;">痛风图像分割系统</span>
		<div style="  color: #F7F9FA ;margin-top: -100px">
			<el-form label-width="80px" label-position="left" ref="form" :model="form" :rules="rules" style="" class="login-box"  size="mini" >
        <div style="margin-bottom: 40px">
          <span style="font-size: 30px; color: black;">欢迎注册</span>
          <div style="font-size: 15px; color: black;">
            已有账号 ？<router-link to="/login" class="title" style="color: #1E6CA9; font-size: 15px">登录</router-link>
          </div>
        </div>
        <el-form-item label="用户类型" class="label"  >
          <el-select v-model="form.roleId" placeholder="请选择用户类型" style="width: 330px">
            <el-option label="管理员" value=1></el-option>
            <el-option label="技术人员" value=2></el-option>
            <el-option label="医护人员" value=3></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="用户名" class="label">
          <el-input type="text" placeholder="请设置用户名" v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="密码" class="label">
          <el-input type="password" placeholder="请设置密码"  v-model="form.pwd"></el-input>
        </el-form-item>
<!--        <el-form-item label="手机号" class="label">-->
<!--          <el-input type="phone" placeholder="可用于登录和找回密码"  v-model="sizeForm.name"></el-input>-->
<!--        </el-form-item>-->
<!--        <el-form-item label="验证码" class="label">-->
<!--          <el-input type="key" placeholder="请输入验证码"  v-model="sizeForm.name" style="width: 200px;"></el-input>-->
<!--          <el-button  type="primary"   style="width: 100px;  font-size: 15px; margin-left: 25px"  >获取验证码</el-button>-->
<!--        </el-form-item>-->
				<el-form-item class="button">
					<el-button  type="primary" round @click="onSubmit" style="width: 200px; margin-left: -50px;  margin-top: 8px; font-size: 15px"  >注册</el-button>
				</el-form-item>
			</el-form>
		</div>
	</div>
</template>

<script>
	import axios from 'axios';
	export default {
		name: 'Register',
		data() {
			return {
				form: {
					name: '',
					pwd: '',
          roleId : '',
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
			}
		},
		methods: {
			onSubmit() {
				const msg = {
					name: this.form.name,
					password: this.form.pwd,
          roleId: this.form.roleId,
					// password2: this.form.pwd2,
					// password3:this.form.pwd3,
					// source: this.form.resource
				};
				axios.post('http://localhost:5000/user_register', msg).then((res) => {
					var success = res.data.status;
					if (success === 'success') {
            this.$message({
							message: '注册成功，请登录！',
							type: 'success'
						});
						this.run();
					} else if (success === 'failed') {
						this.$message({
							message: '请检查输入信息！',
							type: 'warning'
						});
					} else {
						this.$message({
							message: '账号已被注册',
							type: 'warning'
						});
					}

				})


			},
			tologin() {
				this.$router.push({
					name: 'Login'
				});
			},
			run() {
				this.$router.push("/login");
			},

		},
	}
</script>

<style lang="css" >
	.login-box {
		width: 450px;
		height: 450px;
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

