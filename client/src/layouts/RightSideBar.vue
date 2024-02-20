<template>
  <div class="right-side-bar">
    <q-form class="search-form flex items-center row" @submit="goSearch(searchVal)">
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

    <div class="container" ref="containerRef">
      <TrendsList class="q-my-md" />

      <RandomFollowList />
    </div>
  </div>
</template>

<script>
import TrendsList from '@components/TrendsList.vue';
import RandomFollowList from "@components/RandomFollowList.vue";
import { onMounted, ref } from "vue";
import { Notify } from "quasar";
import { useRouter } from "vue-router";
import { useQuasar } from 'quasar'

export default {
  name: "RightSideBar",
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

    const $q = useQuasar();
    const containerRef = ref(null);
    function setStickyTop() {
      const screenHeight = $q.screen.height;
      const containerHeight = containerRef.value.offsetHeight;

      console.log(screenHeight)
      console.log(containerHeight)
      containerRef.value.style.top = screenHeight >= containerHeight ? '66px' : `-${containerHeight - screenHeight + 100}px`;
    }

    onMounted(() => {
      setStickyTop();
    });

    return {
      searchVal,
      goSearch,
      containerRef,
    };
  },
};
</script>

<style lang="scss">
.right-side-bar {
  width: 350px;
  min-width: 350px;
  padding: 0 4px 16px 16px;
  border-left: 1px solid rgba(0,0,0,0.12);
  > .search-form {
    width: 100%;
    height: 50px;
    position: sticky;
    top: 0;
    right: 0;
    z-index: 99;
    border-radius: 0;
    background: white;
    color: block;
    .q-field {
      height: 40px;
      min-height: 0;
      width: 100%;
      &__inner {
        .q-field__control {
          &:before {
            border: none;
            background: $grey-2;
          }
        }
      }


    }
  }
  > .container {
    position: sticky;
    position: -webkit-sticky;
    top: 66px;
    > .trends-list {
      background: $grey-1;
    }
    > .random-follow-list {
      background: $grey-1;
    }
  }

}
</style>
