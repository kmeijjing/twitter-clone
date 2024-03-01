<template>
  <q-item
    clickable
    target="_self"
    :to="link"
    :active="$route.path === link"
    class="gnb-item"
    active-class="active-item"
  >
    <q-item-section v-if="icon" avatar>
      <q-icon flat round :name="icon" :color="color" />
    </q-item-section>

    <q-item-section class="" style="align-items: start; font-size: 20px;">
      {{ title }}
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "EssentialLink",
  props: {
    title: {
      type: String,
      required: true,
    },
    caption: {
      type: String,
      default: "",
    },
    link: {
      type: String,
      default: "",
    },
    icon: {
      type: String,
      default: "",
    },
    activeIcon: {
      type: String,
      default: "",
    },
    color: {
      type: String,
      default: "grey-10",
    },
  },
});
</script>

<style lang="scss">
.gnb-item {
  padding: 0 24px 0 16px;
  border-radius: 24px;
  width: fit-content;
  .q-item__section {
    min-width: 0;
    .q-icon {
      font-size: 30px !important;
    }
  }
  &.active-item {
    .q-item__section {
      color: $primary !important;
      font-weight: 800;
      .q-icon {
        color: $primary !important;
      }
    }
  }
}
</style>
