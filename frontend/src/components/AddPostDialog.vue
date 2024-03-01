<template>
  <q-dialog ref="dialogRef" class="add-post-dialog">
    <q-card>
      <q-card-actions class="flex row items-center justify-between">
        <q-btn flat dense round icon="close" color="grey-9" @click="onDialogCancel()" class="close-btn" />
        <q-space />
        <q-btn flat rounded no-caps label="Drafts" color="primary" class="draft-btn" />
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
        height: 54px;
        padding: 0 12px;
        .close-btn {
          .q-btn__content {
            .q-icon {
              font-size: 20px;
            }
          }
        }
        .draft-btn {
          height: 32px;
          min-height: 32px;
          padding: 0;
          .q-btn__content {
            .block {
              font-size: 14px;
              font-weight: 700;
            }
          }
        }
      }
      .add-post-card {
        padding: 16px;
        .q-card__section {
          .q-form {
            .form-bottom {
              margin-left: -50px;
            }
          }
        }
      }
    }
  }
}
</style>
