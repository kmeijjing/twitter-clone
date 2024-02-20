<template>
  <q-layout view="lHh lpR lFf">
    <LeftSideMenu v-if="$q.platform.is.desktop" />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from "vue";
import LeftSideMenu from "./LeftSideMenu.vue";

export default defineComponent({
  name: "MainLayout",
  components: {
    LeftSideMenu,
  },

  setup() {
    return {
    };
  },
});
</script>

<style lang="scss">
@media screen and (max-width: 1190px) {
  .q-layout {
    .q-page-container {
      padding-left: 70px !important;
    }
  }
}
</style>
