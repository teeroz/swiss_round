<template>
  <div class="container my-4">
    <form class="container">
      <div class="row form-group">
        <label for="exampleInputTitle">제목</label>
        <input ref="title" type="text" class="form-control" aria-describeBy="TitleHelp" :placeholder="defaultTitle" maxlength="32" v-model="league.title" autofocus required @keyup.enter="submit">
        <small id="TitleHelp" class="form-text text-muted">입력하지 않을 경우 오늘 날짜로 입력됩니다.</small>
      </div>
      <div class="row form-group">
        <label for="exampleInputTie">순위</label>
        <select class="form-control mb-1" disabled>
          <option>승수</option>
        </select>
        <select class="form-control my-1" disabled>
          <option>부크홀츠</option>
        </select>
        <select class="form-control my-1" disabled>
          <option>승자승원칙</option>
        </select>
        <select class="form-control my-1" disabled>
          <option>최대연승수</option>
        </select>
        <select class="form-control my-1" disabled>
          <option>연승시작라운드</option>
        </select>
        <small id="descriptionHelp" class="form-text text-muted">위 순서에 따라 순위가 결정됩니다.</small>
      </div>
      <div class="row justify-content-end">
        <button type="button" class="btn btn-secondary col-2 mx-2" @click="cancel">취소</button>
        <button type="button" class="btn btn-primary col-2" @click="submit">확인</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'TheLeagueForm',

  props: {
    league: {
      type: Object,
      required: true
    },
    defaultTitle: {
      type: String,
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

  mounted: function () {
    this.$refs.title.focus()
  },

  methods: {
    cancel: function () {
      this.$router.go(-1)
    },

    submit: function () {
      if (this.league.title) {
        this.league.title = this.league.title.trim()
      }

      if (!this.league.title || this.league.title.length <= 0) {
        this.league.title = this.defaultTitle
      }

      this.submitCallback()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

