<template>
  <div>
    <the-navbar mode="HOME">
    </the-navbar>

    <div class="container">
      <div class="card mt-3">
        <div class="card-body">
          <div class="text-center mb-5">
            <div class="row justify-content-center mb-2">
              <img src="/static/facebook-login.png" width="222" height="49" @click="authenticate('facebook')" />
            </div>
            <div class="row justify-content-center mb-2">
              <img src="/static/kakao-login.png" width="222" height="49" @click="authenticate('github')" />
            </div>
            <div class="row justify-content-center mb-2">
              <input ref="username" type="text" class="form-control mr-1" style="width: 150px;" placeholder="username" maxlength="20">
              <button type="button" class="btn btn-primary" @click="login()">로그인</button>
            </div>
          </div>

          <h5 class="card-title">변경사항</h5>
          <p class="card-text mb-4">
            <small>
              <strong>v1.3.0</strong>&nbsp;&nbsp;<span class="text-muted">at 2018.05.28</span><br />
              - 카카오 계정으로 로그인 하기 추가<br />
            </small>
            <small>
              <strong>v1.2.2</strong>&nbsp;&nbsp;<span class="text-muted">at 2018.01.11</span><br />
              - 승점 계산할 때 승 3점, 무 1점으로 변경 (기존 승 2점, 무 1점) <br />
              - 리그 생성할 때 로그인 화면으로 튕기는 버그 픽스 <br />
              - 리그 플레이어 목록에서 경기 시작 전에 승무패 표시하지 않도록 수정 <br />
            </small>
          </p>
          <h5 class="card-title">소개</h5>
          <p class="card-text mb-1">
            <small>
              스위스 라운드 방식의 리그를 위한 비영리 목적의 어플입니다. 
              사설 리그를 운영하기 위하여 만들었으나 필요한 분들을 위하여 공개하였습니다.
              사용하면서 궁금한 점이나 개선에 대한 의견이 있으면 이메일로 연락주세요. <br />
              <span class="text-muted">by prophet75 at gmail.com</span>
            </small>
          </p>
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
    },

    login: function () {
      if (!this.$refs.username.value) {
        alert('로그인 아이디를 입력해주세요.')
        return
      }

      this.$auth.login({ username: this.$refs.username.value }).then(res => {
        this.$auth.user = {
          id: res.data.name,
          name: res.data.name
        }
        this.$router.push({ name: 'leagues' })
      })
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
