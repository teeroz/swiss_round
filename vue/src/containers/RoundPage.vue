<template>
  <div>
    <the-navbar :title="round.no + ' 라운드'" :goBack="goBack">
      <div>
        <button type="button" class="btn btn-secondary navbar-toggler" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="fas fa-bars"></i>
        </button>
        <div class="dropdown-menu" style="right: 0; left: auto;">
          <button type="button" class="dropdown-item" @click="remove">삭제</button>
        </div>
      </div>
    </the-navbar>

    <the-loading ref="loading">
      <div class="list-group">
        <span
           v-for="match in matches"
           :key="match.id"
           class="list-group-item border-left-0 border-right-0"
           >
          <div class="d-flex justify-content-center">
            <div class="col-6 text-right">
              <span @click="goPlayerPage(match.player1)">
                <small>{{ match.player1.wins }}승</small> {{ match.player1.name }}
              </span>
              <button 
                type="button" 
                class="btn btn-sm ml-1"
                :class="{'btn-secondary': match.score1 == match.score2, 'btn-primary': match.score1 > match.score2, 'btn-danger': match.score1 < match.score2}"
                @click="updateScore(match, match.score1 ? 0 : 1, 0)"
                >
                <template v-if="match.score1 > match.score2">승</template>
                <template v-else-if="match.score1 < match.score2">패</template>
                <template v-else>무</template>
              </button>
            </div>
            <div><small>vs</small></div>
            <div class="col-6 text-left">
              <button 
                type="button" 
                class="btn btn-sm mr-1"
                :class="{'btn-secondary': match.score2 == match.score1, 'btn-primary': match.score2 > match.score1, 'btn-danger': match.score2 < match.score1}"
                @click="updateScore(match, 0, match.score2 ? 0 : 1)"
                >
                <template v-if="match.score2 > match.score1">승</template>
                <template v-else-if="match.score2 < match.score1">패</template>
                <template v-else>무</template>
              </button>
              <span @click="goPlayerPage(match.player2)">
                {{ match.player2.name }} <small>{{ match.player2.wins }}승</small>
              </span>
            </div>
          </div>
        </span>
      </div>

      <div class="text-center my-3">
        <button 
          type="button" 
          class="btn" 
          :class="{'btn-primary': isComplete, 'btn-secondary': !isComplete}"
          @click="nextRound"
          :disabled="!isComplete">
          <i class="fas fa-arrow-right"></i> <strong><span>다음 라운드 시작하기</span></strong>
        </button>
      </div>
    </the-loading>
  </div>
</template>

<script>
export default {
  name: 'RoundPage',

  data: function () {
    return {
      round: { no: '' },
      matches: [],
      isComplete: false
    }
  },

  created: function () {
    this.$axios.swiss.get(`league/${this.$route.params.league_id}/round/${this.$route.params.round_id}`)
      .then(res => {
        this.round = res.data.round
        this.matches = res.data.matches
        this.checkIsComplete()
        this.$refs.loading.stop()
      })
  },

  methods: {
    goBack: function () {
      this.$router.push({ name: 'league', params: { id: this.$route.params.league_id }, query: { mode: 'ROUNDS' } })
    },

    remove: function () {
      if (!confirm('정말로 이 라운드를 삭제하시겠습니까?')) {
        return false
      }

      this.$refs.loading.start()
      this.$axios.swiss.delete(`league/${this.$route.params.league_id}/round/${this.$route.params.round_id}`)
        .then(this.goBack)
    },

    nextRound: function () {
      this.$refs.loading.start()

      this.$axios.swiss.post(`league/${this.$route.params.league_id}/round`)
        .then(res => {
          if (!res.data['id']) {
            alert('더 이상 라운드를 만들 수 없습니다.')
            this.$refs.loading.stop()
            return
          }

          this.$router.push({ name: 'round', params: { league_id: this.$route.params.league_id, round_id: res.data.id } })
        })
    },

    updateScore: function (match, score1, score2) {
      match.score1 = score1
      match.score2 = score2

      this.$axios.swiss.put(`league/${this.$route.params.league_id}/round/${this.$route.params.round_id}/match/${match.id}`,
        {score1: score1, score2: score2})
        .then(res => {
          this.matches = res.data.matches
          this.checkIsComplete()
        })
    },

    goPlayerPage: function (player) {
      if (player.is_ghost) {
        return
      }

      this.$router.push({ name: 'player', params: { league_id: this.$route.params.league_id, player_id: player.id } })
    },

    checkIsComplete: function () {
      let isComplete = true
      for (const key in this.matches) {
        const match = this.matches[key]
        if (match.score1 === match.score2) {
          isComplete = false
          break
        }
      }
      this.isComplete = isComplete
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
