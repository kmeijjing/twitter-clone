<template>
  <q-card flat class="random-follow-list">
    <div class="card-title">Who to follow</div>
    <q-list>
      <RandomFollowListItem
        v-for="(u, i) in randomUsers"
        :key="i"
        :id="u.id"
        :name="u.name"
        :email="u.email"
        :bio="u.bio"
        :bioShow="false"
        :profile_image="u.profile_image"
      />
    </q-list>
    <q-btn
      flat
      dense
      :ripple="false"
      label="Show more"
      color="primary"
      size="sm"
    />
  </q-card>
</template>

<script>
import { ref, onBeforeMount } from "vue";
import { Cookies } from "quasar";
import RandomFollowListItem from "@components/RandomFollowListItem.vue";

export default {
  name: "RandomFollowList",
  components: { RandomFollowListItem },

  setup () {
    const user = Cookies.get('user');
    const randomUsers = ref([]);

    function getUserRandom() {
    }

    onBeforeMount(() => {
      getUserRandom();
    })

    return {
      randomUsers,
    }
  }

}
</script>

<style lang="scss">
.random-follow-list {
  > .q-btn {
    margin: 12px 24px;
  }
  .desc {
    padding: 0 16px;
    margin: -10px 0 12px;
    font-size: 13px;
    color: $grey-7;
  }
  .chips {
    padding: 0 16px;
    .q-chip {
      &__content {
        margin-right: 10px;
      }
    }
  }
}
</style>
