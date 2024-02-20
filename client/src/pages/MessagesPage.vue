<template>
  <q-page class="messages-page flex no-wrap">
    <div class="left-section">
      <div class="page-header flex no-wrap items-center justify-between">
        Messages
        <div>
          <q-btn flat dense round :ripple="false" :icon="outlinedSettings" color="grey-9" class="q-mr-sm" />
          <q-btn flat dense round :ripple="false" :icon="outlinedSend" color="grey-9" @click="newMsgDialog" />
        </div>
      </div>

      <q-card v-if="!chatPeopleArr.length" flat class="no-messages">
        <div class="title">
          Welcome to your inbox!
        </div>
        <div class="desc">
          Drop a line, share posts and more with private conversations between you and others on X.
        </div>
        <q-btn rounded unelevated no-caps :ripple="false" label="Write a message" color="primary" @click="newMsgDialog" />
      </q-card>
      <q-card v-else flat class="message-list">
        <q-form class="q-px-md q-my-sm search-form">
          <q-input
            v-model="searchVal"
            dense
            rounded
            outlined
            placeholder="Search for people and group"
            @update:modelValue="searchChat(searchVal)"
          >
            <template v-slot:prepend>
              <q-icon name="search" />
            </template>
          </q-input>
        </q-form>

        <q-list>
          <q-item
            v-for="(p, i) in chatPeopleArr"
            :key="i"
            clickable
            :active="p.sc_id === activeChat.sc_id"
            active-class="active-item"
            @click="updateActiveChat(i)"
          >
            <q-avatar class="bg-deep-purple-1 q-mr-sm" size="48px">
              <img v-if="p.profile_image" :src="`profileImgs/${p.user_id}/${p.profile_image}`" />
              <q-icon v-else name="person" size="30px" color="indigo-3" />
            </q-avatar>
            <q-item-section class="info">
              <div class="title">{{ p.name }}</div>
              <div class="desc text-grey-7">{{ p.email }}</div>
            </q-item-section>
            <q-btn flat dense round :ripple="false" icon="more_horiz" color="indigo-4" class="bg-grey-4 more-btn absolute">
              <q-menu class="chat-message-more-options-menu">
                <q-list>
                  <q-item clickable>
                    <q-item-section class="flex row nowrap">
                      <q-icon name="delete_outline" color="negative" size="20px" class="q-mr-sm" />
                      <span>Delete conversation</span>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </q-item>
        </q-list>
      </q-card>
    </div>

    <q-separator vertical />

    <div class="right-section flex flex-center">
      <q-card v-if="!chatPeopleArr.length" flat class="no-messages">
        <div class="title">
          Select a message
        </div>
        <div class="desc">
          Choose from your existing conversations, start a new one, or just keep swimming.
        </div>
        <q-btn rounded unelevated no-caps :ripple="false" label="New message" color="primary" @click="newMsgDialog" />
      </q-card>

      <div v-else class="full-width message-container">
        <q-card  flat class="q-pl-md q-pr-sm flex no-wrap items-center justify-between profile-section">
          <q-card-section class="q-pa-none flex items-center">
            <q-avatar class="bg-deep-purple-1 q-mr-sm" size="40px">
              <img v-if="activeChat.profile_image" :src="`profileImgs/${activeChat.user_id}/${activeChat.profile_image}`" />
              <q-icon v-else name="person" size="15px" color="indigo-3" />
            </q-avatar>
            <q-item-section class="info">
              <div class="title">{{ activeChat.name }}</div>
              <div class="desc text-grey-7">{{ activeChat.email }}</div>
            </q-item-section>
          </q-card-section>

          <q-card-section>
            <q-btn flat dense round icon="info" />
          </q-card-section>
        </q-card>

        <div class="message-section">
          <q-scroll-area ref="messageScrollRef">
            <div class="full-width">
              <q-card flat class="join-date-card full-width q-mt-md">
                <q-card-section>
                  <div class="name text-bold">{{ activeChat.name }}</div>
                  <div class="email text-grey-7">{{ activeChat.email }}</div>
                  <div class="date">
                    <q-icon name="calendar_month" />
                    <span>Joined {{ activeChat.created_at }}</span>
                  </div>
                </q-card-section>
              </q-card>

              <q-separator color="indigo-1" class="full-width q-ma-md" />

              <q-list class="full-width flex column justify-end">
                <chat-message-item
                  v-for="(m, i) in messages"
                  :key="i"
                  :mId="m.m_id"
                  :userId="m.user_id"
                  :name="m.user_id !== user.id ? m.name : ''"
                  :profileImage="m.profile_img"
                  :text="[`${m.message}`]"
                  :sent="m.user_id === user.id"
                  :createdAt="m.created_at.split('T')[1]"
                  :bgColor="m.user_id === user.id ? 'primary' : 'grey-4'"
                  :textColor="m.user_id === user.id ? 'white' : 'black'"
                  class="full-width"
                  @deleteMessage="deleteMessage(i)"
                />
              </q-list>
            </div>
          </q-scroll-area>

          <q-form class="full-width flex no-wrap items-center" @submit="createMessage">
            <q-btn flat dense round icon="collections" />
            <q-btn flat dense round icon="gif_box" class="q-mr-sm" />
            <q-input v-model="messageVal" autogrow outlined rounded dense class="full-width" />
            <q-btn type="submit" flat dense round icon="send" :disable="!messageVal" class="q-ml-sm" />
          </q-form>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, watch, onBeforeMount } from 'vue';
