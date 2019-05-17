<script>
import axios from 'axios'
import router from '../router/index.js'

export default {
  install: function (Vue) {
    Vue.prototype.$axios = {
      swiss: {
        _request: function (method, path, params) {
          return new Promise(resolve => {
            method(`http://swiss.teeroz.net:8080/swiss/api/${path}`, params)
            .then(res => resolve(res))
            .catch(e => {
              if (e.response) {
                if (e.response.status === 403) {
                  router.push({ name: 'login' })
                  return
                } else if (e.response.status === 404) {
                  router.push({ name: 'login' })
                  return
                }

                // console.error(e.response.data)
              }
              alert(e.toString())
            })
          })
        },

        get: function (path, params) {
          return this._request(axios.get, path, params)
        },

        post: function (path, params) {
          return this._request(axios.post, path, params)
        },

        put: function (path, params) {
          return this._request(axios.put, path, params)
        },

        delete: function (path, params) {
          return this._request(axios.delete, path, params)
        }
      },

      facebook: {
        _request: function (method, path, params) {
          return new Promise(resolve => {
            method(`https://graph.facebook.com/v2.11/${path}`, params)
            .then(res => resolve(res))
            .catch(e => {
              /*
              if (e.response) {
                console.error(e.response.data)
              }
              */
              alert(e.toString())
            })
          })
        },

        get: function (path, params) {
          return this._request(axios.get, path, params)
        }
      }
    }
  }
}
</script>
