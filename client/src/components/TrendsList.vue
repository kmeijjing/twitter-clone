<template>
  <q-card flat class="trends-list">
    <div class="card-title">Trend for you</div>
    <q-list>
      <TrendsListItem
        v-show="i < 5"
        v-for="(k, i) in keywords"
        :key="i"
        :keyword="k"
      />
    </q-list>
    <q-btn
      flat
      dense
      :ripple="false"
      label="Show more"
      color="primary"
      size="sm"
      to="/trends"
    />
  </q-card>
</template>

<script>
import { defineComponent, ref, onBeforeMount } from "vue";
import TrendsListItem from '@components/TrendsListItem.vue';


export default defineComponent({
  components: { TrendsListItem },
  setup () {
    const keywords = ref([]);
    function getTrendList() {
      keywords.value = [
        'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend', 'trend'
      ]
    }

    onBeforeMount(() => {
      getTrendList();
    })

    return {
      keywords,
    };
  },
});
</script>

<style lang="scss">
.trends-list {
  > .q-btn {
    margin: 12px 24px;
  }
}
</style>
