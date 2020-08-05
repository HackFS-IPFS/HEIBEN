import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/user/login/',
    // url: '/vue-element-admin/user/login',
    method: 'POST',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/api/user/info/',
    // url: '/vue-element-admin/user/info',
    method: 'GET',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/api/user/logout/',
    // url: '/vue-element-admin/user/login',
    method: 'POST'
  })
}
