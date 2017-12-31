<template>
  <div class="container my-4">
    <form class="container">
      <div class="row form-group">
        <label for="exampleInputName">이름</label>
        <input ref="name" type="text" class="form-control" placeholder="홍길동" maxlength="8" v-model="player.name" autofocus required>
      </div>
      <div class="row form-group">
        <label for="exampleInputMemo">메모</label>
        <input type="text" class="form-control" maxlength="64" v-model="player.memo">
      </div>
      <div class="row justify-content-end">
        <button type="button" class="btn btn-secondary col-2 mx-2" @click="cancel">취소</button>
        <button type="submit" class="btn btn-primary col-2" @click="submit">확인</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'ThePlayerForm',

  props: {
    player: {
      type: Object,
      required: true
    },
    submitCallback: {
      type: Function,
      required: true
    }
  },

  data: function () {
    return { }
  },

  methods: {
    cancel: function () {
      this.$router.go(-1)
    },

    submit: function () {
      if (!this.player.name.trim()) {
        alert('이름을 입력해주세요.')
        return
      }

      if (this.player.name) {
        this.player.name = this.player.name.trim()
      }

      if (this.player.memo) {
        this.player.memo = this.player.memo.trim()
      }

      this.submitCallback()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
