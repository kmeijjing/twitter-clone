<template>
  <q-drawer
    v-model="drawer"
    show-if-above
    side="left"
    :mini="$q.screen.width <= 1190"
    :width="240"
    :breakpoint="500"
    :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-white'"
    class="left-drawer"
  >
    <q-scroll-area class="fit" :horizontal-thumb-style="{ opacity: 0 }">
      <q-list padding>
        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          :title="link.title"
          :icon="link.icon"
          :link="link.link"
        />

        <q-btn
          rounded
          unelevated
          no-caps
          label="Post"
          color="primary"
          class="add-post-btn"
          style="width: 200px"
          @click="openAddPostDialog"
        />

        <MyAccountItem />

      </q-list>
    </q-scroll-area>
  </q-drawer>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { linksList } from "@constants/menu.js"
import { Dialog } from "quasar";
import { useRouter } from "vue-router";
import EssentialLink from "@components/EssentialLink.vue";
import MyAccountItem from 'src/components/MyAccountItem.vue';
import AddPostDialog from "@components/AddPostDialog.vue";

export default defineComponent({
  name: "LeftSideMenu",
  components: {
    EssentialLink,
    MyAccountItem,
  },
  setup() {
    const router = useRouter();
    function openAddPostDialog() {
      Dialog.create({
        component: AddPostDialog,
        persistent: false,
      }).onOk(() => {
        router.go({ name: 'Home' });
      });
    }

    return {
      drawer: ref(false),
      miniState: ref(true),
      linksList,
      openAddPostDialog,
    }
  },
})
</script>

<style lang="scss">
.q-drawer {
  position: fixed;
  height: 100vh !important;
  border-right: 1px solid rgb(239, 243, 244);
  .q-scrollarea {
    .q-scrollarea__container {
      .q-scrollarea__content {
        .q-list {
          padding: 58px 4px 0;
          display: grid;
          gap: 4px;
          .add-post-btn {
            height: 48px;
            .q-btn__content {
              font-size: 16px;
            }
          }
        }
      }
    }
  }
}

@media screen and (max-width: 1190px) {
  .q-drawer {
    width: 70px;
    min-width: 70px;
    .q-scrollarea {
      .q-scrollarea__container {
        .q-scrollarea__content {
          .q-list {
            justify-content: center;
            .gnb-item {
              width: 48px;
              padding: 0;
              display: flex;
              align-items: center;
              justify-content: center;
              > .q-item__section--side {
                padding-right: 0;
              }
              > .q-item__section--main {
                display: none;
              }

            }
            .add-post-btn {
              width: 48px !important;
              .q-btn__content {
                font-size: 16px;
              }
            }

          }
        }
      }
    }
  }
}
</style>