import { Dialog, Cookies } from 'quasar'
import NewMessageDialog from '@components/messages/NewMessageDialog.vue'
import ChatMessageItem from '@components/messages/ChatMessageItem.vue'
import { outlinedSettings, outlinedSend } from '@quasar/extras/material-icons-outlined';


export default defineComponent({
  name: 'MessagesPage',
  components: { ChatMessageItem },
  setup() {
    const user = Cookies.get('user');

    function newMsgDialog() {
      Dialog.create({
        component: NewMessageDialog,
      });
    }
    const searchVal = ref("")
    const chatPeopleArr = ref([]);
    const activeChat = ref(null);

    function searchChat(val) {
      chatPeopleArr.value.filter((p) => p.name === 'val');
    }

    const messageScrollRef = ref(null);
    function onScrollToBottom() {
      setTimeout(() => {
        messageScrollRef.value.setScrollPercentage('vertical', 1);
      }, 100);
    }
    function getSingleChat() {
    }

    function updateActiveChat(idx) {
      activeChat.value = chatPeopleArr.value[idx];
    }

    const messages = ref([]);
    function getChatMsg() {
    }

    const messageVal = ref("");
    function createMessage() {
    }

    function deleteMessage(idx) {
      messages.value.splice(idx, 1);
    }

    onBeforeMount(() => {
      getSingleChat();
    })

    watch(activeChat, () => {
      getChatMsg();
    })

    return {
      outlinedSettings,
      outlinedSend,
      newMsgDialog,

      user,

      searchVal,
      searchChat,

      chatPeopleArr,
      activeChat,
      updateActiveChat,

      messages,
      getChatMsg,
      messageVal,
      createMessage,
      deleteMessage,
      messageScrollRef,
    }
  },
})
</script>

<style lang="scss">
.messages-page {
  .no-messages {
    width: 380px;
    padding: 32px;
    margin: auto !important;

    .title {
      font-weight: 900;
      font-size: 31px;
      line-height: 36px;
    }
    .desc {
      font-size: 15px;
      line-height: 20px;
      color: $grey-9;
      margin: 8px 0 28px;
    }
    .q-btn {
      height: 52px;
      padding: 8px 32px;
      &__content {
        > .block {
          font-weight: 700;
          font-size: 17px;
        }
      }
    }
  }
  .left-section {
    padding: 0 0 20px;
    min-width: 380px;
    width: 380px;
    .message-list {
      .q-list {
        .q-item {
          transition: all .3s;
          &:hover {
            .more-btn {
              display: block;
            }
          }
          .more-btn {
            display: none;
            top: 8px;
            right: 16px;
            min-width: 20px;
            min-height: 20px;
            .q-btn__content {
              .q-icon {
                font-size: 18px;
              }
            }
          }
        }
        .active-item {
          position: relative;
          &:before {
            content: "";
            width: 2px;
            height: 100%;
            background: $positive;
            position: absolute;
            right: 0;
            top: 0;
            transition: all .3s;
          }
        }
      }

    }
  }
  .right-section {
    width: 100%;
    max-width: 570px;
    .message-container {
      height: 100vh;
      position: relative;
      .q-scrollarea {
        // height: calc(100% - 100px);
        height: 100%;
        &__container {
          // height: calc(100% - 100px);
          .q-scrollarea__content {
            display: flex;
            flex-flow: column nowrap;
            align-items: center;
            justify-content: flex-end;
            overflow-x: hidden;
            .join-date-card {
              .q-card__section {
                font-size: 13px;
                text-align: center;
              }

            }
            .q-list {
            }
          }

          .q-message__content {
          }

        }
      }
      .profile-section {
        width: 100%;
        height: 50px;
        position: absolute;
        top: 0;
        left: 0;
      }
      .message-section {
        height: 100%;
        padding: 50px 0;
        .q-message {
          &-container {
            .q-message-avatar {
              background: $deep-purple-1;
              padding: 9px;

            }
          }
        }
        .q-form {
          height: 50px;
          position: absolute;
          bottom: 0;
          left: 0;
        }
      }
    }
  }
}
</style>
