<template>
  <div>
    <the-navbar mode="HOME">
    </the-navbar>


  <div class="container">
    <div class="card mt-3">
      <div class="card-body">
        <p class="card-text mb-1">
          스위스 라운드 방식의 리그를 위한 비영리 목적의 어플입니다. 
          사설 리그를 운영하기 위하여 만들었으나 필요한 분들을 위하여 공개하였습니다.
          사용하면서 궁금한 점이나 개선에 대한 의견이 있으면 이메일로 연락주세요.
        </p>
        <h6 class="text-muted mb-4">by prophet75 at gmail.com</h6>
        <div class="text-center">
          <img src="/static/facebook-login.png" width="238" height="40" @click="authenticate('facebook')"/>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',

  data: function () {
    return { }
  },

  methods: {
    authenticate: function (provider) {
      this.$auth.authenticate(provider)
        .then(res => {
          this.$auth.user = {
            id: res.data.id,
            name: res.data.name
          }
          this.$router.push({ name: 'leagues' })
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
