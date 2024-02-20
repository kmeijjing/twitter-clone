<template>
  <q-page class="explore-page flex row no-wrap">
    <div class="page-container">
      <div class="page-header flex no-wrap items-center">
        <q-form class="full-width" @submit="goSearch(searchVal)">
          <q-input
            v-model="searchVal"
            dense
            outlined
            rounded
            placeholder="Search for..."
          >
            <template v-slot:prepend>
              <q-icon name="search" />
            </template>
          </q-input>
        </q-form>
        <q-btn flat round icon="settings" color="grey-8" class="q-ml-lg"></q-btn>
      </div>

      <div class="main-img">
        <img src="https://pbs.twimg.com/semantic_core_img/1473076380644478980/R44e40mQ?format=jpg&name=small" width="100%" />
      </div>

      <TrendsList />
    </div>

    <div class="right-side">
      <RandomFollowList />
    </div>
  </q-page>
</template>

<script>
import { ref } from "vue";
import { Notify } from "quasar";
import { useRouter } from "vue-router";
import TrendsList from '@components/TrendsList.vue';
import RandomFollowList from "@components/RandomFollowList.vue";

export default {
  name: "ExplorePage",
  components: { TrendsList, RandomFollowList },
  setup() {
    const router = useRouter();
    const searchVal = ref("");

    function goSearch(val) {
      if (val) {
        router.push(`/search?q=${val}`);
      } else {
        Notify.create({
          classes: "toast-message",
          message: "검색어를 입력해주세요.",
          color: "negative",
          position: "bottom",
        });
      }
    }

    return {
      searchVal,
      goSearch,
    };
  },
};
</script>

<style lang="scss">
.explore-page {
  .page-container{
    max-width: 600px;
    padding: 0 0 20px;
    > .page-header {
      .q-form {
        .q-field {
          height: 40px;
          min-height: 0;
          // width: calc(100% - 62px);
          &__inner {
            .q-field__control {
              &:before {
                border: none;
                background: rgba(232, 234, 246, 0.5);
              }
            }
          }
        }
      }
    }
  }
  .right-side {
    min-width: 350px;
    padding: 16px 4px 16px 16px;
    border-left: 1px solid rgba(0,0,0,0.12);
    > .random-follow-list {
      background: $grey-1;
    }
  }
}
</style>
