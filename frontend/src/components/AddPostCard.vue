<template>
  <q-card flat class="add-post-card">
    <q-card-section>
      <q-avatar color="grey-6" text-color="white" icon="face" size="44px" />

      <q-form @submit="addPost">
        <q-input
          type="text"
          v-model="tweetVal"
          placeholder="지금 무슨일이 일어나고 있나요?!"
          borderless
          dense
          autogrow
        />
        <div class="imgs">
          <div
            v-show="photoImgs.length"
            v-for="(img, i) in photoImgs"
            :key="i"
            class="img"
          >
            <q-img :src="img" />
            <q-btn
              dense
              round
              size="sm"
              icon="close"
              color="grey-8"
              @click="deleteImg(i)"
            />
          </div>
        </div>

        <div class="form-bottom">
          <q-btn
            flat
            dense
            rounded
            :ripple="false"
            color="primary"
            no-caps
            :label="selectVal.label"
            :icon="selectVal.icon"
            class="select-btn"
          >
            <q-menu class="add-tweet-select-options" :offset="[0, 2]">
              <div class="title">Who can reply?</div>
              <div class="desc">
                Choose who can reply to this post.<br />
                Anyone mentioned can always reply.
              </div>
              <q-list>
                <q-item
                  v-for="select in addTweetSelectOptions"
                  :key="select.value"
                  clickable
                  v-close-popup
                  @click="selectVal = select"
                >
                  <q-item-section avatar>
                    <q-avatar
                      :icon="select.icon"
                      color="primary"
                      text-color="white"
                      size="40px"
                    />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label inlined class="text-weight-bold">{{ select.label }}</q-item-label>
                  </q-item-section>
                  <q-icon v-if="select.icon === selectVal.icon" name="check" color="primary" />
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
          <q-separator color="indigo-1" />
          <div class="function-btns flex items-center justify-between">
            <div>
              <q-btn
                v-for="btn in addTweetFunctionButtons"
                :key="btn.label"
                round
                flat
                dense
                :title="btn.label"
                color="light-blue-13"
                :icon="btn.icon"
                @click="clickFunctionBtns(btn.value)"
              />
              <q-file
                v-model="photoFiles"
                name="photoFiles"
                dense
                outlined
                multiple
                append
                accept="image/*"
                max-total-size="5242880"
                max-files="4"
                ref="photoFilesInputRef"
                @update:modelValue="uploadPhotoFiles"
                style="display:none"
              />
            </div>
            <q-btn
              type="submit"
              rounded
              unelevated
              color="primary"
              label="Tweet"
              no-caps
              :disable="!tweetVal"
            />
          </div>
        </div>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import { ref } from "vue";
import { Cookies, Notify } from "quasar";
import { api } from "@boot/axios";

import { outlinedInsertPhoto } from "@quasar/extras/material-icons-outlined";
import {
  addTweetSelectOptions,
  addTweetFunctionButtons,
} from "@constants/tweet.js";

export default {
  name: "AddPostCard",
  emits: ["success"],
  setup(_, { emit }) {
    const selectVal = ref(addTweetSelectOptions[0]);
    const tweetVal = ref("");
    const photoFiles = ref([]);

    function addPost() {
      const formData = new FormData();
      const user = Cookies.get('user');
      formData.append("id", user.id)
      formData.append("tweet", tweetVal.value);
      if (photoFiles.value.length) {
        photoFiles.value.forEach((p) => {
          formData.append(`file`, p);
        });
      }

      api
        .post("/tweet", formData, {
          header: { "Content-Type": "multipart/form-data" },
        })
        .then((res) => {
          emit("success", res);
          tweetVal.value = "";
          photoImgs.value = [];
          photoFiles.value = [];
        })
        .catch((err) => {
          if (err.response) {
            const errText = err.response.data;
            Notify.create({
              classes: "toast-message",
              message: errText,
              color: "negative",
              position: "bottom",
            });
          }
        });
    }

    const photoFilesInputRef = ref(null);
    function clickFunctionBtns(val) {
      switch (val) {
        case 'photo':
          photoFilesInputRef.value.$el.click();
          break;
        default:
          break;
      }
    }

    const photoImgs = ref([]);

    function uploadPhotoFiles(val) {
      // TODO : 사진업로드 4개까지 가능하다는 알람 개발 필요
      photoImgs.value = [];
      val.forEach((v) => {
        const reader = new FileReader();
        reader.onload = function (e) {
          photoImgs.value.push(e.target.result);
        };
        reader.readAsDataURL(v);
      });
    }

    function deleteImg(idx) {
      photoImgs.value.splice(idx, 1);
      photoFiles.value.splice(idx, 1);
    }

    return {
      outlinedInsertPhoto,
      addTweetSelectOptions,
      addTweetFunctionButtons,

      selectVal,
      tweetVal,

      addPost,
      photoFilesInputRef,
      clickFunctionBtns,
      photoFiles,
      photoImgs,
      uploadPhotoFiles,
      deleteImg,
    };
  },
};
</script>

<style lang="scss">
.add-post-card {
  padding: 0 16px;
  .q-card__section {
    display: flex;
    flex-flow: row nowrap;
    align-items: flex-start;
    justify-content: space-between;
    .q-avatar {
      width: 42px;
      height: 42px;
    }
    .q-form {
      width: 100%;
      margin-left: 12px;
      > .q-field {
        margin-bottom: 6px;
        .q-field__inner {
          .q-field__control {
            &-container {
              .q-field__native {
                font-size: 20px;
                line-height: 24px;
                height: 100px !important;
                &::placeholder {
                  color: $grey-7;
                }
              }
            }
          }
        }
      }
      .imgs {
        display: flex;
        flex-flow: row wrap;
        .img {
          width: calc(50% - 3px);
          margin-right: 6px;
          position: relative;
          &:nth-of-type(2),
          &:nth-of-type(4) {
            margin-right: 0;
          }
          > .q-img {
            border-radius: 12px;
            border: 1px solid $indigo-1;
            margin-bottom: 6px;
            position: relative;
          }
          > .q-btn {
            z-index: 1;
            position: absolute;
            top: 2px;
            left: 2px;
          }
        }
      }
      .q-separator {
        margin: 8px 0 10px;
      }
      .select-btn {
        padding: 0 8px;
        margin-left: -10px;
        min-height: 0;
        .q-btn__content {
          .q-icon {
            font-size: 18px;
          }
          .block {
            font-size: 14px;
            font-weight: 700;
          }
        }
      }
      .function-btns {
        margin-left: -10px;
        > div {
          display: flex;
          gap: 4px;
          .q-btn {
            &__content {
              .q-icon {
                font-size: 20px;
              }
            }
          }
        }
        > .q-btn {
          width: 80px;
        }
      }
    }
  }
}
.add-tweet-select-options {
  width: 320px;
  padding: 16px 0 4px;
  border-radius: 12px;
  .title {
    padding: 0 16px;
    font-weight: 700;
  }
  .desc {
    padding: 0 16px;
    margin-bottom: 12px;
    color: $grey-8;
    line-height: 20px;
  }
  .q-list {
    .q-item {
      &__section {
        min-width: 0;
      }
      .q-item__section:first-of-type {
        padding-right: 10px;
      }
      > .q-icon {
        font-size: 20px;
        margin: auto 0;
      }
    }
  }
}
</style>
