import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'first page',
    component: () => import('../views/FirstPage'),

  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    children: [
      {
        path: 'upload',
        component: () => import('@/views/upload.vue')
      },
      {
        path: '/patients/:patientId',
        name: 'PatientImages',
        component: () => import('@/views/PatientImages.vue')
      },
      {
        path: 'image',
        component: () => import('@/views/ImageShow.vue')
      },
      {
        path: 'imageBoard',
        component: () => import('@/views/ImageBoard.vue'),
      },
      {
        path: 'PatientBoard',
        component: () => import('@/views/PatientBoard.vue'),
      },
      {
        name: 'EditImage',
        path: '/edit/:imagePath',
        component: () => import('@/views/ImageShow.vue')
      },
      {
        name: 'CheckImage',
        path: '/check/:imagePath',
        component: () => import('@/views/ImagePathCheck.vue')
      },
      {
        name: 'ImagePathSegment',
        path: '/segment/:imagePath',
        component: () => import('@/views/ImagePathSegment.vue')
      },
      {
        name: 'ImagePathEdit',
        path: '/edit/:patientID',
        component: () => import('@/views/ImagePathEdit.vue')
      },
      {
        name: 'ImageIdShow',
        path: '/show/:patientID',
        component: () => import('@/views/ImageIdShow.vue')
      },
      {
        path: 'imageCheck',
        component: () => import('@/views/ImageCheck.vue')
      },
      {
        path: 'imageDetect',
        component: () => import('@/views/ImageDetect.vue')
      },
      {
        path: 'multiViewCheck',
        component: () => import('@/views/multiViewCheck.vue')
      },
      {
        name: 'ImageLabel',
        path: 'imageLabel',
        component: () => import('@/views/ImageLabel.vue')
      },
      {
        path: 'imageSegment',
        component: () => import('@/views/ImageSegment.vue')
      },
      {
        path: 'role',
        component: () => import('@/views/Role.vue')
      },
      {
        path: 'menu',
        component: () => import('@/views/Menu.vue')
      },
      {
        path: 'user',
        component: () => import('@/views/User.vue')
      },
      {
        path: 'notice',
        component: () => import('@/views/Notice.vue')
      },
      {
        path: 'noticeShow',
        component: () => import('@/views/noticeShow.vue')
      },
      {
        path: 'modelShow',
        component: () => import('@/views/modelShow.vue')
      },
    ]

  },
  {
    path: '/element',
    name: 'Element',
    component: () => import('../views/Element.vue')
  },
  {
    path: '/person',
    name: 'Person',
    component: () => import('../views/Person.vue')
  }
]
// 提供一个重置路由的方法
export const resetRouter = () => {
  router.matcher = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
  })
}
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
