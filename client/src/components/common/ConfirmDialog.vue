<template>
  <q-dialog ref="dialogRef" class="confirm-dialog">
    <q-card>
      <q-card-section>
        <div class="title">{{ title }}</div>
        <div class="desc">{{ desc }}</div>
      </q-card-section>
      <q-card-actions class="flex column">
        <q-btn
          rounded
          dense
          no-caps
          :label="firstBtnLabel"
          :color="firstBtnColor"
          @click="onDialogOK()"
        />
        <q-btn
          rounded
          dense
          outline
          no-caps
          :label="secondBtnLabel"
          color="grey-5"
          @click="onDialogCancel()"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent } from "quasar";

export default {
  name: "ConfirmDialog",
  props: {
    title: {
      type: String,
      default: "",
    },
    desc: {
      type: String,
      default: "",
    },
    firstBtnLabel: {
      type: String,
      default: "",
    },
    firstBtnColor: {
      type: String,
      default: 'black',
    },
    secondBtnLabel: {
      type: String,
      default: "",
    },
  },
  setup() {
    const { dialogRef, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();

    return {
      dialogRef,
      onDialogOK,
      onDialogCancel,
    };
  },
};
</script>

<style lang="scss">
.confirm-dialog {
  .q-dialog__inner {
    .q-card {
      width: 400px;
      padding: 24px;
      border-radius: 12px;
      position: relative;
      .q-card__section {
        .title {
          font-weight: 700;
          font-size: 20px;
        }
        .desc {
          margin-top: 8px;
        }
      }
      .q-card__actions {
        margin-top: 12px;
        .q-btn {
          width: 100%;
          height: 40px;
          margin: 4px 0;
          &__content {
            .block {
              font-size: 15px;
              font-weight: 700;
            }
          }
          &:last-of-type {
            .q-btn__content {
              .block {
                color: black;
              }
            }
          }
        }
      }
    }
  }
}
</style>
