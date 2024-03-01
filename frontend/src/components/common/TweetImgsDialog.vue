<template>
  <q-dialog
    full-width
    full-height
    ref="dialogRef"
    class="tweet-imgs-dialog"
  >
    <q-card square flat class="relative bg-black">
      <q-card-actions
        align="between"
        class="absolute-top z-top q-ma-sm"
      >
        <q-btn
          round
          icon="close"
          color="black"
          @click="onDialogCancel"
        />
        <q-btn
          round
          icon="more_horiz"
          color="black"
        />
      </q-card-actions>

      <q-card-section class="flex items-center justify-center">
        <q-carousel
          swipeable
          animated
          v-model="slide"
          arrows
          control-type="regular"
          control-color="black"
          control-text-color="white"
        >
          <q-carousel-slide
            v-for="(upload, i) in uploads"
            :key="i"
            :name="i"
            :img-src="`/uploads/${upload}`"
          />
        </q-carousel>
      </q-card-section>

      <q-card-actions align="around" class="function-container">
        <q-btn flat dense round :ripple="false" color="grey-8" icon="far fa-comment-alt" class="reply-btn" :label="Number(10).toLocaleString()" />

        <q-btn flat dense round :ripple="false" color="grey-8" icon="fas fa-retweet" class="repost-btn" :label="Number(10).toLocaleString()" />

        <q-btn
          flat
          dense
          round
          :ripple="false"
          :color="like ? 'pink' : 'grey-8'"
          :icon="like ? roundFavorite : roundFavoriteBorder"
          class="like-btn"
          :label="Number(like_count).toLocaleString()"
          @click.stop="onClickLike"
          />

        <q-btn flat dense round :ripple="false" color="grey-8" icon="far fa-share-square" class="share-btn" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref } from 'vue';
import { useDialogPluginComponent, Cookies } from "quasar";
import { api } from "@boot/axios";
import {
  roundComment,
  roundCached,
  roundFavoriteBorder,
  roundFavorite,
  roundIosShare,
} from "@quasar/extras/material-icons-round";

export default {
  name: "TweetImgsDialog",
  props: {
    uploads: Array,
    idx: Number,
    post_id: Number,
    like: Boolean,
    like_count: Number,
    updateLike: {
      type: Function,
    },
  },
  setup(props, { emit }) {
    const { dialogRef, onDialogCancel } =
      useDialogPluginComponent();

    const slide = ref(props.idx);

    function onClickLike() {
      const param = {
        user_id: Cookies.get("user").id,
        tweet_id: props.post_id,
      };
      api
        .post("/like", param)
        .then(() => {
          props.updateLike()
        })
        .catch((err) => {
          console.log(err.message);
        });
    }

    return {
      dialogRef,
      onDialogCancel,

      roundComment,
      roundCached,
      roundFavoriteBorder,
      roundFavorite,
      roundIosShare,

      slide,
      onClickLike
    };
  },
};
</script>

<style lang="scss">
.tweet-imgs-dialog {
  .q-dialog__inner {
    padding: 0;
    display: block;
    .q-card {
      border-radius: 0 !important;
      .q-card__section {
        height: calc(100% - 58px);
        width: 100%;
        .q-carousel {
          width: 100%;
          height: 100%;
          background: none;
          .q-carousel__slides-container {
            .q-panel {
              .q-carousel__slide {
                background-repeat: no-repeat;
                background-size: contain;
              }
            }
          }
        }
      }
      .function-container {
        max-width: 568px;
        margin: 0 auto;
        padding: 8px 0;
        .q-btn {
          &__content {
            color: white;
            .q-icon {
              font-size: 15px;
            }
            .block {
              font-size: 13px;
            }
          }
          .q-focus-helper {
            opacity: 0 !important;
          }
          &:hover {
            .q-icon {
              &:after {
                content: '';
                width: 40px;
                height: 40px;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                border-radius: 20px;
              }
            }
          }
        }
        .reply-btn, .share-btn {
          &:hover {
            .q-icon {
              color: $primary;
              &:after {
                background: rgba(3, 169, 244, 0.18);
              }
            }
            .block {
              color: $primary;
            }
          }
        }
        .repost-btn {
          &:hover {
            .q-icon {
              color: $green;
              &:after {
                background: rgba(76, 175, 80, 0.18);
              }
            }
            .block {
              color: $green;
            }
          }
        }
        .like-btn {
          &:hover {
            .q-icon {
              color: $pink;
              &:after {
                background: rgba(233, 30, 99, 0.18);
              }
            }
            .block {
              color: $pink;
            }
          }
        }
      }
    }
  }
}
</style>
