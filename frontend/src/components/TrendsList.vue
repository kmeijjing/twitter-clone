<template>
  <q-card flat class="trends-list">
    <div class="card-title">Trends for you</div>
    <q-list>
      <TrendsListItem
        v-show="i < 5"
        v-for="(k, i) in keywords"
        :key="i"
        :keyword="k"
      />
      <q-item clickable @click="$router.push({ name: 'Trends' })">
        <q-item-section class="text-primary">
          Show more
        </q-item-section>
      </q-item>
    </q-list>
  </q-card>
</template>

<script>
import { defineComponent, ref, onBeforeMount } from "vue";
import { api } from "@boot/axios";

import TrendsListItem from '@components/TrendsListItem.vue';


export default defineComponent({
  components: { TrendsListItem },
  setup () {
    const keywords = ref([]);
    function getTrendList() {
      api.get('/trend').then((res) => {
        keywords.value = res.data.body;
      }).catch((err) => {
        console.log(err);
      }).finally(() => {
      })
    }

    onBeforeMount(() => {
      getTrendList();
    });


    return {
      keywords,
    };
  },
});
</script>

<style lang="scss">
.trends-list {
  overflow: hidden;
}
</style>
