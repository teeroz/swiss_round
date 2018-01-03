<template>
  <div>
    <the-navbar :title="player.name">
      <div>
        <button type="button" class="btn btn-secondary navbar-toggler" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="fas fa-bars"></i>
        </button>
        <div class="dropdown-menu" style="right: 0; left: auto;">
          <button type="button" class="dropdown-item" @click="editBasic">수정</button>
          <div class="dropdown-divider"></div>
          <template v-if="player.is_dropped">
            <button type="button" class="dropdown-item" @click="undrop">참가</button>
          </template>
          <template v-else>
            <button type="button" class="dropdown-item" @click="drop">드랍</button>
          </template>
          <div class="dropdown-divider"></div>
          <button type="button" class="dropdown-item" @click="editFamily">가족설정</button>
        </div>
      </div>
    </the-navbar>

    <div class="container">
      <div class="card my-4">
        <div class="card-header text-white bg-secondary">
          기본정보
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <span>이름</span>
            <span class="text-muted">{{ player.name }}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center" v-if="player.memo">
            <span>메모</span>
            <span class="text-muted">{{ player.memo }}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center" v-if="player.family.length > 0">
            <span>가족</span>
            <span class="text-muted">
              <template v-for="(familyMember, index) in player.family">
                {{ familyMember.name }}<template v-if="index+1 < player.family.length">,</template>
              </template>
            </span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <span>상태</span>
            <span class="text-muted">{{ player.is_dropped ? '기권' : '참가중' }}</span>
          </li>
        </ul>
      </div>

      <div class="card my-4">
        <div class="card-header text-white bg-secondary">
          성적
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <span>순위</span>
            <span class="text-muted">{{ player.ranking }}위</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <span>승패</span>
            <span class="text-muted">
              <template v-if="player.wins > 0">{{ player.wins }}승</template>
              <template v-if="player.draws > 0">{{ player.draws }}무</template>
              <template v-if="player.loses > 0">{{ player.loses }}패</template>
            </span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <span>상대승수합</span>
            <span class="text-muted">{{ player.opponents_total_wins }}승</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center">
            <span>최대연승</span>
            <span class="text-muted">
              <template v-if="player.max_strikes_count > 0">
                {{ player.max_strikes_count }}연승
              </template>
              <template v-if="player.max_strikes_count <= 0">
                X
              </template>
            </span>
          </li>
        </ul>
      </div>

      <div class="card my-4" v-if="matches.length > 0">
        <div class="card-header text-white bg-secondary">
          대전기록
        </div>
        <ul class="list-group list-group-flush">
          <li 
            v-for="match in matches"
            :key="match.id"
            class="list-group-item d-flex justify-content-between align-items-center" 
            >
            <span @click="goPlayerPage(match.opponent)">
              <small>vs</small> {{ match.opponent.name }} 
              <small class="text-muted">{{ match.opponent.wins }}승</small>
            </span>
            <button 
              type="button" 
              class="btn btn-sm ml-1"
              :class="{'btn-secondary': match.result == 'D', 
                       'btn-primary': match.result == 'W', 
                       'btn-danger': match.result == 'L'}"
              >
              <template v-if="match.result == 'W'">승</template>
              <template v-else-if="match.result == 'L'">패</template>
              <template v-else>무</template>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayerPage',

  data: function () {
    return {
      player: { id: 0, name: '', family: [] },
      matches: []
    }
  },

  created: function () {
    this.$axios.swiss.get(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`)
      .then(res => {
        this.player = res.data.player
        this.matches = res.data.matches
      })
  },

  methods: {
    editBasic: function () {
      this.$router.push({ name: 'playerEditBasic', params: { league_id: this.$route.params.league_id, player_id: this.$route.params.player_id } })
      return false
    },

    editFamily: function () {
      this.$router.push({ name: 'playerEditFamily', params: { league_id: this.$route.params.league_id, player_id: this.$route.params.player_id } })
      return false
    },

    drop: function () {
      this.$axios.swiss.put(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`, { is_dropped: true })
        .then(res => {
          this.player = res.data.player
        })
    },

    undrop: function () {
      this.$axios.swiss.put(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`, { is_dropped: false })
        .then(res => {
          this.player = res.data.player
        })
    },

    goPlayerPage: function (player) {
      if (player.is_ghost) {
        return
      }

      this.$router.push({ name: 'player', params: { league_id: this.$route.params.league_id, player_id: player.id } })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
