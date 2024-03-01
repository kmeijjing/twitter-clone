<template>
  <q-page class="trends-page flex row no-wrap">
    <div class="left-part full-width">
      <q-card class="page-header flex items-center justify-between full-width" flat>
        <q-card-section class="q-pa-none flex items-center">
          <q-btn flat dense round :ripple="false" icon="arrow_back" @click="router.go(-1)" class="q-mr-md"></q-btn>
          <strong>Trends</strong>
        </q-card-section>

        <q-btn flat round dense :ripple="false" icon="settings" class="q-ml-md"></q-btn>
      </q-card>

      <q-card flat>
        <q-list>
          <TrendsListItem
            v-for="(k, i) in keywords"
            :key="i"
            :keyword="k"
          />
        </q-list>
      </q-card>
    </div>

    <RightSideBar :isTrendList="false" />
  </q-page>
</template>

<script>
import { ref, onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';
import { api } from "@boot/axios";
import TrendsListItem from '@components/TrendsListItem.vue';
import RightSideBar from 'src/layouts/RightSideBar.vue';
// import RandomFollowComponent from "@components/common/RandomFollowComponent.vue";



export default {
  name: 'TrendsPage',
  components: { TrendsListItem, RightSideBar },
  setup() {
    const router = useRouter();
    const keywords = ref([]);

    function getTrendList() {
      api.get('/trend').then((res) => {
        keywords.value = res.data.body;
      }).catch((err) => {
        console.log(err);
      }).finally(() => {
      })
    }

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

    onBeforeMount(() => {
      getTrendList();
    })

    return {
      router,
      keywords,
      searchVal,
      goSearch,
    }
  },
}
</script>

<style lang="scss">
.trends-page {
  .left-part {
    padding: 0 0 20px;
    max-width: 600px;
    border-right: 1px solid rgb(239, 243, 244);
    .page-header {
      padding: 0 24px;
      .q-card__section {
        font-size: 18px;
      }
    }
  }
  .right-part {
    min-width: 350px;
    max-width: 350px;
    flex-grow: 1;
    position: relative;
    padding: 70px 10px 20px 16px;
    width: 100%;
    .right-page-header {
      width: 100%;
      max-width: 350px;
      height: 50px;
      position: fixed;
      top: 0;
      right: 0;
      z-index: 99;
      border-radius: 0;
      background: rgba(255, 255, 255, 0.75);
      color: block;
      .q-card__section {
        display: flex;
        align-items: center;
        padding: 0 10px 0 16px;
        .q-field {
          height: 40px;
          min-height: 0;
          width: 100%;
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
    > .random-follow-component {
      background: rgba(232, 234, 246, 0.5);
    }
  }
}
</style>
