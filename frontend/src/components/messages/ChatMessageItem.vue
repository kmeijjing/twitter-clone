<template>
  <q-item
    class="full-width q-py-none q-px-sm q-mb-sm chat-message-item"
    :class="sent ? 'chat-message-item-sent-them' : 'chat-message-item-sent-me'"
  >
    <q-avatar class="bg-deep-purple-1" size="48px">
      <img v-if="profileImage" :src="`profileImgs/${userId}/${profileImage}`" />
      <q-icon v-else name="person" size="30px" color="indigo-3" />
    </q-avatar>
    <q-item-section>
      <div class="name">{{ name }}</div>
      <div class="text-box flex row no-wrap items-end justify-start">
        <div class="text" :class="`bg-${bgColor} text-${textColor}`">
          <div
            v-for="(t, i) in text"
            :key="i"
          >
            {{ t }}
          </div>
        </div>
        <div class="datetime text-grey-6">{{ createdAt }}</div>
        <q-btn flat dense round :ripple="false" icon="more_horiz" color="indigo-4" class="bg-indigo-1 q-mx-sm more-btn">
          <q-menu class="chat-message-more-options-menu">
            <q-list>
              <q-item clickable v-if="sent" @click="deleteMessage">
                <q-item-section class="flex row nowrap">
                  <q-icon name="delete_outline" color="negative" size="20px" class="q-mr-sm" />
                  <span>Delete for you</span>
                </q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section class="flex row nowrap">
                  <q-icon name="content_copy" color="secondary" size="20px" class="q-mr-sm" />
                  <span>Copy message</span>
                </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </div>
    </q-item-section>
  </q-item>
</template>

<script>
import { Dialog } from "quasar";
import ConfirmDialog from "@components/common/ConfirmDialog.vue";

export default {
  name: 'ChatMessageItem',
  props: {
    mId: Number,
    userId: Number,
    name: String,
    profileImage: String,
    text: Array,
    sent: Boolean,
    createdAt: String,
    bgColor: String,
    textColor: String,
  },
  setup(props, {emit}) {
    function deleteMessage() {
      Dialog.create({
        component: ConfirmDialog,
        componentProps: {
          title: 'Delete message?',
          desc: "This message will be deleted for you. Other people in the conversation will still be able to see it.",
          firstBtnLabel: 'Delete',
          firstBtnColor: 'negative',
          secondBtnLabel: 'Cancel',
        }
      }).onOk(() => {
      })
    }

    return {
      deleteMessage,
    }
  },
}
</script>

<style lang="scss">
.chat-message-item {
  &:hover {
    background: none;
    .more-btn {
      display: inline-flex !important;
      transition: all .3s;
    }
  }
  .q-avatar {
    position: absolute;
    z-index: 10;
  }
  .q-item__section {
    margin-left: 56px;
    .name {
      font-size: 12px;
      opacity: .6;
    }
    .text-box {
      width: fit-content;
      .text {
        padding: 8px 16px;
        position: relative;
      }
      .datetime {
        font-size: 11px;
      }
      .more-btn {
        min-width: 20px;
        min-height: 20px;
        display: none;
        transition: all .3s;
        .q-btn__content {
          .q-icon {
            font-size: 18px;
          }
        }
      }
    }
  }
}

.chat-message-item-sent-me {
  .q-avatar {
    position: absolute;
    bottom: 0;
    left: 8px;
    z-index: 10;
  }
  .q-item__section {
    .text-box {
      .text {
        border-radius: 18px 18px 18px 0px;
        &:before {
          content: "";
          position: absolute;
          z-index: 2;
          bottom: -2px;
          left: -7px;
          height: 20px;
          border-left: 20px solid $grey-4;
          border-bottom-right-radius: 16px 14px;
          -webkit-transform: translate(0, -2px);
          transform: translate(0, -2px);
        }
        &:after {
          content: "";
          position: absolute;
          z-index: 3;
          bottom: -2px;
          left: 4px;
          width: 26px;
          height: 20px;
          background: white;
          border-bottom-right-radius: 10px;
          -webkit-transform: translate(-30px, -2px);
          transform: translate(-30px, -2px);
        }
      }
      .datetime {
        margin-left: 8px;
      }
    }
  }
}
.chat-message-item-sent-them {
  .q-avatar {
    position: absolute;
    bottom: 0;
    right: 8px;
    z-index: 10;
    display: none;
  }
  .q-item__section {
    justify-content: flex-end;
    align-items: flex-end;
    margin-right: 8px;
    .text-box {
      flex-flow: row-reverse;
      .text {
        border-radius: 18px 18px 0px 18px;
        &:before {
          content: "";
          position: absolute;
          z-index: -1;
          bottom: -2px;
          right: -7px;
          height: 20px;
          border-right: 20px solid $primary;
          border-bottom-left-radius: 16px 14px;
          -webkit-transform: translate(0, -2px);
          transform: translate(0, -2px);
        }
        &:after {
          content: "";
          position: absolute;
          z-index: 1;
          bottom: -2px;
          right: -56px;
          width: 26px;
          height: 20px;
          background: white;
          border-bottom-left-radius: 10px;
          -webkit-transform: translate(-30px, -2px);
          transform: translate(-30px, -2px);
        }
      }
      .datetime {
        margin-right: 8px;
      }
    }
  }
}

.chat-message-more-options-menu {
  .q-list {
    .q-item {
      &__section {
        display: flex;
        flex-flow: row nowrap;
        align-items: center;
        justify-content: flex-start;
        > span {
          font-size: 13px;
        }
      }
    }
  }
}
</style>
