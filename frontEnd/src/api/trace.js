import request from '@/utils/request'

export function fetchProduct(productID) {
  return request({
    url: '/api/trace/',
    // baseURL: process.env.VUE_APP_BASE_API2,
    baseURL: 'http://127.0.0.1:5000',
    method: 'GET',
    params: { productID }
  })
}

export function createProduct(data) {
  return request({
    url: '/api/add/',
    baseURL: 'http://127.0.0.1:5000',
    method: 'POST',
    data
  })
}
