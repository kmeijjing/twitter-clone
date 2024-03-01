<template>
  <q-page class="explore-page flex row no-wrap">
    <div class="page-container">
      <div class="page-header flex no-wrap items-center">
        <SearchForm />
        <q-btn flat round icon="settings" color="grey-8" class="q-ml-lg"></q-btn>
      </div>

      <div class="main-img">
        <img src="https://pbs.twimg.com/semantic_core_img/1473076380644478980/R44e40mQ?format=jpg&name=small" width="100%" />
      </div>

      <TrendsList />
    </div>

    <RightSideBar :isTrendList="false" :isSearchBar="false" />
  </q-page>
</template>

<script>
import SearchForm from "src/components/SearchForm.vue";
import TrendsList from '@components/TrendsList.vue';
import RightSideBar from "src/layouts/RightSideBar.vue";

export default {
  name: "ExplorePage",
  components: { SearchForm, TrendsList, RightSideBar },
  setup() {
    return {
    };
  },
};
</script>

<style lang="scss">
.explore-page {
  .page-container{
    max-width: 600px;
    padding: 0 0 20px;
    .trends-list {
      border-radius: 0px;
    }
  }
}
</style>
