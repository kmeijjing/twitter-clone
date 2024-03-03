<template>
  <div
    v-if="$q.screen.width >= 1020"
    class="right-side-bar"
    :class="isSearchBar ? 'right-side-bar--search' : 'right-side-bar--no-search'"
  >
    <SearchForm v-if="isSearchBar" />

    <div class="container" ref="containerRef">
      <TrendsList v-if="isTrendList" class="q-my-md" />

      <RandomFollowList v-if="isRandomFollowList" />
    </div>
  </div>
</template>

<script>
import { onMounted, onUpdated, ref } from "vue";
import { Notify } from "quasar";
import { useRouter } from "vue-router";
import { useQuasar } from 'quasar'
import SearchForm from "src/components/SearchForm.vue";
import TrendsList from '@components/TrendsList.vue';
import RandomFollowList from "@components/RandomFollowList.vue";

export default {
  name: "RightSideBar",
  components: { SearchForm, TrendsList, RandomFollowList },
  props: {
    isSearchBar: {
      type: Boolean,
      default: true,
    },
    isTrendList: {
      type: Boolean,
      default: true,
    },
    isRandomFollowList: {
      type: Boolean,
      default: true,
    },
    mouseDeltaY: {
      type: Number,
      default: 0,
    }
  },
  setup(props) {
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
      setTimeout(() => {
        const screenHeight = $q.screen.height;
        const containerHeight = containerRef.value.offsetHeight;
        const topPosition  = props.isSearchBar ? '60px' : '12px';
        // console.log(containerRef)
        // console.log('screenHeight : ', screenHeight);
        // console.log('containerHeight : ', containerHeight);
        containerRef.value.style.top = screenHeight >= containerHeight ? topPosition : `-${containerHeight - screenHeight + 100}px`;

        console.log(containerRef.value.style.top);
      }, 3000)
    }

    onMounted(() => {
      setStickyTop();
    });

    onUpdated(() => {
    })

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
  padding: 0 4px 64px 16px;
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
  }
  > .container {
    position: sticky;
    position: -webkit-sticky;
    > .trends-list {
      background: $grey-1;
    }
    > .random-follow-list {
      background: $grey-1;
    }
  }
  &.right-side-bar--search {
    > .container {
      top: 60px;
    }
  }
  &.right-side-bar--no-search {
    > .container {
      top: 12px;
    }
  }
}
</style>
