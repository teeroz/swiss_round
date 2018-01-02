<script>
import axios from 'axios'

export default {
  install: function (Vue, options) {
    Vue.prototype.$axios = {
      swiss: {
        _request: function (method, path, params) {
          return new Promise((resolve, reject) => {
            method(`http://swiss.teeroz.net:8080/swiss/api/${path}`, params)
            // method(`http://localhost:8000/swiss/api/${path}`, params)
            .then(res => resolve(res))
            .catch(e => {
              if (e.response) {
                console.error(e.response.data)
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
      }
    }
  }
}
</script>
