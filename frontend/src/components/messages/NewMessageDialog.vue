<template>
  <q-dialog persistent ref="dialogRef" class="new-message-dialog" @keydown.esc="onDialogCancel">
    <q-card>
      <q-card-section class="dialog-header flex row items-center" flat>
        <q-btn
          flat
          dense
          round
          :ripple="false"
          icon="close"
          class="close-btn"
          @click="onDialogCancel"
        />
        <strong>New message</strong>
        <!-- <q-btn
          rounded
          :ripple="false"
          no-caps=""
          color="black"
          label="next"
          :disable="!peopleArr.length"
          class="next-btn"
          @click="createChat(peopleArr)"
        /> -->
      </q-card-section>

      <q-card-section class="search-section">
        <q-input
          v-model="searchVal"
          dense
          rounded
          autofocus
          placeholder="Search people"
          @update:modelValue="goSearch(searchVal)"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>
      </q-card-section>

      <!-- <q-card-section v-if="peopleArr.length" class="chip-section">
        <q-chip
          v-for="(p, i) in peopleArr"
          :key="i"
          removable
          outline
          :ripple="false"
          color="indigo-2"
          class="text-black"
          @remove="removePeople(i)"
        >
          <q-avatar class="bg-deep-purple-1">
            <img v-if="p.profile_image" :src="`profileImgs/${p.id}/${p.profile_image}`">
            <q-icon v-else name="person" color="indigo-3" size="16px" />
          </q-avatar>
          {{ p.name }}
        </q-chip>
      </q-card-section>
      <q-separator v-if="peopleArr.length" color="indigo-2" /> -->

      <q-scroll-area style="height: 450px" visible>
        <q-list>
          <q-item
            clickable
            v-for="(s, i) in searchResultArr"
            :key="i"
            @click="addPeople(i)"
          >
            <q-avatar class="bg-deep-purple-1" size="48px">
              <img v-if="s.profile_image" :src="`profileImgs/${s.id}/${s.profile_image}`" />
              <q-icon v-else name="person" size="30px" color="indigo-3" />
            </q-avatar>
            <q-item-section class="info">
              <div class="title">{{ s.name }}</div>
              <div class="desc">{{ s.email }}</div>
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref } from "vue";
import { useDialogPluginComponent } from "quasar";

export default {
  components: {},
  setup() {
    const { dialogRef, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();

    const searchVal = ref("");
    const searchResultArr = ref([]);

    function goSearch(val) {
      if (val) {
      } else {
        searchResultArr.value = [];
      }
    }

    function createChat(idx) {
    }

    const peopleArr = ref([]);
    function addPeople(idx) {
      createChat(idx);
    }

    function removePeople(idx) {
      peopleArr.value.splice(idx, 1);
    }

    return {
      dialogRef,
      onDialogOK,
      onDialogCancel,

      searchVal,
      searchResultArr,
      goSearch,

      peopleArr,
      addPeople,
      removePeople,

      createChat,
    };
  },
};
</script>

<style lang="scss">
.new-message-dialog {
  .q-dialog__inner {
    .q-card {
      width: 100%;
      max-height: 600px;
      padding: 50px 0 0;
      position: relative;
      border-radius: 12px;
      .dialog-header {
        position: absolute;
        height: 50px;
        width: 100%;
        top: 0;
        left: 0;
        padding: 0 12px;
        .close-btn {
          margin-right: 12px;
        }
        .next-btn {
          position: absolute;
          top: 50%;
          transform: translateY(-50%);
          right: 12px;
        }
      }
      .search-section {
        .q-field {
          &__inner {
            .q-field__control {
              padding: 0 18px;
            }
          }
        }
        .q-field--focused {
          .q-field__inner {
            .q-field__control {
              .q-field__prepend {
                .q-icon {
                  color: $primary !important;
                }
              }
            }
          }
        }
      }
      .chip-section {
        padding: 4px 16px;
        .q-chip {
          &__content {
            color: black;
            .q-avatar {
              font-size: 20px;
            }
          }
        }
      }
      .q-scrollarea {
        &__container {
          .q-scrollarea__content {
            .q-list {
              .q-item {
                .q-avatar {
                  margin-right: 12px;
                }
                .q-item__section {
                  .title {
                    line-height: 15px;
                    font-weight: 700;
                  }
                  .desc {
                    line-height: 15px;
                    color: $grey-7;
                    margin-top: 4px;
                  }
                }

              }
            }
          }
        }
        &__thumb {
          display: block !important;
        }
      }
    }
  }
}
</style>
