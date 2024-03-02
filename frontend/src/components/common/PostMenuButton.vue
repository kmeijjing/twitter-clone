<template>
  <q-btn flat dense round :ripple="false" icon="more_horiz" color="grey-8" class="post-menu-button" @click.stop>
    <q-menu class="post-menu" v-if="userId === post_user_id">
      <q-list>
        <q-item clickable @click="onDeletePost">
          <q-item-section side>
            <q-icon name="far fa-trash-alt" size="18px" color="red" />
          </q-item-section>
          <q-item-section class="text-red text-weight-bold">Delete</q-item-section>
        </q-item>

        <q-item
          v-for="(menu) in postMenu"
          :key="menu.title"
        >
          <q-item-section side>
            <q-icon :name="menu.icon" size="18px" color="dark" />
          </q-item-section>
          <q-item-section class="text-weight-bold">
            {{ menu.title }}
          </q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </q-btn>
</template>

<script>
import { Cookies, Dialog } from 'quasar';
import { postMenu } from  '@constants/post';
import ConfirmDialog from '@components/common/ConfirmDialog.vue';

export default {
  name: 'PostMenuButton',
  props: {
    post_user_id: {
      type: Number,
      required: true,
    },
  },
  setup(_, { emit }) {
    const userId = Cookies.get('user').id;

    function onDeletePost() {
      Dialog.create({
        component: ConfirmDialog,
        componentProps: {
          title: 'Delete tweet?',
          desc: 'This can’t be undone and it will be removed from your profile, the timeline of any accounts that follow you, and from Twitter search results.',
          firstBtnLabel: 'Delete',
          firstBtnColor: 'negative',
          secondBtnLabel: 'Cancel'
        }
      }).onOk(() => {
        emit("delete:post");
      })
    }

    return {
      postMenu,
      userId,
      onDeletePost,

    }
  },
}
</script>

<style lang="scss">
.post-menu-button {
  width: 34px;
  height: 34px;
  position: absolute;
  top: 6px;
  right: 10px;
  &:hover {
    background: rgba(3, 169, 244, 0.1) !important;
    .q-focus-helper {
      opacity: 0 !important;
      &:before, &:after {
        opacity: 0 !important;
      }
    }
    .q-btn__content {
      .q-icon {
        color: $primary;
      }
    }
  }
  .q-btn__content {
    .q-icon {
      font-size: 18px;
    }
  }
}
.post-menu {
  width: 300px;
  border-radius: 12px;
  .q-list {
    .q-item {
      padding: 12px 16px;
    }
  }
}
</style>
