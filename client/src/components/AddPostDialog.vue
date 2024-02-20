<template>
  <q-dialog ref="dialogRef" class="add-post-dialog">
    <q-card>
      <q-card-actions class="row">
        <q-btn flat dense round icon="close" color="grey-10" @click="onDialogCancel()" class="close-btn" />
        <q-space />
        <q-btn flat rounded no-caps label="Draft" color="primary" />
      </q-card-actions>

      <AddPostCard @success="onDialogOK" />
    </q-card>
  </q-dialog>
</template>

<script>
import { ref } from "vue";
import { useDialogPluginComponent } from "quasar";
import AddPostCard from "@components/AddPostCard.vue";

const selectOptions = [
  { label: "Everyone", value: "every" },
  { label: "People you follow", value: "follower" },
  { label: "Only people you mention", value: "mentionPeople" },
];

export default {
  name: "AddPostDialog",
  components: { AddPostCard },
  setup() {
    const { dialogRef, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();

    const selectVal = ref(selectOptions[0]);

    return {
      dialogRef,
      onDialogOK,
      onDialogCancel,

      selectOptions,
      selectVal,
    };
  },
};
</script>

<style lang="scss">
.add-post-dialog {
  .q-dialog__inner {
    > .q-card {
      width: 100%;
      .q-card__actions {
        height: 48px;
        padding: 12px;
      }
      .add-post-card {
        padding: 12px;
      }
    }
  }
}
</style>
