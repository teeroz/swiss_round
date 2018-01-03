<template>
  <div>
    <the-navbar :title="league.title" :goBack="goBack">
      <div>
        <button type="button" class="btn btn-secondary navbar-toggler" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="fas fa-bars"></i>
        </button>
        <div class="dropdown-menu" style="right: 0; left: auto;">
          <button type="button" class="dropdown-item" @click="edit">수정</button>
          <div class="dropdown-divider"></div>
          <button type="button" class="dropdown-item" @click="remove">삭제</button>
        </div>
      </div>
    </the-navbar>

    <ul class="nav nav-tabs mt-2 league-tab">
      <li class="nav-item">
        <span class="nav-link" :class="{active: mode === 'PLAYERS'}" @click="showPlayers">
          플레이어
          <span 
              class="badge badge-pill" 
              :class="{'badge-primary': mode === 'PLAYERS', 'badge-secondary': mode !== 'PLAYERS'}"
              >
            {{ players.length }}
          </span>
        </span>
      </li>
      <li class="nav-item" @click="showRounds">
        <span class="nav-link" :class="{active: mode === 'ROUNDS'}">
          라운드
          <span 
              class="badge badge-pill" 
              :class="{'badge-primary': mode === 'ROUNDS', 'badge-secondary': mode !== 'ROUNDS'}"
              >
            {{ rounds.length }}
          </span>
        </span>
      </li>
    </ul>

    <div class="list-group" v-if="mode === 'PLAYERS'">
      <router-link
         v-for="(player, index) in players"
         :to="{name: 'player', params: {league_id: player.league, player_id: player.id}}"
         :key="player.id"
         class="list-group-item list-group-item-action border-left-0 border-right-0"
         >
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <span class="badge badge-secondary badge-pill">{{ player.ranking }}</span>
            <span :class="{'dropped': player.is_dropped, 'text-muted': player.is_dropped}">
              {{ player.name }}
            </span>
          </div>
          <span class="text-muted">
            <template v-if="player.wins > 0">{{ player.wins }}승</template>
            <template v-if="player.draws > 0">{{ player.draws }}무</template>
            <template v-if="player.loses > 0">{{ player.loses }}패</template>
          </span>
        </div>
      </router-link>

      <router-link
         :to="{name: 'playerAdd', params: {league_id: league.id}}"
         class="list-group-item list-group-item-action active border-left-0 border-right-0 d-flex justify-content-center"
         :class="{'mt-1': players.length <= 0}"
      >
        플레이어 추가
      </router-link>
    </div>

    <div class="list-group" v-if="mode === 'ROUNDS'">
      <router-link
         v-for="round in rounds"
         :to="{name: 'round', params: {league_id: round.league, round_id: round.id}}"
         :key="round.id"
         class="list-group-item list-group-item-action border-left-0 border-right-0"
      >
        {{ round.no }} 라운드
      </router-link>

      <span
         class="list-group-item list-group-item-action active border-left-0 border-right-0 d-flex justify-content-center"
         :class="{'mt-1': rounds.length <= 0}"
         @click="startNewRound"
      >
        새 라운드 시작
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeaguePage',

  data: function () {
    let mode = 'PLAYERS'
    if (this.$route.query.mode) {
      mode = this.$route.query.mode
    }

    return {
      league: { id: 0, title: '' },
      players: [],
      rounds: [],
      mode: mode
    }
  },

  created: function () {
    this.$axios.swiss.get(`league/${this.$route.params.league_id}`)
      .then(res => {
        this.league = res.data.league
        this.players = res.data.players
        this.rounds = res.data.rounds
      })
  },

  methods: {
    goBack: function () {
      this.$router.push({ name: 'leagues' })
    },

    edit: function () {
      this.$router.push({ name: 'leagueEdit', params: { league_id: this.$route.params.league_id } })
    },

    remove: function () {
      if (!confirm('정말로 이 리그를 삭제하시겠습니까?')) {
        return
      }

      this.$axios.swiss.delete(`league/${this.$route.params.league_id}`)
        .then(this.goBack)
    },

    showPlayers: function () {
      this.$router.replace({ name: 'league', params: { league_id: this.$route.params.league_id }, query: { mode: 'PLAYERS' } })
      this.mode = 'PLAYERS'
    },

    showRounds: function () {
      this.$router.replace({ name: 'league', params: { league_id: this.$route.params.league_id }, query: { mode: 'ROUNDS' } })
      this.mode = 'ROUNDS'
    },

    startNewRound: function () {
      this.$axios.swiss.post(`league/${this.$route.params.league_id}/round`)
        .then(res => {
          console.log(res.data)
          if (!res.data['id']) {
            alert('더 이상 라운드를 만들 수 없습니다.')
            return
          }

          this.$router.push({ name: 'round', params: { league_id: this.league.id, round_id: res.data.id } })
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .dropped {
    text-decoration: line-through;
  }
</style>
